import sys
import os
import hydra


@hydra.main()
def experiment(_cfg):
    print("Working directory : {}".format(os.getcwd()))


if __name__ == "__main__":
    sys.exit(experiment())
