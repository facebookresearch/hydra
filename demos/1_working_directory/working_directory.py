import sys
import os
import hydra


@hydra.main()
def experiment(cfg):
    print(f"Working directory : {os.getcwd()}")


if __name__ == "__main__":
    sys.exit(experiment())
