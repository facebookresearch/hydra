# Async execution direction

Status: exploratory design note.

Target release: not Hydra 1.4.0.

## Summary

Hydra's current launcher and sweeper model is synchronous and batch-oriented. A
sweeper produces a batch of jobs, a launcher launches that batch, and Hydra
expects completed job results before the control flow continues.

That model is simple, but it is also one of the deepest design limitations in
Hydra. It makes it hard to represent remote schedulers, adaptive sweepers,
dynamic job graphs, and long-running distributed workloads without forcing them
through a synchronous result-returning API.

Fire-and-forget launching is a real user request, but it is not the main
motivation. It is a symptom of the larger issue: Hydra does not have a first
class execution model that separates submission, supervision, control,
communication, and result collection.

## Current model

The current launcher contract is effectively:

- receive a batch of job overrides
- launch the jobs
- wait for the jobs
- return completed job results

This works naturally for local execution and simple parallel execution. It does
not map well to queue-based or distributed execution systems such as Slurm, RQ,
Ray, Airflow, or other schedulers.

In those systems, submitting work and collecting results are distinct lifecycle
steps. A job may be submitted successfully but not yet running. It may be
running but not complete. It may need to report intermediate metrics back to a
controller. It may create more work dynamically.

Hydra's current synchronous model has no honest representation for that middle
state.

## The original design problem

The original design problem is that Hydra treats launch as a synchronous batch
operation that returns completed results. That conflates several separate
concepts:

- generating work
- submitting work
- supervising work
- waiting for work
- reporting progress or metrics
- collecting final results
- deciding what work to run next

When these concepts are bundled together, queue-based systems are forced into
bad choices:

- block until remote jobs finish
- return fake completed results
- throw after enqueueing work
- smuggle scheduler ids through return values
- rely on output directories and ad hoc files for coordination

Those are signs that the abstraction is wrong for async execution.

## Motivation

A proper async execution model could enable more than submit-and-exit behavior.

### Dynamic work graphs

Jobs could launch subjobs without relying on manually managed directories,
sentinel files, or external scripts. This opens the door to dynamic DAG-like
execution while keeping Hydra's config and override model as the way work is
described.

This is workflow-engine territory, or at least the seed of it. The important
question is whether Hydra should own that model and keep it Hydra-shaped.

### More efficient HPO

Some HPO sweepers should not need to wait for an entire batch before making the
next decision. If one job is slow, it should not necessarily block the sweeper
from consuming faster results and scheduling more work.

Async execution could let adaptive sweepers react as results arrive, support
early stopping or pruning, and make better use of cluster resources.

### Honest async launchers

Launchers for Slurm, RQ, Ray, Airflow, and similar systems could submit work and
represent that work as submitted or running instead of pretending it is already
complete.

### Better control-plane design

Some execution patterns need a live control process. That process may need to
schedule jobs, receive metrics, observe failures, prune trials, and persist
state. Hydra currently lacks a clear story for where that control process lives
and how launched jobs communicate back to it.

## Minimum useful scope

The minimum useful scope is the first hop: a command-line Hydra invocation should
be able to schedule work into a queue and exit without pretending the scheduled
work has completed.

That first hop is valuable on its own. Users should be able to use Hydra as a
clean submission frontend for configured jobs, especially in scheduler-backed
environments where keeping the original shell, SSH session, or local Python
process alive is undesirable.

This first hop does not require solving the entire dynamic execution problem. It
does require an honest representation of submitted work, and it requires Hydra
to avoid corrupting the existing completed-result contract.

If the first-hop model also clarifies the local execution state story, especially
job directories, metadata, and how submitted work is identified, then Hydra can
later expose a cleaner API for subsequent launching. That would make dynamic
DAG-like patterns possible without relying on manually managed output
directories, sentinel files, or custom scheduler scripts.

In other words:

- first, support command-line submission to a queue cleanly
- then, if execution state and local directory semantics are clear, build toward
  jobs launching additional configured jobs
- only after that, consider richer controller-driven dynamic execution

## Bidirectional communication

An explicit goal of this direction is to design a bidirectional communication
channel between the launching instance, or controller, and the child jobs it
starts.

The channel should allow the controller to communicate intent to jobs, and jobs
to communicate state back to the controller. This may include:

- job identity and parent-child relationships
- lifecycle state
- intermediate metrics
- objective values
- logs or log locations
- failure information
- cancellation or pruning requests
- requests to launch additional configured work

This channel is important for adaptive sweepers, dynamic DAG-like execution, and
clean recovery/resume behavior. It should not be modeled as incidental files in
job output directories unless the filesystem is deliberately chosen as one
backend for the communication channel.

## Sweepers and the control plane

Async execution is not only a launcher problem.

Some sweepers are static. They can enumerate work up front and may be compatible
with submit-only execution.

Other sweepers are adaptive. HPO sweepers may need to:

- observe completed trials
- receive objective values or intermediate metrics
- decide the next trials based on previous results
- stop or prune bad trials
- coordinate parallel workers
- persist and resume study state
- communicate with running jobs

For those sweepers, fire-and-forget is insufficient. There may need to be a
control job or controller process. That controller might run locally, on the
cluster, inside a scheduler, or in a backend-specific service.

This is why async launching is a larger execution-control design. A launcher
cannot solve it alone.

## Ownership

Hydra likely needs to own the execution semantics, even if it delegates concrete
execution to backends.

