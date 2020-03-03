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
conda create -n hydra38 python=3.8 -y
```

<div class="alert alert--info" role="alert">
<strong>NOTE</strong>:
The core Hydra framework supports Python 3.6 or newer. You may need to create additional environments for different Python versions if
CI detect issues on supported version of Python.
</div>
<br/>

Activate the environment:
```
conda activate hydra38
```
From the source tree, install Hydra in development mode with the following command:
```
pip install -e ".[dev]" -e .
```
## Nox
Hydra is using a test automation tool called [nox](https://github.com/theacodes/nox) to manage tests, linting, code coverage etc. 
`nox` will run all the configured sessions. You can see the full list of nox sessions with `nox -l` and run specific sessions
with `nox -s NAME` (you may need to quote the session name in some cases)

## Code style guide
The code need to pass verification by the following tools:
 - `black .` : Automatic code formatting for Python
 - `flake8` : PEP8 compliance checker for Python, this includes copyright header verification
 - `isort .` : Ensure imports are sorted properly
 - `mypy --strict .` : Ensures code passes strict type checking
 
The easiest way to run all the required verifications is with `nox -s lint`.

It is also recommended that you install pre-commit hooks (use `pre-commit install`), this will ensure that those tests
are ran just before you commit your code.

Any pull request that does not pass the linting will fail the automated testing.


## Testing
### With pytest
Use `pytest` at the repository root to run all the Hydra core tests.
To run the tests of individual plugins, use `pytest plugins/NAME`.
<div class="alert alert--info" role="alert">
<strong>NOTE</strong>:
Some plugins supports fewer versions of Python than the Hydra core. 
</div>

### With nox
See `nox -l`. a few examples:
* `nox -s test_core` will test Hydra core on all supported Python versions
* `nox -s "test_core-3.6(pip install)"` : Test on Python 3.6 with `pip install` as installation method
* `nox -s "test_plugins-3.8(pip install -e)"` : Test plugins on Python 3.8 with `pip install -e` as installation method  

## NEWS Entries
The `NEWS.md` file is managed using `towncrier` and all non trivial changes
must be accompanied by a news entry.

To add an entry to the news file, first you need to have created an issue
describing the change you want to make. A Pull Request itself *may* function as
such, but it is preferred to have a dedicated issue (for example, in case the
PR ends up rejected due to code quality reasons).

Once you have an issue or pull request, you take the number and you create a
file inside of the ``news/`` directory named after that issue number with one of the following extensions:
* `removal` : Removal or deprecation of a feature
* `feature` : New feature
* `bugfix` : Bug fix
* `plugin` : New plugin, or an update to an existing plugin
* `config` : Changes or addition to the configuration structure of Hydra
* `docs` : Major addition or updates to documentation

If your issue or PR number is ``1234`` and this change is fixing a bug, then you would
create a file ``news/1234.bugfix``. PRs can span multiple categories by creating
multiple files (for instance, if you added a feature and deprecated/removed the
old feature at the same time, you would create ``news/NNNN.feature`` and
``news/NNNN.removal``). Likewise if a PR touches multiple issues/PRs you may
create a file for each of them with the exact same contents and Towncrier will
deduplicate them.


### Contents of a NEWS entry
The contents of this file is markdown formatted text that will be used
as the content of the news file entry. You do not need to reference the issue
or PR numbers here as towncrier will automatically add a reference to all of
the affected issues when rendering the news file.

In order to maintain a consistent style in the `NEWS.md` file, it is
preferred to keep the news entry to the point, in sentence case, shorter than
80 characters and in an imperative tone -- an entry should complete the sentence
"This change will ...". In rare cases, where one line is not enough, use a
summary line in an imperative tone followed by a blank line separating it
from a description of the feature/change in one or more paragraphs, each wrapped
at 80 characters. Remember that a news entry is meant for end users and should
only contain details relevant to an end user.
