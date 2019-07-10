## Customized logging

This example shows you how to use your own python logging configuration file.
Changes here are that this logger only outputs to stdout and it has a simpler log line pattern.

.hydra/hydra.yaml
```yaml
defaults:
  - logging
```

.hydra/logging.yaml
```yaml
hydra:
  # python logging configuration
  logging:
    version: 1
    formatters:
      simple:
        format: '[%(levelname)s] - %(message)s'
    handlers:
      console:
        class: logging.StreamHandler
        formatter: simple
        stream: ext://sys.stdout
    root:
      level: INFO
      handlers: [console]

    disable_existing_loggers: False
```
 
Output:

```bash
$ python demos/99_hydra_configuration/logging/main.py
[INFO] - Info level message
```