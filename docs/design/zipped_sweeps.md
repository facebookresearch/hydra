# Zipped sweep dimensions

Status: proposal.

Related issues:
[facebookresearch/hydra#1258](https://github.com/facebookresearch/hydra/issues/1258)
and
[facebookresearch/hydra#2759](https://github.com/facebookresearch/hydra/issues/2759).

## Summary

Hydra should support a correlated, or zipped, sweep dimension:

```text
model_optimizer=zip(
  model=choice(resnet,vit),
  optimizer=choice(sgd,adamw)
)
```

`model_optimizer` is the name of the sweep dimension. The expression describes
two choices:

```text
model=resnet optimizer=sgd
model=vit optimizer=adamw
```

It does not describe the four-element Cartesian product of `model` and
`optimizer`.

Hydra can implement this without changing the Sweeper or Launcher interfaces.
Each zipped row is registered as an ephemeral ConfigStore option, and the
`zip(...)` expression is lowered to an ordinary categorical config-group
sweep in a dedicated internal zip namespace. Existing sweepers can then treat
the entire row as one sweep dimension.

Other sweep dimensions remain independent. The Basic Sweeper naturally takes
their Cartesian product:

```text
model_optimizer=zip(
  model=choice(resnet,vit),
  optimizer=choice(sgd,adamw)
) seed=1,2,3
```

This produces six jobs: the two `(model, optimizer)` rows crossed with the
three seeds.

## Motivation

Hydra currently treats each sweep override as an independent dimension. For
example:

```text
model=resnet,vit optimizer=sgd,adamw
```

describes four jobs. There is no built-in way to state that `resnet` should be
paired with `sgd` and `vit` should be paired with `adamw`.

Users can encode such relationships in experiment config groups, but that
requires creating files or registering application-specific configs. The
relationship is often local to one invocation and should be expressible at the
command line.

The desired abstraction is one correlated sweep dimension that happens to set
multiple Hydra overrides. It is not a new sweeping algorithm.

## Goals

- Express correlated choices across multiple override keys.
- Give every correlated dimension a stable, user-selected name.
- Support both config-group selections and ordinary config values.
- Compose zipped dimensions with ordinary sweep dimensions.
- Allow the same expression in the command line and in a configured multirun.
- Allow users to inspect the generated choices and their contents without
  running the sweep.
- Keep the Sweeper and Launcher interfaces unchanged.
- Work with the Basic Sweeper and with plugins that support ordinary
  categorical dimensions.
- Avoid creating temporary config files.
- Preserve Hydra's normal composition and override precedence.
- Avoid anonymous generated identifiers on user-facing surfaces.

## Non-goals

- Add a general constraint language between arbitrary sweep dimensions.
- Define correlations over continuous intervals.
- Change how a sweeper explores independent dimensions.
- Require sweepers or launchers to understand a new `ZipSweep` type.
- Persist generated config options beyond the Hydra invocation that owns them.

## Proposed syntax

`zip(...)` is a sweep value assigned to a user-selected dimension name. Its
named arguments are Hydra override keys:

```text
model_optimizer_batch_size=zip(
  model=choice(resnet,vit),
  optimizer=choice(sgd,adamw),
  training.batch_size=choice(32,64)
)
```

The left-hand side names the correlated dimension. It is not a config value
that will be added to the composed application config.

The dimension name must not collide with an application config key or config
group.

Members can use explicit lists:

```text
letter_number=zip(
  letter=[a,b,c,d],
  number=[1,2,3,4]
)
```

This describes four choices:

```text
letter=a number=1
letter=b number=2
letter=c number=3
letter=d number=4
```

Within `zip(...)`, a top-level list is an ordered source of row values. To use
lists themselves as the values assigned by each row, wrap them in an explicit
choice, for example `items=choice([a,b],[c,d])`.

Members can also use finite discrete sweeps. All members must have the same
number of elements. Row `i` contains element `i` from every member.

Explicit `choice(...)` syntax avoids ambiguity between commas that separate
members of `zip(...)` and commas that form a simple choice sweep.

The braces of a dict literal are unnecessary:

```text
model_optimizer=zip(
  {model: choice(resnet,vit), optimizer: choice(sgd,adamw)}
)
```

The mapping is already expressed by the named arguments. More importantly, a
dedicated grammar can treat each argument name as a Hydra override key instead
of limiting it to an ordinary function keyword identifier.

Like `range()` and `choice()`, `zip(...)` appears on the right-hand side of an
ordinary named sweep override. Unlike those functions, it produces one sweep
dimension whose choices apply several overrides. Its member syntax therefore
needs specialized parsing even though the surrounding `name=zip(...)` form
already fits the override grammar.

The exact member grammar is intentionally left for the grammar design. It may
require extending the current function grammar to support dotted config keys,
nested config groups, and package-qualified group keys.

The initial form should require:

- a valid, non-empty dimension name on the left-hand side
- no collision between that name and an application key or config group
- at least two named members
- unique override keys
- finite, non-empty explicit lists or discrete sweeps
- equal cardinality across all members
- no independently shuffled member sweep

Continuous `interval(...)` values cannot be zipped because they do not provide
ordered, finite elements.

Shuffling an individual member would destroy the declared row relationship and
is illegal. Shuffling the completed zipped dimension is legal and operates on
whole rows:

```text
model_optimizer=shuffle(
  zip(
    model=choice(resnet,vit),
    optimizer=choice(sgd,adamw)
  )
)
```

### Configured multiruns

Naming the dimension also gives `zip(...)` a natural representation in
`hydra.sweeper.params`, where the mapping key is already the sweep dimension
name:

```yaml
hydra:
  sweeper:
    params:
      model_optimizer: >-
        zip(model=choice(resnet,vit),optimizer=choice(sgd,adamw))
      seed: 1,2,3
```

This is equivalent to:

```text
model_optimizer=zip(
  model=choice(resnet,vit),
  optimizer=choice(sgd,adamw)
) seed=1,2,3
```

The same lowering path should handle the command-line and config forms. A
sweeper configuration that uses the standard parameter mapping receives the
lowered categorical dimension rather than needing to understand `zip(...)`.
The internal config-group namespace and options are not exposed in the
configured multirun.

## Composition with other dimensions

Each named `zip(...)` expression is one dimension. Every ordinary sweep and
every additional named `zip(...)` expression is another independent dimension.

For example:

```text
model_optimizer=zip(
  model=choice(resnet,vit),
  optimizer=choice(sgd,adamw)
)
dataset_augmentation=zip(
  dataset=choice(imagenet,cifar10),
  augmentation=choice(strong,light)
)
seed=1,2
```

The Basic Sweeper sees three dimensions with cardinalities 2, 2, and 2, and
therefore launches eight jobs.

Optimizing sweepers need not enumerate the full Cartesian product. They see the
two generated groups as independent categorical parameters and can explore the
combined search space using their normal algorithm.

## ConfigStore lowering

Hydra lowers a command-line zipped dimension before the initial multirun
composition. A zipped dimension from `hydra.sweeper.params` is lowered after
the controller config is composed and before the sweeper consumes the
parameter mapping. For this input:

```text
model_optimizer=zip(
  model=choice(resnet,vit),
  optimizer=choice(sgd,adamw)
)
```

Hydra creates a config group for `model_optimizer` in a dedicated internal zip
sweep namespace. The group has string options named `choice1`, `choice2`, and
so on. Conceptually, the options are:

```yaml
# choice1, package="_global_"
defaults:
  - override /model: resnet
  - override /optimizer: sgd
```

```yaml
# choice2, package="_global_"
defaults:
  - override /model: vit
  - override /optimizer: adamw
```

The sweeper receives an ordinary categorical dimension backed by this internal
group:

```text
<zip sweep namespace>/model_optimizer=choice(choice1,choice2)
```

This is an internal representation, not user-facing syntax. The Basic Sweeper
can expand it through its existing categorical sweep support, and optimizing
sweepers can treat it as one categorical parameter. For a concrete job,
normal Defaults List composition selects the generated option and applies the
corresponding `model` and `optimizer` choices.

Rows can also contain ordinary config values. For example, the first row of:

```text
model_batch_size=zip(
  model=choice(resnet,vit),
  training.batch_size=choice(32,64)
)
```

is represented conceptually as:

```yaml
defaults:
  - override /model: resnet

training:
  batch_size: 32
```

The generated option uses the `_global_` package so its contents compose at the
same locations targeted by the original keys.

Config-group keys, including nested groups and package-qualified groups, must
be resolved using the same config repository and rules as ordinary overrides.
The generated Defaults List entries must retain those group and package
semantics.

## Why ConfigStore

ConfigStore is already a Hydra config source and its nodes can contain Defaults
Lists. It therefore provides the required behavior without generating files or
teaching the composition engine about a new kind of config source.

The generated configs are registered through ConfigStore and consumed through
Hydra's ConfigRepository abstraction, like other config groups. Sweepers and
launchers do not need to know how the group is stored.

Using ConfigStore also preserves the separation of responsibilities:

- Hydra parses and lowers the correlated dimension.
- ConfigStore holds the ephemeral rows.
- Defaults List composition applies each row.
- Sweepers operate on ordinary categorical dimensions.
- Launchers receive ordinary concrete jobs.

The generated options should use a provider name such as `hydra.zip` so
diagnostics can identify their origin.

## Namespace and scope

Generated groups belong to one multirun and live in a dedicated internal zip
sweep namespace. The exact namespace is an implementation detail.

Hydra rejects a public dimension name that collides with an application config
key or config group. Internal group registration, ownership, and cleanup remain
behind the ConfigRepository abstraction and must not affect application-defined
configs or later Hydra invocations.

## Precedence

Lowering must preserve Hydra's existing precedence rules.

Values selected by a generated row behave like values supplied by a config.
An explicit command-line override remains higher priority. In particular, a
normal command-line config-group override must win over a Defaults List
override inside the generated row.

The implementation should diagnose cases where a zipped member is shadowed by
another sweep dimension, because allowing two dimensions to control the same
key would make the search space misleading. Whether a fixed command-line
override may intentionally shadow one member of a zipped row remains an open
UX decision, but its precedence must not depend on the generated group name.

## User-facing metadata

The user-selected dimension name is the public identity of the correlated
sweep. The dedicated backing group path is internal. Generated option names
such as `choice1` are ordinary categorical values and may appear in sweep
inspection and optimizer reporting:

```text
model_optimizer=choice1
```

Each concrete job retains the expanded task overrides:

```text
model=resnet optimizer=sgd seed=1
```

These concrete overrides are stored in `hydra.overrides.task`,
`.hydra/overrides.yaml`, and the corresponding `JobReturn`. They must be
sufficient to rerun the job without the ephemeral generated group.

The original named `zip(...)` expression should remain available in
multirun-level provenance. Sweeper result reporting can refer to the public
dimension name while Hydra presents the selected row's concrete expansion.

## Inspection without execution

Hydra should expose the generated choices and their concrete contents without
launching jobs. Conceptually:

```text
model_optimizer:
  choice1:
    model=resnet
    optimizer=sgd
  choice2:
    model=vit
    optimizer=adamw
```

For the Basic Sweeper, this dry mode can also show the fully expanded Cartesian
job plan after combining zipped and ordinary dimensions. For optimizing
sweepers, which may choose trials adaptively, it can show the search-space
dimension and the contents of each zipped choice without claiming to know the
future trial sequence.

The Basic Sweeper should expose this as `hydra.sweeper.dry_run=true`. The common
inspection API for adaptive sweepers is part of the implementation design. The
capability should be owned by Hydra rather than implemented only by the Basic
Sweeper.

## Sweeper compatibility

This design deliberately avoids adding a `ZipSweep` value to the Sweeper API.
A compatible sweeper only needs to support an ordinary categorical parameter
whose values are generated ConfigStore options.

The Basic Sweeper should work through its existing Cartesian-product logic.
Optimizing sweepers can treat each zipped dimension as one categorical
parameter.

Hydra 1.4 should normalize the bundled sweepers, including Ax, so all of them
support this ordinary categorical representation from both command-line and
configured multiruns.

A sweeper that cannot handle an ordinary categorical config-group sweep is not
made compatible by this design.

Launchers require no changes because lowering is complete before concrete jobs
reach them.

## Parsing and lowering sequence

A multirun follows this sequence:

1. Recognize named `dimension=zip(...)` sweep values in command-line overrides
   and standard sweeper parameter mappings.
2. Parse the dimension name, each member key, and each discrete sweep.
3. Reject a dimension-name collision or independently shuffled member.
4. Resolve member keys as config groups or config value paths.
5. Validate cardinality, canonical key uniqueness, and supported sweep types.
6. Register one `_global_` config option per row as `choice1`, `choice2`, and so
   on in the dedicated zip sweep namespace.
7. Present the generated group to the sweeper as one ordinary categorical
   dimension.
8. Let the selected sweeper expand or optimize the resulting dimensions.
9. Compose each concrete job through the normal config loader.
10. Record the expanded constituent overrides in the job so it can be rerun
    without the generated group.

Generated options must be available through the ConfigRepository before any
composition that selects them.

## Validation and errors

Errors should refer to the original expression and member key, not only to a
generated ConfigStore path.

Hydra should reject:

- a missing or invalid left-hand dimension name
- a dimension name that collides with an application config key or group
- duplicate zipped dimension names
- positional `zip(...)` arguments
- fewer than two members
- duplicate member keys
- empty member sweeps
- unequal member cardinalities
- continuous or otherwise non-enumerable sweeps
- a shuffled member sweep
- nested `zip(...)` expressions
- keys that ordinary Hydra override resolution would reject
- members that sweep Hydra's own configuration

Errors discovered while composing a generated row should identify the original
row and the constituent overrides.

## Open questions

### Exact grammar

The outer `name=zip(...)` shape is selected. The exact grammar for member keys,
package-qualified groups, nested groups, override operators, and row-level
transformations remains TBD.

### Supported discrete sweep forms

Explicit lists and `choice(...)` are sufficient for the first implementation.
`range(...)` is also finite and naturally zip-compatible. `glob(...)` can be
supported after the member key has been resolved as a config group. The initial
implementation should choose the smallest set that can share one validation
and enumeration path.

### Override operators inside `zip(...)`

The first version can require members to target existing config groups and
config values. Supporting append or force-add members would require the
dedicated grammar to accept `+` or `++` on member keys and the generated row to
preserve those semantics.

### Inspection interface

The Basic Sweeper should use `hydra.sweeper.dry_run=true` to inspect its
Cartesian plan. A common programmatic API for inspecting generated zipped
choices and adaptive sweeper search spaces remains TBD.

## Test strategy

The implementation should cover:

- parser acceptance and diagnostics
- explicit-list members and list-valued choices
- stable dimension naming and collision handling
- equal and unequal member cardinalities
- config values
- config groups, nested groups, and package-qualified groups
- equivalent command-line and `hydra.sweeper.params` forms
- zipped dimensions crossed with ordinary choice and range dimensions
- multiple independent zipped dimensions
- rejection of shuffled members and row-level shuffling of the completed zip
- command-line precedence
- Basic Sweeper job generation and ordering
- dry inspection of generated choices and Basic Sweeper Cartesian plans
- all bundled sweeper parameter conversions, including Ax
- launchers receiving only concrete jobs
- concrete, rerunnable job override metadata and override directory names
- generated-group scoping across success, failure, and repeated Compose API use
- isolation from application config groups and keys
