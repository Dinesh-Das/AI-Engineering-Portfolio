# Reverse engineering: conversational-support-flow

## Problem and reconstructed mechanism

Route support turns among order lookup, policy retrieval and live research.

CrewAI conversational routing persists session context; order lookup is deterministic while policy and research use agents.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [order_db.py](order_db.py) | TrackingEvent, Order, OrderManagementAPI, latest_event, get_order | dataclasses, datetime, pathlib, sqlite3 |
| [support_flow.py](support_flow.py) | extract_order_id, SupportState, SupportFlow, handle_order_lookup, handle_return_policy, handle_research | crewai, crewai_tools, dotenv, logging, order_db, os, re, uuid |
| [frontend/app/api/copilotkit/route.ts](frontend/app/api/copilotkit/route.ts) | backend/configuration source; inspect directly | .ts |
| [frontend/app/chat.tsx](frontend/app/chat.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/app/globals.css](frontend/app/globals.css) | backend/configuration source; inspect directly | .css |
| [frontend/app/layout.tsx](frontend/app/layout.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/app/page.tsx](frontend/app/page.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/app/providers.tsx](frontend/app/providers.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/eslint.config.mjs](frontend/eslint.config.mjs) | backend/configuration source; inspect directly | .mjs |
| [frontend/next.config.ts](frontend/next.config.ts) | backend/configuration source; inspect directly | .ts |
| [frontend/postcss.config.mjs](frontend/postcss.config.mjs) | backend/configuration source; inspect directly | .mjs |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [order_db.py](order_db.py) | 26 | TrackingEvent | A tracking event for an order. |
| [order_db.py](order_db.py) | 35 | Order | An order. |
| [order_db.py](order_db.py) | 94 | OrderManagementAPI | Stand-in for a call to the internal order-management API. |
| [order_db.py](order_db.py) | 46 | latest_event | The latest tracking event for the order, or None if there are none yet. |
| [order_db.py](order_db.py) | 100 | get_order | FunctionDef |
| [support_flow.py](support_flow.py) | 50 | extract_order_id | Pull a known order id out of free text, e.g. "Where is order 4471?" -> "4471". |
| [support_flow.py](support_flow.py) | 63 | SupportState | Adds the two fields later turns resolve pronouns against. |
| [support_flow.py](support_flow.py) | 106 | SupportFlow | ClassDef |
| [support_flow.py](support_flow.py) | 113 | handle_order_lookup | Status, tracking, or delivery date for an order. |
| [support_flow.py](support_flow.py) | 159 | handle_return_policy | Returns, refunds, exchanges, and damaged item claims. |
| [support_flow.py](support_flow.py) | 209 | handle_research | Live carrier delays, weather disruptions, current external conditions. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `openrouter/openai/gpt-4o`
- `openrouter/openai/gpt-4o-mini`

Detected import roots: `ag_ui_crewai`, `crewai`, `crewai_tools`, `dataclasses`, `datetime`, `dotenv`, `fastapi`, `logging`, `order_db`, `os`, `pathlib`, `re`, `sqlite3`, `support_flow`, `uuid`

Retained dependency manifests: [pyproject.toml](pyproject.toml), [frontend/package.json](frontend/package.json)

Environment names detected from code/configuration:

- `CREWAI_BACKEND_URL`
- `EXA_API_KEY`
- `OPENROUTER_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [frontend/.gitignore](frontend/.gitignore) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/AGENTS.upstream.md](frontend/AGENTS.upstream.md) | Quarantined imported agent instructions as reference documentation. |
| [frontend/AGENTS.upstream.md](frontend/AGENTS.upstream.md) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/app/api/copilotkit/route.ts](frontend/app/api/copilotkit/route.ts) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/app/chat.tsx](frontend/app/chat.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/app/favicon.ico](frontend/app/favicon.ico) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/app/globals.css](frontend/app/globals.css) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/app/layout.tsx](frontend/app/layout.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/app/page.tsx](frontend/app/page.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/app/providers.tsx](frontend/app/providers.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/CLAUDE.upstream.md](frontend/CLAUDE.upstream.md) | Quarantined imported agent instructions as reference documentation. |
| [frontend/CLAUDE.upstream.md](frontend/CLAUDE.upstream.md) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/eslint.config.mjs](frontend/eslint.config.mjs) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/next.config.ts](frontend/next.config.ts) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/package-lock.json](frontend/package-lock.json) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/package.json](frontend/package.json) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/postcss.config.mjs](frontend/postcss.config.mjs) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/README.md](frontend/README.md) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/tsconfig.json](frontend/tsconfig.json) | Restored frontend source/asset after UI scope was authorized. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/conversational-support-flow); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
