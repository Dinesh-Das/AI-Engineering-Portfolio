# Reverse engineering: colbert-rag

## Problem and reconstructed mechanism

Understand late interaction through ColBERT-style MaxSim scoring.

Each query token takes its maximum dot product across document tokens; summing those maxima ranks documents.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
versioned embedding model -> candidate index -> top-N candidates -> optional precise reranking -> top-k evidence -> generator
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [colbert.py](colbert.py) | compute_relevance_scores, test_compute_relevance_scores | torch |
| [maxsim.py](maxsim.py) | score_document, rank_documents | collections, math |
| [tests/test_maxsim.py](tests/test_maxsim.py) | MaxSimTests, test_token_maxima_are_summed, test_padding_cannot_outscore_negative_real_tokens, test_top_k_is_respected_with_stable_ties, test_bad_shapes_empty_masks_and_nonfinite_values_fail | importlib, maxsim, pathlib, sys, unittest |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [colbert.py](colbert.py) | 3 | compute_relevance_scores | Compute relevance scores for top-k documents given a query. |
| [colbert.py](colbert.py) | 35 | test_compute_relevance_scores | FunctionDef |
| [maxsim.py](maxsim.py) | 29 | score_document | Sum each query token's best real document-token dot product. |
| [maxsim.py](maxsim.py) | 47 | rank_documents | Return (original_index, score) pairs for top k, with stable index tie breaks. |
| [tests/test_maxsim.py](tests/test_maxsim.py) | 10 | MaxSimTests | ClassDef |
| [tests/test_maxsim.py](tests/test_maxsim.py) | 11 | test_token_maxima_are_summed | FunctionDef |
| [tests/test_maxsim.py](tests/test_maxsim.py) | 14 | test_padding_cannot_outscore_negative_real_tokens | FunctionDef |
| [tests/test_maxsim.py](tests/test_maxsim.py) | 17 | test_top_k_is_respected_with_stable_ties | FunctionDef |
| [tests/test_maxsim.py](tests/test_maxsim.py) | 20 | test_bad_shapes_empty_masks_and_nonfinite_values_fail | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `collections`, `importlib`, `math`, `maxsim`, `pathlib`, `sys`, `torch`, `unittest`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [maxsim.py](maxsim.py) | Added tested CPU MaxSim scoring with padding masks, finite shape validation and top-k ranking. |
| [tests/test_maxsim.py](tests/test_maxsim.py) | Added regression tests for negative-token padding, shape validation, stable ties and top-k. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/colbert-rag); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
