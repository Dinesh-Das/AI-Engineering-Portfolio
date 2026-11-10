# Reverse engineering: open-agent-builder

## Problem and reconstructed mechanism

Study backend execution of AI workflows, MCP tools, guardrails and approval steps.

API routes and Convex data/functions implement the orchestration backend; restored visual-builder components and UI routes consume that orchestration state.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

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
| [app/layout.tsx](app/layout.tsx) | backend/configuration source; inspect directly | .tsx |
| [app/page.tsx](app/page.tsx) | backend/configuration source; inspect directly | .tsx |
| [app/sign-in/[[...sign-in]]/page.tsx](app/sign-in/%5B%5B...sign-in%5D%5D/page.tsx) | backend/configuration source; inspect directly | .tsx |
| [app/sign-up/[[...sign-up]]/page.tsx](app/sign-up/%5B%5B...sign-up%5D%5D/page.tsx) | backend/configuration source; inspect directly | .tsx |
| [app/workflows/[workflowId]/page.tsx](app/workflows/%5BworkflowId%5D/page.tsx) | backend/configuration source; inspect directly | .tsx |
| [app/workflows/[workflowId]/run/page.tsx](app/workflows/%5BworkflowId%5D/run/page.tsx) | backend/configuration source; inspect directly | .tsx |
| [app/workflows/page.tsx](app/workflows/page.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/endpoints/EndpointsCrawl/EndpointsCrawl.tsx](components/app/%28home%29/sections/endpoints/EndpointsCrawl/EndpointsCrawl.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/endpoints/EndpointsExtract/EndpointsExtract.tsx](components/app/%28home%29/sections/endpoints/EndpointsExtract/EndpointsExtract.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/endpoints/EndpointsMap/EndpointsMap.tsx](components/app/%28home%29/sections/endpoints/EndpointsMap/EndpointsMap.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/endpoints/EndpointsScrape/EndpointsScrape.tsx](components/app/%28home%29/sections/endpoints/EndpointsScrape/EndpointsScrape.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/endpoints/EndpointsSearch/EndpointsSearch.tsx](components/app/%28home%29/sections/endpoints/EndpointsSearch/EndpointsSearch.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/endpoints/Extract/Extract.tsx](components/app/%28home%29/sections/endpoints/Extract/Extract.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/endpoints/Mcp/Mcp.tsx](components/app/%28home%29/sections/endpoints/Mcp/Mcp.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero/Background/_svg/CenterStar.tsx](components/app/%28home%29/sections/hero/Background/_svg/CenterStar.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero/Background/Background.tsx](components/app/%28home%29/sections/hero/Background/Background.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero/Background/BackgroundOuterPiece.tsx](components/app/%28home%29/sections/hero/Background/BackgroundOuterPiece.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero/Badge/Badge.tsx](components/app/%28home%29/sections/hero/Badge/Badge.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero/Hero.tsx](components/app/%28home%29/sections/hero/Hero.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero/Pixi/Pixi.tsx](components/app/%28home%29/sections/hero/Pixi/Pixi.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero/Pixi/tickers/ascii.ts](components/app/%28home%29/sections/hero/Pixi/tickers/ascii.ts) | backend/configuration source; inspect directly | .ts |
| [components/app/(home)/sections/hero/Pixi/tickers/features/cell.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/cell.ts) | backend/configuration source; inspect directly | .ts |
| [components/app/(home)/sections/hero/Pixi/tickers/features/cellReveal.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/cellReveal.ts) | backend/configuration source; inspect directly | .ts |
| [components/app/(home)/sections/hero/Pixi/tickers/features/components/AnimatedRect.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/components/AnimatedRect.ts) | backend/configuration source; inspect directly | .ts |
| [components/app/(home)/sections/hero/Pixi/tickers/features/components/BlinkingContainer.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/components/BlinkingContainer.ts) | backend/configuration source; inspect directly | .ts |
| [components/app/(home)/sections/hero/Pixi/tickers/features/components/Dot.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/components/Dot.ts) | backend/configuration source; inspect directly | .ts |
| [components/app/(home)/sections/hero/Pixi/tickers/features/crawl.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/crawl.ts) | backend/configuration source; inspect directly | .ts |
| [components/app/(home)/sections/hero/Pixi/tickers/features/index.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/index.ts) | backend/configuration source; inspect directly | .ts |
| [components/app/(home)/sections/hero/Pixi/tickers/features/mapping.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/mapping.ts) | backend/configuration source; inspect directly | .ts |
| [components/app/(home)/sections/hero/Pixi/tickers/features/scrape.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/scrape.ts) | backend/configuration source; inspect directly | .ts |
| [components/app/(home)/sections/hero/Pixi/tickers/features/search.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/search.ts) | backend/configuration source; inspect directly | .ts |
| [components/app/(home)/sections/hero/Title/Title.tsx](components/app/%28home%29/sections/hero/Title/Title.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-flame/HeroFlame.tsx](components/app/%28home%29/sections/hero-flame/HeroFlame.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-input/_svg/ArrowRight.tsx](components/app/%28home%29/sections/hero-input/_svg/ArrowRight.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-input/_svg/Globe.tsx](components/app/%28home%29/sections/hero-input/_svg/Globe.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-input/Button/Button.tsx](components/app/%28home%29/sections/hero-input/Button/Button.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-input/HeroInput.tsx](components/app/%28home%29/sections/hero-input/HeroInput.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-input/Tabs/Mobile/Mobile.tsx](components/app/%28home%29/sections/hero-input/Tabs/Mobile/Mobile.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-input/Tabs/Tabs.tsx](components/app/%28home%29/sections/hero-input/Tabs/Tabs.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-scraping/_svg/BrowserMobile.tsx](components/app/%28home%29/sections/hero-scraping/_svg/BrowserMobile.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-scraping/_svg/BrowserTab.tsx](components/app/%28home%29/sections/hero-scraping/_svg/BrowserTab.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-scraping/Code/Code.tsx](components/app/%28home%29/sections/hero-scraping/Code/Code.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-scraping/Code/Loading/_svg/Check.tsx](components/app/%28home%29/sections/hero-scraping/Code/Loading/_svg/Check.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-scraping/Code/Loading/Loading.tsx](components/app/%28home%29/sections/hero-scraping/Code/Loading/Loading.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-scraping/HeroScraping.css](components/app/%28home%29/sections/hero-scraping/HeroScraping.css) | backend/configuration source; inspect directly | .css |
| [components/app/(home)/sections/hero-scraping/HeroScraping.tsx](components/app/%28home%29/sections/hero-scraping/HeroScraping.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/hero-scraping/Tag/Tag.tsx](components/app/%28home%29/sections/hero-scraping/Tag/Tag.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/step2/Step2Placeholder.tsx](components/app/%28home%29/sections/step2/Step2Placeholder.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/ConfirmDialog.tsx](components/app/%28home%29/sections/workflow-builder/ConfirmDialog.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/ConnectionMapperModal.tsx](components/app/%28home%29/sections/workflow-builder/ConnectionMapperModal.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/ConnectorsPanel.tsx](components/app/%28home%29/sections/workflow-builder/ConnectorsPanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/CustomNodes.tsx](components/app/%28home%29/sections/workflow-builder/CustomNodes.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/DataNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/DataNodePanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/EdgeLabelModal.tsx](components/app/%28home%29/sections/workflow-builder/EdgeLabelModal.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/ExecutionPanel.tsx](components/app/%28home%29/sections/workflow-builder/ExecutionPanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/ExportLangGraphButton.tsx](components/app/%28home%29/sections/workflow-builder/ExportLangGraphButton.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/ExtractNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/ExtractNodePanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/HTTPNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/HTTPNodePanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/LogicNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/LogicNodePanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/MCPPanel.tsx](components/app/%28home%29/sections/workflow-builder/MCPPanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/NodeArgumentsPanel.tsx](components/app/%28home%29/sections/workflow-builder/NodeArgumentsPanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/NodeIOBadges.tsx](components/app/%28home%29/sections/workflow-builder/NodeIOBadges.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/NodePanel.tsx](components/app/%28home%29/sections/workflow-builder/NodePanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/NoteNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/NoteNodePanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/OutputSchemaPanel.tsx](components/app/%28home%29/sections/workflow-builder/OutputSchemaPanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/PasteConfigModal.tsx](components/app/%28home%29/sections/workflow-builder/PasteConfigModal.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/PreviewPanel.tsx](components/app/%28home%29/sections/workflow-builder/PreviewPanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/PublishModal.tsx](components/app/%28home%29/sections/workflow-builder/PublishModal.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/SaveAsTemplateModal.tsx](components/app/%28home%29/sections/workflow-builder/SaveAsTemplateModal.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/SettingsPanelSimple.tsx](components/app/%28home%29/sections/workflow-builder/SettingsPanelSimple.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/ShareWorkflowModal.tsx](components/app/%28home%29/sections/workflow-builder/ShareWorkflowModal.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/StartNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/StartNodePanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/TestEndpointPanel.tsx](components/app/%28home%29/sections/workflow-builder/TestEndpointPanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/ToolsNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/ToolsNodePanel.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/UniversalOutputSelector.tsx](components/app/%28home%29/sections/workflow-builder/UniversalOutputSelector.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/VariableReferencePicker.tsx](components/app/%28home%29/sections/workflow-builder/VariableReferencePicker.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/WorkflowBuilder.tsx](components/app/%28home%29/sections/workflow-builder/WorkflowBuilder.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/app/(home)/sections/workflow-builder/WorkflowNameEditor.tsx](components/app/%28home%29/sections/workflow-builder/WorkflowNameEditor.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/FirecrawlIcon/FirecrawlIcon.tsx](components/FirecrawlIcon/FirecrawlIcon.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/hooks/use-dropdown-hover.ts](components/hooks/use-dropdown-hover.ts) | backend/configuration source; inspect directly | .ts |
| [components/providers/BigIntProvider.tsx](components/providers/BigIntProvider.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/animated-dot-icon.tsx](components/shared/animated-dot-icon.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/ascii-background.tsx](components/shared/ascii-background.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/ascii-flame-background.tsx](components/shared/ascii-flame-background.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/button/Button.css](components/shared/button/Button.css) | backend/configuration source; inspect directly | .css |
| [components/shared/button/Button.tsx](components/shared/button/Button.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/buttons/capsule-button.tsx](components/shared/buttons/capsule-button.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/buttons/fire-action-link.tsx](components/shared/buttons/fire-action-link.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/buttons/index.ts](components/shared/buttons/index.ts) | backend/configuration source; inspect directly | .ts |
| [components/shared/buttons/slate-button.tsx](components/shared/buttons/slate-button.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/color-styles/color-styles.tsx](components/shared/color-styles/color-styles.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/combobox/combobox.tsx](components/shared/combobox/combobox.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/effects/flame/ascii-explosion.tsx](components/shared/effects/flame/ascii-explosion.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/effects/flame/auth-pulse/auth-pulse.tsx](components/shared/effects/flame/auth-pulse/auth-pulse.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/effects/flame/core-flame.tsx](components/shared/effects/flame/core-flame.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/effects/flame/flame-background.tsx](components/shared/effects/flame/flame-background.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/effects/flame/Flame.tsx](components/shared/effects/flame/Flame.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/effects/flame/hero-flame-right.tsx](components/shared/effects/flame/hero-flame-right.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/effects/flame/hero-flame.tsx](components/shared/effects/flame/hero-flame.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/effects/flame/index.ts](components/shared/effects/flame/index.ts) | backend/configuration source; inspect directly | .ts |
| [components/shared/effects/flame/slate-grid/slate-grid.tsx](components/shared/effects/flame/slate-grid/slate-grid.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/effects/flame/subtle-explosion.tsx](components/shared/effects/flame/subtle-explosion.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/effects/flame/subtle-wave/subtle-wave.tsx](components/shared/effects/flame/subtle-wave/subtle-wave.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/effects/index.ts](components/shared/effects/index.ts) | backend/configuration source; inspect directly | .ts |
| [components/shared/effects/subtle-ascii-animation.tsx](components/shared/effects/subtle-ascii-animation.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/ErrorBoundary.tsx](components/shared/ErrorBoundary.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/firecrawl-icon/firecrawl-icon-static.tsx](components/shared/firecrawl-icon/firecrawl-icon-static.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/firecrawl-icon/firecrawl-icon.tsx](components/shared/firecrawl-icon/firecrawl-icon.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/flame-button.tsx](components/shared/flame-button.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/_svg/Logo.tsx](components/shared/header/_svg/Logo.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/BrandKit/_svg/Download.tsx](components/shared/header/BrandKit/_svg/Download.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/BrandKit/_svg/Guidelines.tsx](components/shared/header/BrandKit/_svg/Guidelines.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/BrandKit/_svg/Icon.tsx](components/shared/header/BrandKit/_svg/Icon.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/BrandKit/BrandKit.tsx](components/shared/header/BrandKit/BrandKit.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Dropdown/Content/Content.tsx](components/shared/header/Dropdown/Content/Content.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Dropdown/Content/NavItemRow.tsx](components/shared/header/Dropdown/Content/NavItemRow.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Dropdown/Github/Flame/Flame.tsx](components/shared/header/Dropdown/Github/Flame/Flame.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Dropdown/Github/Github.tsx](components/shared/header/Dropdown/Github/Github.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Dropdown/Mobile/Item/Item.tsx](components/shared/header/Dropdown/Mobile/Item/Item.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Dropdown/Mobile/Mobile.tsx](components/shared/header/Dropdown/Mobile/Mobile.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Dropdown/Stories/_svg/ArrowUp.tsx](components/shared/header/Dropdown/Stories/_svg/ArrowUp.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Dropdown/Stories/_svg/Replit.tsx](components/shared/header/Dropdown/Stories/_svg/Replit.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Dropdown/Stories/Flame/Flame.tsx](components/shared/header/Dropdown/Stories/Flame/Flame.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Dropdown/Stories/Stories.tsx](components/shared/header/Dropdown/Stories/Stories.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Dropdown/Wrapper/Wrapper.tsx](components/shared/header/Dropdown/Wrapper/Wrapper.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Github/_svg/GithubIcon.tsx](components/shared/header/Github/_svg/GithubIcon.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Github/GithubClient.tsx](components/shared/header/Github/GithubClient.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/HeaderContext.tsx](components/shared/header/HeaderContext.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/_svg/Affiliate.tsx](components/shared/header/Nav/_svg/Affiliate.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/_svg/Api.tsx](components/shared/header/Nav/_svg/Api.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/_svg/ArrowRight.tsx](components/shared/header/Nav/_svg/ArrowRight.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/_svg/Careers.tsx](components/shared/header/Nav/_svg/Careers.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/_svg/Changelog.tsx](components/shared/header/Nav/_svg/Changelog.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/_svg/Chats.tsx](components/shared/header/Nav/_svg/Chats.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/_svg/Lead.tsx](components/shared/header/Nav/_svg/Lead.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/_svg/MCP.tsx](components/shared/header/Nav/_svg/MCP.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/_svg/Platforms.tsx](components/shared/header/Nav/_svg/Platforms.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/_svg/Research.tsx](components/shared/header/Nav/_svg/Research.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/_svg/Student.tsx](components/shared/header/Nav/_svg/Student.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/_svg/Templates.tsx](components/shared/header/Nav/_svg/Templates.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/Item/_svg/ChevronDown.tsx](components/shared/header/Nav/Item/_svg/ChevronDown.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/Item/Item.tsx](components/shared/header/Nav/Item/Item.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/Nav.tsx](components/shared/header/Nav/Nav.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Nav/RenderEndpointIcon.tsx](components/shared/header/Nav/RenderEndpointIcon.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Toggle/Toggle.tsx](components/shared/header/Toggle/Toggle.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/header/Wrapper/Wrapper.tsx](components/shared/header/Wrapper/Wrapper.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/hero-flame.tsx](components/shared/hero-flame.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/animated-chevron.tsx](components/shared/icons/animated-chevron.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/animated-icons.tsx](components/shared/icons/animated-icons.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/arrow-animated.tsx](components/shared/icons/arrow-animated.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/check.tsx](components/shared/icons/check.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/chevron-slide.tsx](components/shared/icons/chevron-slide.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/copied.tsx](components/shared/icons/copied.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/copy.tsx](components/shared/icons/copy.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/curve.tsx](components/shared/icons/curve.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/fingerprint-icon.tsx](components/shared/icons/fingerprint-icon.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/GitHub.tsx](components/shared/icons/GitHub.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/Logo.tsx](components/shared/icons/Logo.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/openai.tsx](components/shared/icons/openai.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/source-icon.tsx](components/shared/icons/source-icon.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/symbol-colored.tsx](components/shared/icons/symbol-colored.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/symbol-white.tsx](components/shared/icons/symbol-white.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/tremor-placeholder.tsx](components/shared/icons/tremor-placeholder.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/wordmark-colored.tsx](components/shared/icons/wordmark-colored.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/icons/wordmark-white.tsx](components/shared/icons/wordmark-white.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/image/getImageSrc.ts](components/shared/image/getImageSrc.ts) | backend/configuration source; inspect directly | .ts |
| [components/shared/image/Image.tsx](components/shared/image/Image.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/layout/animated-height.tsx](components/shared/layout/animated-height.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/layout/animated-width.tsx](components/shared/layout/animated-width.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/layout/curvy-rect-divider.tsx](components/shared/layout/curvy-rect-divider.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/layout/curvy-rect.tsx](components/shared/layout/curvy-rect.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/loading/Shimmer.tsx](components/shared/loading/Shimmer.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/loading/usage-loading.tsx](components/shared/loading/usage-loading.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/lockBody.tsx](components/shared/lockBody.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/logo-cloud/index.ts](components/shared/logo-cloud/index.ts) | backend/configuration source; inspect directly | .ts |
| [components/shared/logo-cloud/logo-cloud.tsx](components/shared/logo-cloud/logo-cloud.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/logo-cloud/logo-cloud2/Logocloud.css](components/shared/logo-cloud/logo-cloud2/Logocloud.css) | backend/configuration source; inspect directly | .css |
| [components/shared/logo-cloud/logo-cloud2/Logocloud.tsx](components/shared/logo-cloud/logo-cloud2/Logocloud.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/macbook-scroll.tsx](components/shared/macbook-scroll.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/notifications/slack-notification.tsx](components/shared/notifications/slack-notification.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/pixi/Pixi.tsx](components/shared/pixi/Pixi.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/pixi/PixiAssetManager.ts](components/shared/pixi/PixiAssetManager.ts) | backend/configuration source; inspect directly | .ts |
| [components/shared/pixi/utils.ts](components/shared/pixi/utils.ts) | backend/configuration source; inspect directly | .ts |
| [components/shared/play-tabs.tsx](components/shared/play-tabs.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/Playground/Context/types.ts](components/shared/Playground/Context/types.ts) | backend/configuration source; inspect directly | .ts |
| [components/shared/portal-to-body/PortalToBody.tsx](components/shared/portal-to-body/PortalToBody.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/preview/json-error-highlighter.tsx](components/shared/preview/json-error-highlighter.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/preview/live-preview-frame.tsx](components/shared/preview/live-preview-frame.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/preview/multiple-web-browsers.tsx](components/shared/preview/multiple-web-browsers.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/preview/web-browser.tsx](components/shared/preview/web-browser.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/pylon.tsx](components/shared/pylon.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/search-params-provider/search-params-provider.tsx](components/shared/search-params-provider/search-params-provider.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/section-head/SectionHead.css](components/shared/section-head/SectionHead.css) | backend/configuration source; inspect directly | .css |
| [components/shared/section-head/SectionHead.tsx](components/shared/section-head/SectionHead.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/section-title/SectionTitle.tsx](components/shared/section-title/SectionTitle.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/tabs/Tabs.tsx](components/shared/tabs/Tabs.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/ui/app-dialog.tsx](components/shared/ui/app-dialog.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/ui/ascii-dot-loader.tsx](components/shared/ui/ascii-dot-loader.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/ui/dot-grid-loader.tsx](components/shared/ui/dot-grid-loader.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/ui/empty-state.tsx](components/shared/ui/empty-state.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/ui/index.ts](components/shared/ui/index.ts) | backend/configuration source; inspect directly | .ts |
| [components/shared/ui/loading-state.tsx](components/shared/ui/loading-state.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/ui/mobile-sheet.tsx](components/shared/ui/mobile-sheet.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/ui/stat-card.tsx](components/shared/ui/stat-card.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/shared/utils/portal-to-body.tsx](components/shared/utils/portal-to-body.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/button-demo.tsx](components/ui/button-demo.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/button.tsx](components/ui/button.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/code.tsx](components/ui/code.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/image.tsx](components/ui/image.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/index.ts](components/ui/index.ts) | backend/configuration source; inspect directly | .ts |
| [components/ui/loading-dashboard.tsx](components/ui/loading-dashboard.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/LoadingDots/index.ts](components/ui/LoadingDots/index.ts) | backend/configuration source; inspect directly | .ts |
| [components/ui/LoadingDots/LoadingDots.module.css](components/ui/LoadingDots/LoadingDots.module.css) | backend/configuration source; inspect directly | .css |
| [components/ui/LoadingDots/LoadingDots.tsx](components/ui/LoadingDots/LoadingDots.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/magic/animated-shiny-text-lw.tsx](components/ui/magic/animated-shiny-text-lw.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/magic/animated-shiny-text.tsx](components/ui/magic/animated-shiny-text.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/magic/dock.tsx](components/ui/magic/dock.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/magic/dot-pattern.tsx](components/ui/magic/dot-pattern.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/magic/gradual-spacing.tsx](components/ui/magic/gradual-spacing.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/magic/ripple.tsx](components/ui/magic/ripple.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/menu-header.tsx](components/ui/menu-header.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/menu.tsx](components/ui/menu.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/modal.tsx](components/ui/modal.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/motion/scramble-text.tsx](components/ui/motion/scramble-text.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/motion/text-reveal.tsx](components/ui/motion/text-reveal.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/scrollbar.tsx](components/ui/scrollbar.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/accordion.tsx](components/ui/shadcn/accordion.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/alert-dialog.tsx](components/ui/shadcn/alert-dialog.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/badge.tsx](components/ui/shadcn/badge.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/button.css](components/ui/shadcn/button.css) | backend/configuration source; inspect directly | .css |
| [components/ui/shadcn/button.tsx](components/ui/shadcn/button.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/card.tsx](components/ui/shadcn/card.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/checkbox.tsx](components/ui/shadcn/checkbox.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/collapsible.tsx](components/ui/shadcn/collapsible.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/combobox.tsx](components/ui/shadcn/combobox.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/context-menu.tsx](components/ui/shadcn/context-menu.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/data-table.tsx](components/ui/shadcn/data-table.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/dialog.tsx](components/ui/shadcn/dialog.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/dropdown-menu.tsx](components/ui/shadcn/dropdown-menu.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/form.tsx](components/ui/shadcn/form.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/input.tsx](components/ui/shadcn/input.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/label.tsx](components/ui/shadcn/label.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/navigation-menu.tsx](components/ui/shadcn/navigation-menu.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/popover.tsx](components/ui/shadcn/popover.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/progress.tsx](components/ui/shadcn/progress.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/scroll-area.tsx](components/ui/shadcn/scroll-area.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/select.tsx](components/ui/shadcn/select.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/separator.tsx](components/ui/shadcn/separator.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/sheet.tsx](components/ui/shadcn/sheet.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/slider.tsx](components/ui/shadcn/slider.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/switch.tsx](components/ui/shadcn/switch.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/tabs.tsx](components/ui/shadcn/tabs.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/textarea.tsx](components/ui/shadcn/textarea.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/toast.tsx](components/ui/shadcn/toast.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/toggle.tsx](components/ui/shadcn/toggle.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/tooltip-radix.tsx](components/ui/shadcn/tooltip-radix.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/shadcn/tooltip.tsx](components/ui/shadcn/tooltip.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/spinner.tsx](components/ui/spinner.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/table.tsx](components/ui/table.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/ui/video.tsx](components/ui/video.tsx) | backend/configuration source; inspect directly | .tsx |
| [components/workflow/WorkflowExecutionRenderer.tsx](components/workflow/WorkflowExecutionRenderer.tsx) | backend/configuration source; inspect directly | .tsx |
| [hooks/useApprovalWatch.ts](hooks/useApprovalWatch.ts) | backend/configuration source; inspect directly | .ts |
| [hooks/useDebouncedEffect.ts](hooks/useDebouncedEffect.ts) | backend/configuration source; inspect directly | .ts |
| [hooks/useWorkflow.ts](hooks/useWorkflow.ts) | backend/configuration source; inspect directly | .ts |
| [hooks/useWorkflowExecution.ts](hooks/useWorkflowExecution.ts) | backend/configuration source; inspect directly | .ts |
| [styles/additional-styles/custom-fonts.css](styles/additional-styles/custom-fonts.css) | backend/configuration source; inspect directly | .css |
| [styles/additional-styles/theme.css](styles/additional-styles/theme.css) | backend/configuration source; inspect directly | .css |
| [styles/additional-styles/utility-patterns.css](styles/additional-styles/utility-patterns.css) | backend/configuration source; inspect directly | .css |
| [styles/chrome-bug.css](styles/chrome-bug.css) | backend/configuration source; inspect directly | .css |
| [styles/components/button.css](styles/components/button.css) | backend/configuration source; inspect directly | .css |
| [styles/components/code.css](styles/components/code.css) | backend/configuration source; inspect directly | .css |
| [styles/components/index.css](styles/components/index.css) | backend/configuration source; inspect directly | .css |
| [styles/design-system/animations.css](styles/design-system/animations.css) | backend/configuration source; inspect directly | .css |
| [styles/design-system/base/body.css](styles/design-system/base/body.css) | backend/configuration source; inspect directly | .css |
| [styles/design-system/base/layout.css](styles/design-system/base/layout.css) | backend/configuration source; inspect directly | .css |
| [styles/design-system/base/reset.css](styles/design-system/base/reset.css) | backend/configuration source; inspect directly | .css |
| [styles/design-system/colors.css](styles/design-system/colors.css) | backend/configuration source; inspect directly | .css |
| [styles/design-system/fonts.css](styles/design-system/fonts.css) | backend/configuration source; inspect directly | .css |
| [styles/design-system/typography.css](styles/design-system/typography.css) | backend/configuration source; inspect directly | .css |
| [styles/design-system/utilities.css](styles/design-system/utilities.css) | backend/configuration source; inspect directly | .css |
| [styles/fire.css](styles/fire.css) | backend/configuration source; inspect directly | .css |
| [styles/main.css](styles/main.css) | backend/configuration source; inspect directly | .css |
| [styles/workflow-execution.css](styles/workflow-execution.css) | backend/configuration source; inspect directly | .css |

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
- `BASE_SRC`
- `E2B_API_KEY`
- `ENV_VAR`
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
| [app/layout.tsx](app/layout.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [app/page.tsx](app/page.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [app/sign-in/[[...sign-in]]/page.tsx](app/sign-in/%5B%5B...sign-in%5D%5D/page.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [app/sign-up/[[...sign-up]]/page.tsx](app/sign-up/%5B%5B...sign-up%5D%5D/page.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [app/workflows/[workflowId]/page.tsx](app/workflows/%5BworkflowId%5D/page.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [app/workflows/[workflowId]/run/page.tsx](app/workflows/%5BworkflowId%5D/run/page.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [app/workflows/page.tsx](app/workflows/page.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/endpoints/EndpointsCrawl/EndpointsCrawl.tsx](components/app/%28home%29/sections/endpoints/EndpointsCrawl/EndpointsCrawl.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/endpoints/EndpointsExtract/EndpointsExtract.tsx](components/app/%28home%29/sections/endpoints/EndpointsExtract/EndpointsExtract.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/endpoints/EndpointsMap/EndpointsMap.tsx](components/app/%28home%29/sections/endpoints/EndpointsMap/EndpointsMap.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/endpoints/EndpointsScrape/EndpointsScrape.tsx](components/app/%28home%29/sections/endpoints/EndpointsScrape/EndpointsScrape.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/endpoints/EndpointsSearch/EndpointsSearch.tsx](components/app/%28home%29/sections/endpoints/EndpointsSearch/EndpointsSearch.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/endpoints/Extract/Extract.tsx](components/app/%28home%29/sections/endpoints/Extract/Extract.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/endpoints/Mcp/Mcp.tsx](components/app/%28home%29/sections/endpoints/Mcp/Mcp.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Background/_svg/CenterStar.tsx](components/app/%28home%29/sections/hero/Background/_svg/CenterStar.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Background/Background.tsx](components/app/%28home%29/sections/hero/Background/Background.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Background/BackgroundOuterPiece.tsx](components/app/%28home%29/sections/hero/Background/BackgroundOuterPiece.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Badge/Badge.tsx](components/app/%28home%29/sections/hero/Badge/Badge.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Hero.tsx](components/app/%28home%29/sections/hero/Hero.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Pixi/Pixi.tsx](components/app/%28home%29/sections/hero/Pixi/Pixi.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Pixi/tickers/ascii.ts](components/app/%28home%29/sections/hero/Pixi/tickers/ascii.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Pixi/tickers/features/cell.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/cell.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Pixi/tickers/features/cellReveal.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/cellReveal.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Pixi/tickers/features/components/AnimatedRect.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/components/AnimatedRect.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Pixi/tickers/features/components/BlinkingContainer.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/components/BlinkingContainer.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Pixi/tickers/features/components/Dot.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/components/Dot.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Pixi/tickers/features/crawl.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/crawl.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Pixi/tickers/features/index.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/index.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Pixi/tickers/features/mapping.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/mapping.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Pixi/tickers/features/scrape.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/scrape.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Pixi/tickers/features/search.ts](components/app/%28home%29/sections/hero/Pixi/tickers/features/search.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero/Title/Title.tsx](components/app/%28home%29/sections/hero/Title/Title.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-flame/data.json](components/app/%28home%29/sections/hero-flame/data.json) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-flame/HeroFlame.tsx](components/app/%28home%29/sections/hero-flame/HeroFlame.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-input/_svg/ArrowRight.tsx](components/app/%28home%29/sections/hero-input/_svg/ArrowRight.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-input/_svg/Globe.tsx](components/app/%28home%29/sections/hero-input/_svg/Globe.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-input/Button/Button.tsx](components/app/%28home%29/sections/hero-input/Button/Button.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-input/HeroInput.tsx](components/app/%28home%29/sections/hero-input/HeroInput.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-input/Tabs/Mobile/Mobile.tsx](components/app/%28home%29/sections/hero-input/Tabs/Mobile/Mobile.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-input/Tabs/Tabs.tsx](components/app/%28home%29/sections/hero-input/Tabs/Tabs.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-scraping/_svg/BrowserMobile.tsx](components/app/%28home%29/sections/hero-scraping/_svg/BrowserMobile.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-scraping/_svg/BrowserTab.tsx](components/app/%28home%29/sections/hero-scraping/_svg/BrowserTab.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-scraping/Code/Code.tsx](components/app/%28home%29/sections/hero-scraping/Code/Code.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-scraping/Code/Loading/_svg/Check.tsx](components/app/%28home%29/sections/hero-scraping/Code/Loading/_svg/Check.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-scraping/Code/Loading/Loading.tsx](components/app/%28home%29/sections/hero-scraping/Code/Loading/Loading.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-scraping/HeroScraping.css](components/app/%28home%29/sections/hero-scraping/HeroScraping.css) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-scraping/HeroScraping.tsx](components/app/%28home%29/sections/hero-scraping/HeroScraping.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/hero-scraping/Tag/Tag.tsx](components/app/%28home%29/sections/hero-scraping/Tag/Tag.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/step2/Step2Placeholder.tsx](components/app/%28home%29/sections/step2/Step2Placeholder.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/ConfirmDialog.tsx](components/app/%28home%29/sections/workflow-builder/ConfirmDialog.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/ConnectionMapperModal.tsx](components/app/%28home%29/sections/workflow-builder/ConnectionMapperModal.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/ConnectorsPanel.tsx](components/app/%28home%29/sections/workflow-builder/ConnectorsPanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/CustomNodes.tsx](components/app/%28home%29/sections/workflow-builder/CustomNodes.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/DataNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/DataNodePanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/EdgeLabelModal.tsx](components/app/%28home%29/sections/workflow-builder/EdgeLabelModal.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/ExecutionPanel.tsx](components/app/%28home%29/sections/workflow-builder/ExecutionPanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/ExportLangGraphButton.tsx](components/app/%28home%29/sections/workflow-builder/ExportLangGraphButton.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/ExtractNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/ExtractNodePanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/HTTPNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/HTTPNodePanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/LogicNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/LogicNodePanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/MCPPanel.tsx](components/app/%28home%29/sections/workflow-builder/MCPPanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/NodeArgumentsPanel.tsx](components/app/%28home%29/sections/workflow-builder/NodeArgumentsPanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/NodeIOBadges.tsx](components/app/%28home%29/sections/workflow-builder/NodeIOBadges.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/NodePanel.tsx](components/app/%28home%29/sections/workflow-builder/NodePanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/NoteNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/NoteNodePanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/OutputSchemaPanel.tsx](components/app/%28home%29/sections/workflow-builder/OutputSchemaPanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/PasteConfigModal.tsx](components/app/%28home%29/sections/workflow-builder/PasteConfigModal.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/PreviewPanel.tsx](components/app/%28home%29/sections/workflow-builder/PreviewPanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/PublishModal.tsx](components/app/%28home%29/sections/workflow-builder/PublishModal.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/SaveAsTemplateModal.tsx](components/app/%28home%29/sections/workflow-builder/SaveAsTemplateModal.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/SettingsPanelSimple.tsx](components/app/%28home%29/sections/workflow-builder/SettingsPanelSimple.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/ShareWorkflowModal.tsx](components/app/%28home%29/sections/workflow-builder/ShareWorkflowModal.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/StartNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/StartNodePanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/TestEndpointPanel.tsx](components/app/%28home%29/sections/workflow-builder/TestEndpointPanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/ToolsNodePanel.tsx](components/app/%28home%29/sections/workflow-builder/ToolsNodePanel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/UniversalOutputSelector.tsx](components/app/%28home%29/sections/workflow-builder/UniversalOutputSelector.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/VariableReferencePicker.tsx](components/app/%28home%29/sections/workflow-builder/VariableReferencePicker.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/WorkflowBuilder.tsx](components/app/%28home%29/sections/workflow-builder/WorkflowBuilder.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/app/(home)/sections/workflow-builder/WorkflowNameEditor.tsx](components/app/%28home%29/sections/workflow-builder/WorkflowNameEditor.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/FirecrawlIcon/FirecrawlIcon.tsx](components/FirecrawlIcon/FirecrawlIcon.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/hooks/use-dropdown-hover.ts](components/hooks/use-dropdown-hover.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/providers/BigIntProvider.tsx](components/providers/BigIntProvider.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/animated-dot-icon.tsx](components/shared/animated-dot-icon.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/ascii-background.tsx](components/shared/ascii-background.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/ascii-flame-background.tsx](components/shared/ascii-flame-background.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/button/Button.css](components/shared/button/Button.css) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/button/Button.tsx](components/shared/button/Button.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/buttons/capsule-button.tsx](components/shared/buttons/capsule-button.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/buttons/fire-action-link.tsx](components/shared/buttons/fire-action-link.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/buttons/index.ts](components/shared/buttons/index.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/buttons/slate-button.tsx](components/shared/buttons/slate-button.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/color-styles/color-styles.tsx](components/shared/color-styles/color-styles.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/combobox/combobox.tsx](components/shared/combobox/combobox.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/ascii-explosion.tsx](components/shared/effects/flame/ascii-explosion.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/auth-pulse/auth-pulse.tsx](components/shared/effects/flame/auth-pulse/auth-pulse.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/auth-pulse/pulse-data.json](components/shared/effects/flame/auth-pulse/pulse-data.json) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/core-flame.json](components/shared/effects/flame/core-flame.json) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/core-flame.tsx](components/shared/effects/flame/core-flame.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/explosion-data.json](components/shared/effects/flame/explosion-data.json) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/flame-background.tsx](components/shared/effects/flame/flame-background.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/Flame.tsx](components/shared/effects/flame/Flame.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/hero-flame-data.json](components/shared/effects/flame/hero-flame-data.json) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/hero-flame-right.tsx](components/shared/effects/flame/hero-flame-right.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/hero-flame.tsx](components/shared/effects/flame/hero-flame.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/index.ts](components/shared/effects/flame/index.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/slate-grid/grid-data.json](components/shared/effects/flame/slate-grid/grid-data.json) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/slate-grid/slate-grid.tsx](components/shared/effects/flame/slate-grid/slate-grid.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/subtle-explosion.tsx](components/shared/effects/flame/subtle-explosion.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/subtle-wave/subtle-wave.tsx](components/shared/effects/flame/subtle-wave/subtle-wave.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/flame/subtle-wave/wave-data.json](components/shared/effects/flame/subtle-wave/wave-data.json) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/index.ts](components/shared/effects/index.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/effects/subtle-ascii-animation.tsx](components/shared/effects/subtle-ascii-animation.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/ErrorBoundary.tsx](components/shared/ErrorBoundary.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/firecrawl-icon/firecrawl-icon-static.tsx](components/shared/firecrawl-icon/firecrawl-icon-static.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/firecrawl-icon/firecrawl-icon.tsx](components/shared/firecrawl-icon/firecrawl-icon.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/flame-button.tsx](components/shared/flame-button.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/_svg/Logo.tsx](components/shared/header/_svg/Logo.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/BrandKit/_svg/Download.tsx](components/shared/header/BrandKit/_svg/Download.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/BrandKit/_svg/Guidelines.tsx](components/shared/header/BrandKit/_svg/Guidelines.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/BrandKit/_svg/Icon.tsx](components/shared/header/BrandKit/_svg/Icon.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/BrandKit/BrandKit.tsx](components/shared/header/BrandKit/BrandKit.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Dropdown/Content/Content.tsx](components/shared/header/Dropdown/Content/Content.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Dropdown/Content/NavItemRow.tsx](components/shared/header/Dropdown/Content/NavItemRow.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Dropdown/Github/Flame/data.json](components/shared/header/Dropdown/Github/Flame/data.json) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Dropdown/Github/Flame/Flame.tsx](components/shared/header/Dropdown/Github/Flame/Flame.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Dropdown/Github/Github.tsx](components/shared/header/Dropdown/Github/Github.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Dropdown/Mobile/Item/Item.tsx](components/shared/header/Dropdown/Mobile/Item/Item.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Dropdown/Mobile/Mobile.tsx](components/shared/header/Dropdown/Mobile/Mobile.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Dropdown/Stories/_svg/ArrowUp.tsx](components/shared/header/Dropdown/Stories/_svg/ArrowUp.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Dropdown/Stories/_svg/Replit.tsx](components/shared/header/Dropdown/Stories/_svg/Replit.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Dropdown/Stories/Flame/Flame.tsx](components/shared/header/Dropdown/Stories/Flame/Flame.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Dropdown/Stories/Stories.tsx](components/shared/header/Dropdown/Stories/Stories.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Dropdown/Wrapper/Wrapper.tsx](components/shared/header/Dropdown/Wrapper/Wrapper.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Github/_svg/GithubIcon.tsx](components/shared/header/Github/_svg/GithubIcon.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Github/GithubClient.tsx](components/shared/header/Github/GithubClient.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/HeaderContext.tsx](components/shared/header/HeaderContext.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/_svg/Affiliate.tsx](components/shared/header/Nav/_svg/Affiliate.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/_svg/Api.tsx](components/shared/header/Nav/_svg/Api.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/_svg/ArrowRight.tsx](components/shared/header/Nav/_svg/ArrowRight.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/_svg/Careers.tsx](components/shared/header/Nav/_svg/Careers.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/_svg/Changelog.tsx](components/shared/header/Nav/_svg/Changelog.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/_svg/Chats.tsx](components/shared/header/Nav/_svg/Chats.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/_svg/Lead.tsx](components/shared/header/Nav/_svg/Lead.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/_svg/MCP.tsx](components/shared/header/Nav/_svg/MCP.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/_svg/Platforms.tsx](components/shared/header/Nav/_svg/Platforms.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/_svg/Research.tsx](components/shared/header/Nav/_svg/Research.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/_svg/Student.tsx](components/shared/header/Nav/_svg/Student.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/_svg/Templates.tsx](components/shared/header/Nav/_svg/Templates.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/Item/_svg/ChevronDown.tsx](components/shared/header/Nav/Item/_svg/ChevronDown.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/Item/Item.tsx](components/shared/header/Nav/Item/Item.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/Nav.tsx](components/shared/header/Nav/Nav.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Nav/RenderEndpointIcon.tsx](components/shared/header/Nav/RenderEndpointIcon.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Toggle/Toggle.tsx](components/shared/header/Toggle/Toggle.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/header/Wrapper/Wrapper.tsx](components/shared/header/Wrapper/Wrapper.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/hero-flame.tsx](components/shared/hero-flame.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/animated-chevron.tsx](components/shared/icons/animated-chevron.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/animated-icons.tsx](components/shared/icons/animated-icons.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/arrow-animated.tsx](components/shared/icons/arrow-animated.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/check.tsx](components/shared/icons/check.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/chevron-slide.tsx](components/shared/icons/chevron-slide.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/copied.tsx](components/shared/icons/copied.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/copy.tsx](components/shared/icons/copy.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/curve.tsx](components/shared/icons/curve.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/fingerprint-icon.tsx](components/shared/icons/fingerprint-icon.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/GitHub.tsx](components/shared/icons/GitHub.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/Logo.tsx](components/shared/icons/Logo.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/openai.tsx](components/shared/icons/openai.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/source-icon.tsx](components/shared/icons/source-icon.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/symbol-colored.tsx](components/shared/icons/symbol-colored.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/symbol-white.tsx](components/shared/icons/symbol-white.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/tremor-placeholder.tsx](components/shared/icons/tremor-placeholder.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/wordmark-colored.tsx](components/shared/icons/wordmark-colored.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/icons/wordmark-white.tsx](components/shared/icons/wordmark-white.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/image/getImageSrc.ts](components/shared/image/getImageSrc.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/image/Image.tsx](components/shared/image/Image.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/layout/animated-height.tsx](components/shared/layout/animated-height.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/layout/animated-width.tsx](components/shared/layout/animated-width.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/layout/curvy-rect-divider.tsx](components/shared/layout/curvy-rect-divider.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/layout/curvy-rect.tsx](components/shared/layout/curvy-rect.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/loading/Shimmer.tsx](components/shared/loading/Shimmer.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/loading/usage-loading.tsx](components/shared/loading/usage-loading.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/lockBody.tsx](components/shared/lockBody.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/logo-cloud/index.ts](components/shared/logo-cloud/index.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/logo-cloud/logo-cloud.tsx](components/shared/logo-cloud/logo-cloud.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/logo-cloud/logo-cloud2/Logocloud.css](components/shared/logo-cloud/logo-cloud2/Logocloud.css) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/logo-cloud/logo-cloud2/Logocloud.tsx](components/shared/logo-cloud/logo-cloud2/Logocloud.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/macbook-scroll.tsx](components/shared/macbook-scroll.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/notifications/slack-notification.tsx](components/shared/notifications/slack-notification.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/pixi/Pixi.tsx](components/shared/pixi/Pixi.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/pixi/PixiAssetManager.ts](components/shared/pixi/PixiAssetManager.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/pixi/utils.ts](components/shared/pixi/utils.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/play-tabs.tsx](components/shared/play-tabs.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/Playground/Context/types.ts](components/shared/Playground/Context/types.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/portal-to-body/PortalToBody.tsx](components/shared/portal-to-body/PortalToBody.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/preview/json-error-highlighter.tsx](components/shared/preview/json-error-highlighter.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/preview/live-preview-frame.tsx](components/shared/preview/live-preview-frame.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/preview/multiple-web-browsers.tsx](components/shared/preview/multiple-web-browsers.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/preview/web-browser.tsx](components/shared/preview/web-browser.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/pylon.tsx](components/shared/pylon.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/search-params-provider/search-params-provider.tsx](components/shared/search-params-provider/search-params-provider.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/section-head/SectionHead.css](components/shared/section-head/SectionHead.css) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/section-head/SectionHead.tsx](components/shared/section-head/SectionHead.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/section-title/SectionTitle.tsx](components/shared/section-title/SectionTitle.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/tabs/Tabs.tsx](components/shared/tabs/Tabs.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/ui/app-dialog.tsx](components/shared/ui/app-dialog.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/ui/ascii-dot-loader.tsx](components/shared/ui/ascii-dot-loader.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/ui/dot-grid-loader.tsx](components/shared/ui/dot-grid-loader.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/ui/empty-state.tsx](components/shared/ui/empty-state.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/ui/index.ts](components/shared/ui/index.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/ui/loading-state.tsx](components/shared/ui/loading-state.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/ui/mobile-sheet.tsx](components/shared/ui/mobile-sheet.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/ui/stat-card.tsx](components/shared/ui/stat-card.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/shared/utils/portal-to-body.tsx](components/shared/utils/portal-to-body.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/button-demo.tsx](components/ui/button-demo.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/button.tsx](components/ui/button.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/code.tsx](components/ui/code.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/image.tsx](components/ui/image.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/index.ts](components/ui/index.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/loading-dashboard.tsx](components/ui/loading-dashboard.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/LoadingDots/index.ts](components/ui/LoadingDots/index.ts) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/LoadingDots/LoadingDots.module.css](components/ui/LoadingDots/LoadingDots.module.css) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/LoadingDots/LoadingDots.tsx](components/ui/LoadingDots/LoadingDots.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/magic/animated-shiny-text-lw.tsx](components/ui/magic/animated-shiny-text-lw.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/magic/animated-shiny-text.tsx](components/ui/magic/animated-shiny-text.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/magic/dock.tsx](components/ui/magic/dock.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/magic/dot-pattern.tsx](components/ui/magic/dot-pattern.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/magic/gradual-spacing.tsx](components/ui/magic/gradual-spacing.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/magic/ripple.tsx](components/ui/magic/ripple.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/menu-header.tsx](components/ui/menu-header.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/menu.tsx](components/ui/menu.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/modal.tsx](components/ui/modal.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/motion/scramble-text.tsx](components/ui/motion/scramble-text.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/motion/text-reveal.tsx](components/ui/motion/text-reveal.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/scrollbar.tsx](components/ui/scrollbar.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/accordion.tsx](components/ui/shadcn/accordion.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/alert-dialog.tsx](components/ui/shadcn/alert-dialog.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/badge.tsx](components/ui/shadcn/badge.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/button.css](components/ui/shadcn/button.css) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/button.tsx](components/ui/shadcn/button.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/card.tsx](components/ui/shadcn/card.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/checkbox.tsx](components/ui/shadcn/checkbox.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/collapsible.tsx](components/ui/shadcn/collapsible.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/combobox.tsx](components/ui/shadcn/combobox.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/context-menu.tsx](components/ui/shadcn/context-menu.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/data-table.tsx](components/ui/shadcn/data-table.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/dialog.tsx](components/ui/shadcn/dialog.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/dropdown-menu.tsx](components/ui/shadcn/dropdown-menu.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/form.tsx](components/ui/shadcn/form.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/input.tsx](components/ui/shadcn/input.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/label.tsx](components/ui/shadcn/label.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/navigation-menu.tsx](components/ui/shadcn/navigation-menu.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/popover.tsx](components/ui/shadcn/popover.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/progress.tsx](components/ui/shadcn/progress.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/scroll-area.tsx](components/ui/shadcn/scroll-area.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/select.tsx](components/ui/shadcn/select.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/separator.tsx](components/ui/shadcn/separator.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/sheet.tsx](components/ui/shadcn/sheet.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/slider.tsx](components/ui/shadcn/slider.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/switch.tsx](components/ui/shadcn/switch.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/tabs.tsx](components/ui/shadcn/tabs.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/textarea.tsx](components/ui/shadcn/textarea.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/toast.tsx](components/ui/shadcn/toast.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/toggle.tsx](components/ui/shadcn/toggle.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/tooltip-radix.tsx](components/ui/shadcn/tooltip-radix.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/shadcn/tooltip.tsx](components/ui/shadcn/tooltip.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/spinner.tsx](components/ui/spinner.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/table.tsx](components/ui/table.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/ui/video.tsx](components/ui/video.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [components/workflow/WorkflowExecutionRenderer.tsx](components/workflow/WorkflowExecutionRenderer.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [hooks/useApprovalWatch.ts](hooks/useApprovalWatch.ts) | Restored frontend source/asset after UI scope was authorized. |
| [hooks/useDebouncedEffect.ts](hooks/useDebouncedEffect.ts) | Restored frontend source/asset after UI scope was authorized. |
| [hooks/useWorkflow.ts](hooks/useWorkflow.ts) | Restored frontend source/asset after UI scope was authorized. |
| [hooks/useWorkflowExecution.ts](hooks/useWorkflowExecution.ts) | Restored frontend source/asset after UI scope was authorized. |
| [public/compressor.json](public/compressor.json) | Restored frontend source/asset after UI scope was authorized. |
| [public/favicon.png](public/favicon.png) | Restored frontend source/asset after UI scope was authorized. |
| [styles/additional-styles/custom-fonts.css](styles/additional-styles/custom-fonts.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/additional-styles/theme.css](styles/additional-styles/theme.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/additional-styles/utility-patterns.css](styles/additional-styles/utility-patterns.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/chrome-bug.css](styles/chrome-bug.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/colors.json](styles/colors.json) | Restored frontend source/asset after UI scope was authorized. |
| [styles/components/button.css](styles/components/button.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/components/code.css](styles/components/code.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/components/index.css](styles/components/index.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/design-system/animations.css](styles/design-system/animations.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/design-system/base/body.css](styles/design-system/base/body.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/design-system/base/layout.css](styles/design-system/base/layout.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/design-system/base/reset.css](styles/design-system/base/reset.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/design-system/colors.css](styles/design-system/colors.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/design-system/fonts.css](styles/design-system/fonts.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/design-system/typography.css](styles/design-system/typography.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/design-system/utilities.css](styles/design-system/utilities.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/fire.css](styles/fire.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/main.css](styles/main.css) | Restored frontend source/asset after UI scope was authorized. |
| [styles/workflow-execution.css](styles/workflow-execution.css) | Restored frontend source/asset after UI scope was authorized. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/open-agent-builder); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
