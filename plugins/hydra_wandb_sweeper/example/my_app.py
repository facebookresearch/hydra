import logging
import random
import threading
from time import sleep

import hydra
import wandb
from hydra.types import TaskFunction
from omegaconf import DictConfig

logger = logging.getLogger(__name__)


class DummyTraining(TaskFunction):
    def __init__(self) -> None:
        self.ready_to_checkpoint = True

    def __call__(self, cfg: DictConfig) -> float:
        """
        A dummy function to minimize
        Minimum is 0.0 at:
        lr = 0.12, dropout=0.33, db=mnist, batch_size=4

        ------------------------------------------------------------------------
        to execute code locally:
          `python my_app.py --multirun +sweeper=wandb`
        ------------------------------------------------------------------------


        ------------------------------------------------------------------------
        to execute code on SLURM cluster to test wandb pre-emption:
          `python my_app.py --multirun +sweeper=wandb +launcher=submitit_remote`
          then execute `scancel --signal=USR1 <JOB_ID>`

          --> requires submit it launcher to be installed
              `pip install hydra-submitit-launcher --upgrade`
        ------------------------------------------------------------------------
        """
        dropout = cfg.model.dropout
        batch_size = cfg.experiment.batch_size
        database = cfg.experiment.db
        lr = cfg.experiment.lr

        # Here goes some long calculation
        best = 1e8
        num_iters = 100.0
        for i in range(int(num_iters)):
            self.ready_to_checkpoint = False

            # NOTE: Be careful not to log too quickly, it could cause an os._exit(-1) from wandb which can't
            # be caught for graceful exit. Since this task function is running on a thread spun by the agent,
            # once an os._exit(-1) occurs from wandb, all parent threads are eliminated, including the launcher.
            sleep(0.5)

            noise = random.random() / 10.0
            out = (
                float(
                    abs(dropout - 0.33)
                    + int(database == "mnist")
                    + abs(lr - 0.12)
                    + abs(batch_size - 4)
                )
                + noise
                + (2.0 ** ((-0.4 * i) + 3))
            )
            out = max(out, 0.0)
            wandb.log({"out": out})
            if (i + 1) % 10 == 0:
                logger.info(f"{100*i/num_iters:.1f}% done...")
            if out < best:
                best = out

            # Simulate a bunch of important computations needed before saving whatever
            # you want to save, like model parameters.
            # NOTE: Optional. Uncomment this if you want to further test out pre-emption.
            # sleep(5)

            # This is to signal that when pre-emption happens, wait until all important computations
            # are finished before finishing execution of checkpoint function.
            self.ready_to_checkpoint = True

            # Simulate unimportant computations before starting next iteration.
            # NOTE: Optional. Uncomment this if you want to further test out
            # pre-emption ready_to_checkpoint might not be True for long enough
            # for the custom submitit checkpoint to catch it mid-run and send a
            # wandb alert.
            # sleep(3)

        logger.info(
            f"best dummy_training(dropout={dropout:.3f}, lr={lr:.3f}, db={database}, batch_size={batch_size}) "
            f"= {best:.3f}"
        )

        return best


if __name__ == "__main__":
    dummy_training = DummyTraining()
    app = hydra.main(config_path="conf", config_name="config")(dummy_training.__call__)
    app()
