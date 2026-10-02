# AI Agent Security Lab

A defensive learning portfolio by [Stefan / Keedz1Off](https://github.com/Keedz1Off): AI-agent trust boundaries, tool authorization, output handling and invariant testing.

**Working approach:** understand the failure mode, define an invariant, implement a control, and check it with regression tests and reproducible randomized inputs. Fuzzing is my intended main testing direction; this repository currently contains a small seeded policy fuzzer, not a coverage-guided fuzzing platform.

## Scope

The application lets a user select one synthetic document. An agent may propose a read, but only application-owned policy grants authority. Retrieved content and model output are untrusted data. This lab checks the downstream authorization boundary; it does not run an LLM or measure prompt-injection success.

Implemented controls:

- exact tool and argument schema;
- per-request document allowlist using opaque IDs;
- rejected and successful calls both consume a finite session budget;
- HTML text-node escaping and output length limits;
- deterministic regression tests plus 2,000 seeded randomized proposals.

No network, shell, filesystem access tools, credentials or live targets are involved. All records are synthetic. See [control walkthroughs](docs/CONTROLS.md) and the [testing methodology](docs/TESTING.md).

## Run

Python 3.11+; standard library only. No API key or package installation required.

```bash
python lab.py
python -m unittest discover -s tests -v
```

The demo prints an allowed synthetic report, rejects an out-of-scope document, and renders escaped text. The test suite should finish with `OK`.

## OWASP study map

This map is deliberately pinned to **OWASP Top 10 for LLM Applications 2025**, not a claim to track the newest edition. Category mapping is educational, not certification or complete coverage.

| 2025 category | Study/control focus | Repository status |
| --- | --- | --- |
| LLM01 Prompt Injection | Keep retrieved text separate from authority | Downstream policy tests only |
| LLM02 Sensitive Information Disclosure | Restrict records to user-selected scope | Synthetic record tests |
| LLM03 Supply Chain | Review dependencies and provenance | Study topic; standard-library runtime |
| LLM04 Data and Model Poisoning | Track dataset origin and changes | Study topic |
| LLM05 Improper Output Handling | Encode for the destination context | HTML text-node tests |
| LLM06 Excessive Agency | Minimize tools and permissions | Tool/schema tests |
| LLM07 System Prompt Leakage | Keep secrets out of prompts | Study topic |
| LLM08 Vector and Embedding Weaknesses | Enforce retrieval access controls | Study topic; no vector store |
| LLM09 Misinformation | Check claims against evidence | Study topic |
| LLM10 Unbounded Consumption | Bound work and output | Session/output tests |

Source: [OWASP 2025 category index](https://genai.owasp.org/llm-top-10/). The implementation and test coverage descriptions above refer to this repository's own code.

## Evidence and limitations

`lab.py` contains the controls; `tests/test_lab.py` contains the executable evidence. A passing test supports only the property it asserts. It does not prove an agent is secure or demonstrate a real vulnerability.

The trusted caller must authenticate the user and construct `Scope` from their permitted selection. The demo has no login, multi-tenant service, concurrent session storage, sandbox, or model. A production system also needs durable budgets, concurrency control, retrieval authorization, monitoring and independent review. HTML escaping here applies only to text nodes. Output-size checks occur after generation and do not cap model-provider costs.

This is an independent educational portfolio, not an official OWASP project, production audit, exploit collection or claim of discovered third-party vulnerabilities.
