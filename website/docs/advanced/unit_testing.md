---
id: unit_testing
title: Composing configs in unit tests
---

Use the [Compose API](../experimental/hydra_compose.md) to compose configs inside unit tests.  
 
Each of the 3 initialization methods: `initialize()`, `initialize_config_module()` and `initialize_config_dir()` has a
corresponding context that can be used in unit tests.

Check the [example test](https://github.com/facebookresearch/hydra/tree/master/examples/advanced/hydra_app_example/tests/test_example.py) to see
them in action.

```python
@contextmanager
def initialize_ctx(
    config_path: Optional[str] = None,
    job_name: Optional[str] = "app",
    caller_stack_depth: int = 1,
) -> Any:
  ...


@contextmanager
def initialize_config_module_ctx(config_module: str, job_name: str = "app") -> Any:
  ...

@contextmanager
def initialize_config_dir_ctx(
    config_dir: str, job_name: Optional[str] = "app", caller_stack_depth: int = 1,
) -> Any:
  ...
```