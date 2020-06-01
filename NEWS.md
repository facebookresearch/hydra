1.0.0-rc1 (2020-05-31)
======================
Hydra 1.0 is a major release introducing many new features and breaking some compatibility.

Features
--------
- Upgrade to OmegaConf 2.0 ([Release notes](https://github.com/omry/omegaconf/releases/tag/2.0.0)) (#630)
- Optional config type safety via Structured Configs (#629)
- Improve command line and config composition error reporting (#349)
- Hydra config can now be accessed through interpolation using ${hydra:key}, for example ${hydra:job.name} ([#325](https://github.com/facebookresearch/hydra/issues/325))
- Support for setting environment variable of running job ([#7](https://github.com/facebookresearch/hydra/issues/7))
- Changes command line processing (requiring + and ~ prefixes for appending and removing items) ([#598](https://github.com/facebookresearch/hydra/issues/598))
- Introducing `@package` header for config files ([#586](https://github.com/facebookresearch/hydra/issues/586))
- Add command line override flags for `config_path` and `config_name` ([#386](https://github.com/facebookresearch/hydra/issues/386))
- hydra.main() now take an optional cfg object to passthrough to the function ([#575](https://github.com/facebookresearch/hydra/issues/575))
- Add hydra.experimental.{initialize_with_file, initialize_with_module} ([#574](https://github.com/facebookresearch/hydra/issues/574))
- Support for disabling the creation of the `.hydra` subdirectory by overriding "hydra.output_subdir" to "null" ([#324](https://github.com/facebookresearch/hydra/issues/324))
- Add `hydra.utils.call()` to call methods and functions as well as instantiate objects.  Search module paths more generically. ([#498](https://github.com/facebookresearch/hydra/issues/498))
- Add support for overriding package from command line and defaults list ([#235](https://github.com/facebookresearch/hydra/issues/235))
- Config source is now abstracted, allowing additional config sources to be used ([#257](https://github.com/facebookresearch/hydra/issues/257))
- New ConfigSource plugin API allowing configs to be provided by external plugins ([#367](https://github.com/facebookresearch/hydra/issues/367))
- Add isort to ensure imports are always sorted ([#340](https://github.com/facebookresearch/hydra/issues/340))
- Codebase is now passing mypy --strict type checking ([#342](https://github.com/facebookresearch/hydra/issues/342))
- Improve performance of plugin discovery and instantiation ([#489](https://github.com/facebookresearch/hydra/issues/489))
- Modules whose name starts with "_" are skipped during plugin discovery ([#494](https://github.com/facebookresearch/hydra/issues/494))

Plugins
-------
- Add [Ax](https://ax.dev) Sweeper plugin ([Shagun Sodhani](https://shagunsodhani.com/))
- Add [Nevergrad](https://github.com/facebookresearch/nevergrad) Sweeper plugin ([Jérémy Rapin](https://github.com/jrapin))
- Add [Joblib](https://joblib.readthedocs.io/en/latest/) Launcher plugin ([Jan-Matthis](https://github.com/jan-matthis))
- Add [Submitit](https://github.com/facebookincubator/submitit) Launcher plugin to launch jobs to SLURM clusters
- Add [Fish](https://fishshell.com/) shell Tab Completion plugin ([Binsheng Liu](https://binshengliu.github.io/)) ([#549](https://github.com/facebookresearch/hydra/issues/549))

API Change (Renames, deprecations and removals)
-----------------------------------------------
- Drop support Python 2.7 and 3.5 ([#313](https://github.com/facebookresearch/hydra/issues/313))
- hydra.main() now takes an additional optional config_name and composite-style config_path is deprecated ([#395](https://github.com/facebookresearch/hydra/issues/395))
- Launcher API launch method now takes an additional initial_job_idx indicating the id of the first job in the batch ([#284](https://github.com/facebookresearch/hydra/issues/284))
- Singleton metaclass is now exposed at hydra.core.Singleton ([#371](https://github.com/facebookresearch/hydra/issues/371))
- Moved HydraConfig from hydra.plugins.common.utils to hydra.core ([#371](https://github.com/facebookresearch/hydra/issues/371))
- Move several formerly internal APIs to hydra/core to ensure plugins does not need to use internal APIs ([#371](https://github.com/facebookresearch/hydra/issues/371))
- Plugin import now requires explicit name (from hydra.plugins.launcher import Launcher) ([#371](https://github.com/facebookresearch/hydra/issues/371))
- Object Config "class" field is deprecated in favor of "cls" and will be removed in a future version. ([#389](https://github.com/facebookresearch/hydra/issues/389))
- Experimental compose API config_file changed to config_name ([#395](https://github.com/facebookresearch/hydra/issues/395))
- User plugins should be modified to not import twice during plugin discovery. see issue for details. ([#482](https://github.com/facebookresearch/hydra/issues/482))
- Change hydra.core.plugins.Plugins class to a Singleton. access should be changed to the pattern Plugins.instance().foo() ([#489](https://github.com/facebookresearch/hydra/issues/489))
- Plugins should now include test fixtures (sweep_runner, task_runner) via a standardized conftest.py ([#521](https://github.com/facebookresearch/hydra/issues/521))
- Switch Python 3 native namespace packages for plugins (See task for details) ([#534](https://github.com/facebookresearch/hydra/issues/534))
- Packaged configuration directories now requires an `__init__.py` at their top level ([#536](https://github.com/facebookresearch/hydra/issues/536))
- Appending config groups to the defaults list via the command line now requires a + prefix ([#598](https://github.com/facebookresearch/hydra/issues/598))
- Removing an item from the defaults list by assigning null (db=null) is deprecated, use ~db instead ([#598](https://github.com/facebookresearch/hydra/issues/598))
- Installed Hydra applications no longer need have an additional `entry()` function on the stack ([#92](https://github.com/facebookresearch/hydra/issues/92))

Bug Fixes
---------

- Fix a bug causing sys.exit() error code to not be propagated ([#351](https://github.com/facebookresearch/hydra/issues/351))
- Shutdown logging subsystem aftter job finishes to ensure log files are flushed and closed ([#378](https://github.com/facebookresearch/hydra/issues/378))
- Fix a bug with utils.instantiate() failing if params contains interpolated values. ([#388](https://github.com/facebookresearch/hydra/issues/388))
- Allow hydra.utils.instantiate() to accept non primitive objects for passthrough by name ([#400](https://github.com/facebookresearch/hydra/issues/400))
- Fix to work when an Hydra app is executed in Jupyter notebook using the %run command ([#481](https://github.com/facebookresearch/hydra/issues/481))
- Plugins are no longer imported twice during plugin discovery ([#482](https://github.com/facebookresearch/hydra/issues/482))
- to_absolute_dir(path) now converts relative path to be relative to os.cwd() when used outside of Hydra ([#496](https://github.com/facebookresearch/hydra/issues/496))

Improved Documentation
----------------------

- Working examples are provided for all Hydra plugins in [plugins/examples](https://github.com/facebookresearch/hydra/tree/master/plugins/examples) ([#253](https://github.com/facebookresearch/hydra/issues/253))
- The basic tutorial was rewritten to reflect many changes ([#602](https://github.com/facebookresearch/hydra/issues/602))
- Add a new tutorial covering Structured Configs ([#628](https://github.com/facebookresearch/hydra/issues/628))


0.11.3 (2019-12-29)
===================

Bug Fixes
---------

- Pin Hydra 0.11 to OmegaConf 1.4 to avoid breaking compatibility when OmegaConf 2.0 is released ([#334](https://github.com/facebookresearch/hydra/issues/334))

Improved Documentation
----------------------

- Document a simple Ray example ([#317](https://github.com/facebookresearch/hydra/issues/317))


0.11.2 (2019-12-04)
===================

Features
--------

- Change website from cli.dev to hydra.cc (#314)

Bug Fixes
---------

- Fixes --cfg command line flag not working (#305)


0.11.0 (2019-11-19)
===================

Features
--------

- Add hydra.experimental API for composing configuration on demand (hydra.experimental.compose) (#219)
- Add hydra.utils.get_original_cwd() to access original working directory and hydra.utils.to_absolute_path() to convert a path to absolute path (#251)
- Change hydra logging format pattern, example: "[2019-10-22 16:13:10,769][HYDRA] Installed Hydra Plugins" (#254)
- Change --cfg to require config type (one of 'job', 'hydra' or 'all') (#270)
- Upgrade to OmegaConf 1.4.0, see full change log [here](https://github.com/omry/omegaconf/releases/tag/1.4.0) (#280)
- Experimental support for Jupyter notebooks via compose API (#281)
- Allow configuring override_dirname via hydra.job.config.override_dirname to exclude specific keys or change separator characters (#95)

Bug Fixes
---------

- Fix a bug that caused out of order composition when mixing config-groups with non-config-group in the defaults block (#261)
- Allow '=' to be used in the value of an override, eg. foo=bar=10 (key foo, value bar=10). (#266)
- Allow composing config files with dot in their name (foo.bar.yaml) (#271)

Plugins
-------

- hydra-colorlog plugin adds colored log output.

Improved Documentation
----------------------

- Document utils.get_original_cwd() and utils.to_absolute_path("foo") (#251)


0.10.0 (2019-10-19)
===================

Configuration structure changes
-------------------------------

- Change the default sweep subdir from ${hydra.job.num}_${hydra.job.id} to ${hydra.job.num} (#150)

Features
--------

- App help now contains config groups and generated config
  App help can now be customized
  Hydra help is now available via --hydra-help (#1)
- Simplify install and uninstall commands for tab completion (#200)
- hydra.runtime.cwd now contains the original working directory the app was launched from (#244)

Bug Fixes
---------

- Fix an error with tab completion that occurred when a TAB was pressed after two spaces (#203)
- Fix a bug when sweeping over groups that are used in an interpolation in defaults (#206)
- Fix tab completion for cases where app name looks like foo.par (#213)

Improved Documentation
----------------------

- Describe news fragment types in more details in development/contributing (#150)
- Examples dir now mirrors the structure of the website docs (#209)


0.9.0 (2019-10-01)
==================

Deprecations and Removals
-------------------------

- Old demos directory was removed and a new tutorial directory as added (#167)

Features
--------

- Make strict mode the default when a config file is specified directly (#150)
- Replace --verbose with a standard override (hydra.verbose) (#161)
- Add IntegrationTestSuite to test_utils for testing Launcher plugins (#168)
- Add support for specifying which config to print in -c, options are job (default), hydra or all. (#176)
- Hydra is now hosted on https://cli.dev! (#75)
- Move all Hydra configuration files to a subfolder (.hydra by default) under the output folder (#77)

Bug Fixes
---------

- Fix a bug in tab completion of missing mandatory values. (#145)
- Fix a bug with multirun overriding free config groups (not in defaults) when strict mode is enabled (#181)
- Fix a bug that prevented sweeping over an unspecified ('???') default group (#187)

Improved Documentation
----------------------

- Updated the primary tutorial on the web site and added a brand new tutorial directory (#58)
- Documented debugging methods in website (#6)


0.1.5 (2019-09-22)
==================

Deprecations and Removals
-------------------------

- Move FAIRTask, Submititit and FAIR-cluster-defaults plugins to fairinternal/hydra-fair-plugins repository (#138)
- Remove Fairtask and Submitit example configs from demos as they are no longer needed (#146)

Features
--------

- Created hydra-core pip package, Hydra can now installed with 'pip install hydra-core' (#143)
- Finalized submitit support (#18)

Plugins
-------

- Add default launcher config for Fairtask and Submitit launcher plugins


0.1.4 (2019-09-18)
==================

Features
--------

- hydra.utils.instantiate() can now take an additional optional kwargs dictionary to pass to constructor of the instantiated object (#142)
- Initial support for bash completion, see documentation for details (#8)

Bug Fixes
---------

- Fixed Town Crier to generate correct links to issues in generated news file. (#122)
- Fixed bug with overriding hydra defaults from user config file. (#123)
- Fixed Singletons not getting serialized to remote jobs. (#128)
- Fixed a bug that prevented using submitit in strict mode (#129)
- Fixed example submitit config to set the job name (#133)


0.1.3 (2019-09-02)
==================

Configuration structure changes
-------------------------------

- Changed Hydra core defaults to be more appropriate for open source use. To get the FAIR cluster defaults install the fair_cluster plugin (#103)
- Changed output directories default to group by day (output/DAY/TIME instead of output/DAY_TIME) (#121)

Features
--------

- Added the ability to prevent a default from being merged it by assigning null to it (hydra/launcher=null) (#106)
- Implemented Plugin discovery mechanism, this can be used to find all installed plugins that implement a specific interface (#119)
- Implemented an API to for manipulating the config search path (#120)

Bug Fixes
---------

- Fixed config loading to properly support the use case in demos/8_specializing_config (#104)
- Fixed error message when the user config contains defaults that is a mapping and not a list (#107)
- Fixed config loading order to allow properly overriding Hydra config groups from user config (#115)

Plugins
-------

- New plugin: fair_cluster
  Change Hydra defaults to be appropriate for the FAIR cluster

Improved Documentation
----------------------

- Initial search path and plugins documentation (#103)


0.1.2 (2019-08-26)
==================

Deprecations and Removals
-------------------------

- Hydra config groups were moved to the hydra/namespace (#101)
- Removed support for .hydra directory, Hydra can be configured directly from the job config. (#91)

Bug Fixes
---------

- Config loading rewrite fixed #88 (#88)


0.1.1 (2019-08-22)
==================

Deprecations and Removals
-------------------------

- Move non-public APIs into hydra._internal:
    - Moved non-API code into hydra._interanl to flag it as private.
    - Moved plugin interfaces into hydra.plugins.
    - Moved code meant to be used by plugins to hydra.plugins.common. (#78)

Features
--------

- Integrated towncrier to bring you this news! (#45)
- Hydra is now compatible with Windows (#63)
- Hydra apps can now be packaged and installed along with their configuration files. (#87)

Bug Fixes
---------

- It is now possible to use ${override_dirname} in the output directory of a local job (#31)
- Override_dirname separator changed from : to =, for example: foo/a:10,b:10 => foo/a=10,b=10 (#63)
- Fixed automatic detection of missing copyright headers (#72)
- fixed a bug that caused an empty config to be returned if specifed config file did not have a .yaml extension. (#80)
- Multi change diff:
    - Logging config search path in verbose logging to assist debugging of config load issues
    - Saving hydra.yaml into the job dir to assist debugging hydra issues
    - Fixed a bug caused by fairtask logging change
    - Improved integration-tests debuggability by switching hydra to debug logging in them
    - Added selective plugin testing to nox using env, for example PLUGINS=fairtask would only test fairtask. (#87)

Improved Documentation
----------------------

- Improved the contributing docs (#45)
- Documented Hydra app packaging under Deployment/Application packaging (#87)
