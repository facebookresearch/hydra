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
pip install -r requirements/dev.txt -e .
```

### Website setup

The website is built using [Docusaurus 2](https://v2.docusaurus.io/).  
Run the following commands from the `website` directory.

#### Install

```
$ yarn
```
#### Local Development

```
$ yarn start
```

This command starts a local development server and open up a browser window. Most changes are reflected live without having to restart the server.

For more details, refer [here](https://github.com/facebookresearch/hydra/blob/master/website/README.md).


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
 - `yamllint .` : Ensures that yaml files are syntactically correct and properly indented.

The easiest way to run the required verifications is: 
 - `nox -s lint` : for the Hydra core
 - `nox -s lint_plugins` : for the included plugins

isort is a bit tricky to run for plugins. the best way to get it to sort the plugins imports is with the FIX environment
variable:
```
$ FIX=1 nox -s lint_plugins
```

It is also recommended that you install pre-commit hooks (use `pre-commit install`).
pre-commit will execute some of the above tets when you commit your code locally. 
You can disable it by appending `-n` to your commit command: `git commit -am wip -n`

Pull requests that does not lint will fail the automated testing.

## Testing
### With pytest
Use `pytest` at the repository root to run all the Hydra core tests.
To run the tests of individual plugins, use `pytest plugins/NAME`.
<div class="alert alert--info" role="alert">
<strong>NOTE</strong>:
Some plugins support fewer versions of Python than the Hydra core.
</div>

### With nox
See `nox -l`. a few examples:
* `nox -s test_core` will test Hydra core on all supported Python versions
* `nox -s "test_core-3.6(pip install)"` : Test on Python 3.6 with `pip install` as installation method
* `nox -s "test_plugins-3.8(pip install -e)"` : Test plugins on Python 3.8 with `pip install -e` as installation method

## NEWS Entries
The [`NEWS.md`](https://github.com/facebookresearch/hydra/blob/master/NEWS.md) file is managed using `towncrier` and all non trivial changes
must be accompanied by a news entry.

To add an entry to the news file, first you need to have created an issue
describing the change you want to make. A Pull Request itself *may* function as
such, but it is preferred to have a dedicated issue (for example, in case the
PR ends up rejected due to code quality reasons).

Once you have an issue or pull request, you take the number and you create a
file inside of the ``news/`` directory named after that issue number with one of the following extensions:
* `api_change` : API Change (Renames, deprecations and removals)
* `feature` : Addition of a new feature
* `bugfix` : Fixing of a bug
* `docs` : Addition or updates to documentation
* `plugin` : Addition of changes to a plugin
* `config` : Changes or addition to the configuration structure
* `maintenance` : Changes that improve maintainability of the code

If your issue or PR number is ``1234`` and this change is fixing a bug, then you would
create a file ``news/1234.bugfix``. PRs can span multiple categories by creating
multiple files (for instance, if you added a feature and deprecated/removed the
old feature at the same time, you would create ``news/NNNN.feature`` and
``news/NNNN.api_change``). Likewise if a PR touches multiple issues/PRs you may
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
