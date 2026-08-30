from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github/workflows"
ENTRYPOINT = WORKFLOWS / "org-quality-gate.yml"
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def load(path: Path) -> dict:
    with path.open() as file:
        return yaml.load(file, Loader=yaml.BaseLoader)


def evaluate(detected: dict[str, bool], needs: dict[str, object]) -> subprocess.CompletedProcess[str]:
    aggregate = load(ENTRYPOINT)["jobs"]["quality-gate"]["steps"][0]["run"]
    script = aggregate.split("node <<'NODE'\n", 1)[1].rsplit("\nNODE", 1)[0]
    with tempfile.NamedTemporaryFile("w", suffix=".mjs") as temporary:
        temporary.write(script)
        temporary.flush()
        return subprocess.run(
            ["node", temporary.name],
            env={**os.environ, "DETECTED": json.dumps(detected), "NEEDS": json.dumps(needs)},
            text=True, capture_output=True, check=False,
        )


class PublicRequiredWorkflowContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = load(ENTRYPOINT)
        self.jobs = self.workflow["jobs"]

    def test_entrypoint_is_public_ruleset_compatible(self) -> None:
        self.assertEqual(self.workflow["name"], "Public organization quality gate")
        self.assertEqual(set(self.workflow["on"]), {"pull_request", "merge_group"})
        self.assertEqual(self.workflow["permissions"], {"contents": "read"})

    def test_detection_is_capability_based_not_repository_named(self) -> None:
        detect = self.jobs["detect"]
        self.assertEqual(set(detect["outputs"]), {"node", "python", "swift"})
        script = next(step for step in detect["steps"] if step.get("id") == "capabilities")["run"]
        self.assertIn("package.json", script)
        self.assertIn("uv.lock", script)
        self.assertIn("Package.swift", script)
        for repository in ("cmd-ime", "airis-keeper", "mindbase", "airis-mcp-gateway"):
            self.assertNotIn(repository, script)

    def test_detection_fixture_reports_each_supported_capability(self) -> None:
        script = next(
            step for step in self.jobs["detect"]["steps"] if step.get("id") == "capabilities"
        )["run"]
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "package.json").write_text("{}\n")
            (root / "api").mkdir()
            (root / "api/uv.lock").write_text("")
            (root / "mac").mkdir()
            (root / "mac/Package.swift").write_text("// fixture\n")
            output = root / "output"
            result = subprocess.run(
                ["bash", "-c", script], cwd=root,
                env={**os.environ, "GITHUB_OUTPUT": str(output)},
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                set(output.read_text().splitlines()), {"node=true", "python=true", "swift=true"}
            )

    def test_aggregate_matches_job_applicability_and_avoids_cancelled_runs(self) -> None:
        aggregate = self.jobs["quality-gate"]
        self.assertEqual(
            aggregate["needs"], ["detect", "secret-scan", "node-ci", "python-ci", "swift-ci"]
        )
        self.assertEqual(aggregate["if"], "${{ !cancelled() }}")
        detected = aggregate["steps"][-1]["env"]["DETECTED"]
        self.assertIn('"detect": true', detected)
        self.assertIn('"secret-scan": true', detected)
        for lane in ("node", "python", "swift"):
            self.assertEqual(
                self.jobs[f"{lane}-ci"]["if"],
                f"${{{{ needs.detect.outputs.{lane} == 'true' }}}}",
            )
            self.assertIn(
                f'"{lane}-ci": ${{{{ needs.detect.outputs.{lane} == \'true\' }}}}', detected
            )

    def test_external_actions_are_immutable_current_releases(self) -> None:
        expected = {
            "actions/checkout": "3d3c42e5aac5ba805825da76410c181273ba90b1",
            "actions/setup-node": "820762786026740c76f36085b0efc47a31fe5020",
            "actions/setup-python": "5fda3b95a4ea91299a34e894583c3862153e4b97",
            "astral-sh/setup-uv": "20cfd1bf945f4377ade1205e4dbc17946fc9a30d",
            "pnpm/action-setup": "0977fd99725f1db4007ccb2928dbb4e90d06cc86",
        }
        observed: dict[str, set[str]] = {}
        for path in WORKFLOWS.glob("*.yml"):
            for job in load(path).get("jobs", {}).values():
                for step in job.get("steps", []):
                    reference = step.get("uses", "")
                    if not reference or reference.startswith("./"):
                        continue
                    owner, revision = reference.rsplit("@", 1)
                    self.assertRegex(revision, FULL_SHA)
                    observed.setdefault(owner, set()).add(revision)
        for owner, revision in expected.items():
            self.assertEqual(observed.get(owner), {revision})

    def test_runtime_pins_are_current_and_lockfile_driven(self) -> None:
        source = ENTRYPOINT.read_text()
        self.assertIn("node-version: '24'", source)
        self.assertIn("pnpm-lock.yaml", source)
        self.assertIn("package-lock.json", source)
        self.assertIn("version: '0.12.7'", source)
        self.assertIn("GITLEAKS_VERSION: '8.30.1'", source)

    def test_cross_repository_workflow_has_no_relative_uses(self) -> None:
        source = ENTRYPOINT.read_text()
        self.assertNotRegex(source, r"(?m)^\s*uses:\s+\./")


class RequiredGateFailClosedBehaviorTests(unittest.TestCase):
    def test_all_applicable_lanes_must_succeed(self) -> None:
        detected = {"detect": True, "secret-scan": True, "node-ci": True,
                    "python-ci": False, "swift-ci": False}
        base = {"detect": {"result": "success"}, "secret-scan": {"result": "success"},
                "python-ci": {"result": "skipped"}, "swift-ci": {"result": "skipped"}}
        for state in ("missing", "skipped", "failure", "cancelled"):
            with self.subTest(state=state):
                needs = dict(base)
                if state != "missing":
                    needs["node-ci"] = {"result": state}
                result = evaluate(detected, needs)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("node-ci", result.stderr)
        green = evaluate(detected, {**base, "node-ci": {"result": "success"}})
        self.assertEqual(green.returncode, 0, green.stderr)


if __name__ == "__main__":
    unittest.main()
