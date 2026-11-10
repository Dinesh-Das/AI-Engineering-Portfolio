# Learning path after OCR

You already have experience turning unstructured inputs into text. Use that as the starting point for grounding, state, evaluation and model adaptation.

| Order | Projects to start with | Skill to demonstrate before moving on |
| --- | --- | --- |
| 0 | local-chatgpt, local-chatgpt with Gemma 3, local-chatgpt with DeepSeek, deepseek-thinking-ui, qwen3-thinking-ui, gpt-oss-thinking-ui, streaming-ai-chatbot | Trace UI input, model request, incremental output and terminal state; distinguish fixtures, live inference, traces and final-answer correctness |
| 1 | simple-rag-workflow, document-chat-rag, github-rag | Separate parsing, chunking, retrieval and generation; cite the exact supporting source |
| 2 | modernbert-rag, colbert-rag, fastest-rag-stack, fastest-rag-milvus-groq | Measure recall before optimizing search latency or quantization |
| 3 | corrective-rag, firecrawl-agent, trustworthy-rag, rag-sql-router | Recognize insufficient evidence, route correctly and abstain when appropriate |
| 4 | ai_news_generator, agentic_rag, book-writer-flow, content_planner_flow | Trace an agent/tool/state transition and recover safely from a failed step |
| 5 | llamaindex-mcp, cursor_linkup_mcp, mcp-agentic-rag, agent2agent-demo, acp-code | Define tool/message contracts and enforce permissions outside the model |
| 6 | database-memory-agent, zep-memory-assistant, agent-with-mcp-memory, context-engineering-pipeline | Test correction, deletion, user isolation and context-budget tradeoffs |
| 7 | eval-and-observability and the model-comparison projects | Use independent ground truth, blinded judging and executable correctness checks |
| 8 | chat-with-audios, multi-modal-rag, deepseek-multimodal-RAG, video-rag-gemini | Preserve timing/page/visual evidence through multimodal processing |
| 9 | real-time-voicebot, rag-voice-agent, multilingual-meeting-notes-generator | Measure turn latency, interruption behavior and language-specific quality |
| 10 | siamese-network, knowledge distillation, DeepSeek-finetuning, Build-reasoning-model, grpo-finetuning-qwen3 | Prevent data leakage and reward shortcuts; compare baseline, trained and exported models |
| 11 | deploy-agentic-rag, kitops-mcp, build-code-harness, open-agent-builder | Package immutable artifacts and prove authorization, restart recovery and rollback |

For every project, produce four small artifacts yourself: a one-page architecture sketch, a runnable tiny fixture, a before/after evaluation record and a paragraph explaining one deployment tradeoff. These are better evidence of understanding than running a notebook once.

The [learning contract](LEARNING_CONTRACT.md) applies to normal, invalid, failed, interrupted, concurrent and changed-model/UI scenarios. The UI experiment desk keeps predictions and observations alongside the conversation, and its export preserves terminal states. Existing [OCR learning material](LOCAL_OCR_PROJECTS.md) remains in the moved folders.

Do not skip the tree-only projects in PROJECT_INDEX.md. Some contain a smaller, clearer implementation of a concept than the larger demos. Guide-only folders are useful architecture-reading exercises, but studying their README does not validate an external service.
