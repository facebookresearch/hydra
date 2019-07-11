import logging
import sys
import os
import hydra

log = logging.getLogger(__name__)


@hydra.main()
def experiment(_cfg):
    print(f"Working directory : {os.getcwd()}")


if __name__ == "__main__":
    sys.exit(experiment())
