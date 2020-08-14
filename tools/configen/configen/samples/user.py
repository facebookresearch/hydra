# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
class User:
    def __init__(self, age: int, name: str):
        self.age = age
        self.name = name

    def __repr__(self):
        return f"User: name={self.name}, age={self.age}"
