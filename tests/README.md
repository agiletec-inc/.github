# Public required-gate contract tests

Run from the repository root without leaving bytecode artifacts:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

The tests parse the self-contained public ruleset workflow. They verify
capability-based Node, uv/Python, and Swift lanes, current immutable action and
runtime pins, read-only permissions, and the absence of relative reusable
workflow/action references that would resolve in the consumer repository. The
stable aggregate evaluates GitHub's structured `toJSON(needs)` shape
(`{"job": {"result": "success"}}`) and fails closed for every applicable lane.
