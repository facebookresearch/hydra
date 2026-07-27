# Persistent tab completion service

Status: design direction.

Target release: after Hydra 1.4.0.

Related issue:
[facebookresearch/hydra#934](https://github.com/facebookresearch/hydra/issues/934).

## Purpose

This note records the direction for accelerating Hydra tab completion. It is
intended to be a base for a later detailed design, not a protocol or
implementation specification.

The central idea is a shared persistent service named
`hydra-completion-accelerator`. Users install it once, and Hydra applications
register with it when tab completion is activated for them. Each application
starts normally, performs its imports and Structured Config registrations, and
enters the function wrapped by `hydra.main`. In completion-service mode, Hydra
does not run the user's task. The accelerator keeps initialized applications
available and routes subsequent completion requests to the correct one.

## Problem

Hydra currently starts the application for every completion request. Each
press of Tab repeats Python startup, application imports, plugin discovery,
Structured Config registration, search-path construction, and config
composition.

For small applications this may be acceptable. For applications that import
large frameworks or register many configs, completion can become too slow to
be useful.

Caching a list of candidates is not a general solution. Earlier overrides can
change the Defaults List, available config groups, and valid choices. Source
files, config files, plugins, custom config sources, and resolvers may also
change. The reusable unit is the initialized application environment, not one
particular composed config.

## Direction

A user deploys one `hydra-completion-accelerator` and can use it with multiple
Hydra applications. Each application registration records how and where to
start that application. The accelerator remains available across shell
completion requests and routes each request to the corresponding application.

The service starts each application through its normal script, module, or
installed entry point. Normal imports and top-level registrations run. When a
program enters wrapped `hydra.main`, Hydra detects completion-service mode and
takes control without calling the task function.

The initialized application worker then serves completion requests. It retains
expensive startup state such as imported modules, Structured Config
registrations, plugins, resolvers, and the application's config search path.
Each request still gets isolated request state so overrides or mutable Hydra
state from one query cannot affect another.

Fresh request state does not necessarily require full recomposition. The
service can retain a small bounded cache of recent base compositions for each
application, for example the last ten. Each entry contains the config composed
with a particular sequence of config-group selections, before applying
ordinary command-line value overrides. A request can reuse the matching base
config and apply any remaining overrides in isolated request state.

Changes to config-group selections, config sources, or other
composition-affecting inputs require a different entry or invalidate existing
entries. The later design should define the exact cache key, capacity, reuse,
invalidation rules, and service-wide resource limits.

The broad architecture has three roles:

- a shell client that requests candidates
- `hydra-completion-accelerator`, which registers, routes to, and monitors
  applications
- one or more Hydra application workers that perform composition

These are roles, not a required process topology. A later design should decide
the protocol, process boundaries, deployment interface, application isolation,
and identity model.

## The `hydra.main` boundary

Entering wrapped `hydra.main` is the natural boundary between application
startup and completion service operation.

Decorator evaluation is too early. An application can perform additional
imports and registrations after defining its decorated function and before
calling it. An arbitrary registration call is also not a boundary because
there may be many registrations and Hydra cannot know which is the last one.

Once the application invokes its decorated main function, normal top-level
execution has reached Hydra. In completion-service mode, Hydra can initialize
composition, signal that the application is ready, and serve requests without
running user code intended for the configured task.

Registrations performed inside the task function are not included. Such
registrations are already too late for Hydra's normal initial composition.

## Deployment and lifecycle

The accelerator is installed as a [Reploy](https://reploy.yadan.net/)
application:

```text
reploy install hydra-completion-accelerator
```

Registering an application does not require a separate management step. When a
user activates Hydra tab completion for an application, Hydra detects the
accelerator and registers the application with it. Subsequent completion
requests discover and use the accelerator automatically.

Users should be able to inspect, refresh, and remove individual application
registrations. Registration must work for ordinary Python scripts as well as
packaged applications. Project metadata may improve environment discovery, but
it cannot be a requirement for the basic model.

A shell client needs a reliable way to find the service and the application
registration corresponding to the command being completed. Different
applications, working trees, and Python environments must not be confused. The
detailed identity, isolation, and discovery model is left for the later
design.

If the accelerator is not installed or a matching application registration is
not available, Hydra's existing one-shot completion remains available. Fast
completion is an optional acceleration path, not a new requirement for using
Hydra.

## Readiness and source changes

An application worker cannot provide its only health signal. Application
imports may fail, exit, or hang before control reaches Hydra. The service must
therefore own startup monitoring and expose enough per-application status to
distinguish an unavailable service from an application that failed to start.

The application becomes ready only after it reaches wrapped `hydra.main` and
Hydra verifies that composition works. Completion requests must also have a
bounded response time so a composition hang cannot block the shell
indefinitely.

During development, source and config changes may require rebuilding or
restarting an application worker. A watch mode could combine change detection,
debounce, and a build process. A replacement should become active only after
it starts successfully and passes its readiness check. Until then, the
previous healthy instance of that application should remain available.

This provides mechanical safety but cannot determine whether a developer
considers an edit complete. Explicit refresh and control over automatic
rebuilding should remain possible.

The exact watch set, build inputs, timeout policy, and replacement mechanism
belong in the later design.

## Reploy

Reploy deploys `hydra-completion-accelerator`. It may also provide isolated
application workloads, builds from local source, lifecycle management,
readiness, and healthy replacement.

Hydra should own the meaning of completion-service mode, the point at which
`hydra.main` declares readiness, request isolation, and completion semantics.
A deployment runtime can own building, starting, monitoring, and replacing
application workloads.

Reploy is a requirement for this acceleration path, not for Hydra or one-shot
completion.

Workload isolation is useful for dependency management and reproducibility,
but it is not a security boundary for untrusted code. Starting an application
worker executes that application's imports with the user's authority.

## Relationship to Structured Config registration

This direction preserves the current Structured Config registration model.
Providers can continue to register configs through ordinary application
imports before the program enters wrapped `hydra.main`.

A separate provider discovery mechanism may still be useful for static
inspection, packaging, or tools that must avoid executing the application. It
is not required to accelerate tab completion and should be evaluated
independently.

## Requirements for a later design

A detailed design should define:

- how `hydra-completion-accelerator` is packaged and deployed through Reploy
- how completion activation registers an application
- how users inspect, refresh, and remove application registrations
- how registrations persist or recover across accelerator restarts
- how a shell maps an invocation to the correct application registration
- how registered source and Python environments become application workers
- how completion-service mode is activated
- the request and response protocol
- isolation between applications and between requests
- concurrency and service-wide resource limits
- readiness, timeout, diagnostics, and recovery behavior
- source change detection and healthy replacement
- the boundary between Hydra and a deployment runtime
- local access control and treatment of sensitive configuration data
- compatibility and fallback behavior

It should validate that warm service results match one-shot completion, that
the task function is never called, that requests do not leak state, and that a
failed replacement cannot evict a healthy service.
