# Feature Flag Quality Gate

`quality-gate` runs this check in every repository. A repository without
`.airis/flags.toml` succeeds without a feature-flag check. Repositories that
declare flags own their flag metadata and the two test commands below.

The organization ruleset enforces `.github/workflows/org-quality-gate.yml`.
It has `pull_request` and `merge_group` triggers and delegates to this reusable
quality gate; callers must not add path filters to their own quality workflow.

```toml
[[flags]]
key = "checkout.v2"
kind = "release"
type = "boolean"
owner = "team:billing"
expires = "2026-12-31"
cleanup_issue = "https://github.com/agiletec-inc/example/issues/123"

[flags.tests.off]
command = "pnpm test:checkout-v2-off"
environment = { CHECKOUT_V2 = "false" }

[flags.tests.on]
command = "pnpm test:checkout-v2-on"
environment = { CHECKOUT_V2 = "true" }
```

`release` and `experiment` flags are temporary. They require an owner, an
unexpired `expires` date, a cleanup issue, and successful off/on tests. `ops`,
`permission`, and `kill_switch` flags require an owner but are not required to
have an expiry or test pair.
