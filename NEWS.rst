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
