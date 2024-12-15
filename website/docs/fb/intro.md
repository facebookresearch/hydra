---
id: intro
title: Hydra at Facebook
---

### Intro
Facebook has multiple different environments, such as the **Internal FB Cluster**, the **FAIR Cluster** etc.

The FB specific docs are describing the differences.

### Release strategy
Hydra's source of truth is the [GitHub repo](https://github.com/facebookresearch/hydra).

Hydra is developed using release branches. Once a new major is released, it is maintained in patch only mode.
Primary development is happening on the `master` branch.

When a new major version of Hydra is released, a new release branch is created in Hydra repo. A corresponding Hydra version will be created inside `github/facebookresearch/hydra_VERSION` to track
the release branch.

Hydra is trying hard to remain backward compatible between two subsequent versions and in most cases the upgrade will be smooth.
There could be some new deprecations warnings that should be fixed before the next major version.

### Maintaining this documentation
This documentation lives in in the Hydra repo which is publicly accessible. The pages will only normally render on the internal
copy of the docs, but keep in mind that everyone can read those docs in the repo if they want to.

1. Do not put anything sensitive here, no root passwords or launch codes.
2. If you are in need to have sensitive Hydra related documentation please reach out to the maintainers of Hydra for help.
