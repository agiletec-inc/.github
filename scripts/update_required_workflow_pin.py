#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
import urllib.error
import urllib.request
from typing import Any


ORGANIZATION = "agiletec-inc"
SOURCE_REPOSITORY = "github-actions"
CANARY_REPOSITORY = "agiletec"
RULESET_ID = 19456040
TARGET_WORKFLOW = ".github/workflows/org-quality-gate.yml"
IMPLEMENTATION_WORKFLOW = ".github/workflows/quality-gate.yml"
CANARY_RULESET_NAME = "Candidate Org quality gate"
UPDATE_FIELDS = (
    "name",
    "target",
    "enforcement",
    "bypass_actors",
    "conditions",
    "rules",
)


class UpdateError(RuntimeError):
    pass


class GitHubApi:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token

    def request(self, method: str, path: str, body: object | None = None) -> object:
        encoded = None if body is None else json.dumps(body).encode()
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=encoded,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "X-GitHub-Api-Version": "2026-03-10",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = response.read()
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
            raise UpdateError(f"GitHub API {method} {path} failed: {error}") from error
        try:
            return json.loads(payload)
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise UpdateError(
                f"GitHub API {method} {path} returned invalid JSON"
            ) from error

    def get_object(self, path: str) -> dict[str, Any]:
        payload = self.request("GET", path)
        if not isinstance(payload, dict):
            raise UpdateError(f"GitHub API GET {path} did not return an object")
        return payload

    def get_array(self, path: str) -> list[object]:
        payload = self.request("GET", path)
        if not isinstance(payload, list):
            raise UpdateError(f"GitHub API GET {path} did not return an array")
        return payload

    def put_object(self, path: str, body: object) -> dict[str, Any]:
        payload = self.request("PUT", path, body)
        if not isinstance(payload, dict):
            raise UpdateError(f"GitHub API PUT {path} did not return an object")
        return payload


