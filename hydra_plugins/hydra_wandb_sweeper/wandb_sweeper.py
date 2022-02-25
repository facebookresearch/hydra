import functools
import itertools
import logging
import typing

import omegaconf
import wandb
from hydra.core import plugins
from hydra.core.override_parser import overrides_parser, types
from hydra.plugins import sweeper

from hydra_plugins.hydra_wandb_sweeper import config

SUPPORTED_DISTRIBUTIONS = {
    "constant": ["value"],
    "categorical": ["values"],
    "int_uniform": ["min", "max"],
    "uniform": ["min", "max"],
    "q_uniform": ["min", "max"],
    "log_uniform": ["min", "max"],
    "q_log_uniform": ["min", "max"],
    "inv_log_uniform": ["min", "max"],
    "normal": ["mu", "sigma"],
    "q_normal": ["mu", "sigma"],
    "log_normal": ["mu", "sigma"],
    "q_log_normal": ["mu", "sigma"],
}


def get_wandb_parameter(override):

    value = override.value()

    def set_parameter(parameter, distribution, *args):
        keys = SUPPORTED_DISTRIBUTIONS[distribution]
        parameter["distribution"] = distribution
        for key, value in zip(keys, args):
            parameter[key] = value

    distribution = None
    if getattr(value, "tags", None):
        assert len(value.tags) == 1
        distribution = list(value.tags)[0]
        if distribution not in SUPPORTED_DISTRIBUTIONS:
            raise ValueError(
                f"{distribution=} not supported. "
                f"Supported Distributions: {list(SUPPORTED_DISTRIBUTIONS.keys())}"
            )

    parameter = {}

    if not override.is_sweep_override():
        distribution = "constant"
        set_parameter(parameter, distribution, value)

        return parameter

    if override.is_interval_sweep():
        distribution = distribution or "uniform"

        if distribution in ("categorical", "constant"):
            raise ValueError(
                f"interval sweep doesn't support categorical/constant distribution"
            )

        set_parameter(parameter, distribution, value.start, value.end)
        return parameter

    if override.is_choice_sweep() or override.is_range_sweep():
        choices = [
            x for x in override.sweep_iterator(transformer=types.Transformer.encode)
        ]

        distribution = distribution or "categorical"

        if distribution != "categorical":
            raise ValueError(
                f"Choice Sweep and Range Sweep doesn't allow {distribution=}"
            )

        set_parameter(parameter, distribution, choices)
        return parameter

    raise NotImplementedError(f"{override} not supported by WandB sweeper")


class WandbSweeper(sweeper.Sweeper):
    def __init__(self, wandb_sweep_config: omegaconf.DictConfig) -> None:
        self.wandb_sweep_config = wandb_sweep_config
        self._sweep_id = None
        self._preemptible = wandb_sweep_config["preemptible"]
        self.agent_run_count = self.wandb_sweep_config.get["count"]

        self.job_idx = itertools.count(0)

    def setup(self, config, hydra_context, task_function) -> None:
        self.config = config

        self._task_function = functools.partial(
            self.wandb_task,
            task_function=task_function,
            count=self.agent_run_count,
        )
        self.hydra_context = hydra_context

        self.launcher = plugins.Plugins.instance().instantiate_launcher(
            config=config,
            hydra_context=hydra_context,
            task_function=self._task_function,
        )
        self.sweep_dict = {
            "name": self.wandb_sweep_config.name,
            "method": self.wandb_sweep_config.method,
            "parameters": {},
        }
        early_terminate = self.wandb_sweep_config.early_terminate
        metric = self.wandb_sweep_config.metric

        if metric:
            self.sweep_dict.update({"metric": omegaconf.OmegaConf.to_container(metric)})

        if early_terminate:
            self.sweep_dict.update(
                {"early_terminate": omegaconf.OmegaConf.to_container(early_terminate)}
            )

    @property
    def sweep_id(self):
        return self._sweep_id

    def sweep(self, arguments):
        parser = overrides_parser.OverridesParser.create(
            config_loader=self.hydra_context.config_loader
        )
        parsed = parser.parse_overrides(arguments)
        sweep_id = self.wandb_sweep_config["sweep_id"]

        parameters = self.sweep_dict["parameters"]

        for override in parsed:
            parameters[override.get_key_element()] = get_wandb_parameter(override)

        if not sweep_id:
            sweep_id = wandb.sweep(
                self.sweep_dict,
                entity=self.wandb_sweep_config.entity,
                project=self.wandb_sweep_config.project,
            )
        else:
            logging.info(f"Reusing Sweep with ID: {sweep_id}")
        self._sweep_id = sweep_id

        overrides = []
        for i in range(self.wandb_sweep_config.num_agents):
            overrides.append(tuple(f"{key}=-1" for key in parameters))

        self.launcher.launch(overrides, initial_job_idx=next(self.job_idx))

    def wandb_task(self, base_config, task_function, count):
        def run():
            with wandb.init(resume=self._preemptible) as run:
                if self._preemptible:
                    wandb.mark_preempting()
                run_id = run.id
                override_config = run.config
            override_config = omegaconf.DictConfig(override_config.as_dict())
            config = omegaconf.OmegaConf.merge(base_config, override_config)
            task_function(config, run_id)

        if not self.sweep_id:
            raise ValueError(f"sweep_id cannot be {self.sweep_id}")

        logging.info("Launching agent")
        wandb.agent(self.sweep_id, function=run, count=count)
