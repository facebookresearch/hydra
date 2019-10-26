---
id: contributing
title: Contributing
sidebar_label: Contributing
---

This guide assumes you have forked and checked-out the repository.
It is recommended that you install Hydra in a virtual environment like conda or virtualenv.

### Environment setup
Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) and create an empty Conda environment with:
```
conda create -n hydra37 python=3.7 -y
```

<div class="alert alert--info" role="alert">
<strong>NOTE</strong>:
The core Hydra framework supports Python 2.7 or newer. You may need to create additional environments for different Python versions if
CI detect issues on supported version of Python.
</div>
<br/>

Activate the environment:
```
conda activate hydra37
```
From the source tree, install Hydra in development mode with the following command:
```
pip install -e '.[dev]' -e .
```

### Pre commit hooks
It is highly recommended that you install pre commit hooks into your local git repository.
```
pre-commit install
```
Pre commit hooks can help you catch problems before you push your pull request.
#### Hooks
 - black : automatic code formatting for Python
 - flake8: pep8 compliance checker for Python, this includes copyright header verification.
any PR that does not pass black and flake8 will fail the automated testing.


## Testing
There are two ways to run the tests:
### With pytest
use `pytest` at the repository root to run all the Hydra core tests.
To run the tests of individual plugins, use `pytest plugins/NAME`.
<div class="alert alert--info" role="alert">
<strong>NOTE</strong>:
Some plugins supports fewer versions of Python than the Hydra core. 
</div>

### With nox
Nox is a test automation tool that is used by the CI to test Hydra under multiple Python versions with a single command.

To trigger a full nox run, just run `nox`.

You may want to run specific nox sessions as well to speed things up. 
`nox -l` will list all available sessions.
You can use `nox -s NAME` to run a specific session.

For example:
 * `nox -s test_core` will test Hydra core on all supported Python versions
 * `nox -s lint` will lint the code in both Python 2 and Python 3.
 * `nox -s coverage` will run the code coverage tool

## NEWS Entries
The `NEWS.rst` file is managed using `towncrier` and all non trivial changes
must be accompanied by a news entry.

To add an entry to the news file, first you need to have created an issue
describing the change you want to make. A Pull Request itself *may* function as
such, but it is preferred to have a dedicated issue (for example, in case the
PR ends up rejected due to code quality reasons).

Once you have an issue or pull request, you take the number and you create a
file inside of the ``news/`` directory named after that issue number with one of the following extensions:
* `removal` : Removal of deprecation of a feature
* `feature` : Addition of a new feature
* `bugfix` : Fixing of a bug
* `docs` : Addition or updates to documentation
* `plugin` : Addition of changes to a plugin
* `config` : Changes or addition to the configuration structure

If your issue or PR number is ``1234`` and this change is fixing a bug, then you would
create a file ``news/1234.bugfix``. PRs can span multiple categories by creating
multiple files (for instance, if you added a feature and deprecated/removed the
old feature at the same time, you would create ``news/NNNN.feature`` and
``news/NNNN.removal``). Likewise if a PR touches multiple issues/PRs you may
create a file for each of them with the exact same contents and Towncrier will
deduplicate them.


### Contents of a NEWS entry
The contents of this file are reStructuredText formatted text that will be used
as the content of the news file entry. You do not need to reference the issue
or PR numbers here as towncrier will automatically add a reference to all of
the affected issues when rendering the news file.

In order to maintain a consistent style in the ``NEWS.rst`` file, it is
preferred to keep the news entry to the point, in sentence case, shorter than
80 characters and in an imperative tone -- an entry should complete the sentence
"This change will ...". In rare cases, where one line is not enough, use a
summary line in an imperative tone followed by a blank line separating it
from a description of the feature/change in one or more paragraphs, each wrapped
at 80 characters. Remember that a news entry is meant for end users and should
only contain details relevant to an end user.
