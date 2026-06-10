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
names (`secret-scan / scan`, `ci / ci`) + thin per-repo callers seeded from the org
reusables. See `ci-cd-trigger-strategy.md` § Org-wide enforcement model.

## Summary

| Area | State |
|---|---|
| Policy / SSoT (`ci-cd-trigger-strategy.md`) | ✅ done |
| Reusable workflows (`secret-scan`, `node-pnpm-ci`, `rust-cargo-ci`, `python-ci`, `swift-ci`, `docker-publish`, `auto-merge`) | ✅ exist (multi-lang as of 2026-06-10) |
| Reusable actions SHA-pinned (in `.github` repo) | ✅ done + Dependabot bumps |
| Starter templates (`workflow-templates/`) | ✅ added (node/rust/python/swift) |
| Bulk caller distribution script | ✅ added (`scripts/distribute-ci-callers.sh`) |
| Reusable **adoption** across repos | ⚠️ thin — run distribution script (see matrix) |
| org ruleset "Require status checks" created | ❌ TODO (manual; after pilot confirms check names) |
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

1. **Pilot one repo** (e.g. `airis-keeper`): add the caller, open a PR, confirm the real
   check names via `gh pr checks` are `secret-scan / scan` and `ci / ci`, and that
   private→ARC / public→hosted runner routing works.
2. **Create the org ruleset** "Require status checks to pass" with those exact check names.
   Start in **Evaluate** (dry-run), watch Rule Insights, then flip to **Active**.
3. **Bulk-distribute callers** to the remaining simple repos:
   `APPLY=1 .github/scripts/distribute-ci-callers.sh` (auto-detects language + visibility;
   skips `.github`, agiletec, agile-server, airis-studio).
4. **Migrate bespoke `ci.yml`** in the multi-lang repos to call the new reusables
   (`rust-cargo-ci` / `python-ci` / `swift-ci`), folding per-repo knobs into reusable inputs.
5. **Heavy bespoke repos** (agiletec / airis-studio / agile-server): keep custom CI but make
   it emit the `ci` / `secret-scan` check names, or exclude them from the ruleset target.
6. **SHA-pin actions in consumer repos** + add Dependabot `github-actions` (the reusables in
   `.github` are already pinned + Dependabot-tracked).
7. **Private release-driven migration** (plan 520 Step 5–9) for agiletec / agile-server.
8. **Runner-label consolidation** via ARC runner scale sets (cluster change → agile-server
   GitOps PR).

Items 1–6 are low-risk (incremental PRs). Items 7–8 touch prod / the cluster and need
dedicated, separately-approved efforts.
