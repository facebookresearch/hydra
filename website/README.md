# Website

This website is built using Docusaurus 3, a modern static website generator.

### Installation

The website requires Node.js 20 or newer.

```
$ corepack pnpm install
```

pnpm is configured to avoid resolving npm package versions published in the
last 10 days during dependency updates.

### Local Development

```
$ corepack pnpm start
```

This command starts a local development server and open up a browser window. Most changes are reflected live without having to restart the server.

### Build

```
$ corepack pnpm build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

Done automatically once a website change is landed to main.


### Adding pages

New pages, e.g., for a new plugin, should be added to `docs/`. They can be accessed on a local server via `http://localhost:3000/docs/page_name`.
