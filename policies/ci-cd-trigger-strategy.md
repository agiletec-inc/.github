# CI/CD Trigger Strategy

Canonical policy for build / deploy triggers across all `agiletec-inc` repositories.

This is the single source of truth. Repo-level `CLAUDE.md` files should
reference this document rather than restate the policy. Local
checkout-root notes (e.g. `agiletec-inc/CLAUDE.md` on a developer
machine) should link here, not duplicate.

## Goals

1. **`main` is always shippable.** Code lands via PR + Required checks. Direct push is banned by the Org Ruleset "Main Branch Protection".
2. **`main` merge auto-deploys services to staging.** Passing the quality gate and merging *is* the "ready for stg" signal — no separate Release to cut. Staging is the non-exposed home cluster / the staging Worker env.
3. **Staging is light, not GitOps.** k3s services bake straight into the node's containerd (`nerdctl --namespace k8s.io build` + `kubectl rollout restart`); Workers use `wrangler deploy --env staging`. No Zot / immutable-SHA / cross-repo-bump ceremony for stg (that's a prod concern). Single-node + private = rebuildable-from-main, so the reproducibility cost isn't worth paying here.
4. **Production is a deliberate promotion.** Gated by GitHub `environment: prd` (required reviewers) on the reproducible path (Zot immutable SHA + ArgoCD GitOps). No accidental promotion.
5. **Distributables publish on a Release tag** (`<app>-vMAJOR.MINOR.PATCH`), not on every main commit. WIP apps that cut no tag stay unpublished automatically.
6. **Manual force-deploy to staging is always available** (`workflow_dispatch` + an on-node script) for when the auto pipeline (ARC runners / merge / sync) stalls and "just won't reflect."

## Trigger map

| Stage | Trigger | Effect | Notes |
|---|---|---|---|
| Quality gate | `pull_request` | `secret-scan` + language `ci` reusables (required by the org ruleset) | Green → **auto-merge** via `agiletec-automerge` App |
| Stage deploy — k3s service | `push: branches: [main]` (paths-filtered) | On the GPU node: `nerdctl --namespace k8s.io build -t <img>:stg` → `kubectl rollout restart deploy/<x> -n <app>-stg`. No Zot, no bump PR, no ArgoCD. | Build break visible on the merge commit; staging is rebuildable from main |
| Stage deploy — Worker | `push: branches: [main]` (paths-filtered) | `wrangler deploy --env staging` | Registry-free |
| Force-deploy (escape hatch) | `workflow_dispatch` / on-node script | Same bake + `rollout restart` (k3s) or `wrangler deploy --env staging` (Worker), run out-of-band | Bypasses ARC queue / stuck sync |
| Publish — distributable | `release: types: [published]` (`<app>-vX.Y.Z`) | Build + publish the artifact (npm / Homebrew / GHCR / GitHub Release) | Not per-commit; no tag → no publish |
| Production — service | Manual promote, `environment: prd` | Reviewer gate → reproducible path: pin Zot immutable SHA in the deploy repo → ArgoCD reconciles | Reviewer absent = no prod deploy |

### Tag naming convention (distributables / prod promotion)

`<app>-vMAJOR.MINOR.PATCH[-suffix]`. Examples:

- `airis-agent-v1.4.2`
- `airis-evidence-script-v2.0.0-rc.1`
- `cmd-ime-v0.7.0`

The workflow extracts `<app>` and `<version>` with bash `BASH_REMATCH`
against an allowlist of known app names. Unknown app → `::error::`,
no bump attempted. Tag parsers using `sed` / `cut` / `awk` are brittle
against hyphenated app names (`bid-alert`, `evidence-script`); use
regex with explicit alternation.

## Org-wide enforcement model (CI / quality gates)

CI/品質ゲートは **org ルールセット "Require status checks to pass"**（Team プランで利用可）
で強制する。各リポは薄い caller（`.github/workflows/ci.yml`）で `agiletec-inc/.github` の
reusable を呼ぶだけ。**ロジックの SSoT は reusable 側**（修正は 1 箇所）。

