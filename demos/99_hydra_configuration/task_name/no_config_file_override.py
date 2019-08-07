import hydra
from hydra.utils import JobRuntime


@hydra.main()
def experiment(_cfg):
    print(JobRuntime().get('name'))


if __name__ == "__main__":
    experiment()
