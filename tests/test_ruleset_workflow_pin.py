from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/update_required_workflow_pin.py"
PROPOSED_SHA = "a" * 40
CANARY_HEAD_SHA = PROPOSED_SHA
RULESET_PATH = "/orgs/agiletec-inc/rulesets/19456040"


def live_ruleset() -> dict[str, Any]:
    return {
        "id": 19456040,
        "name": "Org quality gate",
        "target": "branch",
        "source_type": "Organization",
        "source": "agiletec-inc",
        "enforcement": "active",
        "conditions": {
            "repository_name": {
                "include": ["~ALL"],
                "exclude": ["archived-example"],
                "protected": True,
            },
            "ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []},
        },
        "bypass_actors": [
            {"actor_id": 42, "actor_type": "Integration", "bypass_mode": "pull_request"}
        ],
        "rules": [
            {"type": "deletion"},
            {
                "type": "pull_request",
                "parameters": {
                    "required_approving_review_count": 0,
                    "allowed_merge_methods": ["merge"],
                },
            },
            {
                "type": "workflows",
                "parameters": {
                    "do_not_enforce_on_create": True,
                    "workflows": [
                        {
                            "repository_id": 9001,
                            "path": ".github/workflows/org-quality-gate.yml",
                            "ref": "refs/heads/main",
                            "sha": "c" * 40,
                        },
                        {
                            "repository_id": 8123,
                            "path": ".github/workflows/other.yml",
                            "ref": "refs/heads/stable",
                            "sha": "f" * 40,
                        },
                    ],
                },
            },
        ],
    }


class FakeGitHub:
    def __init__(self) -> None:
        self.ruleset = live_ruleset()
        self.second_ruleset: dict[str, Any] | None = None
        self.ruleset_get_count = 0
        self.fail_path: str | None = None
        self.invalid_json_path: str | None = None
        self.compare_status = "ahead"
        self.canary_conclusion: str | None = "success"
        self.canary_check_name = "test"
        self.canary_workflow_path = ".github/workflows/ci.yml"
        self.canary_run_head_sha = CANARY_HEAD_SHA
        self.requests: list[dict[str, Any]] = []
        fixture = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: object) -> None:
                return

            def send_json(
                self,
                status: int,
                payload: object,
                headers: dict[str, str] | None = None,
            ) -> None:
                body = json.dumps(payload).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                for key, value in (headers or {}).items():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self) -> None:
                fixture.requests.append({"method": "GET", "path": self.path})
                if self.path == fixture.fail_path:
                    self.send_json(503, {"message": "unavailable"})
                    return
                if self.path == fixture.invalid_json_path:
                    body = b"not-json"
                    self.send_response(200)
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return
                if self.path == "/repos/agiletec-inc/github-actions":
                    self.send_json(200, {"id": 9001, "default_branch": "main"})
                elif (
                    self.path
                    == f"/repos/agiletec-inc/github-actions/commits/{PROPOSED_SHA}"
                ):
                    self.send_json(200, {"sha": PROPOSED_SHA})
                elif self.path == (
                    f"/repos/agiletec-inc/github-actions/compare/{PROPOSED_SHA}...main"
                ):
                    self.send_json(200, {"status": fixture.compare_status})
                elif self.path == "/repos/agiletec-inc/github-actions/pulls/321":
                    self.send_json(
                        200,
                        {
                            "state": "open",
                            "head": {"sha": CANARY_HEAD_SHA},
                            "base": {"ref": "main"},
                        },
                    )
                elif self.path == (
                    f"/repos/agiletec-inc/github-actions/commits/{CANARY_HEAD_SHA}/check-runs"
                    "?filter=latest&per_page=100"
                ):
                    self.send_json(
                        200,
                        {
                            "check_runs": [
                                {
                                    "name": fixture.canary_check_name,
                                    "status": "completed"
                                    if fixture.canary_conclusion is not None
                                    else "in_progress",
                                    "conclusion": fixture.canary_conclusion,
                                    "app": {"slug": "github-actions"},
                                    "details_url": "https://api.github.test/repos/agiletec-inc/github-actions/actions/runs/777",
                                }
                            ]
                        },
                    )
                elif self.path == "/repos/agiletec-inc/github-actions/actions/runs/777":
                    self.send_json(
                        200,
                        {
                            "id": 777,
                            "head_sha": fixture.canary_run_head_sha,
                            "path": fixture.canary_workflow_path,
                        },
                    )
                elif self.path == RULESET_PATH:
                    fixture.ruleset_get_count += 1
                    payload = fixture.ruleset
                    if (
                        fixture.ruleset_get_count == 2
                        and fixture.second_ruleset is not None
                    ):
                        payload = fixture.second_ruleset
                    self.send_json(200, payload)
                else:
                    self.send_json(404, {"message": "not found"})

            def do_PUT(self) -> None:
                length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(length)
                try:
                    payload: object = json.loads(body)
                except json.JSONDecodeError:
                    payload = body.decode(errors="replace")
                fixture.requests.append(
                    {
                        "method": "PUT",
                        "path": self.path,
                        "headers": dict(self.headers),
                        "body": payload,
                    }
                )
                if self.path != RULESET_PATH or not isinstance(payload, dict):
                    self.send_json(400, {"message": "invalid update"})
                    return
                readback = {
                    "id": 19456040,
                    "source_type": "Organization",
                    "source": "agiletec-inc",
                    **payload,
                }
                fixture.ruleset = readback
                self.send_json(200, readback)

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    @property
    def base_url(self) -> str:
        host, port = self.server.server_address
        return f"http://{host}:{port}"

    def __enter__(self) -> "FakeGitHub":
        self.thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()

    def puts(self) -> list[dict[str, Any]]:
        return [request for request in self.requests if request["method"] == "PUT"]


