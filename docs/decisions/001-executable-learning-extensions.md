# ADR-001: Shared executable learning contracts

Status: Accepted. Date: 2026-11-10.

## Context

The collection contains 109 source-backed projects plus four independently maintained OCR repositories. Frameworks, credentials, hardware and deployment targets differ substantially. Enhancing every project must preserve the mechanism, hands-on learning and honest verification scope, without merging their incompatible dependency environments or overwriting personal notes.

## Decision

Keep the original implementations and targeted source fixes. Add a per-project launcher, source-specific profile, synthetic inputs, environment inventory and enhancement guide, backed by a shared standard-library CPU runtime. Choose a contract relevant to each project's category and use actual algorithms/state/files for normal, invalid, missing, recovery and isolation checks. Expose commands that consume real user data as well as fixtures. Keep OCR project histories independent and commit only our additions there.

Separate three evidence layers: deterministic CPU checks; native application/browser suites; real model/provider/GPU and production qualification. Fingerprint the extension sources and profiles in the executed coverage report. Keep deployment proposals and the CPU-only Dockerfiles explicit about what they package and what has not been run.

## Alternatives considered

Copying the runtime into every folder permits standalone export but creates 113 copies to maintain; the seven existing learning UIs already have their own independent packaging contract. Installing every model/framework would combine incompatible environments and incur unapproved provider/model costs without ground-truth data. A docs-only enhancement would not supply executable evidence. Rewriting every demo behind a generic API would obscure its original learning mechanism.

## Consequences

Project extensions require the collection's parent `workbench_core` package and Python 3.12+. CPU operations are inspectable and inexpensive, but do not replace embedding, inference, training or original integration work. Production integrations must map trusted identity to scope, add durable distributed execution and evaluate task quality on independently labeled data. The generator owns new guides/configuration; journals remain user-owned. Original fixes retain provenance hashes.
