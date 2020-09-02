---
id: documentation
title: Documentation
sidebar_label: Documentation
---

## NEWS Entries
The [`NEWS.md`](https://github.com/facebookresearch/hydra/blob/master/NEWS.md) file is managed using `towncrier` and all non-trivial changes
must be accompanied by a news entry.

To add an entry to the news file, first, you need to have created an issue
describing the change you want to make. A Pull Request itself *may* function as
such, but it is preferred to have a dedicated issue (for example, in case the
PR ends up rejected due to code quality reasons).

Once you have an issue or pull request, you take the number, and you create a
file inside the ``news/`` directory named after that issue number with one of the following extensions:
* `api_change` : API Change (Renames, deprecations, and removals)
* `feature` : Addition of a new feature
* `bugfix` : Fixing of a bug
* `docs` : Addition or updates to documentation
* `plugin` : Addition of changes to a plugin
* `config` : Changes or addition to the configuration structure
* `maintenance` : Changes that improve the maintainability of the code

If your issue or PR number is ``1234`` and this change is fixing a bug, you would
create a file ``news/1234.bugfix``. PRs can span multiple categories by creating
multiple files (for instance, if you added a feature and deprecated/removed the
old feature at the same time, you would create ``news/NNNN.feature`` and
``news/NNNN.api_change``). Likewise, if a PR touches multiple issues/PRs, you may
create a file for each of them with the exact same contents, and Towncrier will
deduplicate them.


### Contents of a NEWS entry
The contents of this file are markdown formatted text that will be used
as the content of the news file entry. You do not need to reference the issue
or PR numbers here as towncrier will automatically add a reference to all of
the affected issues when rendering the news file.

To maintain a consistent style in the `NEWS.md` file, it is
preferred to keep the news entry to the point, in sentence case, shorter than
80 characters and in an imperative tone -- an entry should complete the sentence
"This change will ...". In rare cases, where one line is not enough, use a
summary line in an imperative tone followed by a blank line separating it
from a description of the feature/change in one or more paragraphs, each wrapped
at 80 characters. Remember that a news entry is meant for end users and should
only contain details relevant to an end user.

## Website setup

The website is built using [Docusaurus 2](https://v2.docusaurus.io/).  
Run the following commands from the `website` directory.

### Install

```
$ yarn
```
### Local Development

```
$ yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

For more details, refer [here](https://github.com/facebookresearch/hydra/blob/master/website/README.md).
