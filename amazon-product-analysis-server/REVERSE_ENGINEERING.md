# Reverse engineering: amazon-product-analysis-server

## Problem and reconstructed mechanism

Expose product research and comparison through an MCP server.

TypeScript MCP resources call Bright Data tools and structure product results; restored interactive components render the structured tool results.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
authenticated client -> tool discovery -> argument validation -> authorized operation -> bounded backend call -> structured result
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |
| [index.ts](index.ts) | backend/configuration source; inspect directly | .ts |
| [resources/amazon-product-analysis/brightdata-tools.ts](resources/amazon-product-analysis/brightdata-tools.ts) | backend/configuration source; inspect directly | .ts |
| [resources/amazon-product-analysis/server.ts](resources/amazon-product-analysis/server.ts) | backend/configuration source; inspect directly | .ts |
| [resources/amazon-product-analysis/types.ts](resources/amazon-product-analysis/types.ts) | backend/configuration source; inspect directly | .ts |
| [resources/amazon-product-analysis/utils.ts](resources/amazon-product-analysis/utils.ts) | backend/configuration source; inspect directly | .ts |
| [resources/amazon-product-analysis/components/CustomerReviews.tsx](resources/amazon-product-analysis/components/CustomerReviews.tsx) | backend/configuration source; inspect directly | .tsx |
| [resources/amazon-product-analysis/components/DeliveryInfo.tsx](resources/amazon-product-analysis/components/DeliveryInfo.tsx) | backend/configuration source; inspect directly | .tsx |
| [resources/amazon-product-analysis/components/Features.tsx](resources/amazon-product-analysis/components/Features.tsx) | backend/configuration source; inspect directly | .tsx |
| [resources/amazon-product-analysis/components/ImageGallery.tsx](resources/amazon-product-analysis/components/ImageGallery.tsx) | backend/configuration source; inspect directly | .tsx |
| [resources/amazon-product-analysis/components/index.ts](resources/amazon-product-analysis/components/index.ts) | backend/configuration source; inspect directly | .ts |
| [resources/amazon-product-analysis/components/PricingDeal.tsx](resources/amazon-product-analysis/components/PricingDeal.tsx) | backend/configuration source; inspect directly | .tsx |
| [resources/amazon-product-analysis/components/ProductCard.tsx](resources/amazon-product-analysis/components/ProductCard.tsx) | backend/configuration source; inspect directly | .tsx |
| [resources/amazon-product-analysis/components/ProductSpecs.tsx](resources/amazon-product-analysis/components/ProductSpecs.tsx) | backend/configuration source; inspect directly | .tsx |
| [resources/amazon-product-analysis/components/SellerInfo.tsx](resources/amazon-product-analysis/components/SellerInfo.tsx) | backend/configuration source; inspect directly | .tsx |
| [resources/amazon-product-analysis/hooks/index.ts](resources/amazon-product-analysis/hooks/index.ts) | backend/configuration source; inspect directly | .ts |
| [resources/amazon-product-analysis/hooks/useProductAnalysis.ts](resources/amazon-product-analysis/hooks/useProductAnalysis.ts) | backend/configuration source; inspect directly | .ts |
| [resources/amazon-product-analysis/widget.tsx](resources/amazon-product-analysis/widget.tsx) | backend/configuration source; inspect directly | .tsx |
| [resources/styles.css](resources/styles.css) | backend/configuration source; inspect directly | .css |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `importlib`, `pathlib`, `sys`

Retained dependency manifests: [package.json](package.json)

Environment names detected from code/configuration:

- `BRIGHTDATA_API_KEY`
- `MAX_FEATURES_DISPLAY`
- `MCP_URL`
- `OPENAI_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [resources/amazon-product-analysis/components/CustomerReviews.tsx](resources/amazon-product-analysis/components/CustomerReviews.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [resources/amazon-product-analysis/components/DeliveryInfo.tsx](resources/amazon-product-analysis/components/DeliveryInfo.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [resources/amazon-product-analysis/components/Features.tsx](resources/amazon-product-analysis/components/Features.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [resources/amazon-product-analysis/components/ImageGallery.tsx](resources/amazon-product-analysis/components/ImageGallery.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [resources/amazon-product-analysis/components/index.ts](resources/amazon-product-analysis/components/index.ts) | Restored frontend source/asset after UI scope was authorized. |
| [resources/amazon-product-analysis/components/PricingDeal.tsx](resources/amazon-product-analysis/components/PricingDeal.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [resources/amazon-product-analysis/components/ProductCard.tsx](resources/amazon-product-analysis/components/ProductCard.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [resources/amazon-product-analysis/components/ProductSpecs.tsx](resources/amazon-product-analysis/components/ProductSpecs.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [resources/amazon-product-analysis/components/SellerInfo.tsx](resources/amazon-product-analysis/components/SellerInfo.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [resources/amazon-product-analysis/hooks/index.ts](resources/amazon-product-analysis/hooks/index.ts) | Restored frontend source/asset after UI scope was authorized. |
| [resources/amazon-product-analysis/hooks/useProductAnalysis.ts](resources/amazon-product-analysis/hooks/useProductAnalysis.ts) | Restored frontend source/asset after UI scope was authorized. |
| [resources/amazon-product-analysis/widget.tsx](resources/amazon-product-analysis/widget.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [resources/styles.css](resources/styles.css) | Restored frontend source/asset after UI scope was authorized. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/schema.json](enhancement/examples/schema.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/amazon-product-analysis-server); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
