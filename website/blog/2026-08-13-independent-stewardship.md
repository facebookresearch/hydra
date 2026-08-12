---
title: "Hydra's next chapter: independent stewardship"
author: Omry Yadan
author_title: Creator of Hydra
author_url: https://github.com/omry
author_image_url: https://github.com/omry.png
tags: [Hydra]
image: /img/Hydra-Readme-logo2.svg
---

In 2019, while working at Facebook, I started Hydra to make it easier to build
and configure complex applications. We
[released it as open source](https://engineering.fb.com/2019/10/03/open-source/hydra/)
under the MIT license, and it grew far beyond its original setting.

Hydra became what it is because of its users, contributors, and maintainers.
People adopted it in research labs, startups, large companies, and personal
projects. They reported problems, proposed ideas, wrote plugins, improved the
documentation, and helped shape the project over many years.

Today, I am happy to share that Hydra has moved from Meta stewardship to an
independent home under the
[Hydra Ecosystem](https://github.com/hydra-ecosystem) GitHub organization.

<!--truncate-->

## What the agreement covers

Meta and I signed an agreement transferring to me the Hydra-related rights and
project assets specified in the agreement. These include:

- the Hydra GitHub repository;
- the `hydra.cc` domain;
- the specified Hydra packages published on PyPI;
- Meta's rights in the Hydra name and logo; and
- the specified project accounts used to operate Hydra.

The existing GitHub repository was transferred rather than replaced with a
fork. This preserved the repository's history, issues, pull requests, releases,
and community context.

Alongside Hydra's move, I will move OmegaConf, currently hosted at
[omry/omegaconf](https://github.com/omry/omegaconf), into the Hydra Ecosystem
organization so that Hydra and its configuration foundation have a shared
long-term home.

## What is not changing

Hydra remains under the MIT license. The transfer does not include copyright in
Meta's historical code contributions. That code remains part of Hydra under the
MIT license, with applicable license and copyright notices preserved. The
transfer changes stewardship and project control without changing the ownership
history of existing contributions.

No immediate action is required from Hydra users. Existing packages continue to
work, and existing GitHub links redirect to the new location. You can update
your local Git remotes to the new organization at your convenience.

## What independent stewardship means

The move gives Hydra a clear home outside Meta for future project decisions,
including governance, releases, infrastructure, security, and community
processes. It also keeps the door open to a future foundation or another
durable organizational home if that becomes the right choice.

When I left Facebook at the end of 2021, a small team continued to maintain
Hydra. Over time, as its members moved on, that team dispersed and development
slowed.

Adoption, however, continued to grow. GitHub now reports
[more than 40,000 public repositories](https://github.com/hydra-ecosystem/hydra/network/dependents)
as direct dependents of Hydra. The new
[Hydra Landscape](https://hydra.cc/docs/landscape/) is a curated directory of
more than 100 applications, frameworks, tools, plugins, and learning resources.
It offers a window into that much larger ecosystem, not an exhaustive survey of
it.

In recent months, I have returned to actively maintaining Hydra and OmegaConf.
The number of open issues and pull requests has already fallen substantially in
both projects. Work on Hydra 1.4 is underway, and it is already available as a
development release. There is still much to do, but maintenance is active
again.

Practical transition work remains. I am finalizing release
publishing and moving the remaining Meta-dependent infrastructure,
contribution, and community processes to project-controlled systems. Security
reports can now be
[submitted privately through GitHub](https://github.com/hydra-ecosystem/hydra/security/advisories/new).

The contribution process deserves particular care. Hydra historically used
Meta's contributor license agreement. Going forward, Hydra will use a
project-controlled CLA. I will publish the CLA together with details of the new
process once both are finalized. Pull requests already open during the
transition will be handled individually.

## What comes next

Completing Hydra 1.4 is the next major priority. More broadly, I intend to keep
the project actively maintained and responsive to the community.

If you are feeling adventurous, try the
[Hydra 1.4 development release](https://hydra.cc/docs/intro/#installation)
and report any problems you find.

This transition is not a product relaunch or a change in Hydra's purpose. It is
a change in stewardship that gives the project a cleaner and more sustainable
foundation for its next chapter.

I am grateful to Jon Janzen, Jonathan Torres, and the people at Meta who helped
work through an unusual transfer. I am also deeply grateful to Hydra's
maintainers, contributors, and users for building and sustaining the project.

I look forward to continuing that work and giving Hydra and OmegaConf a stable,
active home for the years ahead.
