import hydra


# Put the configuration into strict mode before merging it with the command line overrides.
# This will result with a KeyError if a key that does not already exist in the configuration is being accessed.
# This applies both for read (using the config) and for write (overriding the config from the command line)
@hydra.main(config_path='config.yaml', strict=True)
def experiment(cfg):
    # this would result in an exception
    if cfg.bad_key:
        pass
    # this would also result in an aception
    cfg.bad_key = True


if __name__ == "__main__":
    experiment()
