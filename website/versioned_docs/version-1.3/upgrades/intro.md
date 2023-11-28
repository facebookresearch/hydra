---
id: intro
title: Introduction
sidebar_label: Introduction
---

Upgrading to a new Hydra version is usually an easy process.
Also since Hydra version 1.2, backwards compatibility is improved
by giving the user more control over appropriate defaults
through the use of the [version_base parameter](version_base.md).

:::info NOTE
Hydra versioning has only major versions and patch versions. A bump of the first two version digits is considered a major release.
A major release may have multiple followup patch releases that will fix bugs without introducing new functionality.
:::


## Major version upgrades
Hydra will typically provide helpful warnings about required changes, sometimes pointing to an upgrade page that provides more details about the required changes.

For a smooth upgrade experience, please follow these simple rules:
- **Upgrade to the latest patch version first**.
  e.g: If you are upgrading from 1.0 to 1.1, be sure to upgrade to the latest 1.0 version first (1.0.6).
- **Address ALL runtime warnings issued by Hydra.**  
  A warning in one version is likely to become a far less friendly error in the next major version.
- **Do not skip major versions**.  
  e.g: If you are upgrading from Hydra 1.0 to Hydra 1.2 - Do it by
  - Upgrading from 1.0 to 1.1, addressing all the warnings.
  - Upgrading from 1.1 to 1.2, addressing all the warnings.

## Patch version upgrades
Patch releases normally contains only bug fixes and are thus safe and easy to upgrade (e.g. **1.0.3** to **1.0.6**).  
In rare cases, patch releases will introduce new warnings. Be sure to address them before upgrading to the next major version.

## Dev release upgrades
Development releases are subject to breaking changes without notice. Please be aware that upgrading to a new development release
is more likely to introduce some breakage. No attempt will be made to make upgrading between development releases easy.
