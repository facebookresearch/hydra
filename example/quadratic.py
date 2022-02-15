from typing import Any

import hydra
from omegaconf import DictConfig
import wandb

@hydra.main(config_path="conf", config_name="config")
def evaluate(cfg: DictConfig, run_id) -> Any:
    x = cfg.x
    y = cfg.y
    print("here")
    with wandb.init(id=run_id) as run:
      run.log({"loss": x - y})

if __name__ == "__main__":
    evaluate()
