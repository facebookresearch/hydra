---
id: documentation
title: Documentation
sidebar_label: Documentation
---

import GithubLink from "@site/src/components/GithubLink"

## NEWS Entries
The <GithubLink to="NEWS.md">NEWS.md</GithubLink> file is managed using
`towncrier`. Contributor instructions for news fragments are maintained in
<GithubLink to="CONTRIBUTING.md">CONTRIBUTING.md</GithubLink>.

## Website setup

The website is built using [Docusaurus 2](https://v2.docusaurus.io/).  
Run the following commands from the `website` directory.

### Install

```
$ corepack pnpm install
```

pnpm is configured to avoid resolving npm package versions published in the
last 10 days during dependency updates.

### Local Development

```
$ corepack pnpm start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

For more details, refer <GithubLink to="website/README.md">here</GithubLink>.
