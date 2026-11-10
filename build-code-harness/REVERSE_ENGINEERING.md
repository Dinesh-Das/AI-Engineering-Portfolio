# Reverse engineering: build-code-harness

## Problem and reconstructed mechanism

Study a coding-agent harness with planning, tools, checkpoints and approval.

The harness gives a model repository tools and a test runner; the bundled bank-account task is deliberately buggy learning material.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [code_harness.py](code_harness.py) | require_approval, run_tests | crewai, crewai_tools, dotenv, os |
| [workspace/account.py](workspace/account.py) | InsufficientFunds, BankAccount, deposit, withdraw, transfer |  |
| [workspace/tests/test_account.py](workspace/tests/test_account.py) | test_deposit_increases_balance, test_withdraw_decreases_balance, test_overdraft_is_blocked, test_transfer_moves_money_between_accounts, test_transfer_respects_overdraft | account, pytest |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [code_harness.py](code_harness.py) | 163 | require_approval | FunctionDef |
| [code_harness.py](code_harness.py) | 42 | run_tests | Run the pytest suite at the given path inside the sandbox and return the result. |
| [workspace/account.py](workspace/account.py) | 4 | InsufficientFunds | ClassDef |
| [workspace/account.py](workspace/account.py) | 8 | BankAccount | ClassDef |
| [workspace/account.py](workspace/account.py) | 14 | deposit | FunctionDef |
| [workspace/account.py](workspace/account.py) | 20 | withdraw | FunctionDef |
| [workspace/account.py](workspace/account.py) | 26 | transfer | FunctionDef |
| [workspace/tests/test_account.py](workspace/tests/test_account.py) | 5 | test_deposit_increases_balance | FunctionDef |
| [workspace/tests/test_account.py](workspace/tests/test_account.py) | 11 | test_withdraw_decreases_balance | FunctionDef |
| [workspace/tests/test_account.py](workspace/tests/test_account.py) | 17 | test_overdraft_is_blocked | FunctionDef |
| [workspace/tests/test_account.py](workspace/tests/test_account.py) | 24 | test_transfer_moves_money_between_accounts | FunctionDef |
| [workspace/tests/test_account.py](workspace/tests/test_account.py) | 32 | test_transfer_respects_overdraft | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `openrouter/openai/gpt-4o-mini`

Detected import roots: `account`, `crewai`, `crewai_tools`, `dotenv`, `os`, `pytest`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `E2B_API_KEY`
- `MODEL`
- `OPENAI_API_KEY`
- `OPENROUTER_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/build-code-harness); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
