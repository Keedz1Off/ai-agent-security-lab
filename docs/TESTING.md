# Testing and fuzzing methodology

## Current executable evidence

Run `python -m unittest discover -s tests -v`. Ten tests cover an allowed read, cross-record denial, tool/schema restrictions, output encoding and length boundaries, trusted budget validation, and exhaustion after successful or rejected attempts.

The randomized test generates 2,000 proposals with seed `20251001`. Its corpus includes wrong types, missing authority, unexpected fields, invalid tool names and both selected and unselected document IDs. Each case uses a fresh session so budget exhaustion cannot mask schema failures. The separate budget tests exercise state transitions.

The oracle is deliberately small: only the exact canonical read request may succeed. On denial, no action may be completed. The test requires both acceptance and rejection to occur so an implementation that blocks everything cannot pass.

This is bounded randomized policy testing. It is not coverage-guided fuzzing, real-model evaluation, a benchmark, or evidence of third-party exploitability.

## Next research steps

Extend defensive testing with generated multi-call sequences, independent access-control oracles, persisted seeds and minimized failing cases. Measure branch coverage before claiming broader coverage. If a property fails, record the seed and minimal input, expected invariant, actual result and regression test for the fix.

For model-integrated evaluation, keep policy assertions separate from answer-quality metrics and use synthetic data. Count whether unauthorized effects occurred, not whether the model produced a particular refusal phrase. Scope and authorization must remain application-owned throughout evaluation.

## Report template

- Control and scope
- Security invariant
- Code revision and environment
- Synthetic fixture and seed
- Expected and observed result
- Fix and regression test
- Limitations and remaining assumptions

Only report verified observations. Planned work and study topics are not completed findings.
