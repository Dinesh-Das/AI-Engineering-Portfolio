# Completed OCR work preserved locally

These folders were moved into this workspace by the user after the initial collection import. Their code, existing documentation and learning material are preserved without reimporting upstream versions. They remain separate from the 109 source-port projects and are not automatically staged in this task's commits.

| Existing folder | Starting guide | Existing design/specification |
| --- | --- | --- |
| Latex-OCR-Lama | [README](../Latex-OCR-Lama/README.md) | Existing tests and dependency locks remain alongside the implementation |
| gemma3-ocr | [README](../gemma3-ocr/README.md) | [SPEC](../gemma3-ocr/SPEC.md) |
| llama-ocr | [README](../llama-ocr/README.md) | [SPEC](../llama-ocr/SPEC.md), [validation](../llama-ocr/VALIDATION.md) |
| qwen-2.5VL-ocr | [README](../qwen-2.5VL-ocr/README.md) | [SPEC](../qwen-2.5VL-ocr/SPEC.md) |

Continue using the original project instructions and learning notes in each folder. The collection-wide learning contract is a guide for future additions, not evidence that these completed projects were reviewed or modified in the UI expansion.

The subsequent all-113 enhancement pass includes these four projects. Each now has `enhance.py`, an `ENHANCEMENTS.md` guide and a preserved personal journal. Objective CER/WER and one-to-one region metrics accept actual labeled output without loading a model. Their native suites passed after the additions; see [verification and scope](OCR_ENHANCEMENT_VALIDATION.md). Each remains an independent Git repository; its enhancement additions are committed there rather than added as an embedded repository to the parent collection.
