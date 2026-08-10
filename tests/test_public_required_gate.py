from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github/workflows"
WORKFLOW = WORKFLOWS / "org-quality-gate.yml"
ACTION = ROOT / ".github/actions/evaluate-required-gate/action.yml"
EVALUATOR = ROOT / ".github/scripts/evaluate_required_gate.mjs"


def read_yaml(path: Path) -> dict:
    """Use BaseLoader so GitHub's `on` remains a mapping key."""
    with path.open() as file:
        return yaml.load(file, Loader=yaml.BaseLoader)


def evaluate(detected: dict[str, bool], needs: dict[str, object]) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["DETECTED"] = json.dumps(detected)
    environment["NEEDS"] = json.dumps(needs)
    return subprocess.run(
        ["node", str(EVALUATOR)], cwd=ROOT, env=environment, capture_output=True, text=True, check=False
    )


class PublicRequiredWorkflowContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(WORKFLOW.is_file(), f"missing public workflow: {WORKFLOW}")
        self.workflow = read_yaml(WORKFLOW)
        self.jobs = self.workflow["jobs"]

    def test_required_entrypoint_supports_pull_request_and_merge_group(self) -> None:
        self.assertEqual(self.workflow["name"], "Organization quality gate")
        self.assertEqual(set(self.workflow["on"]), {"pull_request", "merge_group"})
        self.assertEqual(self.workflow["permissions"], {"contents": "read"})

    def test_cmd_ime_lane_preserves_active_swift_inputs(self) -> None:
        lane = self.jobs["cmd-ime-swift-ci"]
        self.assertEqual(lane["uses"], "./.github/workflows/swift-ci.yml")
        self.assertEqual(lane["needs"], "detect")
        self.assertEqual(lane["if"], "${{ needs.detect.outputs.cmd-ime-swift == 'true' }}")
        self.assertEqual(lane["with"], {
            "working-directory": "apps/cmd-ime-swift",
            "release-command": "CMDIME_BUILD_MODE=local bash scripts/package.sh",
        })

    def test_airis_keeper_lane_preserves_pnpm_node_20(self) -> None:
        lane = self.jobs["airis-keeper-node-ci"]
        self.assertEqual(lane["uses"], "./.github/workflows/node-pnpm-ci.yml")
        self.assertEqual(lane["needs"], "detect")
        self.assertEqual(lane["if"], "${{ needs.detect.outputs.airis-keeper-node == 'true' }}")
        self.assertEqual(lane["with"], {"node-version": "20", "package-manager": "pnpm"})

    def test_secret_scan_and_aggregate_are_wired_through_structured_needs(self) -> None:
        self.assertEqual(self.jobs["secret-scan"]["uses"], "./.github/workflows/secret-scan.yml")
        aggregate = self.jobs["quality-gate"]
        self.assertEqual(aggregate["name"], "quality-gate")
        self.assertEqual(aggregate["needs"], ["detect", "secret-scan", "cmd-ime-swift-ci", "airis-keeper-node-ci"])
        self.assertEqual(aggregate["if"], "${{ always() }}")
        evaluator = next(step for step in aggregate["steps"] if step.get("id") == "evaluate")
        self.assertEqual(evaluator["uses"], "./.github/actions/evaluate-required-gate")
        self.assertEqual(evaluator["with"]["needs"], "${{ toJSON(needs) }}")
        self.assertIn('"secret-scan": true', evaluator["with"]["detected"])
        self.assertIn('"cmd-ime-swift-ci": ${{ needs.detect.outputs.cmd-ime-swift == \'true\' }}', evaluator["with"]["detected"])
        self.assertIn('"airis-keeper-node-ci": ${{ needs.detect.outputs.airis-keeper-node == \'true\' }}', evaluator["with"]["detected"])

    def test_public_adapters_are_read_only_hosted_and_pinned(self) -> None:
        expected_runners = {"secret-scan.yml": "ubuntu-24.04", "swift-ci.yml": "macos-14", "node-pnpm-ci.yml": "ubuntu-24.04"}
        for name, runner in expected_runners.items():
            workflow = read_yaml(WORKFLOWS / name)
            self.assertEqual(workflow["permissions"], {"contents": "read"})
            job = workflow["jobs"]["scan" if name == "secret-scan.yml" else "ci"]
            self.assertEqual(job["runs-on"], runner)
            for step in job["steps"]:
                reference = step.get("uses")
                if reference:
                    owner_repository, revision = reference.rsplit("@", 1)
                    self.assertIn(owner_repository, {"actions/checkout", "actions/setup-node", "pnpm/action-setup"})
                    self.assertRegex(revision, r"^[0-9a-f]{40}$")

    def test_node_adapter_locks_node_20_and_gitleaks_is_not_caller_selectable(self) -> None:
        node = read_yaml(WORKFLOWS / "node-pnpm-ci.yml")
        self.assertEqual(node["on"]["workflow_call"]["inputs"]["node-version"]["default"], "20")
        job = node["jobs"]["ci"]
        self.assertNotIn("container", job)
        setup = next(step for step in job["steps"] if step.get("uses", "").startswith("actions/setup-node@"))
        self.assertEqual(setup["uses"], "actions/setup-node@a0853c24544627f65ddf259abe73b1d18a591444")
        self.assertEqual(setup["with"]["node-version"], "20.20.2")
        self.assertIn("REQUESTED_NODE_VERSION", next(step for step in job["steps"] if step.get("name") == "Validate supported Node major")["env"])
        pnpm = next(step for step in job["steps"] if step.get("uses", "").startswith("pnpm/action-setup@"))
        self.assertEqual(pnpm["uses"], "pnpm/action-setup@0977fd99725f1db4007ccb2928dbb4e90d06cc86")
        self.assertNotIn("ff378ebe6b225b0680b81c1ad4498ae0d1d3a5e3", pnpm["uses"])

        secret = read_yaml(WORKFLOWS / "secret-scan.yml")
        self.assertNotIn("inputs", secret["on"]["workflow_call"])
        scan = secret["jobs"]["scan"]
        gitleaks = next(step for step in scan["steps"] if step.get("name") == "Run gitleaks")
        self.assertEqual(gitleaks["env"]["GITLEAKS_VERSION"], "8.30.1")

    def test_node_adapter_fails_when_a_required_script_is_absent(self) -> None:
        node = read_yaml(WORKFLOWS / "node-pnpm-ci.yml")
        detection = next(step for step in node["jobs"]["ci"]["steps"] if step.get("name") == "Detect declared quality scripts")
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            (temporary / "package.json").write_text(json.dumps({"scripts": {"lint": "true", "test": "true"}}))
            output = temporary / "github-output"
            result = subprocess.run(
                ["bash", "-lc", detection["run"]],
                cwd=temporary,
                env={**os.environ, "GITHUB_OUTPUT": str(output)},
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required package scripts: typecheck, build", result.stderr)

    def test_evaluator_action_and_script_are_local_closure(self) -> None:
        self.assertTrue(ACTION.is_file())
        self.assertTrue(EVALUATOR.is_file())
        action = read_yaml(ACTION)
        self.assertEqual(action["runs"]["using"], "composite")
        self.assertEqual(action["runs"]["steps"][0]["run"], 'node "$GITHUB_ACTION_PATH/../../scripts/evaluate_required_gate.mjs"')


class RequiredGateFailClosedBehaviorTests(unittest.TestCase):
    detected = {"secret-scan": True, "cmd-ime-swift-ci": True, "airis-keeper-node-ci": False}

    def assert_failed(self, needs: dict[str, object]) -> None:
        result = evaluate(self.detected, needs)
        self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_missing_applicable_lane_fails_closed(self) -> None:
        self.assert_failed({"detect": {"result": "success"}, "secret-scan": {"result": "success"}})

    def test_failure_cancelled_and_skipped_applicable_lanes_fail_closed(self) -> None:
        for result in ("failure", "cancelled", "skipped"):
            with self.subTest(result=result):
                self.assert_failed({"detect": {"result": "success"}, "secret-scan": {"result": "success"}, "cmd-ime-swift-ci": {"result": result}})

    def test_failed_detector_or_nonapplicable_lane_fails_closed(self) -> None:
        self.assert_failed({"detect": {"result": "failure"}, "secret-scan": {"result": "success"}, "cmd-ime-swift-ci": {"result": "success"}})
        self.assert_failed({"detect": {"result": "success"}, "secret-scan": {"result": "success"}, "cmd-ime-swift-ci": {"result": "success"}, "airis-keeper-node-ci": {"result": "cancelled"}})

    def test_every_applicable_lane_success_is_green(self) -> None:
        result = evaluate(self.detected, {"detect": {"result": "success"}, "secret-scan": {"result": "success"}, "cmd-ime-swift-ci": {"result": "success"}, "airis-keeper-node-ci": {"result": "skipped"}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Quality gate passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
