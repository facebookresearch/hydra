# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import hydra


class DBConnection:
    def connect(self):
        pass


class MySQLConnection(DBConnection):
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def connect(self):
        print(
            "MySQL connecting to {} with user={} and password={}".format(
                self.host, self.user, self.password
            )
        )


class PostgreSQLConnection(DBConnection):
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        print(
            "PostgreSQL connecting to {} "
            "with user={} and password={} and database={}".format(
                self.host, self.user, self.password, self.database
            )
        )


@hydra.main(config_path="conf/config.yaml")
def my_app(cfg):
    connection = hydra.utils.instantiate(cfg.db)
    connection.connect()


if __name__ == "__main__":
    my_app()
