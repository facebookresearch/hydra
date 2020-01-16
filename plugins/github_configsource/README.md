# Hydra GitHub config source plugin
This plugin adds support for fetching configurations directly from a GitHub repository using the GitHub GraphQL API.
It adds a new config source scheme, github://, for example - adding this as a config source.

`github://owner.repo/path[?ref=ref]`

owner: repository owner or organization
repo: repository name
path: path inside the repository
ref: branch, tag or commit hash, defaults to master

Example github source path: 
```
github://facebookresearch.hydra/tests/test_apps/config_source_test_configs?ref=master
```
In this example, the owner is `facebookresearch`, the repo is `hydra`, the path is 
`/tests/test_apps/config_source_test_configs` and the branch/tag/commit is `master`  
                                       
and would grant access to files inside [tests/test_apps/config_source_test_configs](https://github.com/facebookresearch/hydra/tree/master/tests/test_apps/config_source_test_configs) in the master branch of the Hydra repo.

To gain access to a different branch, tag or commit hash, you can use:
 `github://facebookresearch.hydra/tests/test_apps/config_source_test_configs?ref=COMMIT_HASH_OR_NAME`


Important:
This plugin is experimental. performance is not good and GitHub rate limit is ridicules.
Do not use for serious work unless you are willing to invest time solving those issues.