Hydra already owns:

- config composition
- override parsing
- sweeper decisions
- launcher selection
- job numbering
- job directories
- callbacks
- logging
- plugin integration

Async execution cuts across all of these. If Hydra does not own the semantics,
the abstractions will leak through every launcher and sweeper plugin.

At the same time, Hydra should avoid becoming a general-purpose workflow engine
by accident. The goal should be a Hydra-shaped execution model: config-first,
sweep-aware, plugin-friendly, and focused on Hydra use cases.

## Relationship to Ray

Ray is a useful reference point and may be a viable backend for some execution
patterns. It provides a strong API surface for remote work, actors, futures, and
distributed execution.

However, Ray should not be treated as a substitute for Hydra's execution model.
The Ray AWS launcher is already one of Hydra's most complex launchers. Some of
that complexity comes from AWS, but Ray itself also contributes significant
operational and integration complexity:

- cluster lifecycle
- credentials and cloud configuration
- dependency and environment setup
- packaging and file transfer
- resource configuration
- log and error retrieval
- retries and failures
- version drift
- CI and testing complexity
- user mental model mismatch

Ray can be a backend, but making Ray the semantic center would make Hydra
Ray-shaped. Hydra should define the lifecycle semantics it needs, and backends
such as Ray, Slurm, local execution, RQ, or Airflow can implement those
semantics where appropriate.

## Separate project

An async execution model could be incubated in a separate project, but that is
not obviously attractive as the long-term answer.

A separate project could reduce risk and allow experimentation. It could also
create a confusing boundary, duplicate Hydra concepts, or become a second Hydra
runtime outside the main project.

If async execution is core to Hydra's launcher and sweeper story, the long-term
semantics probably belong in Hydra, even if experimental work starts elsewhere.

## Migration

Any realistic design needs a long migration path.

Hydra cannot require all launchers and sweepers to move to a new model at once.
Existing plugins and user workflows must continue to work.

A plausible migration direction:

- keep the current synchronous launcher model as a compatibility model
- introduce a new execution model as opt-in
- migrate local/basic execution first
- allow new async-aware plugins to use the new model
- allow sweepers to declare which execution modes they support
- reject unsupported combinations clearly
- provide compatibility adapters where possible
- only consider deprecating the old model after a long coexistence period

The first goal is not to replace every launcher. The first goal is to create a
place where async execution can exist without corrupting the current
result-returning contract.

## Non-goals

This is not planned for Hydra 1.4.0.

This note does not propose accepting existing fire-and-forget Submitit patches.

This note does not define a final API.

This note does not commit Hydra to implementing async execution.

This note does not require Hydra to implement a general-purpose workflow engine.

## Interim policy

Until Hydra has a real async execution design, patches should not fake async
behavior inside the current synchronous launcher model.

In particular, launchers should not return completed job results for work that
has only been submitted.

Fire-and-forget requests should be treated as design inputs for this larger
execution model, not as isolated launcher options.

## Related issues and PRs

- [#64](https://github.com/facebookresearch/hydra/issues/64): Break `--sweep`
  into its base components.
- [#284](https://github.com/facebookresearch/hydra/issues/284): Launcher should
  support `initial_job_num`.
- [#692](https://github.com/facebookresearch/hydra/issues/692): Support
  non-blocking launching.
- [#851](https://github.com/facebookresearch/hydra/issues/851): Evaluate using
  the configured launcher in regular runs.
- [#1847](https://github.com/facebookresearch/hydra/issues/1847): Submitit
  option to not wait for finished jobs.
- [#1928](https://github.com/facebookresearch/hydra/issues/1928): Failed
  Submitit jobs are still reported as completed.
- [#2171](https://github.com/facebookresearch/hydra/pull/2171): Non-blocking
  Slurm job submission option.
- [#2479](https://github.com/facebookresearch/hydra/issues/2479): Exit after
  Submitit schedules a Slurm job.
- [#2965](https://github.com/facebookresearch/hydra/pull/2965): No-block Slurm.
- [#3017](https://github.com/facebookresearch/hydra/pull/3017): Submitit
  launcher async support.
- [#3058](https://github.com/facebookresearch/hydra/issues/3058): Submit Slurm
  jobs eagerly.
- [#3082](https://github.com/facebookresearch/hydra/issues/3082): Submitit
  multirun without sweeping.
- [#3128](https://github.com/facebookresearch/hydra/pull/3128): Submitit
  `wait_for_completion` option.

## Open questions

- Is async execution important enough to justify redesigning the launcher and
  sweeper model?
- Should Hydra own this model, or should it delegate to an existing system?
- If Hydra owns it, how narrow can the model remain while still being useful?
- Is a control job a first-class Hydra concept?
- Where can the control process run?
- How do jobs report metrics, objective values, logs, and failures back to the
  controller?
- How should dynamic subjobs be represented?
- Which sweepers can support submit-only execution?
- Which sweepers require a live controller?
- How should resume and reconnect work?
- How should existing plugins migrate?
- Is this future-major-version scope, or should it remain outside Hydra?

## Initial recommendation

Do not include async execution work in Hydra 1.4.0.

Keep existing fire-and-forget and non-blocking launcher requests open as
far-future design inputs.

Avoid accepting patches that make the current synchronous model less honest.

If this direction is pursued, start with a small experimental design that proves
the control-plane story before attempting to migrate major plugins.
