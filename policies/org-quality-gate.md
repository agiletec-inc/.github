# Organization quality gate contract

The organization-required workflow always runs its secret scan, feature-flag check, and final
aggregator. A repository that already enforces language and build gates in its own required CI may
be listed centrally in `org-quality-gate.yml` with `stack-checks: false`. This prevents duplicate
generic Node, Bun, Python, Rust, and Swift jobs.

The exception is controlled in this repository, not by files from the pull request under test, so
a product-repository pull request cannot exempt itself. Before adding an exception, verify that the
repository ruleset requires its native canonical CI. The exception never disables the
organization-wide security checks or final aggregator.
