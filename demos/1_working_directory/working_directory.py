import datetime
import os

import hydra


@hydra.main()
def experiment(_cfg):
    print("Working directory : {}".format(os.getcwd()))
    with open("output.txt", "w") as f:
        f.write("The time is {}\n".format(datetime.datetime.now()))


if __name__ == "__main__":
    experiment()
