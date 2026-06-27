# Contributing to hydra
We want to make contributing to this project as easy and transparent as
possible.

Please see the [developer guide](https://hydra.cc/docs/development/overview/) on the website.
Maintainers can find the release process in the [release guide](website/docs/development/release.md).

## Development Environment

Use a project-local virtual environment at `.venv` for Hydra development:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
pip install -e .
```

The core Hydra framework supports multiple Python versions. Use additional
environments when you need to reproduce or validate behavior on a specific
supported Python version, but keep the default local checkout environment in
`.venv`.

## Pull Requests
We welcome your pull requests.

1. Fork the repo and create your feature branch from `main`.
2. If you've added code add suitable tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite and lint pass.
5. If you haven't already, complete the Contributor License Agreement ("CLA").

For non-trivial features, API changes, or user-visible behavior changes, please
open an issue or design discussion and wait for maintainer feedback before
starting substantial implementation work. Pull requests in these areas should
link to the issue or discussion where the direction was agreed. Pull requests
without prior design alignment may be redirected to discussion before
implementation review.

## News fragments

All non-trivial user-visible changes should include a news fragment.

Use the issue or pull request number as the filename, with one of these
extensions:

- `api_change`: API changes, renames, deprecations, and removals
- `feature`: new features
- `bugfix`: bug fixes
- `docs`: documentation additions or updates
- `config`: configuration structure changes
- `maintenance`: maintainability improvements

For Hydra core changes, place the fragment in `news/`, for example
`news/1234.bugfix`. For plugin changes, place it in the relevant plugin's
`news/` directory, for example
`plugins/hydra_optuna_sweeper/news/1234.feature`.

Pull requests can span multiple categories by creating multiple fragments. For
example, if a pull request adds a feature and deprecates an old feature at the
same time, create both `news/1234.feature` and `news/1234.api_change`.
Likewise, if a pull request touches multiple issues or pull requests, you may
create one fragment for each number with the same contents; the release tooling
deduplicates them when rendering release notes.

Keep the fragment concise and user-facing. Prefer sentence case, under 80
characters, and imperative tone. A fragment should complete the sentence "This
change will ...". You do not need to mention issue or pull request numbers in
the fragment text; the release tooling adds references when rendering release
notes.

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
