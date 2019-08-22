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
