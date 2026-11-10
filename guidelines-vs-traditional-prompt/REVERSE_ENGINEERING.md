# Reverse engineering: guidelines-vs-traditional-prompt

## Problem and reconstructed mechanism

Compare structured conversational guidelines with a traditional instruction prompt.

Parlant tool-backed policy guidance is compared with an ordinary OpenAI prompt over the same domain questions.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [demo_comparison.py](demo_comparison.py) | main | asyncio, os, parlant_client_utils, rich_table_formatter, traditional_llm_prompt |
| [parlant_agent_server.py](parlant_agent_server.py) | get_policy_types, calculate_coverage_recommendation, check_health_impact, get_premium_factors, explain_policy_riders, get_application_steps, get_agent_contact, main | asyncio, dotenv, os, parlant |
| [parlant_client_utils.py](parlant_client_utils.py) | create_client, create_session, send_user_message, await_ai_reply, get_session_reasoning | asyncio, os, parlant, typing |
| [rich_table_formatter.py](rich_table_formatter.py) | print_comparison_rich, format_query_text, format_traditional_text, format_parlant_text, format_reasoning_text | rich |
| [traditional_llm_prompt.py](traditional_llm_prompt.py) | call_traditional_llm | dotenv, openai, os |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [demo_comparison.py](demo_comparison.py) | 14 | main | Compare Traditional LLM vs Parlant agent responses. |
| [parlant_agent_server.py](parlant_agent_server.py) | 11 | get_policy_types | Retrieves comprehensive information about available life insurance policy types. |
| [parlant_agent_server.py](parlant_agent_server.py) | 31 | calculate_coverage_recommendation | Calculates personalized life insurance coverage recommendation. |
| [parlant_agent_server.py](parlant_agent_server.py) | 59 | check_health_impact | Analyzes how specific health conditions affect life insurance rates and underwriting. |
| [parlant_agent_server.py](parlant_agent_server.py) | 92 | get_premium_factors | Returns factors that affect life insurance premium pricing. |
| [parlant_agent_server.py](parlant_agent_server.py) | 107 | explain_policy_riders | Explains available policy riders and add-ons. |
| [parlant_agent_server.py](parlant_agent_server.py) | 121 | get_application_steps | Provides the step-by-step application process. |
| [parlant_agent_server.py](parlant_agent_server.py) | 137 | get_agent_contact | Provides comprehensive contact information for licensed insurance agents. |
| [parlant_agent_server.py](parlant_agent_server.py) | 152 | main | Initialize the Parlant life insurance agent with tools and guidelines. |
| [parlant_client_utils.py](parlant_client_utils.py) | 9 | create_client | Create a Parlant client connection. |
| [parlant_client_utils.py](parlant_client_utils.py) | 15 | create_session | Create a new Parlant session with retry logic. |
| [parlant_client_utils.py](parlant_client_utils.py) | 30 | send_user_message | Send a user message to the Parlant session. |
| [parlant_client_utils.py](parlant_client_utils.py) | 41 | await_ai_reply | Wait for and collect all AI agent messages from a Parlant session. |
| [parlant_client_utils.py](parlant_client_utils.py) | 78 | get_session_reasoning | Summarize which guidelines and tools the agent used for this session. |
| [rich_table_formatter.py](rich_table_formatter.py) | 6 | print_comparison_rich | Render a beautiful comparison table using Rich library. |
| [rich_table_formatter.py](rich_table_formatter.py) | 44 | format_query_text | Format query text - keep it concise and readable. |
| [rich_table_formatter.py](rich_table_formatter.py) | 63 | format_traditional_text | Format traditional LLM response - handle verbose content. |
| [rich_table_formatter.py](rich_table_formatter.py) | 96 | format_parlant_text | Format Parlant response - handle structured content. |
| [rich_table_formatter.py](rich_table_formatter.py) | 129 | format_reasoning_text | Format reasoning text - handle structured guidelines and tools. |
| [traditional_llm_prompt.py](traditional_llm_prompt.py) | 227 | call_traditional_llm | Call traditional LLM with the given query and prompt. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `gpt-4`

Detected import roots: `asyncio`, `dotenv`, `openai`, `os`, `parlant`, `parlant_client_utils`, `rich`, `rich_table_formatter`, `traditional_llm_prompt`, `typing`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `OPENAI_API_KEY`
- `PARLANT_BASE_URL`

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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/guidelines-vs-traditional-prompt); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
