---
id: task_name
title: Customizing task name
sidebar_label: Customizing task name
---

There are two ways to override the task name, via the command line and via the configuration file.

### Via the command line
Code:
```python
@hydra.main()
def experiment(_cfg):
    print(JobRuntime().get('name'))
```

By default the task name matches the python file name:
```text
$ python no_config_file_override.py
no_config_file_override
```

We can override with hydra.name from the command line:
```text
$ python no_config_file_override.py  hydra.name=overridden_name
overridden_name
```

### Via the configuration file

`config.yaml`:
```yaml
hydra:
  name: name_from_config_file
```

```python
@hydra.main(config_path='config.yaml')
def experiment(_cfg):
    print(JobRuntime().get('name'))
```

By default, we would get the name from the config file:
```text
$ python with_config_file_override.py
name_from_config_file
```
But we can still override it from the command line:
```text
$ python with_config_file_override.py hydra.name=overridden_name
overridden_name
```

Check the [runnable example](https://github.com/facebookresearch/hydra/tree/master/demos/99_hydra_configuration/task_name).