- **ターゲティング = custom property**（GitHub Well-Architected 推奨。repo 名リストでない）。
  org custom property **`ci_managed`**（true_false, GA 2026-01-13・Team 可）を定義し、ルールセット
  "Org CI required checks"（id 17507867）を `props.ci_managed:true` フィルタで対象化。**リポは
  property を立てるだけで enroll、ルールセット定義は不変**。
- **必須チェック名**: `secret-scan / scan` と `ci / ci`（reusable 呼びのチェック名は
  `<caller job 名> / <reusable 内 job 名>` で合成）。内部 job 名は `secret-scan.yml`→`scan` /
  言語 reusable→`ci` に固定済み（enforce 前に安定したチェック名を出す = Well-Architected 準拠）。
- **caller 配布**: 新規リポは Actions タブの starter template（`.github/workflow-templates/`）から
  1 クリック。既存リポは **リポ毎のレビュー付き移行 PR**（PM/run-command を検証。盲目的な一括
  置換はしない）。配布後にそのリポへ `ci_managed=true` を付与。
- **runner ルーティング**: caller が private→`agiletec-self-hosted-runner` / public→hosted を指定。
- **secret-scan**: gitleaks バイナリ直叩き（org でも `GITLEAKS_LICENSE` 不要）。漏洩で実際に
  job を fail させる（`continue-on-error` による空虚な緑を排除）。
- **ロールアウト**: evaluate→pilot→expand→enforce のうち **evaluate は Enterprise 限定**。Team は
  **pilot（対象を 1 リポに絞った active）** で代替（airis-keeper で実証済）。

> **不採用**: org ルールセットの "Require workflows to pass before merging"（ゲートを各リポに
> 自動注入し caller ファイルを不要にする機能）は **GitHub Enterprise Cloud 限定**。org plan が
> `team` の間は使えない（設定画面に出ても実行されない）。Enterprise upgrade（$4→$21/user）は
> 小規模 org に過剰なため、上記の status-check 強制で同等の効果を得る。差は「caller ファイルが
> 各リポに要るか否か」だけ。
> 参照: [Available rules for rulesets](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)

## Visibility model

The trigger model is the same for private and public repos. What
differs is which guards do the heavy lifting.

| Concern | Private (`agiletec` / `agile-server` / 他 private) | Public (`cmd-ime` / `airis-mcp-gateway` / `airis-workspace` / `mindbase` / `airis-code` / `homebrew-tap` / 等) |
|---|---|---|
| Blast radius on secret leak | Contained to org boundary; time to rotate | Instant world-wide propagation; no time to react |
| Runtime secret injection | **Doppler required** (`doppler run --` / k8s operator → Secret) | GitHub Secrets / env (acceptable because secrets are scoped, not user-facing) |
| Secret scanning | **GitHub Advanced Security (paid)** on Team/Enterprise — verify with org admin | **Free, default-available** (verify ON in Settings → Code security) |
| Push protection | Paid via GHAS | Free for public repos; **must be enabled** at repo or org level (default is OFF for repos, must be flipped) |
| CodeQL | Paid via GHAS | Free for public repos; add `codeql.yml` workflow |
| Runner | ARC self-hosted (`agiletec-self-hosted-runner`, `airis-studio-runners`, `agile-server-runner`); minimize hosted-minute spend | GitHub-hosted (`ubuntu-latest` / `macos-latest`); free for public |
| Cross-repo PR auth | GitHub App + `create-github-app-token@v3`, scoped permissions. **PAT banned.** | Standard `GITHUB_TOKEN` or minimally-scoped fine-grained PAT |
| Auto-merge | Via the `agiletec-automerge` GitHub App (the default `GITHUB_TOKEN` returns "Resource not accessible by integration" for the enable-auto-merge API) | Same App also works; or use `gh pr merge --auto` from the workflow with a PAT for repos that allow it |
| Reusable CI workflows | Pull from `agiletec-inc/.github` (`secret-scan.yml`, `node-pnpm-ci.yml`, `rust-cargo-ci.yml`, `python-ci.yml`, `swift-ci.yml`, `docker-ghcr-publish.yml`, `auto-merge.yml`) with `runs-on: agiletec-self-hosted-runner` | Pull the same reusables with `runs-on: ubuntu-latest` (default) |

