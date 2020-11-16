import multiprocessing as mp
import os
import time

import hydra
from omegaconf import DictConfig, OmegaConf
import torch
import torch.distributed as dist


def setup(master_addr, master_port, rank, world_size, backend):
    """Initializes distributed process group.

    Arguments:
        rank: the rank of the current process.
        world_size: the total number of processes.
        backend: the backend used for distributed processing.
    """
    os.environ["MASTER_ADDR"] = master_addr
    os.environ["MASTER_PORT"] = master_port
    dist.init_process_group(backend=backend, rank=rank, world_size=world_size)


def cleanup():
    dist.destroy_process_group()


@hydra.main(config_path="conf", config_name="config")
def main(cfg: DictConfig):
    setup(cfg.master_addr, cfg.master_port, cfg.rank, cfg.world_size, cfg.backend)
    group = dist.new_group(list(range(cfg.world_size)))
    tensor = torch.rand(1)
    print("Rank {} - {}".format(cfg.rank, tensor[0]))
    dist.reduce(tensor, dst=0, op=dist.ReduceOp.SUM, group=group)
    if cfg.rank == 0:
        tensor /= 4
        print("Rank {} has average: {}".format(cfg.rank, tensor[0]))
    cleanup()


if __name__ == "__main__":
    main()
