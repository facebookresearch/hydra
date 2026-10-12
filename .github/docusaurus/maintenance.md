# Docusaurus dependency maintenance

The shared toolchain is Node 24 and pnpm 11.21.0. Dependency resolution uses a
10-day release delay, restricted dependency sources and explicit dependency-script
approvals. Application dependency versions, site configuration, overrides and
exact security exceptions remain project configuration.

`.github/docusaurus.json` selects the documentation directory. The website owns
its normal `build` script and all build prerequisites; the audit runs that script
without configuring or duplicating the website's build internals.

The project configuration sets the audit schedule; new deployments without a
schedule default to January 30 at 02:00 UTC. The single `Docusaurus dependency
audit` workflow also supports manual dispatch on the default branch. It attempts
security fixes at all severities
before other stable upgrades, performs a frozen installation and production
build, and reports the results in an umbrella PR. Failed candidates are published
as drafts and fail the workflow after the report is retained. Successful reruns
leave an existing draft for human review. No report is committed.
The PR is titled `Docusaurus maintenance: security audit and dependency upgrades`,
distinct from individual Dependabot update PRs and security alerts.
Only the project's manifest, lockfile and required pnpm security exceptions enter
that dependency PR. Findings and validation failures remain visible.

Documentation vulnerabilities are accepted between maintenance reviews. Scope
Dependabot update suppression and alert dismissal to this deployment's lockfile;
leave other ecosystems unchanged. Repository permissions and alert-dismissal
rules require separate verification.

Reports include all changed locked version sets and candidate dependency-file
SHA-256 hashes. Successful and failed command output, including warnings, is
retained in grouped workflow logs. When a run makes no dependency changes, it
leaves an existing PR branch and its report unchanged; the new report remains in
the Actions summary and artifact.

Generated commits use ordinary messages, so normal PR checks and post-merge
CI/deployment remain enabled. GitHub may require approval to run checks on a PR
created with the workflow token. Nothing is merged automatically.

Files under `.github/docusaurus/` are copied unchanged from the producer. The
single audit workflow is generated from its shared template, rendering only
the schedule from `.github/docusaurus.json`. Put project customization in that
configuration, then regenerate; do not edit generated files. Verify shared-file
hashes, the exact generated workflow and a no-change adoption rerun.
