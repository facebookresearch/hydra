import hydra


@hydra.main()
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    experiment()
