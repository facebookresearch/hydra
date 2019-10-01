0.9.0 (2019-10-01)
==================

Deprecations and Removals
-------------------------

- Old demos directory was removed and a new tutorial directory as added (`#167 <https://github.com/facebookresearch/hydra/issues/167>`_)

Features
--------

- Make strict mode the default when a config file is specified directly (`#150 <https://github.com/facebookresearch/hydra/issues/150>`_)
- Replace --verbose with a standard override (hydra.verbose) (`#161 <https://github.com/facebookresearch/hydra/issues/161>`_)
- Add IntegrationTestSuite to test_utils for testing Launcher plugins (`#168 <https://github.com/facebookresearch/hydra/issues/168>`_)
- Add support for specifying which config to print in -c, options are job (default), hydra or all. (`#176 <https://github.com/facebookresearch/hydra/issues/176>`_)
- Hydra is now hosted on https://cli.dev! (`#75 <https://github.com/facebookresearch/hydra/issues/75>`_)
- Move all Hydra configuration files to a subfolder (.hydra by default) under the output folder (`#77 <https://github.com/facebookresearch/hydra/issues/77>`_)

Bug Fixes
---------

- Fix a bug in tab completion of missing mandatory values. (`#145 <https://github.com/facebookresearch/hydra/issues/145>`_)
- Fix a bug with multirun overriding free config groups (not in defaults) when strict mode is enabled (`#181 <https://github.com/facebookresearch/hydra/issues/181>`_)
- Fix a bug that prevented sweeping over an unspecified ('???') default group (`#187 <https://github.com/facebookresearch/hydra/issues/187>`_)

Improved Documentation
----------------------

- Updated the primary tutorial on the web site and added a brand new tutorial directory (`#58 <https://github.com/facebookresearch/hydra/issues/58>`_)
- Documented debugging methods in website (`#6 <https://github.com/facebookresearch/hydra/issues/6>`_)


0.1.5 (2019-09-22)
==================

Deprecations and Removals
-------------------------

- Move FAIRTask, Submititit and FAIR-cluster-defaults plugins to fairinternal/hydra-fair-plugins repository (`#138 <https://github.com/facebookresearch/hydra/issues/138>`_)
- Remove Fairtask and Submitit example configs from demos as they are no longer needed (`#146 <https://github.com/facebookresearch/hydra/issues/146>`_)

Features
--------

- Created hydra-core pip package, Hydra can now installed with 'pip install hydra-core' (`#143 <https://github.com/facebookresearch/hydra/issues/143>`_)
- Finalized submitit support (`#18 <https://github.com/facebookresearch/hydra/issues/18>`_)

Plugins
-------

- Add default launcher config for Fairtask and Submitit launcher plugins


0.1.4 (2019-09-18)
==================

Features
--------

- hydra.utils.instantiate() can now take an additional optional kwargs dictionary to pass to constructor of the instantiated object (`#142 <https://github.com/facebookresearch/hydra/issues/142>`_)
- Initial support for bash completion, see documentation for details (`#8 <https://github.com/facebookresearch/hydra/issues/8>`_)

Bug Fixes
---------

- Fixed Town Crier to generate correct links to issues in generated news file. (`#122 <https://github.com/facebookresearch/hydra/issues/122>`_)
- Fixed bug with overriding hydra defaults from user config file. (`#123 <https://github.com/facebookresearch/hydra/issues/123>`_)
- Fixed Singletons not getting serialized to remote jobs. (`#128 <https://github.com/facebookresearch/hydra/issues/128>`_)
- Fixed a bug that prevented using submitit in strict mode (`#129 <https://github.com/facebookresearch/hydra/issues/129>`_)
- Fixed example submitit config to set the job name (`#133 <https://github.com/facebookresearch/hydra/issues/133>`_)


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
