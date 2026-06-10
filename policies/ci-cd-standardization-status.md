# CI/CD Standardization — Status & Remediation

Companion to [`ci-cd-trigger-strategy.md`](./ci-cd-trigger-strategy.md) (the policy / SSoT).
That document defines the **target**; this one tracks **how far each repo has actually
adopted it** and the prioritized work to close the gaps.

**Snapshot: 2026-06-10** (regenerate by re-surveying `*/.github/workflows/`).

## Enforcement model decision (2026-06-10)

org plan = **`team`**. The ruleset rule "Require workflows to pass before merging"
(auto-injects a gate into every repo, no per-repo file) is **Enterprise Cloud only** and
does not run on Team. Decision: **stay on Team** and enforce CI org-wide via the
**"Require status checks to pass"** ruleset rule (Team-available) + standardized check
names (`secret-scan / scan`, `ci / ci`) + thin per-repo callers from the org reusables.

**Targeting = custom property** (GitHub Well-Architected recommendation, not repo-name
lists): org custom property `ci_managed` (true_false) + ruleset "Org CI required checks"
(id 17507867) filtering on `props.ci_managed:true`. A repo enrolls by setting the property;
the ruleset definition never changes. New repos: starter workflow + property. Existing
repos: per-repo reviewed migration PR, then set the property. See
`ci-cd-trigger-strategy.md` § Org-wide enforcement model.

## Summary

| Area | State |
|---|---|
| Policy / SSoT (`ci-cd-trigger-strategy.md`) | ✅ done |
| Reusable workflows (`secret-scan`, `node-pnpm-ci`, `rust-cargo-ci`, `python-ci`, `swift-ci`, `docker-publish`, `auto-merge`) | ✅ exist (multi-lang as of 2026-06-10) |
| Reusable actions SHA-pinned (in `.github` repo) | ✅ done + Dependabot bumps |
| Starter templates (`workflow-templates/`) | ✅ added (node/rust/python/swift) |
| Custom property `ci_managed` + property-targeted ruleset (id 17507867) | ✅ created (active) |
| Reusable **adoption** across repos | ⚠️ thin — migrate per-repo (see matrix), then set `ci_managed=true` |
| Pilot enrolled (`airis-keeper`, `ci_managed=true`, gated) | ✅ done |
| Public repos on release-driven CD | ✅ done (cmd-ime / airis-mcp-gateway reference impls) |
| Private (agiletec / agile-server) release-driven migration | ❌ TODO (plan 520 Step 5–9) |
| Runner labels unified | ❌ fragmented (4 self-hosted labels) |
| Action SHA-pinning enforced org-wide (consumer repos) | ⚠️ partial — reusables pinned; consumers via migration |

## Reusable-workflow adoption matrix

Which repos **call** each org reusable (`uses: agiletec-inc/.github/.github/workflows/<x>.yml@…`):

| Reusable | Callers (2026-06-10) | Note |
|---|---|---|
| `secret-scan.yml` | `mail-cleanse` | only adopter; should be a **required check everywhere** |
| `node-pnpm-ci.yml` | `airis-code` | most Node/Bun repos still hand-roll `ci.yml` |
| `docker-ghcr-publish.yml` | `mindbase` | GHCR pushers (airis-mcp-gateway/voom) still bespoke |
| `auto-merge.yml` | `airis-mcp-gateway`, `mindbase` | — |

**Gap**: the majority of repos (`agiletec`, `agile-server`, `airis-studio`, `cmd-ime`,
`voom`, `airis-mcp-gateway` CI, …) carry **duplicated bespoke workflows** instead of
calling the reusables. Every duplicate is a place a fix has to be applied N times.

## Runner-label inventory

Self-hosted labels in use (approx. `runs-on:` occurrences across all repos):

