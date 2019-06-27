import sys

import hydra


class Model:
    def __init__(self):
        pass

    def forward(self, x):
        pass


class Alexnet(Model):
    def __init__(self, num_layers):
        print(f"Alexnet: num_layers={num_layers}")
        self.num_layers = num_layers

    def forward(self, x):
        print(f"Alexnet: forward({x})")


class Resnet(Model):
    def __init__(self, num_layers, width):
        print(f"Resnet: num_layers={num_layers}, width={width}")
        self.num_layers = num_layers
        self.width = width

    def forward(self, x):
        print(f"Resnet: forward({x})")


@hydra.main(config_path='conf/config.yaml')
def objects(cfg):
    print(cfg.pretty())
    model = hydra.utils.instantiate(cfg.model)
    model.forward(10)


if __name__ == "__main__":
    sys.exit(objects())
