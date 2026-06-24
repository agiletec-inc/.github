# CI/CD Trigger Strategy

Canonical policy for build / deploy triggers across all `agiletec-inc` repositories.

This is the single source of truth. Repo-level `CLAUDE.md` files should
reference this document rather than restate the policy. Local
checkout-root notes (e.g. `agiletec-inc/CLAUDE.md` on a developer
machine) should link here, not duplicate.

## Goals

(2026-06-12 改定: 旧 release-driven stg deploy 標準と plan 520 は **supersede**。
1人法人 + 自宅単一クラスタに対し、デプロイチェーンの段数そのものが最大の
故障source だったため「merge = stg deploy」に簡素化。)

1. **`main` is always shippable.** Code lands via PR + Required checks. Direct push is banned by the Org Ruleset "Main Branch Protection". **CI required checks は品質ゲートとして不変** — ここがコーディングエージェント (Claude Code) の防波堤。
2. **Stage deploy = `main` push 直デプロイ。** merge された瞬間に stg に出る。中間機械 (bump PR / 耐久マージャ / release tag) を挟まない。デプロイの実行体は GA workflow 1 本 + デプロイスクリプト 1 本で、スクリプトは手動実行の脱出ハッチを兼ねる。
3. **Production deploy = 手動のみ。** `workflow_dispatch` + `environment: prd`(required reviewers)か、運用者の手作業。stg からの自動昇格はしない。
   - **例外: agiletec Supabase (migrations + Edge Functions) は main マージで CI 自動 deploy。** `deploy-supabase.yml` が `push:[main]`(`supabase/**` paths) で起動し、drift gate (`migration list --linked` で prd の REMOTE-only migration を検出して fail) → `db push` → `functions deploy` → post-deploy probe。承認ボタンには依存しない(Team-private では required reviewers が不発)。安全担保は PR ゲート (db reset from scratch + pgTAP + monotonic guard) + deploy 時 drift gate。agiletec の CF frontend promote は従来どおり手動。
4. **ArgoCD はインフラ + Deployment 構造の reconcile 専任。** image の中身はデプロイレーンが直接届ける (固定 mutable タグ、git 外)。image tag churn を GitOps に流さない。
5. **Release tag は public OSS の配布物にだけ使う**(cmd-ime の Homebrew 配布等)。デプロイのトリガーには使わない。

## Trigger map

| Stage | Trigger | Effect | Failure isolation |
|---|---|---|---|
| CI (品質ゲート) | `on: pull_request` | lint / test / build。Required checks (`ci / ci`, `secret-scan / scan`) が merge をブロック | 詰まり = merge 不可で即可視。デプロイには波及しない |
| Stage deploy | `on: push: branches: [main]` (paths-filtered) + `workflow_dispatch` | デプロイスクリプト実行 (例: airis-studio = 既存 ARC runner で nerdctl direct-bake `:stg` → `kubectl rollout restart`。workflow pod に containerd socket を hostPath マウント) | 失敗は workflow run に出る。スクリプト手実行(サーバー上)で即復旧可 |
| Production deploy | `workflow_dispatch` + `environment: prd` (required reviewers) / 手動運用 | 運用者の明示アクションでのみ prd へ | Reviewer absent = no prod deploy |

### Single-environment 運用 (個人ツール tier)

airis-studio のような operator=利用者 のツールは **stg が本番**(別 prd を持たない)。
namespace 分離・CI ゲート・自動デプロイはフル装備のまま、環境を 1 つに畳む。

### Release tag (public OSS 配布物のみ)

`<app>-vMAJOR.MINOR.PATCH[-suffix]`(例: `cmd-ime-v0.7.0`)。配布物
(Homebrew cask、バイナリ)の公開トリガーであり、デプロイとは無関係。

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

## Implementation status (2026-06-12)

> Per-repo adoption status, gap analysis, and the prioritized remediation
> checklist live in the companion doc
> [`ci-cd-standardization-status.md`](./ci-cd-standardization-status.md).

- **airis-studio**: merge=deploy レーン稼働 (deploy-stg.yml、既存 ARC runner
  + nerdctl direct-bake。ホスト常駐物ゼロ)。bump PR / 耐久マージャは撤去済み。
  stg=本番の single-environment 運用。
- **agiletec**: CF Workers (corporate/dashboard) は main push → wrangler deploy
  (ARC) で stg 自動。k3s レーンは廃止済み (agile-server #400 で manifests 全削除、
  bump 機械と bumper App credential も 2026-06-12 に全撤去)。prd は
  Cloudflare (frontend promote = 中井手動) + Supabase (migrations / Edge
  Functions = main マージで CI 自動 deploy・drift gate 付き、上記 §3 例外)。
- **Public repos**: release.yml は配布物の公開用として継続 (cmd-ime /
  airis-mcp-gateway が参照実装)。
- **旧 release-driven stg deploy 標準 (plan 520) は superseded** (2026-06-12)。
- **bump PR 機構は org から完全撤去** (2026-06-12): auto-merge-bumps.yml 削除、
  bump/* ブランチ削除、DEPLOY_BUMPER_* / IMAGE_BUMPER_* org credential 削除、
  agiletec-image-bumper App はアンインストール。

## References

- [GitHub Actions: events that trigger workflows](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows)
- [GitHub Environments and deployment protection rules](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment)
- [About secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning)
- [GitHub Actions 2026 Security Roadmap](https://github.blog/news-insights/product-news/whats-coming-to-our-github-actions-2026-security-roadmap/) — least-privilege `secrets:` policy, scoped secrets
- Reusable workflows in this repo: `secret-scan.yml`, `node-pnpm-ci.yml`, `rust-cargo-ci.yml`, `python-ci.yml`, `swift-ci.yml`, `docker-ghcr-publish.yml`, `auto-merge.yml`
- Starter templates: `.github/workflow-templates/{node,rust,python,swift}-ci.yml`
- Targeting: org custom property `ci_managed` + ruleset "Org CI required checks" (id 17507867)
- [Well-Architected: rulesets best practices](https://wellarchitected.github.com/library/governance/recommendations/managing-repositories-at-scale/rulesets-best-practices/) (custom-property targeting)
