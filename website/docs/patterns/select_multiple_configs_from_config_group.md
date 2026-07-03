---
id: select_multiple_configs_from_config_group
title: Selecting multiple configs from a Config Group
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink text="Example application" to="examples/patterns/multi-select"/>

### Problem
In some scenarios, one may need to select multiple configs from the same Config Group.

### Solution
Use a list of config names as the value of the config group in the Defaults List or in the command line.

### Example

In this example, we configure a server. The server can host multiple websites at the same time.

<div className="row">
<div className="col col--4">

```text title="Config directory"
├── config.yaml
└── server
    ├── apache.yaml
    └── site
        ├── amazon.yaml
        ├── fb.yaml
        └── google.yaml
```
</div>
<div className="col col--4">

```yaml title="config.yaml"
defaults:
  - server/apache





```
</div>

<div className="col col--4">

```yaml title="server/apache.yaml" {3,4}
defaults:
  - site:
    - fb
    - google

host: localhost
port: 443
```
</div>

<div className="col col--4">

```yaml title="server/site/amazon.yaml"
amazon:
  domain: amazon.com
```
</div>
<div className="col col--4">

```yaml title="server/site/fb.yaml"
fb:
  domain: facebook.com
```
</div>
<div className="col col--4">

```yaml title="server/site/google.yaml"
google:
  domain: google.com
```
</div>
</div>

Output:
```yaml title="$ python my_app.py" {3,5}
server:
  site:
    fb:
      domain: facebook.com
    google:
      domain: google.com
  host: localhost
  port: 443
```

Override the selected sites from the command line by passing a list. e.g:
```yaml title="$ python my_app.py 'server/site=[google,amazon]'" {3,5}
server:
  site:
    google:
      domain: google.com
    amazon:
      domain: amazon.com
  host: localhost
  port: 443
```


### Implementation considerations

The following two forms compose the same output:

<div className="row">
<div className="col col--6">

```yaml title="server/apache.yaml" {3,4}
defaults:
  - site:
    - fb
    - google
```
</div>
<div className="col col--6">

```yaml title="Composes like" {2,3}
defaults:
  - site/fb
  - site/google

```
</div>
</div>

Use the nested list form when you want to override the group later with
`'server/site=[...]'`.

To delete one of these non-overridable entries from the command line, use the
exact config path, for example `~server/site/fb`.

All default package for all the configs in `server/site` is `server.site`.
This example uses an explicit nesting level inside each of the website configs to prevent them stepping over one another:
```yaml title="server/site/amazon.yaml" {1}
amazon:
  ...
```
