from hydra import utils
from .launcher import Launcher


class BasicLauncher(Launcher):
    def __init__(self):
        self.config = None
        self.config_loader = None
        self.task_function = None
        self.verbose = None

    def setup(self, config, config_loader, task_function, verbose):
        self.config = config
        self.config_loader = config_loader
        self.task_function = task_function
        self.verbose = verbose

    def launch(self, job_overrides):
        utils.configure_log(None, self.verbose)
        utils.setup_globals()
        runs = []
        for overrides in job_overrides:
            sweep_config = self.config_loader.load_sweep_config(
                self.config, list(overrides)
            )
            utils.HydraConfig().set_config(sweep_config)
            runs.append(
                utils.run_job(
                    config=sweep_config,
                    task_function=self.task_function,
                    verbose=self.verbose,
                    job_dir_key="hydra.run.dir",
                    job_subdir_key=None,
                )
            )
        return runs