**The framing "public CI is lighter" is wrong.** Public CI files are
shorter because the heavy lifting is delegated to GitHub's built-in
features (secret scanning, push protection, CodeQL, hosted runner). The
defense total is at least equal — sometimes higher, since built-ins are
maintained by GitHub. Treat public guards as load-bearing infrastructure,
not optional decoration.

## Required guards per visibility

### Private repos must have

- Branch protection: Required checks pass before merge; merge commit only
  (squash/rebase disabled by Org Ruleset)
- `secret-scan` reusable workflow (`agiletec-inc/.github/.github/workflows/secret-scan.yml`)
  as a required check
- Runtime secrets via Doppler only; no `.env` files in repo
- Cross-repo automation via GitHub Apps with least-privilege scope
- ARC runners only (no GitHub-hosted) for cost containment
- For repos with prod deploy: `environment: prd` with required reviewers

### Public repos must have

- Branch protection: Required checks pass before merge
- **Push protection ENABLED** at repo level (Settings → Code security →
  Secret scanning → Push protection: Enable)
- **Secret scanning ENABLED** (Settings → Code security → Secret scanning)
- `secret-scan` reusable workflow as a required check (belt-and-braces
  with built-in scanning)
- `codeql.yml` workflow as a required check
- `verify-runners` style guard if the repo must stay on GitHub-hosted runner
  (see `airis-mcp-gateway/scripts/test-workflow-runners.sh` for a working
  reference implementation)
- No `.env` files committed; pre-commit hooks reject any matching
  pattern (`.env`, `.env.local`, `.env.*`, `*.pem`, `*credentials*`)
- Dependabot enabled (free, default for public)

## Implementation status (revised 2026-06-11)

> Per-repo adoption status, gap analysis, and the prioritized remediation
> checklist live in the companion doc
> [`ci-cd-standardization-status.md`](./ci-cd-standardization-status.md).

**Policy reversal (2026-06-11):** the earlier plan to migrate *services* off
"main → auto-deploy stg" onto a Release-gated stg deploy is **dropped**. For
single-node, non-exposed staging that Release ceremony (plus the Zot
immutable-SHA + cross-repo bump-PR dance) was over-engineering. Services now
auto-deploy to stg on main merge, lightly (k3s: nerdctl direct-bake;
Worker: `wrangler --env staging`). Release-driven publishing is retained only
for **distributables** (CLI / desktop / npm / Homebrew / Tauri / MCP images),
where shipping every commit is wrong. Production stays a deliberate,
reproducible promotion (`environment: prd` + Zot/GitOps).

- **Distributables (public repos)**: Release-driven. `cmd-ime/release.yml`
  (`pull_request: closed` + `merged` + `workflow_dispatch`),
  `airis-mcp-gateway/release.yml`. Reference implementations — unchanged.
- **Services (k3s + Workers)**: target = main merge → light stg auto-deploy
  (this doc). agiletec Workers already do `wrangler --env staging` on main;
  airis-studio k3s moves from the Zot/bump/ArgoCD path to nerdctl direct-bake +
  `rollout restart` for stg. The persistent `buildkitd` Deployment is retired
  in favour of nerdctl on the node's containerd.
- **Quality gate / auto-merge / org ruleset**: unchanged and still the front
  door for every repo (`ci_managed` + `secret-scan`/`ci` reusables +
  `agiletec-automerge`); roll-out completion tracked in the companion doc.

## References

- [GitHub Actions: events that trigger workflows](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows)
- [GitHub Environments and deployment protection rules](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment)
- [About secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning)
- [GitHub Actions 2026 Security Roadmap](https://github.blog/news-insights/product-news/whats-coming-to-our-github-actions-2026-security-roadmap/) — least-privilege `secrets:` policy, scoped secrets
- Reusable workflows in this repo: `secret-scan.yml`, `node-pnpm-ci.yml`, `rust-cargo-ci.yml`, `python-ci.yml`, `swift-ci.yml`, `docker-ghcr-publish.yml`, `auto-merge.yml`
- Starter templates: `.github/workflow-templates/{node,rust,python,swift}-ci.yml`
- Targeting: org custom property `ci_managed` + ruleset "Org CI required checks" (id 17507867)
- [Well-Architected: rulesets best practices](https://wellarchitected.github.com/library/governance/recommendations/managing-repositories-at-scale/rulesets-best-practices/) (custom-property targeting)
