# Reverse engineering: open-agent-builder

## Problem and reconstructed mechanism

Study backend execution of AI workflows, MCP tools, guardrails and approval steps.

API routes and Convex data/functions implement the orchestration backend; the visual builder and UI routes are omitted.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app/api/approval/[approvalId]/resume/route.ts](app/api/approval/%5BapprovalId%5D/resume/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/approval/[approvalId]/route.ts](app/api/approval/%5BapprovalId%5D/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/approval/route.ts](app/api/approval/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/config/route.ts](app/api/config/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/execute-agent/route.ts](app/api/execute-agent/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/execute-extract/route.ts](app/api/execute-extract/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/execute-guardrails/route.ts](app/api/execute-guardrails/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/execute-mcp/route.ts](app/api/execute-mcp/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/mcp/registry/route.ts](app/api/mcp/registry/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/templates/seed/route.ts](app/api/templates/seed/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/templates/update/route.ts](app/api/templates/update/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/test-mcp-connection/route.ts](app/api/test-mcp-connection/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/workflow/execute/route.ts](app/api/workflow/execute/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/workflows/[workflowId]/execute/route.ts](app/api/workflows/%5BworkflowId%5D/execute/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/workflows/[workflowId]/execute-langgraph/route.ts](app/api/workflows/%5BworkflowId%5D/execute-langgraph/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/workflows/[workflowId]/execute-stream/route.ts](app/api/workflows/%5BworkflowId%5D/execute-stream/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/workflows/[workflowId]/export-code/route.ts](app/api/workflows/%5BworkflowId%5D/export-code/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/workflows/[workflowId]/export-langgraph/route.ts](app/api/workflows/%5BworkflowId%5D/export-langgraph/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/workflows/[workflowId]/resume/route.ts](app/api/workflows/%5BworkflowId%5D/resume/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/workflows/[workflowId]/route.ts](app/api/workflows/%5BworkflowId%5D/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/workflows/cleanup/route.ts](app/api/workflows/cleanup/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/workflows/import-langgraph/route.ts](app/api/workflows/import-langgraph/route.ts) | backend/configuration source; inspect directly | .ts |
| [app/api/workflows/route.ts](app/api/workflows/route.ts) | backend/configuration source; inspect directly | .ts |
| [atoms/sheets.ts](atoms/sheets.ts) | backend/configuration source; inspect directly | .ts |
| [convex/_generated/api.d.ts](convex/_generated/api.d.ts) | backend/configuration source; inspect directly | .ts |
| [convex/_generated/api.js](convex/_generated/api.js) | backend/configuration source; inspect directly | .js |
| [convex/_generated/dataModel.d.ts](convex/_generated/dataModel.d.ts) | backend/configuration source; inspect directly | .ts |
| [convex/_generated/server.d.ts](convex/_generated/server.d.ts) | backend/configuration source; inspect directly | .ts |
| [convex/_generated/server.js](convex/_generated/server.js) | backend/configuration source; inspect directly | .js |
| [convex/admin.ts](convex/admin.ts) | backend/configuration source; inspect directly | .ts |
| [convex/apiKeys.ts](convex/apiKeys.ts) | backend/configuration source; inspect directly | .ts |
| [convex/approvals.ts](convex/approvals.ts) | backend/configuration source; inspect directly | .ts |
| [convex/auth.config.ts](convex/auth.config.ts) | backend/configuration source; inspect directly | .ts |
| [convex/executions.ts](convex/executions.ts) | backend/configuration source; inspect directly | .ts |
| [convex/mcpServers.ts](convex/mcpServers.ts) | backend/configuration source; inspect directly | .ts |
| [convex/schema.ts](convex/schema.ts) | backend/configuration source; inspect directly | .ts |
| [convex/templates.ts](convex/templates.ts) | backend/configuration source; inspect directly | .ts |
| [convex/userLLMKeys.ts](convex/userLLMKeys.ts) | backend/configuration source; inspect directly | .ts |
| [convex/userMCPs.ts](convex/userMCPs.ts) | backend/configuration source; inspect directly | .ts |
| [convex/workflows.ts](convex/workflows.ts) | backend/configuration source; inspect directly | .ts |
| [lib/api/auth.ts](lib/api/auth.ts) | backend/configuration source; inspect directly | .ts |
| [lib/api/config.ts](lib/api/config.ts) | backend/configuration source; inspect directly | .ts |
| [lib/api/llm-keys.ts](lib/api/llm-keys.ts) | backend/configuration source; inspect directly | .ts |
| [lib/api/models.ts](lib/api/models.ts) | backend/configuration source; inspect directly | .ts |
| [lib/approval/approval-store.ts](lib/approval/approval-store.ts) | backend/configuration source; inspect directly | .ts |
| [lib/arcade/auth-store.ts](lib/arcade/auth-store.ts) | backend/configuration source; inspect directly | .ts |
| [lib/arcade/openai-tools.ts](lib/arcade/openai-tools.ts) | backend/configuration source; inspect directly | .ts |
| [lib/arcade/tools.ts](lib/arcade/tools.ts) | backend/configuration source; inspect directly | .ts |
| [lib/arcade/workflow-helpers.ts](lib/arcade/workflow-helpers.ts) | backend/configuration source; inspect directly | .ts |
| [lib/config/llm-config.ts](lib/config/llm-config.ts) | backend/configuration source; inspect directly | .ts |
| [lib/convex/client.ts](lib/convex/client.ts) | backend/configuration source; inspect directly | .ts |
| [lib/errors/index.ts](lib/errors/index.ts) | backend/configuration source; inspect directly | .ts |
| [lib/errors/WorkflowError.ts](lib/errors/WorkflowError.ts) | backend/configuration source; inspect directly | .ts |
| [lib/mcp/mcp-registry.ts](lib/mcp/mcp-registry.ts) | backend/configuration source; inspect directly | .ts |
| [lib/mcp/resolver.ts](lib/mcp/resolver.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/duplicate-detection.ts](lib/workflow/duplicate-detection.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/edge-cleanup.ts](lib/workflow/edge-cleanup.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/error-boundaries.ts](lib/workflow/error-boundaries.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/executors/agent.ts](lib/workflow/executors/agent.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/executors/arcade.ts](lib/workflow/executors/arcade.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/executors/data.ts](lib/workflow/executors/data.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/executors/extract.ts](lib/workflow/executors/extract.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/executors/http.ts](lib/workflow/executors/http.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/executors/logic.ts](lib/workflow/executors/logic.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/executors/mcp.ts](lib/workflow/executors/mcp.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/executors/tools.ts](lib/workflow/executors/tools.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/langgraph.ts](lib/workflow/langgraph.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/mcp-registry.ts](lib/workflow/mcp-registry.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/storage.ts](lib/workflow/storage.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/templates/examples/01-simple-agent.ts](lib/workflow/templates/examples/01-simple-agent.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/templates/examples/index.ts](lib/workflow/templates/examples/index.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/types.ts](lib/workflow/types.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/validation.ts](lib/workflow/validation.ts) | backend/configuration source; inspect directly | .ts |
| [lib/workflow/variable-substitution.ts](lib/workflow/variable-substitution.ts) | backend/configuration source; inspect directly | .ts |
| [next-env.d.ts](next-env.d.ts) | backend/configuration source; inspect directly | .ts |
| [next.config.js](next.config.js) | backend/configuration source; inspect directly | .js |
| [postcss.config.js](postcss.config.js) | backend/configuration source; inspect directly | .js |
| [proxy.ts](proxy.ts) | backend/configuration source; inspect directly | .ts |
| [tailwind.config.ts](tailwind.config.ts) | backend/configuration source; inspect directly | .ts |
| [utils/cn.ts](utils/cn.ts) | backend/configuration source; inspect directly | .ts |
| [utils/init-canvas.ts](utils/init-canvas.ts) | backend/configuration source; inspect directly | .ts |
| [utils/on-visible.ts](utils/on-visible.ts) | backend/configuration source; inspect directly | .ts |
| [utils/set-timeout-on-visible.ts](utils/set-timeout-on-visible.ts) | backend/configuration source; inspect directly | .ts |
| [utils/sleep.ts](utils/sleep.ts) | backend/configuration source; inspect directly | .ts |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

There are no non-UI Python function/class definitions to map. Inspect the configuration, TypeScript sources or integration guide above.

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: No Python import roots; inspect the backend/service configuration.

Retained dependency manifests: [package.json](package.json)

Environment names detected from code/configuration:

- `ABSOLUTE_MAX`
- `ANTHROPIC_API_KEY`
- `ARCADE_API_KEY`
- `E2B_API_KEY`
- `FIRECRAWL_API_KEY`
- `GROQ_API_KEY`
- `MAX_SCRIPT_LENGTH`
- `MOCK_AGENT_RESPONSE`
- `NEXT_PUBLIC_CONVEX_URL`
- `OPENAI_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/open-agent-builder); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
