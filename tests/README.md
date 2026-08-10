# Public required-gate contract tests

Run from the repository root without leaving bytecode artifacts:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

The tests parse the workflow and composite-action YAML structure. They verify
the public closure for its two current consumers: cmd-ime's Swift test and
release smoke, and airis-keeper's pnpm Node 20 baseline. The stable aggregate
evaluates GitHub's structured `toJSON(needs)` shape (`{"job": {"result":
"success"}}`); detector output alone determines the expected fixed lanes.
