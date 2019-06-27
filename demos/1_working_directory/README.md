## Working directory
```python
@hydra.main()
def experiment(cfg):
    print(f"Working directory : {os.getcwd()}")
```
Hydra will change the working directory for you automatically. if you have any outputs you should just write them into
the current working directory.

```text
$ python demos/1_working_directory/working_directory.py
Working directory : /private/home/omry/dev/hydra/outputs/2019-06-27_00-47-26
```

Hydra will drop your config object into your working directory as config.yaml.

```text
$ tree /private/home/omry/dev/hydra/outputs/2019-06-27_00-47-26
/private/home/omry/dev/hydra/outputs/2019-06-27_00-47-26
└── config.yaml
```

[Prev](../0_minimal/README.md) [Up](../README.md) [Next](../2_logging/README.md)