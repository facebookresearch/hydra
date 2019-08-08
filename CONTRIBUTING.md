# Contributing to hydra
We want to make contributing to this project as easy and transparent as
possible.


## Getting started
Checkout this repository, Install Hydra and all the included plugins in development mode with:
```
pip install -e . && find ./plugins/ -name setup.py | xargs dirname | xargs pip install  -e 
```


You can uninstall Hydra and all the included plugins with:
```
pip uninstall -y hydra && find ./plugins/ -name setup.py |\
xargs -i python {}  --name | xargs pip uninstall  -y
```

## Pull Requests
We actively welcome your pull requests.

1. Fork the repo and create your branch from `master`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. If you haven't already, complete the Contributor License Agreement ("CLA").

## Contributor License Agreement ("CLA")
In order to accept your pull request, we need you to submit a CLA. You only need
to do this once to work on any of Facebook's open source projects.

Complete your CLA here: <https://code.facebook.com/cla>

## Issues
We use GitHub issues to track public bugs. Please ensure your description is
clear and has sufficient instructions to be able to reproduce the issue.

Facebook has a [bounty program](https://www.facebook.com/whitehat/) for the safe
disclosure of security bugs. In those cases, please go through the process
outlined on that page and do not file a public issue.

## License
By contributing to hydra, you agree that your contributions will be licensed
under the LICENSE file in the root directory of this source tree.