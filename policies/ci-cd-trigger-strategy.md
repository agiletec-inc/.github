# CI/CD Trigger Strategy

Canonical policy for build / deploy triggers across all `agiletec-inc` repositories.

This is the single source of truth. Repo-level `CLAUDE.md` files should
reference this document rather than restate the policy. Local
checkout-root notes (e.g. `agiletec-inc/CLAUDE.md` on a developer
machine) should link here, not duplicate.

## Goals

1. **`main` is always shippable.** Code lands via PR + Required checks. Direct push is banned by the Org Ruleset "Main Branch Protection".
2. **`main` push builds, but does not deploy.** Image artifacts are produced for every merge; deployment is a separate, deliberate act.
3. **Stage deploy = GitHub Release `published`.** Cutting a Release is the engineer's explicit "this commit is ready for stg" declaration.
4. **Production deploy = GitHub Environment with required reviewers.** No bespoke approval scripts; use the built-in `environment:` protection rule.
5. **Apps without a Release stay out of stg/prd automatically.** Work-in-progress apps don't need feature flags or special-casing — just don't cut a tag.

## Trigger map

| Stage | Trigger | Effect | Failure isolation |
|---|---|---|---|
| Build | `on: push: branches: [main]` (paths-filtered) | Image build + push to registry. No deploy. | Build break visible on the merge commit itself; can't silently rot in deploy land |
| Stage deploy | `on: release: types: [published]` | Bump `values/stg.yaml` `image.tag` in the deploy repo (cross-repo PR) → auto-merge → ArgoCD reconciles | Release with bad tag never matches dispatcher → early exit |
| Production deploy | Same workflow, `environment: prd` declared | Job pauses on `environment` review gate until a required reviewer approves, then bumps `values/prd.yaml` | Reviewer absent = no prod deploy. No accidental promotion |

### Tag naming convention

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

## Implementation status (2026-05-29)

> Per-repo adoption status, gap analysis, and the prioritized remediation
> checklist live in the companion doc
> [`ci-cd-standardization-status.md`](./ci-cd-standardization-status.md).

- **Public repos**: Already on the release-driven model. `cmd-ime/release.yml`
  uses `pull_request: types: [closed]` + `merged == true` + `workflow_dispatch`;
  `airis-mcp-gateway/release.yml` is a dedicated release workflow.
  Reference implementations.
- **Private repos**: `agiletec` and `agile-server` still on the legacy
  "main push → auto-bump → auto-deploy stg" model. Migration to release-driven
  is tracked in plan `~/.claude/plans/520-reach-bit-alert-auto-squishy-allen.md`.

## References

- [GitHub Actions: events that trigger workflows](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows)
- [GitHub Environments and deployment protection rules](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment)
- [About secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning)
- [GitHub Actions 2026 Security Roadmap](https://github.blog/news-insights/product-news/whats-coming-to-our-github-actions-2026-security-roadmap/) — least-privilege `secrets:` policy, scoped secrets
- Reusable workflows in this repo: `secret-scan.yml`, `node-pnpm-ci.yml`, `rust-cargo-ci.yml`, `python-ci.yml`, `swift-ci.yml`, `docker-ghcr-publish.yml`, `auto-merge.yml`
- Starter templates: `.github/workflow-templates/{node,rust,python,swift}-ci.yml`
- Targeting: org custom property `ci_managed` + ruleset "Org CI required checks" (id 17507867)
- [Well-Architected: rulesets best practices](https://wellarchitected.github.com/library/governance/recommendations/managing-repositories-at-scale/rulesets-best-practices/) (custom-property targeting)
