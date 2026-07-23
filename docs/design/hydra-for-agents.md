# Using Hydra applications with AI agents

Hydra applications are agent-ready CLIs by construction.

This does not mean Hydra is an agent framework, agent runtime, MCP
replacement, or LLM orchestration system. The point is simpler: agents need to
operate complex command-line applications, and Hydra already gives those
applications a standardized, inspectable, overrideable configuration interface,
with type validation when Structured Configs or schemas are used.

A Hydra app can be inspected and validated before it is run. Agents can use the
same CLI affordances as humans: application help, Hydra help, composed config
printing, focused config printing, override parsing, and Structured Config
validation.

For reference, see the existing docs for
[Hydra's command line flags](../../website/docs/advanced/hydra-command-line-flags.md),
[debugging and config printing](../../website/docs/tutorials/basic/running_your_app/5_debugging.md),
[override grammar](../../website/docs/advanced/override_grammar/basic.md),
[Structured Configs](../../website/docs/tutorials/structured_config/0_intro.md),
[multirun](../../website/docs/tutorials/basic/running_your_app/2_multirun.md),
and
[instantiating objects](../../website/docs/advanced/instantiate_objects/overview.md).

## Strategic direction

The agent use case is a forcing function for improvements that also help human
users. Agents make existing friction easier to see: surprising filesystem
writes, large composed configs, hard-to-discover config groups, and overrides
whose valid values or types are not obvious from the command line.

The strategy is to strengthen Hydra as an inspectable boundary around complex
applications:

1. Keep inspection separate from execution. Discovery, help, config printing,
   and validation should be cheap and side-effect free.
2. Make Hydra apps more self-describing. A caller should be able to discover
   config groups, options, selected defaults, sources, packages, and types
   without guessing.
3. Preserve the classic experiment-management workflow while allowing a more
   minimal application flavor for users who do not want output directories,
   config snapshots, or job logs unless they opt in.
4. Position Hydra as a better CLI/config substrate for agents, not as an agent
   framework.

## Inspect, validate, run

The recommended loop for an agent operating a Hydra application is:

1. Confirm that the command is a Hydra app and identify the Hydra version.
2. Inspect the app.
3. Inspect the composed config.
4. Use `--package` to inspect only relevant config subtrees when the full config
   is too large.
5. Propose overrides.
6. Validate the composed config with the overrides using `--cfg job --resolve`.
7. Run only after composition succeeds.

Common first-pass inspection commands:

```bash
# Confirm this is a Hydra app and discover the Hydra version.
python app.py --version

# Show application help and user-facing config group choices.
python app.py --help

# Print the composed application config without running the application.
python app.py --cfg job
```

The `--version` flag is a cheap way to discover that a command is a Hydra app
and identify the Hydra version. The core Hydra flag syntax is mostly static for
a given Hydra version, so an agent or skill can usually know it from the
version. The `--hydra-help` output can still contain local Hydra config group
choices from plugins and the config search path. That overlap is one reason a
dedicated config group introspection surface would be useful.

The `--cfg job` flag prints the application config without running the
application. The `--cfg hydra` flag prints Hydra's own config. The `--resolve`
flag resolves interpolations before printing, which is useful before an agent
treats the composed config as the plan it is about to execute.

More specialized inspection commands are useful once the agent knows what it is
looking for:

```bash
# Show the Hydra-specific help surface for an unfamiliar Hydra version.
python app.py --hydra-help

# Inspect Hydra's own composed config when debugging Hydra behavior.
python app.py --cfg hydra

# Show Hydra, plugin, search path, and defaults diagnostics for troubleshooting.
python app.py --info

# Print the resolved application config when interpolations matter.
python app.py --cfg job --resolve
```

Hydra applies command-line overrides when printing configs, so an agent can
validate a proposed change before running it:

```bash
python app.py --cfg job --resolve model=resnet trainer.max_epochs=10
```

If this command fails, the agent should revise the overrides instead of running
the application. If it succeeds and the resolved config is acceptable, the agent
can run the same overrides:

```bash
python app.py model=resnet trainer.max_epochs=10
```

## Focused inspection

Real application configs can be large. Agents should avoid spending context on
unrelated config when a smaller subtree is enough. The `--package` flag selects
the package to print with `--cfg`.

For example, inspect only the `trainer` subtree:

```bash
python app.py --cfg job --package trainer
```

Focused inspection also works with overrides and resolved configs:

```bash
python app.py --cfg job --package trainer --resolve \
  model=resnet trainer.max_epochs=10
```

This is especially useful when an agent already knows the task is about a
specific component such as `trainer`, `model`, `db`, `optimizer`, `hydra.job`,
`hydra.launcher`, or `hydra.sweeper`.

## Validation boundary

Agents make the same kinds of mistakes humans do: wrong types, invalid values,
misspelled config choices, malformed override syntax, and bad assumptions about
the final composed config.

Hydra can catch many of these mistakes at the configuration boundary. Structured
Configs and OmegaConf validation can reject invalid types and missing required
values during composition or access, before the application does work. Config
groups and the override grammar can reject unknown choices or malformed
overrides.

This does not make every application action safe. It gives agents a reliable
pre-run check: compose the exact config that would be used, resolve it when
needed, and inspect the result before executing the application.

## Recommended product improvements

Hydra already gives agents a useful inspection and validation loop. The next
step is to make that loop less surprising for humans and more explicit for
tools.

### Do not create output directories by default

Hydra's current default behavior creates a per-run output directory, even when
`hydra.job.chdir=False`. This is useful for experiment tracking, logs, and
reproducibility, but it is also one of the first things new users notice: trying
a Hydra app leaves an `outputs/` tree behind.

For a future compatibility boundary, ordinary single-run execution should avoid
creating a Hydra-managed output directory unless the application or user opts in.
Inspection commands such as `--version`, `--help`, `--hydra-help`, `--info`,
and `--cfg` should continue to be side-effect free.

One possible lever is an application mode, such as
`@hydra.main(mode=Classic | Minimal, ...)`. `Classic` would preserve today's
behavior. `Minimal` would start from fewer side effects and let applications opt
in to the features they want. This is an idea for the shape of the compatibility
boundary, not a proposed API.

Because this is a breaking change, the migration path should be explicit and
easy:

1. Keep the existing behavior available as the classic mode.
2. Introduce the minimal behavior behind a major version, `version_base`, app
   mode, or another clear compatibility switch.
3. In minimal mode, make filesystem-producing features opt in: per-run
   directory creation, `.hydra` config snapshots, override capture, and job log
   files.
4. Let application authors choose the classic behavior in config or code, so
   existing users do not need to remember an extra command-line override.
5. Document how `hydra.runtime.output_dir` behaves when no managed output
   directory is created. A path that implies a directory was created would be
   misleading, so this probably needs an explicit "no managed output directory"
   state.

Multirun needs separate treatment. Sweeps are more likely to need managed output
directories, but the behavior should still be visible and controllable because a
small override can expand into many filesystem writes.

### Expose config groups and options directly

Agents often need to discover what can be selected before composing a full
config. Hydra's app help already exposes some config group information, but a
more direct introspection surface would be easier for both humans and tools.

Useful static catalog capabilities include:

- List all visible config groups.
- List options for one config group, including nested groups.
- Show the source path or provider for each option when available.
- Offer a machine-readable output mode, such as YAML or JSON, for tools that do
  not want to scrape help text.

Useful contextual preview capabilities include:

- Show the selected default for a group without printing the entire composed
  config.
- Inspect one group option or sub-config in isolation, without requiring a full
  application config to compose successfully when the option is independent
  enough to preview safely.

The goal is to let an agent ask narrow questions such as "what launchers are
available?", "what options exist under `model/`?", or "what does
`db=mysql` contain?" without spending context on unrelated config. The
contextual cases may still depend on defaults lists, package overrides,
interpolations, and config search path state, so the inspection surface should
make those limits visible instead of pretending every sub-config is independent.

Minimal examples of the intended capabilities:

```text
List config groups:
  db
  hydra/launcher
  hydra/sweeper
  model

List options in one group:
  db=mysql
  db=postgresql

Preview one option:
  db=mysql
    driver: mysql
    host: localhost
    port: 3306

Report that a preview is contextual:
  experiment=imagenet
    cannot preview without composing defaults:
    depends on model, optimizer, and dataset choices
```

### Surface type information

Structured Configs already carry type information that can help agents avoid
invalid overrides. Hydra could expose that information as part of inspection.

For Structured Config dataclasses, useful metadata includes field names, types,
defaults, required values, optional fields, containers, enum choices, and the
dataclass backing a node. For plain YAML configs, Hydra can only report inferred
structure and scalar types, but even that is useful.

This would make it easier for agents to propose valid overrides before running
an application. For example, an agent could learn that `trainer.max_epochs` is
an `int`, `optimizer.lr` is a `float`, and `db.password` is required, then
validate the exact override set with `--cfg job --resolve`.

Minimal example of the intended type inspection capability:

```text
trainer:
  max_epochs: int = 10
  accelerator: str = "cpu"
  precision: enum[16, 32, 64] = 32
db:
  host: str = "localhost"
  password: str = ???
```

## Marketing ideas

The marketing angle should be practical and restrained: Hydra applications are
easier for agents to operate because they are easier for anyone to inspect,
configure, validate, and run.

Possible positioning:

- Agent-ready CLIs, without adopting an agent framework.
- Inspect. Validate. Run.
- Make complex Python applications legible to humans and agents.
- A standard configuration interface for tools, scripts, training jobs, and
  agents.
- Before an agent runs your app, Hydra lets it inspect the CLI, compose the
  config, validate overrides, and review the exact plan.
- Hydra is not the agent. Hydra is the control surface the agent can understand.

Possible demo story:

1. Start with an unknown command.
2. Use `--version` to identify it as a Hydra app.
3. Use `--help` and `--cfg job` to inspect the app and composed config.
4. Use focused inspection to look at only `trainer` or `model`.
5. Propose a small override.
6. Validate the exact resolved config.
7. Run only after validation succeeds.

Things to avoid in messaging:

- Do not imply that Hydra makes arbitrary application actions safe.
- Do not imply that Hydra replaces MCP, agent runtimes, orchestration systems,
  or application-specific authorization.
- Do not over-index on agents at the expense of the human CLI story. The same
  affordances should feel valuable even when no agent is involved.

## Generic Hydra app skill

The following is a copy-pasteable skill for agents that need to operate an
unknown Hydra application.

```text
When operating a Hydra app:

1. If the command is not known to be a Hydra app, confirm it and discover the
   Hydra version:
   python app.py --version

2. Inspect the application CLI:
   python app.py --help

   Use --hydra-help only when the Hydra version is unfamiliar or the
   Hydra-specific CLI surface needs to be checked. Use --info for
   troubleshooting plugins, config search path, defaults, or runtime details.

3. Inspect the composed application config without running the app:
   python app.py --cfg job

4. If the config is large, inspect only the relevant subtree:
   python app.py --cfg job --package <package>

5. Propose overrides using Hydra override syntax. Prefer the smallest override
   set needed for the task.

6. Validate the exact proposed config before execution:
   python app.py --cfg job --resolve <overrides>

7. If validation fails, revise the overrides and validate again. Do not run the
   app until composition succeeds and the resolved config matches the intent.

8. Run with the same overrides only after validation succeeds:
   python app.py <overrides>
```

## Security notes

Treat agent-generated overrides as untrusted input. Validate the composed config
before execution, and do not assume that a syntactically valid override is
semantically safe for the application.

Be especially careful with `--multirun` and sweeps. A small-looking override can
expand into many jobs, consume significant resources, or write many outputs.

If the application uses `hydra.utils.instantiate()`, do not blindly accept
arbitrary `_target_` values from untrusted sources. Object instantiation can
execute code, so use trusted configs and application-level allowlists or review
where appropriate.

## Non-goals

Hydra is not becoming an agent framework, agent runtime, MCP replacement, or
vendor-specific LLM integration.

Hydra's role here is to make command-line applications easier to inspect,
configure, validate, and run. These are the same affordances humans need for
complex CLIs, and they are also useful to AI agents operating those CLIs.
