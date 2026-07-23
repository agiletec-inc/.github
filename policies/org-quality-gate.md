# Organization quality gate contract

The organization-required workflow runs the same gate for every repository: stack detection picks
the applicable generic language jobs (Node, Bun, Python, Rust, Swift), and the secret scan,
feature-flag check, and final aggregator always run.

There is no per-repository exception mechanism (owner ruling 2026-07-24). A repository with its own
native CI still runs the generic stack jobs; duplication is accepted in exchange for a single
uniform gate. Do not reintroduce repository-name conditions or opt-out inputs into
`org-quality-gate.yml` / `quality-gate.yml`.
