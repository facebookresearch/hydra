from omegaconf import DictConfig

import hydra


@hydra.main(config_name="config")
def my_app(cfg: DictConfig):
    assert cfg.node.loompa == 10  # attribute style access
    assert cfg["node"]["loompa"] == 10  # dictionary style access
    assert cfg.node.zippity == 10  # Variable interpolation
    assert type(cfg.node.zippity) == int  # Variable interpolation inherits the type
    assert cfg.node.do == "oompa 10"  # string interpolation
    cfg.node.waldo  # raises an exception


if __name__ == "__main__":
    my_app()
