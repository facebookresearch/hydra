import hydra
import wandb
from omegaconf import DictConfig


@hydra.main(config_path="conf", config_name="config")
def evaluate(cfg: DictConfig, run_id=None):
    x = cfg.x
    y = cfg.y
    with wandb.init(id=run_id) as run:
        run.log({"val_loss": x - y})


if __name__ == "__main__":
    evaluate()
