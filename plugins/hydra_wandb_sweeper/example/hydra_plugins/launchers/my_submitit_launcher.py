import logging
from time import sleep
from typing import Any

import wandb
from hydra_plugins.hydra_submitit_launcher.submitit_launcher import BaseSubmititLauncher

logger = logging.getLogger(__name__)

# This has to be located under a hydra_plugins folder or else hydra won't recognize this as a valid plugin.
# Furthermore, placing an __init__.py under hydra_plugins will cause circular import issues with the above
# 'from hydra_plugins' import (which is why hydra says not to do this
# https://hydra.cc/docs/next/advanced/plugins/develop/#internaldocs-banner). However, although Hydra's instantiate
# function can resolve classes without requiring __init__.py, submitit requires this when pickling. Otherwise
# submitit won't be able to find the my_submitit_launcher module. A way around this is to make a nested folder,
# 'launchers', with an __init__.py and place the module there. Then from train.py we register
# hydra_plugins.launchers by value.
class MyBaseSubmititLauncher(BaseSubmititLauncher):
    def __init__(self, **params: Any) -> None:
        super().__init__(**params)

    def checkpoint(self, *args: Any, **kwargs: Any) -> Any:
        """This method is a modified version of the BaseSubmititLauncher.checkpoint method"""
        run = wandb.run

        while not self.task_function.inner_task_function.__self__.ready_to_checkpoint:
            logger.info(
                f"Task function has been pre-empted or timed out. Waiting for it to be ready to be "
                "checkpointed..."
            )
            sleep(1)

        if run is not None:
            logger.info(
                f"Agent has either been pre-empted or timed-out during execution of Run {run.id} ({run.name})."
            )
            run.alert(
                title="Agent Pre-empted/Timed-out",
                text=f"Agent has either been pre-empted or timed-out during execution of Run {run.id} ({run.name}).",
                level=wandb.AlertLevel.INFO,
            )
            logger.info(f"Marking Run {run.id} ({run.name}) as pre-empted")

            # Signal to wandb sweep controller that this run should be requeued to the run queue.
            # Next wandb.init will pull the preempted run from the run queue. The next wandb.init could be
            # from other agents running in parallel or the agent that will be created from this checkpoint.
            run.mark_preempting()
            self.task_function.from_preemption = True

            # Signal to the backend to publish/sync any bufferred results then kill the run.
            # This means that if the underlying run is still running, the next time it does a wandb.log
            # it won't work. Exit code of -1 enforces wandb's sweep controller to actually requeue the run,
            # otherwise it'll assume it exited successfully and won't requeue it.
            run.finish(-1)

        # Requeue task function in a new pickle and node, which means a new agent as well
        return super().checkpoint(*args, **kwargs)


class MyLocalLauncher(MyBaseSubmititLauncher):
    _EXECUTOR = "local"


class MySlurmLauncher(MyBaseSubmititLauncher):
    _EXECUTOR = "slurm"
