# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import hydra


class Model:
    def __init__(self):
        pass

    def forward(self, x):
        pass


class Alexnet(Model):
    def __init__(self, num_layers):
        print("Alexnet: num_layers={}".format(num_layers))
        self.num_layers = num_layers

    def forward(self, x):
        print("Alexnet: forward({})".format(x))


class Resnet(Model):
    def __init__(self, num_layers, width):
        print("Resnet: num_layers={}, width={}".format(num_layers, width))
        self.num_layers = num_layers
        self.width = width

    def forward(self, x):
        print("Resnet: forward({})".format(x))


@hydra.main(config_path="conf/config.yaml")
def experiment(cfg):
    model = hydra.utils.instantiate(cfg.model)
    model.forward(10)


if __name__ == "__main__":
    experiment()