def require_string(record: dict[str, Any], key: str, context: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value:
        raise UpdateError(f"{context} has invalid {key}")
    return value


def require_integer(record: dict[str, Any], key: str, context: str) -> int:
    value = record.get(key)
    if not isinstance(value, int):
        raise UpdateError(f"{context} has invalid {key}")
    return value


def find_target_workflow(ruleset: dict[str, Any], repository_id: int) -> dict[str, Any]:
    rules = ruleset.get("rules")
    if not isinstance(rules, list):
        raise UpdateError("Ruleset has invalid rules")
    matching: list[dict[str, Any]] = []
    for rule in rules:
        if not isinstance(rule, dict) or rule.get("type") != "workflows":
            continue
        parameters = rule.get("parameters")
        workflows = (
            parameters.get("workflows") if isinstance(parameters, dict) else None
        )
        if not isinstance(workflows, list):
            raise UpdateError("Ruleset workflow rule has invalid workflows")
        for workflow in workflows:
            if not isinstance(workflow, dict):
                raise UpdateError("Ruleset contains an invalid workflow entry")
            if (
                workflow.get("repository_id") == repository_id
                and workflow.get("path") == TARGET_WORKFLOW
            ):
                matching.append(workflow)
    if len(matching) != 1:
        raise UpdateError(f"Expected one target workflow, found {len(matching)}")
    if matching[0].get("ref") != "refs/heads/main":
        raise UpdateError("Target workflow ref is not refs/heads/main")
    require_string(matching[0], "sha", "target workflow")
    return matching[0]


def update_payload(
    ruleset: dict[str, Any], repository_id: int, proposed_sha: str
) -> dict[str, Any]:
    missing = [key for key in UPDATE_FIELDS if key not in ruleset]
    if missing:
        raise UpdateError(f"Ruleset is missing update fields: {', '.join(missing)}")
    payload = {key: copy.deepcopy(ruleset[key]) for key in UPDATE_FIELDS}
    target = find_target_workflow(payload, repository_id)
    target["sha"] = proposed_sha
    return payload


def validate_source_candidate(api: GitHubApi, proposed_sha: str) -> int:
    repository = api.get_object(f"/repos/{ORGANIZATION}/{SOURCE_REPOSITORY}")
    repository_id = require_integer(repository, "id", "source repository")
    if require_string(repository, "default_branch", "source repository") != "main":
        raise UpdateError("Source repository default branch is not main")
    commit = api.get_object(
        f"/repos/{ORGANIZATION}/{SOURCE_REPOSITORY}/commits/{proposed_sha}"
    )
    if require_string(commit, "sha", "candidate commit") != proposed_sha:
        raise UpdateError("Candidate commit SHA mismatch")
    comparison = api.get_object(
        f"/repos/{ORGANIZATION}/{SOURCE_REPOSITORY}/compare/{proposed_sha}...main"
    )
    if comparison.get("status") not in {"ahead", "identical"}:
        raise UpdateError("Candidate SHA is not reachable from github-actions main")
    return repository_id


def validate_canary(
    api: GitHubApi, canary_pr: int, proposed_sha: str, repository_id: int
) -> None:
    pull = api.get_object(
        f"/repos/{ORGANIZATION}/{CANARY_REPOSITORY}/pulls/{canary_pr}"
    )
    if pull.get("state") != "open":
        raise UpdateError("Canary pull request is not open")
    base = pull.get("base")
    head = pull.get("head")
    if (
        not isinstance(base, dict)
        or base.get("ref") != "main"
        or not isinstance(head, dict)
    ):
        raise UpdateError("Canary pull request has an invalid base or head")
    head_sha = require_string(head, "sha", "canary pull request head")
    checks = api.get_object(
        f"/repos/{ORGANIZATION}/{CANARY_REPOSITORY}/commits/{head_sha}/check-runs"
        "?filter=latest&per_page=100"
    )
    check_runs = checks.get("check_runs")
    if not isinstance(check_runs, list):
        raise UpdateError("Canary check-runs response is invalid")
    aggregate = [
        check
        for check in check_runs
        if isinstance(check, dict)
        and check.get("name") in {"quality-gate", "quality-gate / quality-gate"}
        and isinstance(check.get("app"), dict)
        and check["app"].get("slug") == "github-actions"
    ]
    if len(aggregate) != 1:
        raise UpdateError(
            f"Expected one canary aggregate check, found {len(aggregate)}"
        )
    if (
        aggregate[0].get("status") != "completed"
        or aggregate[0].get("conclusion") != "success"
    ):
        raise UpdateError("Canary aggregate check is not successful")
    details_url = require_string(aggregate[0], "details_url", "canary aggregate check")
    run_match = re.search(r"/actions/runs/(\d+)(?:/|$)", details_url)
    if run_match is None:
        raise UpdateError("Canary aggregate check has no workflow run URL")

    rulesets = api.get_array(f"/repos/{ORGANIZATION}/{CANARY_REPOSITORY}/rulesets")
    candidates = [
        item
        for item in rulesets
        if isinstance(item, dict) and item.get("name") == CANARY_RULESET_NAME
    ]
    if len(candidates) != 1:
        raise UpdateError(f"Expected one canary Ruleset, found {len(candidates)}")
    canary_ruleset_id = require_integer(candidates[0], "id", "canary Ruleset")
    canary_ruleset = api.get_object(
        f"/repos/{ORGANIZATION}/{CANARY_REPOSITORY}/rulesets/{canary_ruleset_id}"
    )
    if canary_ruleset.get("enforcement") != "active":
        raise UpdateError("Canary Ruleset is not active")
    if find_target_workflow(canary_ruleset, repository_id).get("sha") != proposed_sha:
        raise UpdateError("Canary Ruleset does not pin the proposed SHA")

    run = api.get_object(
        f"/repos/{ORGANIZATION}/{CANARY_REPOSITORY}/actions/runs/{run_match.group(1)}"
    )
    if run.get("head_sha") != head_sha or run.get("path") != TARGET_WORKFLOW:
        raise UpdateError(
            "Canary workflow run does not match the pull request head or path"
        )
    referenced = run.get("referenced_workflows")
    if not isinstance(referenced, list):
        raise UpdateError("Canary workflow run has no provenance")
    expected_path = f"{ORGANIZATION}/{SOURCE_REPOSITORY}/{IMPLEMENTATION_WORKFLOW}@main"
    provenance = [
        item
        for item in referenced
        if isinstance(item, dict) and item.get("path") == expected_path
    ]
    if len(provenance) != 1 or provenance[0].get("sha") != proposed_sha:
        raise UpdateError("Canary workflow provenance does not match the proposed SHA")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposed-sha", required=True)
    parser.add_argument("--canary-pr", type=int, required=True)
    parser.add_argument("--api-base-url", default="https://api.github.com")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.proposed_sha):
        raise UpdateError("--proposed-sha must be a 40-character lowercase commit SHA")
    if args.canary_pr < 1:
        raise UpdateError("--canary-pr must be positive")
    token = os.environ.get("GH_TOKEN")
    if not token:
        raise UpdateError("GH_TOKEN is required")

    api = GitHubApi(args.api_base_url, token)
    repository_id = validate_source_candidate(api, args.proposed_sha)
    validate_canary(api, args.canary_pr, args.proposed_sha, repository_id)
    ruleset_path = f"/orgs/{ORGANIZATION}/rulesets/{RULESET_ID}"
    initial = api.get_object(ruleset_path)
    desired = update_payload(initial, repository_id, args.proposed_sha)
    if args.dry_run:
        print(
            json.dumps(
                {
                    "mode": "dry-run",
                    "ruleset_id": RULESET_ID,
                    "workflow": TARGET_WORKFLOW,
                    "proposed_sha": args.proposed_sha,
                },
                sort_keys=True,
            )
        )
        return 0

    current = api.get_object(ruleset_path)
    if current != initial:
        raise UpdateError("Ruleset changed between validation and update")
    api.put_object(ruleset_path, desired)
    readback = api.get_object(ruleset_path)
    readback_projection = {key: readback.get(key) for key in UPDATE_FIELDS}
    if (
        readback.get("id") != RULESET_ID
        or readback.get("source_type") != initial.get("source_type")
        or readback.get("source") != initial.get("source")
        or readback_projection != desired
    ):
        raise UpdateError("Ruleset read-back does not match the requested update")
    print(
        json.dumps(
            {
                "mode": "updated",
                "ruleset_id": RULESET_ID,
                "workflow": TARGET_WORKFLOW,
                "proposed_sha": args.proposed_sha,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except UpdateError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