| Label | Kind | ~uses | Owner |
|---|---|---|---|
| `airis-studio-runners` | ARC | 19 | airis-studio (GPU build) |
| `agiletec-ci-runner` | ARC | 17 | agiletec |
| `agile-server-runner` | ARC | 8 | agile-server |
| `agiletec-self-hosted-runner` | ARC | 7 | org default (per policy) |
| `ubuntu-latest` / `ubuntu-22.04` / `macos-*` | GitHub-hosted | 45+ | public repos |

**Gap**: four distinct self-hosted labels with overlapping purpose. Policy names
`agiletec-self-hosted-runner` as the private default, but `agiletec-ci-runner` is used
more. Target: consolidate to ARC **runner scale sets** with multilabel (ARC ≥0.14.0),
namespace-isolated, with a small canonical label set (e.g. one general private label +
dedicated labels only where hardware differs, e.g. GPU for airis-studio).

## Action SHA-pinning

- **Status**: not enforced. Most workflows reference mutable tags (`@v4`, `@v2`).
- **Target** (official best practice): pin every action to a **full commit SHA** with a
  trailing `# vX` comment; let Dependabot (`github-actions` ecosystem) bump them.
- **Enforcement**: enable the org **allowed-actions SHA-pinning policy**
  (Settings → Actions → Policies) so unpinned actions fail. Watch the 2026 roadmap
  workflow-dependency lockfile.
- Reference impl: `mail-cleanse/.github/workflows/ci.yml` (checkout/setup-bun SHA-pinned,
  `permissions: contents: read`).

## Registry split (intentional, keep)

| Registry | Repos | Auth |
|---|---|---|
| GHCR | `airis-mcp-gateway`, `voom`, `mindbase` | `GITHUB_TOKEN` + `docker/login-action`, `permissions: packages: write` (no OIDC needed) |
| Zot (in-cluster) | `agiletec`, `airis-studio`, `duplicate-finder` | cluster registry creds |

OIDC is **not required for GHCR**; reserve it for external cloud (e.g. AWS). Current
near-zero OIDC usage is fine.

## Private release-driven migration

- **Status**: ❌ not done. `agiletec/_build-image.yml` still bumps the deploy repo on
  every main push (legacy continuous-deploy). Public repos already migrated.
- **Tracked in**: `~/.claude/plans/520-reach-bit-alert-auto-squishy-allen.md` (Step 5–9:
  `release-deploy.yml`, `environment: prd` reviewer gate, `_build-image.yml` bump removal).
- High-risk (touches prod deploy + cross-repo GitHub App). Execute as a dedicated effort.

## Remediation checklist (prioritized)

- [x] **Pilot** (`airis-keeper`): caller PR #4, checks `secret-scan / scan` + `ci / ci` green,
  public→hosted routing confirmed.
- [x] **Custom property + ruleset**: `ci_managed` (true_false) + ruleset id 17507867 (active)
  targeting `props.ci_managed:true`. airis-keeper enrolled.

1. **Migrate bespoke `ci.yml` per repo** (reviewed PRs, airis-keeper pattern — validate
   package manager / run-command / green). Then set `ci_managed=true` on that repo to enroll.
   Order: voom / mail-cleanse / cmd-ime / duplicate-finder / airis-workspace / mindbase /
   airis-mcp-gateway / mcp (`rust-cargo-ci` / `python-ci` / `swift-ci` / `node-pnpm-ci`).
2. **New repos**: starter workflow (1-click) + `ci_managed=true`.
3. **Heavy bespoke repos** (agiletec / airis-studio / agile-server): leave `ci_managed` unset
   (excluded), or make their CI emit `ci` / `secret-scan` check names before enrolling.
4. **SHA-pin actions in consumer repos** + add Dependabot `github-actions` (the `.github`
   reusables are already pinned + Dependabot-tracked).
5. **Private release-driven migration** (plan 520 Step 5–9) for agiletec / agile-server.
6. **Runner-label consolidation** via ARC runner scale sets (cluster change → agile-server
   GitOps PR).

Items 1–4 are low-risk (incremental PRs). Items 5–6 touch prod / the cluster and need
dedicated, separately-approved efforts.
