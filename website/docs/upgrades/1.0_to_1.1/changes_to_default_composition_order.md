---
id: default_composition_order
title: Changes to default composition order
---
Default composition order is changing in Hydra 1.1.

For this example, let's assume the following two configs:
<div className="row">
<div className="col col--6">

```yaml title="config.yaml"
defaults:
  - foo: bar

foo:
  x: 10
```

</div>

<div className="col  col--6">

```yaml title="foo/bar.yaml"
# @package _group_
x: 20



```
</div>
</div>


<div className="row">
<div className="col">

In **Hydra 1.0**, configs from the Defaults List are overriding *config.yaml*, resulting in the following output:
</div>
<div className="col  col--4">

```yaml {2}
foo:
  x: 20
```
</div>
</div>



<div className="row">
<div className="col">

As of **Hydra 1.1**, *config.yaml* is overriding configs from the Defaults List, resulting in the following output:
</div>
<div className="col  col--4">

```yaml {2}
foo:
  x: 10
```
</div>
</div>


### Migration
For the majority of applications, this will not cause issues. If your application requires the previous behavior, 
you can achieve it by adding `_self_` as the first item in your Defaults List:


<div className="row">
<div className="col col--6">

```yaml title="config.yaml" {2}
defaults:
  - _self_
  - foo: bar

foo:
  x: 10
```
</div>

<div className="col  col--6">

```yaml title="Output config"
foo:
  x: 20




```
</div>
</div>

The Defaults List is described [here](/advanced/defaults_list.md).
