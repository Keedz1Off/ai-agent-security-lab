# AI Agent Security Lab

Two small, reproducible labs for AI-agent trust boundaries. Each lab feeds the same **simulated model proposal** to an unsafe tool runner and to a guarded runner, so the difference comes from application-side authorization rather than a better prompt.

| Lab | Attacker-controlled surface | Unsafe result | Guarded result |
| --- | --- | --- | --- |
| Indirect prompt injection | Retrieved document text | Simulated `send_record` action runs without user permission | Tool action denied because the user's task is only `summarize` |
| Path traversal in a tool call | Model-proposed `read_file` path | File outside the allowed workspace is read | Resolved path must stay inside the workspace |

All data and destinations are synthetic. `send_record` only appends to an in-memory outbox; this repository makes **no network requests** and has no real secrets.

## Run

Python 3.11+; no dependencies or API key:

```bash
python lab.py
python -m unittest discover -s tests -v
```

`lab.py` prints the unsafe and guarded outcomes for both cases. The tests check that a valid read still works, the unsafe runner executes the malicious proposal, the guarded runner denies it, and a path escaping the workspace is rejected.

## How the example is structured

`simulate_model_proposal` is intentionally simple: it treats a `TOOL_CALL:` line in retrieved text as a model-emitted tool call. This **simulates a model following an injected instruction**; it is not a benchmark of any actual model's susceptibility. Both runners receive the same proposal.

The defense is `authorize_action`. It checks the **user's original task**, the specific tool, and the canonical file path. A retrieved page cannot grant tool permissions by saying it is a system message. Prompt wording and keyword filters alone are not the security boundary.

## Threat model and limits

The attacker controls retrieved text, not the user's original request or the policy. The examples cover unauthorized tool use and file access. They do not model browser sessions, real MCP servers, multi-step data exfiltration, symlink races, or a production sandbox. For real systems, also isolate execution, limit network and credentials, validate tool parameters, and require review for sensitive actions.

## References

- [OpenAI: Safety in building agents](https://developers.openai.com/api/docs/guides/agent-builder-safety) — untrusted inputs, structured data flow, tool approvals, and defense in depth.
- [OpenAI: MCP tools, risks and safety](https://developers.openai.com/api/docs/guides/tools-connectors-mcp#risks-and-safety) — prompt injection and approval for sensitive tool calls.
- [OpenAI: Sandbox security](https://developers.openai.com/api/docs/guides/agents-api/environments/security) — isolate agent code and restrict network and credentials.

This is an educational lab, not a claim of a vulnerability in OpenAI, GitHub, or another live service.
