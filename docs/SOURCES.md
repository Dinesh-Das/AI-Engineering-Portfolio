# Sources and evidence boundaries

## Primary project source

[AI Engineering Hub pinned revision](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d). Each project.json maps the retained files to their original path and SHA-256 hash. Per-project conceptual flows and deployment recommendations are interpretations of this source, not upstream runtime measurements.

## Official tooling and production references

- [Python 3.12 AST](https://docs.python.org/3.12/library/ast.html): source parsing and symbol inspection without importing modules.
- [Python 3.12 subprocess](https://docs.python.org/3.12/library/subprocess.html): argument-list execution, explicit working directory and direct-child timeout semantics.
- [Python virtual environments](https://docs.python.org/3.12/library/venv.html): independent project environments.
- [nbconvert notebook execution](https://nbconvert.readthedocs.io/en/stable/execute_api.html): execution deadlines, error handling and output notebooks.
- [nbconvert configuration](https://nbconvert.readthedocs.io/en/latest/config_options.html): strict error raising, widget-state behavior and notebook client settings.
- [LlamaIndex production RAG guidance](https://developers.llamaindex.ai/python/framework/optimizing/production_rag/): retrieval, metadata and production design considerations.
- [LlamaIndex evaluation modules](https://developers.llamaindex.ai/python/framework/module_guides/evaluating/modules/): separate retrieval and response evaluation.
- [Docker build best practices](https://docs.docker.com/build/building/best-practices/): minimal builds, explicit working directories and non-root runtime users.

These references support the collection tooling and proposed boundaries. They do not validate every upstream SDK version. Provider/model compatibility must be checked against the chosen project's own resolved dependency set and actual integration tests.

## UI expansion references

- [Ollama chat API](https://docs.ollama.com/api/chat): REST message payloads and streamed NDJSON responses.
- [Ollama thinking](https://docs.ollama.com/capabilities/thinking): native thinking/content channels and model-specific thinking modes. Displayed traces remain generated output, not correctness evidence.
- [Ollama vision](https://docs.ollama.com/capabilities/vision): base64 image data for REST requests, distinct from SDK file-path convenience.
- [Playwright library](https://playwright.dev/docs/library): isolated browser contexts, explicit lifecycle and local UI verification.

The new learning interfaces use these contracts while retaining the original framework-specific demos. The streaming-ai-chatbot upstream README describes three Motia step files that are absent from the pinned Git tree; its local learning app is explicitly reconstructed, not described as recovered source.
