## Customized logging

This example shows you how to use your own python logging configuration file.
Changes here are that this logger only outputs to stdout and it has a simpler log line pattern.
Note that the resulting config will be a combination of the default logging config and your specification,
With your specification overriding the default.

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
    formatters:
      simple:
        format: '[%(levelname)s] - %(message)s'
    root:
      handlers: [console]
```
 
Output:

```bash
$ python demos/99_hydra_configuration/logging/main.py
[INFO] - Info level message
```