class RulesetWorkflowPinTests(unittest.TestCase):
    def run_update(
        self,
        api: FakeGitHub,
        *,
        dry_run: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(SCRIPT),
            "--proposed-sha",
            PROPOSED_SHA,
            "--canary-pr",
            "321",
            "--api-base-url",
            api.base_url,
        ]
        if dry_run:
            command.append("--dry-run")
        environment = os.environ.copy()
        environment["GH_TOKEN"] = "fixture-token-from-environment"
        return subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_updates_only_target_workflow_sha_and_preserves_ruleset(self) -> None:
        with FakeGitHub() as api:
            before = json.loads(json.dumps(api.ruleset))
            result = self.run_update(api)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(api.puts()), 1)
        update = api.puts()[0]
        self.assertEqual(update["path"], RULESET_PATH)
        expected = {
            key: before[key]
            for key in (
                "name",
                "target",
                "enforcement",
                "bypass_actors",
                "conditions",
                "rules",
            )
        }
        target = expected["rules"][2]["parameters"]["workflows"][0]
        target["sha"] = PROPOSED_SHA
        self.assertEqual(target["ref"], "refs/heads/main")
        self.assertEqual(update["body"], expected)
        ruleset_reads = [
            request
            for request in api.requests
            if request["method"] == "GET" and request["path"] == RULESET_PATH
        ]
        self.assertEqual(
            len(ruleset_reads), 3, "must read, recheck, PUT, then read back"
        )

    def test_dry_run_prints_plan_without_update(self) -> None:
        with FakeGitHub() as api:
            result = self.run_update(api, dry_run=True)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(api.puts(), [])
        self.assertIn(PROPOSED_SHA, result.stdout)
        self.assertIn("dry-run", result.stdout.lower())

    def test_rejects_sha_not_reachable_from_github_actions_main(self) -> None:
        with FakeGitHub() as api:
            api.compare_status = "diverged"
            result = self.run_update(api)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(api.puts(), [])

    def test_requires_successful_repository_native_test_on_canary_head(self) -> None:
        for conclusion in (None, "failure", "cancelled"):
            with self.subTest(conclusion=conclusion), FakeGitHub() as api:
                api.canary_conclusion = conclusion
                result = self.run_update(api)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(api.puts(), [])

    def test_canary_check_and_workflow_run_must_match_candidate(self) -> None:
        cases = (
            ("canary_check_name", "spoofed-check"),
            ("canary_workflow_path", ".github/workflows/spoof.yml"),
            ("canary_run_head_sha", "e" * 40),
        )
        for attribute, value in cases:
            with self.subTest(attribute=attribute), FakeGitHub() as api:
                setattr(api, attribute, value)
                result = self.run_update(api)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(api.puts(), [])

    def test_read_failure_or_invalid_response_fails_closed(self) -> None:
        cases = (
            (RULESET_PATH, None),
            (None, RULESET_PATH),
            (f"/repos/agiletec-inc/github-actions/commits/{PROPOSED_SHA}", None),
        )
        for fail_path, invalid_json_path in cases:
            with self.subTest(path=fail_path or invalid_json_path), FakeGitHub() as api:
                api.fail_path = fail_path
                api.invalid_json_path = invalid_json_path
                result = self.run_update(api)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(api.puts(), [])

    def test_second_read_state_change_prevents_write(self) -> None:
        with FakeGitHub() as api:
            changed = live_ruleset()
            changed["conditions"]["repository_name"]["exclude"].append("new-exclusion")
            api.second_ruleset = changed
            result = self.run_update(api)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(api.puts(), [])

    def test_second_read_current_sha_change_prevents_write(self) -> None:
        with FakeGitHub() as api:
            changed = live_ruleset()
            changed["rules"][2]["parameters"]["workflows"][0]["sha"] = "d" * 40
            api.second_ruleset = changed
            result = self.run_update(api)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(api.puts(), [])

    def test_credentials_are_runtime_only_not_cli_or_repository_secrets(self) -> None:
        self.assertTrue(SCRIPT.is_file(), f"missing implementation: {SCRIPT}")
        source = SCRIPT.read_text()
        self.assertNotIn("--token", source)
        self.assertNotRegex(source, r"gh[pousr]_[A-Za-z0-9_]{20,}")
        self.assertIn("GH_TOKEN", source)
        tracked = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True
        ).stdout.splitlines()
        self.assertFalse(any(Path(path).name == ".env" for path in tracked))


if __name__ == "__main__":
    unittest.main()
