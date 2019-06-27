## Logging
Hydra configures python logging for your job.

```python
# A logger for this file
log = logging.getLogger(__name__)

@hydra.main()
def experiment(cfg):
    log.info("Info level message")
    log.debug("Debug level message")
```

```text
$ python demos/2_logging/logging_example.py
[2019-06-27 00:52:46,653][__main__][INFO] - Info level message
```

You can enable debug logging from the command line.
```text
$ python demos/2_logging/logging_example.py -v root
[2019-06-27 00:53:24,346][__main__][INFO] - Info level message
[2019-06-27 00:53:24,346][__main__][DEBUG] - Debug level message
```

The root logger is a special logger is the parent of all loggers. by using -v root you get verbose logging from
all python loggers, even from libraries.
You can also selectively choose loggers:
```text
$ python demos/2_logging/logging_example.py -v __main__
[2019-06-27 00:54:39,440][__main__][INFO] - Info level message
[2019-06-27 00:54:39,441][__main__][DEBUG] - Debug level message
```
-v takes a comma separated list of loggers.

Logging can be configured using hydra.yaml, more on hydra.yaml later.

[[Prev](../1_working_directory)] [[Up](../README.md)] [[Next](../3_config_file)]
