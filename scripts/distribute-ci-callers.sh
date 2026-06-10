#!/usr/bin/env bash
# Distribute the standard CI caller (.github/workflows/ci.yml) to org repos.
#
# Detects each repo's language, picks the matching reusable, routes the runner by
# visibility (private -> ARC, public -> hosted), and opens a PR. The caller produces
# the org-required checks "secret-scan / scan" and "ci / ci".
#
# Logic lives in agiletec-inc/.github reusables — this only seeds thin callers.
#
# Usage:
#   ./distribute-ci-callers.sh                 # dry-run over all org repos
#   ./distribute-ci-callers.sh repo-a repo-b   # dry-run over a subset
#   APPLY=1 ./distribute-ci-callers.sh repo-a  # actually create the PR
#
# Requires: gh (authenticated), jq.
set -euo pipefail

ORG=agiletec-inc
REF="${CALLER_REF:-main}"   # ref of the reusables to pin in the caller (use a tag/SHA in prod)
APPLY="${APPLY:-0}"

# Repos with heavy bespoke CI — never auto-seed; managed by hand.
SKIP=(.github agiletec agile-server airis-studio)

is_skipped() { local r="$1"; for s in "${SKIP[@]}"; do [ "$r" = "$s" ] && return 0; done; return 1; }

# Does a root file/path exist on the default branch?
has_path() { gh api "repos/$ORG/$1/contents/$2" --silent >/dev/null 2>&1; }

detect_lang() {
  local repo="$1"
  if has_path "$repo" pnpm-lock.yaml || has_path "$repo" package.json; then echo node; return; fi
  if has_path "$repo" Cargo.toml; then echo rust; return; fi
  if has_path "$repo" pyproject.toml || has_path "$repo" requirements.txt || has_path "$repo" uv.lock; then echo python; return; fi
  if has_path "$repo" Package.swift; then echo swift; return; fi
  echo unknown
}

# Emit the caller YAML for a (lang, runner) pair.
# `runner` empty => hosted (public). Swift always uses hosted macOS, so it ignores `runner`.
render_caller() {
  local lang="$1" runner="$2" reusable ci_runner
  case "$lang" in
    node)   reusable=node-pnpm-ci  ;;
    rust)   reusable=rust-cargo-ci ;;
    python) reusable=python-ci     ;;
    swift)  reusable=swift-ci      ;;
  esac
  [ "$lang" = swift ] && ci_runner="" || ci_runner="$runner"

  echo "name: CI"
  echo ""
  echo "# Auto-seeded by .github/scripts/distribute-ci-callers.sh — logic lives in the org reusables."
  echo "# Required checks: \"secret-scan / scan\" and \"ci / ci\"."
  echo "on:"
  echo "  pull_request:"
  echo "  merge_group:"
  echo ""
  echo "concurrency:"
  echo "  group: ci-\${{ github.ref }}"
  echo "  cancel-in-progress: true"
  echo ""
  echo "jobs:"
  echo "  secret-scan:"
  echo "    uses: $ORG/.github/.github/workflows/secret-scan.yml@$REF"
  [ -n "$runner" ] && { echo "    with:"; echo "      runs-on: $runner"; }
  echo "  ci:"
  echo "    uses: $ORG/.github/.github/workflows/$reusable.yml@$REF"
  # Build the ci job's `with:` only when there is something to pass.
  if [ -n "$ci_runner" ] || [ "$lang" = node ] || [ "$lang" = python ]; then
    echo "    with:"
    [ -n "$ci_runner" ] && echo "      runs-on: $ci_runner"
    [ "$lang" = node ]   && echo "      run-command: pnpm turbo run build lint test"
    [ "$lang" = python ] && echo "      tool: auto"
  fi
}

seed_repo() {
  local repo="$1"
  local meta visibility default_branch lang runner
  meta=$(gh api "repos/$ORG/$repo" --jq '{private: .private, branch: .default_branch}')
  visibility=$(echo "$meta" | jq -r '.private')
  default_branch=$(echo "$meta" | jq -r '.branch')
  [ "$visibility" = true ] && runner=agiletec-self-hosted-runner || runner=""

  if has_path "$repo" .github/workflows/ci.yml; then
    echo "  skip $repo: .github/workflows/ci.yml already exists"
    return
  fi
  lang=$(detect_lang "$repo")
  if [ "$lang" = unknown ]; then
    echo "  skip $repo: language not detected"
    return
  fi

  local content; content=$(render_caller "$lang" "$runner")
  echo "  >>> $repo (lang=$lang, private=$visibility, runner=${runner:-hosted})"
  if [ "$APPLY" != 1 ]; then
    echo "$content" | sed 's/^/      | /'
    return
  fi

  local base_sha branch="ci/add-org-ci-caller"
  base_sha=$(gh api "repos/$ORG/$repo/git/ref/heads/$default_branch" --jq '.object.sha')
  gh api -X POST "repos/$ORG/$repo/git/refs" -f ref="refs/heads/$branch" -f sha="$base_sha" >/dev/null 2>&1 || true
  gh api -X PUT "repos/$ORG/$repo/contents/.github/workflows/ci.yml" \
    -f message="ci: adopt org reusable CI caller" \
    -f branch="$branch" \
    -f content="$(printf '%s' "$content" | base64)" >/dev/null
  gh pr create --repo "$ORG/$repo" --base "$default_branch" --head "$branch" \
    --title "ci: adopt org reusable CI caller" \
    --body "Seeds the standard thin CI caller (logic in \`$ORG/.github\` reusables). Produces required checks \`secret-scan / scan\` and \`ci / ci\`."
}

main() {
  local repos=("$@")
  if [ ${#repos[@]} -eq 0 ]; then
    mapfile -t repos < <(gh repo list "$ORG" --limit 200 --json name --jq '.[].name')
  fi
  [ "$APPLY" = 1 ] && echo "APPLY mode — creating PRs" || echo "DRY-RUN — set APPLY=1 to create PRs"
  for repo in "${repos[@]}"; do
    is_skipped "$repo" && { echo "  skip $repo: bespoke/excluded"; continue; }
    seed_repo "$repo"
  done
}

main "$@"
