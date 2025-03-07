"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[3513],{76042:e=>{e.exports=JSON.parse('{"blogPosts":[{"id":"/2022/05/18/Hydra_1.2","metadata":{"permalink":"/blog/2022/05/18/Hydra_1.2","source":"@site/blog/2022-05-18-Hydra_1.2.md","title":"Hydra 1.2","description":"After many months and a lot of hard work by many people, Hydra 1.2 is released!","date":"2022-05-18T00:00:00.000Z","formattedDate":"May 18, 2022","tags":[{"label":"Hydra","permalink":"/blog/tags/hydra"},{"label":"Release","permalink":"/blog/tags/release"}],"readingTime":3.12,"hasTruncateMarker":true,"authors":[{"name":"Padraig Brady","url":"https://github.com/pixelb","imageURL":"https://graph.facebook.com/733244046/picture/?height=200&width=200"}],"frontMatter":{"title":"Hydra 1.2","author":"Padraig Brady","author_url":"https://github.com/pixelb","author_image_url":"https://graph.facebook.com/733244046/picture/?height=200&width=200","tags":["Hydra","Release"],"image":"/img/Hydra-Readme-logo2.svg"},"nextItem":{"title":"Hydra 1.1","permalink":"/blog/2021/06/13/Hydra_1.1"}},"content":"<p align=\\"center\\"><img src=\\"/img/Hydra-Readme-logo2.svg\\" alt=\\"logo\\" width=\\"70%\\" /></p>\\n\\nAfter many months and a lot of hard work by many people, Hydra 1.2 is released!\\nHydra 1.2 comes with OmegaConf 2.2, which has its own share of improvements.\\n\\n\x3c!--truncate--\x3e\\n\\nThis blog post highlights some of the most prominent features, check the release notes for a complete list of changes:\\n- Hydra 1.2 [release notes](https://github.com/facebookresearch/hydra/releases/tag/v1.2.0)\\n- OmegaConf 2.2 [release notes](https://github.com/omry/omegaconf/releases/tag/v2.2.1)\\n\\n### Major new features in Hydra 1.2\\n\\n- Easier integration with existing systems\\n  - Support not changing working directory at runtime\\n  - Default to not implicitly adding directories to the config path\\n- Improved support for reproducible experiments\\n  - Support defining multirun mode and sweeping parameters through config\\n  - Improved callback support for logging / persisting job runs\\n  - A new `--experimental-rerun` option to reproduce persisted single runs\\n- Improved instantiate API functionality\\n  - Support for instances partially defined from config, via a `_partial_` keyword\\n  - Accept `ListConfig`/`list`-type config as top-level input\\n- Better alignment with ecosystem versions\\n  - Support for Python 3.10, and ANTLR 4.9\\n- OmegaConf 2.2:\\n  - More flexible type hints in structured configs\\n  - Native support for bytes and pathlib.Path\\n\\n#### Object instantiation enhancements\\n\\n- Lists can now be passed directly to the instantiate API.\\nFor example one can now do:\\n\\n```python\\nfrom hydra.utils import instantiate\\n\\nlst = [\\n    {\\"_target_\\": \\"pathlib.Path\\", \\"_args_\\": [\\"foo\\"]},\\n    {\\"_target_\\": \\"pathlib.Path\\", \\"_args_\\": [\\"bar\\"]},\\n]\\n\\npaths = instantiate(lst)\\nprint(paths)\\n```\\n\\nResulting in:\\n\\n```python\\n$ python demo.py\\n[PosixPath(\'foo\'), PosixPath(\'bar\')]\\n```\\n\\n- Instances can now be partially defined in config with the `_partial_` keyword.\\nPlease see the [Instantiate API - Partial Instantiation](/docs/advanced/instantiate_objects/overview/#partial-instantiation) docs\\nfor a detailed example.\\n\\n\\n### OmegaConf 2.2 highlights\\n\\n#### More flexible type hints in structured configs\\nOmegaConf 2.2\'s structured configs support runtime type checking for an expanded set of type hints.\\nIt is now possible to use nested container types (e.g. dict-of-dict or list-of-list),\\nunions of primitive types, and containers with optional element types.\\n\\nHere is an example demonstrating these new capabilities:\\n```python\\nfrom dataclasses import dataclass\\nfrom typing import Dict, List, Optional, Union\\nfrom omegaconf import OmegaConf\\n\\n@dataclass\\nclass DemoConfig:\\n    union: Union[int, str, bool]\\n    dict_of_union: Dict[str, Union[int, str]]\\n    list_of_dict: List[Dict[int, float]]\\n    dict_of_optional: Dict[str, Optional[int]]\\n\\ncfg = OmegaConf.structured({\\"foo\\": DemoConfig})\\ncfg.foo.dict_of_union = {\\"abc\\": 123}  # ok\\ncfg.foo.dict_of_union = {\\"abc\\": 10.1}  # raises ValidationError!\\n# Value \'10.1\' of type \'float\' is incompatible with type hint \'Union[int, str]\'\\n```\\n\\n#### Native support for bytes and pathlib.Path\\nOmegaConf now supports binary data via Python\'s bytes type.\\n\\n```python\\ncfg = OmegaConf.create({b\\"binary_key\\": b\\"binary_value\\"})\\n```\\n\\nIn addition, OmegaConf now supports `pathlib.Path` instances as config values, easing workflows that involve the file system.\\n\\n```python\\nfrom pathlib import Path\\ncfg.my_homedir = Path.home()\\nassert cfg.my_homedir.is_dir()\\n```\\n\\nThe `bytes` and `pathlib.Path` types can be used as type hints in structured config class definitions,\\nand configs containing binary and Path data can be round-tripped to/from yaml files via OmegaConf\'s save/load/to_yaml/create methods.\\n\\n```python\\nyaml_data = OmegaConf.to_yaml(cfg)\\ncfg2 = OmegaConf.create(yaml_data)\\nassert cfg2[b\\"binary_key\\"] == b\\"binary_value\\"\\nassert isinstance(cfg2.my_homedir, Path)\\n```\\n\\n### Migrating from 1.1\\nHydra 1.2 is a major release. For most people, migrating from 1.1 to 1.2 will be smooth.\\nIn addition, for this release we introduce support for more compatible upgrades\\nthrough the [version_base](/docs/upgrades/version_base/) mechanism.\\nNew users are encouraged to use the latest defaults by setting `version_base=None` with `@hydra.main()` and `hydra.initialize()`,\\nwhile existing users have more control over what potentially incompatible changes are introduced when upgrading to Hydra 1.2.\\nPlease see the \\"Behavior changes\\" section of the [Hydra 1.2 release notes](https://github.com/facebookresearch/hydra/releases/tag/v1.2.0) for details.\\nOmegaConf 2.2 also has some API changes and deprecations (not protected by version_base), detailed in its [release notes](https://github.com/omry/omegaconf/releases/tag/v2.2.1).\\nPlease feel free to reach out for [help](/docs/intro#community) if you see a change in behavior that is not mentioned in the release notes.\\n\\nThat\'s it for now, take Hydra 1.2 for a spin!"},{"id":"/2021/06/13/Hydra_1.1","metadata":{"permalink":"/blog/2021/06/13/Hydra_1.1","source":"@site/blog/2021-06-13-Hydra_1.1.md","title":"Hydra 1.1","description":"After many months and a lot of hard work by many people, Hydra 1.1 is finally out!","date":"2021-06-13T00:00:00.000Z","formattedDate":"June 13, 2021","tags":[{"label":"Hydra","permalink":"/blog/tags/hydra"},{"label":"Release","permalink":"/blog/tags/release"}],"readingTime":3.73,"hasTruncateMarker":true,"authors":[{"name":"Omry Yadan","title":"Creator of Hydra","url":"https://github.com/omry","imageURL":"https://graph.facebook.com/733244046/picture/?height=200&width=200"}],"frontMatter":{"title":"Hydra 1.1","author":"Omry Yadan","author_title":"Creator of Hydra","author_url":"https://github.com/omry","author_image_url":"https://graph.facebook.com/733244046/picture/?height=200&width=200","tags":["Hydra","Release"],"image":"/img/Hydra-Readme-logo2.svg"},"prevItem":{"title":"Hydra 1.2","permalink":"/blog/2022/05/18/Hydra_1.2"},"nextItem":{"title":"Hydra Ray Launcher","permalink":"/blog/2020/12/22/Hydra_Ray_Launcher"}},"content":"<p align=\\"center\\"><img src=\\"/img/Hydra-Readme-logo2.svg\\" alt=\\"logo\\" width=\\"70%\\" /></p>\\n\\nAfter many months and a lot of hard work by many people, Hydra 1.1 is finally out!  \\nHydra 1.1 comes with OmegaConf 2.1, which has its own share of awesome new features.\\n\\n\x3c!--truncate--\x3e\\n\\nThis blog post highlights some of the most prominent features, check the release notes for a complete list of changes:\\n- Hydra 1.1 [release notes](https://github.com/facebookresearch/hydra/releases/tag/v1.1.0)\\n- OmegaConf 2.1 [release notes](https://github.com/omry/omegaconf/releases/tag/v2.1.0)\\n\\n### Major new features in Hydra 1.1\\n- More powerful config composition\\n  - Every config can now have a Defaults List\\n  - Composition order of current config can be controlled via the `_self_` keyword in the Defaults List\\n  - Support for composing multiple configs from the same config group\\n  - Support for configuring the config search path from the primary config\\n- Recursive instantiation\\n- Experimental callbacks support\\n- OmegaConf 2.1:\\n  - Relative interpolations\\n  - New OmegaConf interpolation grammar supporting nested interpolations and much more\\n  - More powerful custom resolvers\\n\\n### More powerful config composition\\nConfig composition is the key area of improvement in Hydra 1.1.  \\nThe biggest change is support for a Defaults List in any config, and not just the primary config.\\n\\nThis enables many new capabilities:\\n- Any config can now \\"extend\\" other configs. This enables config files to be associated with a Structured Config schema and to extend other config files\\n- A top level \\"experiment config\\" can now override the Defaults List as well as config values\\n- Complex frameworks can now have their own Defaults List, reducing boilerplate\\n\\nOther related changes include the ability to change the order a config is composed relative to config in its Defaults List by \\nadding `_self_` to the Defaults List and the ability to use multiple configs from the same config group.\\n\\nLearn more:\\n- [The Defaults List](/docs/advanced/defaults_list)\\n- [Extending configs](/docs/patterns/extending_configs)\\n- [Structured Configs Schema](/docs/tutorials/structured_config/schema)\\n- [Configuring Experiments](/docs/patterns/configuring_experiments)\\n- [Select multiple configs from config group](/docs/patterns/select_multiple_configs_from_config_group)\\n\\n### Object instantiation enhancements\\n`hydra.utils.instantiate()` now instantiates nested objects recursively.\\n\\nOther enhancements include:\\n- Support for positional arguments via the `_args_` config key\\n- Support for parameter conversion strategy was added via the `_convert_` config key\\n\\nLearn more [here](/docs/advanced/instantiate_objects/overview).\\n\\n### Hydra callbacks\\nA new experimental mechanism for user defined callbacks was added.\\nCallbacks enable user code to be executed automatically at various points in the lifecycle of your application. \\nThere are many potential use cases for this, for example automatic registration with your \\nfavorite experiment-tracking service.\\n\\nLearn more [here](/docs/experimental/callbacks).\\n\\n### OmegaConf 2.1 highlights\\nOmegaConf 2.1 includes many enhancements, bug fixes, and performance improvements.\\n\\n#### Relative interpolations\\nRelative interpolations enable accessing a config node relative to the node defining the interpolation:\\n```yaml\\nx: 10\\nb:\\n  y: 20\\n  a: {x}    # 10, absolute interpolation\\n  b: ${.y}  # 20, relative interpolation\\n  c: ${..x} # 10, relative interpolation\\n```\\n\\n#### Nested interpolations\\nOmegaConf 2.1 adds a new interpolation grammar supporting more sophisticated usage of interpolations.  \\nIn the following example, the default value to use if the environment variable `DB_USER` does not exist is defined in the `default_user` config node:  \\n```yaml\\ndefault_user: root\\ndb_user: ${oc.env:DB_USER,${default_user}}\\n```\\n\\n#### More powerful custom resolvers\\nOmegaConf custom resolvers can now access parent config node or the config root by defining\\nkeyword parameters named `_parent_` and `_root_`.\\n\\nIn the example below, we use `_parent_` to implement a sum function that defaults to 0 if the node does not exist:\\n\\n```python\\ndef sum(a, b, *, _parent_):\\n  return _parent_.get(a, 0) + _parent_.get(b, 0)\\n\\nOmegaConf.register_new_resolver(\\"sum\\", sum)\\ncfg = OmegaConf.create({\\n  \\"node\\": {\\n    \\"a\\": 1,\\n    \\"b\\": 2,\\n    \\"a_plus_b\\": \\"${sum:a,b}\\",\\n    \\"a_plus_z\\": \\"${sum:a,z}\\",\\n  },\\n})\\nprint(cfg.node.a_plus_b)  # 3\\nprint(cfg.node.a_plus_z)  # 1\\n```\\n\\n### Other notable improvements\\n- Config composition, especially for large configs - is significantly faster.\\n- `OmegaConf.resolve(cfg)` can be used for in-place interpolation resolution on a config object\\n- Improved compatibility of OmegaConf config objects with plain dict and list\\n- Support for bracketed style (`foo.bar` is equivalent to `foo[bar]`), this covers interpolations and `OmegaConf.{update, select}` usage\\n- PyDev.Debugger integration for easier debugging of config objects in PyCharm and VSCode\\n\\n### Migrating from 1.0\\nHydra 1.1 is a major release. For most people, migrating from 1.0 to 1.1 will be smooth.\\nHowever, there are some breaking changes listed in the release notes of OmegaConf 2.1 and Hydra 1.1.\\nMost changes come with a deprecation warning pointing to a specific migration guide page.\\nPlease feel free to reach out for [help](/docs/intro#community) if you see a change in behavior that is not mentioned in the release notes.\\n\\nThat\'s it for now, take Hydra 1.1 for a spin!"},{"id":"/2020/12/22/Hydra_Ray_Launcher","metadata":{"permalink":"/blog/2020/12/22/Hydra_Ray_Launcher","source":"@site/blog/2020-12-22-Hydra_Ray_Launcher.md","title":"Hydra Ray Launcher","description":"We are happy to announce that we are adding a Ray Launcher to the Hydra Launchers family.","date":"2020-12-22T00:00:00.000Z","formattedDate":"December 22, 2020","tags":[{"label":"Hydra","permalink":"/blog/tags/hydra"},{"label":"Ray","permalink":"/blog/tags/ray"},{"label":"Plugin","permalink":"/blog/tags/plugin"}],"readingTime":3.465,"hasTruncateMarker":true,"authors":[{"name":"Jieru Hu","url":"https://github.com/jieru-hu","imageURL":"https://graph.facebook.com/733244046/picture/?height=200&width=200"}],"frontMatter":{"title":"Hydra Ray Launcher","author":"Jieru Hu","author_url":"https://github.com/jieru-hu","author_image_url":"https://graph.facebook.com/733244046/picture/?height=200&width=200","tags":["Hydra","Ray","Plugin"],"image":"/img/Hydra-Readme-logo2.svg"},"prevItem":{"title":"Hydra 1.1","permalink":"/blog/2021/06/13/Hydra_1.1"},"nextItem":{"title":"Hydra 1.0","permalink":"/blog/2020/09/03/Hydra_1.0"}},"content":"We are happy to announce that we are adding a [Ray Launcher](https://hydra.cc/docs/plugins/ray_launcher) to the Hydra Launchers family. \\nHydra\'s Launcher plugins enable launching to different environments without changing your existing workflows or application code.\\nThe Hydra Ray Launcher can be used to launch your application to a new or existing [Ray cluster](https://docs.ray.io/en/master/cluster/launcher.html), \\nlocally or on AWS. In this post we demonstrate the major functionalities of the Launcher. \\nFor more details on installation and configuration, please check out the [Hydra Ray Launcher documentation](https://hydra.cc/docs/plugins/ray_launcher/). \\nAs always, please [join our community](https://github.com/facebookresearch/hydra#community) and give us feedback!\\n\x3c!--truncate--\x3e\\n\\n\\n[Ray](https://github.com/ray-project/ray) is a simple yet powerful Python library for parallel and distributed programming. Among the many features it provides, Ray comes with a \\n [cluster launcher](https://docs.ray.io/en/master/cluster/launcher.html#ref-automatic-cluster) that can be used to provision resources and start a Ray cluster on top of them. \\nHydra Ray Launcher is built on top of the [Ray Tasks API](https://docs.ray.io/en/master/ray-overview/index.html#parallelizing-python-java-functions-with-ray-tasks) and the Ray cluster launcher. \\n\\n\\n### Launching to a new or existing AWS cluster\\nHydra Ray Launcher simplifies your experience by allowing the Ray cluster setup to be \\nconfigured transparently by Hydra (eliminating the need for an external YAML file while maintaining \\nthe flexibility). Hydra Ray Launcher comes with reasonable default configurations which can be found \\n[here](https://hydra.cc/docs/plugins/ray_launcher/#ray_aws-launcher) (under the heading, \u201cDiscover ray_aws launcher\'s config\u201d). You can override them in your application\\n config or from the command line to fit your use case. \\n The following Ray Launcher example code (e.g., my_app.py) is runnable and can be found [here](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_ray_launcher/examples/simple). \\n\\nLaunch your Hydra application to AWS by simply overriding: `hydra/launcher=ray_aws`:\\n\\n```commandline\\n$ python my_app.py hydra/launcher=ray_aws task=1,2 --multirun\\n[HYDRA] Ray Launcher is launching 2 jobs, \\n[HYDRA]        #0 : task=1\\n[HYDRA]        #1 : task=2\\n...\\n[HYDRA] Running command: [\'ray\', \'up\', \'-y\', \'/var/folders/n_/9qzct77j68j6n9lh0lw3vjqcn96zxl/T/tmp20qvoy15.yaml\']\\n[HYDRA] Output: INFO services.py:1090 -- View the Ray dashboard at http://127.0.0.1:8265\\n(pid=3823)[__main__][INFO] - Executing task 1\\n(pid=3822)[__main__][INFO] - Executing task 2\\n[HYDRA] Stopping cluster now. (stop_cluster=true)\\n[HYDRA] Deleted the cluster (provider.cache_stopped_nodes=false)\\n[HYDRA] Running command: [\'ray\', \'down\', \'-y\', \'/var/folders/n_/9qzct77j68j6n9lh0lw3vjqcn96zxl/T/tmpfm2ems9v.yaml\']\\n```\\n\\n### Launching to a new local Ray Cluster\\nIf you want to do a quick local test, \\nyou can spin up a local Ray cluster at application run time by specifying `hydra/launcher=ray`. \\nIn this example, we create a new Ray cluster at application time. \\n```commandline\\n$ python my_app.py  --multirun hydra/launcher=ray \\n[HYDRA] Ray Launcher is launching 1 jobs, sweep output dir: multirun/2020-12-17/16-11-28\\n[HYDRA] Initializing ray with config: {\'address\': None}\\n2020-12-17 16:11:29,340 INFO services.py:1090 -- View the Ray dashboard at http://127.0.0.1:8265\\n[HYDRA]        #0 : \\n(pid=62642) [__main__][INFO] - Executing task 1\\n```\\n### Launching to an existing local Ray Cluster\\nYou can launch the application on an existing local Ray cluster by configuring the cluster address\\n and overriding `hydra/launcher=ray`. In the following example we configure the Ray cluster address\\n  to local ray cluster and Hydra Ray Launcher was able to connect to the existing Ray cluster and \\n  execute the application code:\\n```commandline\\n$ python my_app.py  --multirun hydra/launcher=ray hydra.launcher.ray.init.address=localhost:6379\\n[HYDRA] Ray Launcher is launching 1 jobs, sweep output dir: multirun/2020-11-10/15-13-32\\n[HYDRA] Initializing ray with config: {\'num_cpus\': None, \'num_gpus\': None, \'address\': \'localhost:6379\'}\\nINFO worker.py:633 -- Connecting to existing Ray cluster at address: 10.30.99.17:6379\\n[HYDRA]        #0 :\\n(pid=93358) [__main__][INFO] - Executing task 1\\n```\\n\\nHydra Ray Launcher is built on top of Hydra 1.0 and you have access to all of the benefits Hydra brings:\\n\\n### Parameter sweeps and optimization\\nHyperparameter sweeps are common in machine learning research. \\nHydra has built-in grid search and provides several Sweeper plugins for hyperparameter optimization.\\n Sweepers can be used together with Launchers for sweeping on different computing platforms. \\n Start from our documentation [here](https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/) to find more.\\n\\n### Config type safety\\nModern Hydra applications and Hydra Plugins leverage Structured Configs for config validation,\\n and Hydra Ray Launcher is no exception. In the following example, we try to override the Ray cluster\u2019s \\n autoscaling mode with an illegal value:\\n\\n```commandline\\n$ python my_app.py --multirun hydra.launcher.ray.cluster.autoscaling_mode=foo\\nError merging override hydra.launcher.ray.cluster.autoscaling_mode=foo\\nInvalid value \'foo\', expected one of [default, aggressive]\\n        full_key: hydra.launcher.ray.cluster.autoscaling_mode\\n        reference_type=RayClusterConf\\n        object_type=RayClusterConf\\n\\nSet the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.\\n```\\n\\nThat\u2019s it for now! Please try out the new Hydra Ray Launcher and let us know what you think. \\nWe are always happy to connect with you via [GitHub](https://github.com/facebookresearch/hydra) or the [Hydra Chat](https://hydra-framework.zulipchat.com/)."},{"id":"/2020/09/03/Hydra_1.0","metadata":{"permalink":"/blog/2020/09/03/Hydra_1.0","source":"@site/blog/2020-09-03-Hydra_1.0.md","title":"Hydra 1.0","description":"After many months and a lot of hard work by many people, Hydra 1.0 is finally out!","date":"2020-09-03T00:00:00.000Z","formattedDate":"September 3, 2020","tags":[{"label":"Hydra","permalink":"/blog/tags/hydra"},{"label":"Release","permalink":"/blog/tags/release"}],"readingTime":7.13,"hasTruncateMarker":true,"authors":[{"name":"Omry Yadan","title":"Creator of Hydra","url":"https://github.com/omry","imageURL":"https://graph.facebook.com/733244046/picture/?height=200&width=200"}],"frontMatter":{"title":"Hydra 1.0","author":"Omry Yadan","author_title":"Creator of Hydra","author_url":"https://github.com/omry","author_image_url":"https://graph.facebook.com/733244046/picture/?height=200&width=200","tags":["Hydra","Release"],"image":"/img/Hydra-Readme-logo2.svg"},"prevItem":{"title":"Hydra Ray Launcher","permalink":"/blog/2020/12/22/Hydra_Ray_Launcher"},"nextItem":{"title":"New Hydra blog","permalink":"/blog/2020/05/04/New-blog"}},"content":"<p align=\\"center\\"><img src=\\"/img/Hydra-Readme-logo2.svg\\" alt=\\"logo\\" width=\\"70%\\" /></p>\\n\\nAfter many months and a lot of hard work by many people, Hydra 1.0 is finally out!  \\nDespite some very big changes, this is still the Hydra you love - only bigger, stronger and with more heads.\\n\x3c!--truncate--\x3e\\n\\n## Major new features in Hydra 1.0\\n* Config type safety via Structured Configs\\n* More powerful command line\\n* New plugins enabling remote launching and hyper parameter optimization\\n* Improved error reporting\\n* Reduce nesting levels with config packages\\n\\n## Config type safety via Structured Configs\\nStructured Configs is a powerful new feature that enables strongly typed configs that can be validated both statically and at runtime.\\nWith Structured Configs, you use Python dataclasses to describe your configuration structure and types.\\nThey can be used as an alternative to YAML files, or as a way to validate YAML files automatically.\\n\\n<details><summary>See example (Click to expand)</summary>\\n\\nThis example is using a Structured Config as an alternative to a configuration file.\\n\\n```python\\n@dataclass\\nclass MySQLConfig:\\n    host: str = \\"localhost\\"\\n    port: int = 3306\\n\\ncs = ConfigStore.instance()\\ncs.store(name=\\"config\\", node=MySQLConfig)\\n\\n@hydra.main(config_name=\\"config\\")\\ndef my_app(cfg: MySQLConfig) -> None:\\n    if cfg.pork == 80: # pork should be port!\\n        print(\\"Is this a webserver?!\\")\\n```\\n\\nDuck-typing the config object as `MySQLConfig` enables static type checkers like `mypy` to catch\\ntype errors before you run your code:\\n```text title=\\"$ mypy my_app.py\\" \\nmy_app.py:22: error: \\"MySQLConfig\\" has no attribute \\"pork\\"\\nFound 1 error in 1 file (checked 1 source file)\\n```\\n\\nHydra will catch typos, or type errors in the command line:\\n```\\n$ python my_app.py port=fail\\nError merging override port=fail\\nValue \'fail\' could not be converted to Integer\\n        full_key: port\\n        reference_type=Optional[MySQLConfig]\\n        object_type=MySQLConfig\\n```\\n\\n</details><br/>\\n\\nLearn more at the [Structured Configs tutorial](/docs/tutorials/structured_config/intro).\\n\\n## More powerful command line\\nHydra 1.0 introduces a new command line with many new capabilities, such as:\\n\\n- Override, Add or Delete config values or Default list choices\\n- Cast values to coerce their type\\n- Specify dictionaries and lists as values\\n\\n<details><summary>See examples</summary>\\n\\n<div className=\\"row\\">\\n<div className=\\"col col--6\\">\\n\\n```text\\nOverride as usual\\n\\n\\n\\n```\\n\\n```text\\nPrefix with + to add a new field to\\nthe config\\n\\n\\n\\n```\\n\\n```text\\nPrefix with ~ to delete a field from\\nthe config\\n\\n```\\n\\n```text\\nCast values to coerce their type.\\n\\n\\n\\n```\\n\\n```text\\nSupport for dictionaries and lists\\n\\n\\n\\n\\n\\n\\n\\n```\\n\\n</div><div className=\\"col  col--6\\">\\n\\n```yaml\\n$ python my_app.py db.user=root\\ndb:\\n  user: root\\n  pass: secret\\n```\\n\\n```yaml\\n$ python my_app.py +db.timeout=10\\ndb:\\n  user: omry\\n  pass: secret\\n  timeout: 10\\n```\\n\\n```yaml\\n$ python my_app.py \'~db.pass\'\\ndb:\\n  user: omry\\n```\\n\\n```yaml\\n$ python my_app.py \'db.pass=str(42)\'\\ndb:\\n  user: omry\\n  pass: \'42\'\\n```\\n\\n```yaml\\n$ python my_app.py \\\\\\n  \'+db.params={a:10,b:20}\'\\ndb:\\n  user: omry\\n  pass: secret\\n  params:\\n    a: 10\\n    b: 20\\n```\\n\\n</div></div>\\n\\n</details><br/>\\n\\nLearn more at the [Basic Override syntax page](/docs/advanced/override_grammar/basic). \\n\\n## Sweeper improvements\\nAdvanced command line capabilities are making Hydra\'s Basic Sweeper more powerful.\\n\\n- Specify numeric ranges via the command line\\n- Use glob to select multiple config group options without specifying them explicitly\\n- Control sweeping order with sort and shuffle\\n\\n<details><summary>See examples</summary>\\n\\n<div className=\\"row\\">\\n<div className=\\"col col--6\\">\\n\\n```text\\nUse glob to easily select\\nmultiple config group options\\n```\\n\\n```text\\nUse range to specify a range of \\nnumbers\\n\\n\\n```\\n\\n```text\\nYou can sort sweep to run order\\n\\n\\n\\n\\n\\n\\n```\\n\\n```text\\nYou can also shuffle sweeps to run\\nin random order\\n\\n```\\n\\n\\n</div><div className=\\"col  col--6\\">\\n\\n```python\\n$ python my_app.py -m \'db=glob(*)\'\\n# Will sweep over all db options\\n```\\n\\n```python\\n$ python my_app.py --multirun \\\\\\n  \'+number=range(1,4)\'\\n# number will take the values\\n# 1,2 and 3 \\n```\\n\\n\\n```python\\n$ python my_app.py --multirun \\\\\\n  \'+num=sort(3,1,2)\'\\n# Sweep over num in order\\n\\n$ python my_app.py --multirun \\\\\\n  \'+num=sort(3,1,2,reverse=true)\'\\n# Sweep over num in reverse order\\n```\\n\\n```python\\n$ python my_app.py --multirun \\\\\\n  \'+num=shuffle(3,1,2)\'\\n# Sweep over num in random order\\n```\\n\\n</div></div>\\n\\n</details><br/>\\n\\nLearn more at the [Extended Override grammar](/docs/advanced/override_grammar/extended) page.\\n\\n\\n## New plugins\\n### Launchers\\nOne of the early promises of Hydra was that it will enable you to easily launch your application to different clusters.\\nHydra 1.0 adds a few Launchers plugins that starts to make good on that promise.\\n- The [Submitit Launcher](/docs/plugins/submitit_launcher) can launch applications to [SLURM](https://slurm.schedmd.com/documentation.html) cluster using [Submitit](https://github.com/facebookincubator/submitit).  \\n- The [Redis Queue launcher](/docs/plugins/rq_launcher) can launch applications to Redis Queue server.  \\n- The [Joblib Launcher](/docs/plugins/joblib_launcher) can launch your application with joblib, enabling parallel local execution.\\n\\n \\n### Sweepers\\nTwo new Sweeper plugins enables you to automatically find optimal parameters without changing a line of code.\\n- The [Ax Sweeper](/docs/plugins/ax_sweeper) brings the power of [Ax](https://ax.dev) to your Hydra app \\n- The [Nevergrad Sweeper](/docs/plugins/nevergrad_sweeper) brings the power of [Nevergrad](https://facebookresearch.github.io/nevergrad/) to your Hydra app \\n\\nNote that both Sweepers are still in beta and some changes are expected soon. Your feedback can help shape them.\\n\\n### Tab completion\\nIn addition to Bash, Hydra now supports [Fish](https://fishshell.com/) shell Tab Completion.\\n\\n\\n## Compose API improvements\\nThe experimental Compose API is maturing. It is now possible to initialize Hydra in one of 3 ways:\\n- `initialize()`: Initialize with a config path relative to the caller\\n- `initialize_config_module()` : Initialize with config_module (absolute)\\n- `initialize_config_dir()` : Initialize with a config_dir on the file system (absolute)\\n\\nAll initialization methods can be used to initialize Hydra globally or in a context. Making the Compose API ideal for\\nUnit tests and Jupyter notebooks.\\n  \\nLearn more at the [Compose API](/docs/1.0/experimental/compose_api) page.\\n\\n## Improved error reporting\\nReported errors will have un-interesting stack frames removed by default.\\nYou can enable the complete stack trace with the environment variable `HYDRA_FULL_ERROR=1`.\\n\\n<details><summary>See example of an error</summary>\\n\\n```python\\n@hydra.main()\\ndef my_app(cfg: DictConfig) -> None:\\n    1 / 0 # hmmm, seems fishy\\n\\nif __name__ == \\"__main__\\":\\n    my_app()\\n```\\n```python\\n$ python my_app.py\\nTraceback (most recent call last):\\n  File \\"my_app.py\\", line 9, in my_app\\n    1 / 0\\nZeroDivisionError: division by zero\\n\\nSet the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.\\n```\\n\\n</details><br/>\\n<details><summary>See example of a complete stack trace</summary>\\n\\n```python\\n$ HYDRA_FULL_ERROR=1 python my_app.py\\nTraceback (most recent call last):\\n  File \\"my_app.py\\", line 13, in <module>\\n    my_app()\\n  File \\"/home/omry/dev/hydra/hydra/main.py\\", line 32, in decorated_main\\n    _run_hydra(\\n  File \\"/home/omry/dev/hydra/hydra/_internal/utils.py\\", line 355, in _run_hydra\\n    run_and_report(\\n  File \\"/home/omry/dev/hydra/hydra/_internal/utils.py\\", line 210, in run_and_report\\n    raise ex\\n  File \\"/home/omry/dev/hydra/hydra/_internal/utils.py\\", line 207, in run_and_report\\n    return func()\\n  File \\"/home/omry/dev/hydra/hydra/_internal/utils.py\\", line 356, in <lambda>\\n    lambda: hydra.run(\\n  File \\"/home/omry/dev/hydra/hydra/_internal/hydra.py\\", line 107, in run\\n    return run_job(\\n  File \\"/home/omry/dev/hydra/hydra/core/utils.py\\", line 125, in run_job\\n    ret.return_value = task_function(task_cfg)\\n  File \\"my_app.py\\", line 9, in my_app\\n    1 / 0\\nZeroDivisionError: division by zero\\n```\\n\\n</details>\\n\\n## Reduce nesting levels with config packages\\nHydra 1.0 introduces the ability to specify the root `config package` in the config file.\\nSpecifying the root config package help reducing nesting levels in config files.\\nConfig packages can be overridden via the Defaults List or the command line, allowing the reuse of the the same\\nconfig in multiple place in the resulting output without having to duplicate it.\\n\\n\\n<details><summary>See example of reduced nesting</summary>\\n\\nThe following two `db/mysql.yaml` files are equivalent:\\n\\n<div className=\\"row\\">\\n<div className=\\"col col--6\\">\\n\\n```yaml title=\\"Hydra 0.11\\"\\ndb:\\n  host: localhost\\n  port: 3306\\n```\\n\\n</div><div className=\\"col  col--6\\">\\n\\n```yaml title=\\"Hydra 1.0\\"\\n# @package _group_\\nhost: localhost\\nport: 3306\\n```\\n</div></div>\\n\\n</details>\\n\\n \\n<details><summary>See example of config reuse</summary>\\n  \\nAdd the `mysql` config in the packages `db.src` and `db.dst`, reusing `db/mysql.yaml`.\\n\\n<div className=\\"row\\">\\n<div className=\\"col col--6\\">\\n\\n```yaml title=\\"config.yaml\\"\\ndefaults:\\n - db@db.src: mysql\\n - db@db.dst: mysql\\n\\n\\n\\n\\n```\\n</div><div className=\\"col  col--6\\">\\n\\n```yaml title=\\"Interpretation\\"\\ndb:\\n  src:\\n    host: localhost\\n    port: 3306\\n  dst:\\n    host: localhost\\n    port: 3306\\n```\\n</div></div>\\n</details>\\n<br/>\\n\\nLearn more at the [Overriding packages](/docs/advanced/overriding_packages) page.\\n\\n## Misc improvements\\n- The `params` field is eliminated from instantiated objects configs ([details](/docs/upgrades/0.11_to_1.0/object_instantiation_changes))\\n- Support for setting environment variables via the config. (`hydra.job.env_set`) ([details](/docs/configure_hydra/job#hydrajobenv_set))\\n- Hydra\'s config can now be accessed through interpolation using `${hydra:key}`, for example `${hydra:job.name}` ([details](/docs/configure_hydra/intro#runtime-variables))\\n- Introduced `--info` flag for quick access to debug information ([details](/docs/tutorials/basic/running_your_app/debugging#info))\\n- Add `--package` flag, can be used with `--cfg` to print a specific config package ([details](/docs/advanced/hydra-command-line-flags#--package-p))\\n- Override the `config_path` and `config_name` from the command line with `--config-name` and `--config-path` ([details](/docs/advanced/hydra-command-line-flags#--config-path-cp))\\n- Add an additional config directory to the search path with `--config-dir` ([details](/docs/advanced/hydra-command-line-flags#--config-dir-cd))\\n\\n## Migrating from 0.11\\nFor most people, migrating from 0.11 to 1.0 will be smooth.\\nHowever, you will have issues if you are relying on Python 2 support or have used internal APIs.\\n- Hydra 1.0 drops support for [Python 2](https://www.python.org/doc/sunset-python-2/).\\n- If you are relying on internal APIs, Hydra 1.0 will likely break your code. Maintaining backward compatibility for internal APIs is not a goal.\\n- Hydra 0.11 Configs pickled and stored will not unpickle with Hydra 1.0 due to internal changes in OmegaConf.\\n\\nThere are multiple new deprecation warnings, each with a link to mini migration guide.\\n\\n\\nThat\'s it for now, take Hydra 1.0 for a spin!"},{"id":"/2020/05/04/New-blog","metadata":{"permalink":"/blog/2020/05/04/New-blog","source":"@site/blog/2020-05-04-New-blog.md","title":"New Hydra blog","description":"Welcome to the Hydra blog.","date":"2020-05-04T00:00:00.000Z","formattedDate":"May 4, 2020","tags":[{"label":"Hydra","permalink":"/blog/tags/hydra"}],"readingTime":0.155,"hasTruncateMarker":true,"authors":[{"name":"Omry Yadan","title":"Creator of Hydra","url":"https://github.com/omry","imageURL":"https://graph.facebook.com/733244046/picture/?height=200&width=200"}],"frontMatter":{"title":"New Hydra blog","author":"Omry Yadan","author_title":"Creator of Hydra","author_url":"https://github.com/omry","author_image_url":"https://graph.facebook.com/733244046/picture/?height=200&width=200","tags":["Hydra"]},"prevItem":{"title":"Hydra 1.0","permalink":"/blog/2020/09/03/Hydra_1.0"}},"content":"Welcome to the Hydra blog.\\n\x3c!--truncate--\x3e\\n\\nCatching up on some previous content:\\n\\n##### Apr/8/2020\\n[FLOSS Weekly interview](https://twit.tv/shows/floss-weekly/episodes/573)\\n\\n##### Feb/3/2020\\n[PyTorch Medium channel blog post](http://bit.ly/2Sdq2B3)\\n\\n##### Oct/3/2019\\n[Facebook engineering blog release post](https://engineering.fb.com/open-source/hydra/)"}]}')}}]);