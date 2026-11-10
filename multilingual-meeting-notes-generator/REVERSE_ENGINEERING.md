# Reverse engineering: multilingual-meeting-notes-generator

## Problem and reconstructed mechanism

Convert multilingual meeting audio into English notes and assigned action items.

AudioTranscriber produces speaker-aware segments and TextAnalyzer builds typed meeting summaries and actions.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
audio stream/upload -> ASR with timestamps -> turn/segment state -> retrieval or analysis -> model output -> TTS or structured notes
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | main | UI reference |
| [src/data/data_models.py](src/data/data_models.py) | Speaker, TranscriptSegment, ActionItem, MeetingResult, total_words, avg_confidence, unique_speakers_count | dataclasses, datetime, typing |
| [src/services/audio_processor.py](src/services/audio_processor.py) | MeetingProcessor, process_meeting_audio | datetime, src |
| [src/services/text_analyzer.py](src/services/text_analyzer.py) | TextAnalyzer, generate_meeting_summary, extract_action_items, identify_speaker_names, generate_meeting_title | datetime, json, openai, re, src, typing |
| [src/services/transcriber.py](src/services/transcriber.py) | AudioTranscriber, transcribe_audio, get_transcript_duration | assemblyai, os, src, time, typing |
| [cli.py](cli.py) | main | argparse, dataclasses, dotenv, json, os, pathlib, src |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [src/data/data_models.py](src/data/data_models.py) | 9 | Speaker | Represents a speaker in a meeting. |
| [src/data/data_models.py](src/data/data_models.py) | 18 | TranscriptSegment | A segment of transcribed speech. |
| [src/data/data_models.py](src/data/data_models.py) | 28 | ActionItem | A task or action item from the meeting. |
| [src/data/data_models.py](src/data/data_models.py) | 37 | MeetingResult | Complete meeting analysis result. |
| [src/data/data_models.py](src/data/data_models.py) | 49 | total_words | Calculate total words in transcript. |
| [src/data/data_models.py](src/data/data_models.py) | 54 | avg_confidence | Calculate average confidence score. |
| [src/data/data_models.py](src/data/data_models.py) | 61 | unique_speakers_count | Get count of unique speakers. |
| [src/services/audio_processor.py](src/services/audio_processor.py) | 9 | MeetingProcessor | Main service that orchestrates the meeting processing workflow. |
| [src/services/audio_processor.py](src/services/audio_processor.py) | 18 | process_meeting_audio | Process a meeting audio file and generate comprehensive meeting notes. |
| [src/services/text_analyzer.py](src/services/text_analyzer.py) | 9 | TextAnalyzer | Analyzes transcribed text to extract insights and generate summaries. |
| [src/services/text_analyzer.py](src/services/text_analyzer.py) | 17 | generate_meeting_summary | Generate a comprehensive summary of the meeting in bullet point format. |
| [src/services/text_analyzer.py](src/services/text_analyzer.py) | 106 | extract_action_items | Extract action items and tasks from the meeting transcript. |
| [src/services/text_analyzer.py](src/services/text_analyzer.py) | 180 | identify_speaker_names | Identify actual names of speakers from the transcript. |
| [src/services/text_analyzer.py](src/services/text_analyzer.py) | 282 | generate_meeting_title | Generate a descriptive title for the meeting based on content. |
| [src/services/transcriber.py](src/services/transcriber.py) | 10 | AudioTranscriber | Handles audio transcription with speaker diarization. |
| [src/services/transcriber.py](src/services/transcriber.py) | 18 | transcribe_audio | Transcribe audio file with speaker diarization and language detection. |
| [src/services/transcriber.py](src/services/transcriber.py) | 76 | get_transcript_duration | Get duration from the last transcript if available. |
| [cli.py](cli.py) | 10 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `argparse`, `assemblyai`, `dataclasses`, `datetime`, `dotenv`, `gc`, `json`, `openai`, `os`, `pathlib`, `re`, `src`, `streamlit`, `tempfile`, `time`, `typing`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `ASSEMBLYAI_API_KEY`
- `OPENAI_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [cli.py](cli.py) | Added a size-bounded headless meeting-processing CLI with structured JSON output. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/multilingual-meeting-notes-generator); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
