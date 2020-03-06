# Website

This website is built using Docusaurus 2, a modern static website generator.

### Installation

```
$ yarn
```

### Local Development

```
$ yarn start
```

This command starts a local development server and open up a browser window. Most changes are reflected live without having to restart the server.

### Build

```
$ yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

Done automatically once a website change is landed to master.


### Adding pages

New pages, e.g., for a new plugin, should be added to `docs/`. They can be accessed on a local server via `http://localhost:3000/docs/next/page_name`.
