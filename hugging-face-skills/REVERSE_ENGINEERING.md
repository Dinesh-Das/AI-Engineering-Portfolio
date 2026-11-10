# Reverse engineering: hugging-face-skills

## Problem and reconstructed mechanism

Inspect reusable dataset, evaluation, training and publishing scripts for AI agents.

The collection packages operational scripts and reference instructions; no imported skill is automatically installed or activated.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
validated request/job -> isolated runtime -> versioned model/data artifact -> bounded operation -> persisted result and observable status
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [apps/evals-leaderboard/app.py](apps/evals-leaderboard/app.py) | format_model_link, format_source_link, fetch_leaderboard, refresh_handler | UI reference |
| [apps/evals-leaderboard/collect_evals.py](apps/evals-leaderboard/collect_evals.py) | BenchmarkSpec, EvalsCollector, main, matches, log, collect_all, get_leaderboard, save_json, push_to_hub | __future__, argparse, dataclasses, datetime, huggingface_hub, json, os, pathlib |
| [apps/hackers-leaderboard/app.py](apps/hackers-leaderboard/app.py) | format_username, fetch_leaderboard, refresh_handler | UI reference |
| [apps/hackers-leaderboard/collect_points.py](apps/hackers-leaderboard/collect_points.py) | UserStats, PointsCollector, main, total_points, to_dict, log, collect_all, scan_external_repos, get_leaderboard, save_json, push_to_hub | __future__, argparse, dataclasses, datetime, huggingface_hub, json, os, requests |
| [scripts/generate_agents.py](scripts/generate_agents.py) | load_template, parse_frontmatter, collect_skills, render, load_marketplace, generate_readme_table, update_readme, validate_marketplace, main, repl | __future__, json, pathlib, re, sys |
| [skills/hugging-face-datasets/scripts/dataset_manager.py](skills/hugging-face-datasets/scripts/dataset_manager.py) | init_dataset, define_config, load_dataset_template, validate_by_template, validate_training_data, add_rows, load_template, quick_setup, show_stats, list_available_templates | argparse, huggingface_hub, json, os, pathlib, time, typing |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | HFDatasetSQL, main, query, query_raw, describe, sample, count, unique_values, histogram, filter_and_transform, join_datasets, export_to_parquet | argparse, datasets, duckdb, huggingface_hub, json, os, typing |
| [skills/hugging-face-evaluation/examples/artificial_analysis_to_hub.py](skills/hugging-face-evaluation/examples/artificial_analysis_to_hub.py) | get_model_evaluations_data, aa_evaluations_to_model_index, main | argparse, dotenv, huggingface_hub, os, requests |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | load_env, require_markdown_it, require_model_card, require_requests, require_yaml, extract_tables_from_markdown, parse_markdown_table, is_evaluation_table, normalize_model_name, find_main_model_column, find_main_model_row, is_transposed_table | argparse, dotenv, huggingface_hub, markdown_it, os, re, requests, textwrap |
| [skills/hugging-face-evaluation/scripts/inspect_eval_uv.py](skills/hugging-face-evaluation/scripts/inspect_eval_uv.py) | main | __future__, argparse, inspect_evals, os, pathlib, subprocess, sys, typing |
| [skills/hugging-face-evaluation/scripts/inspect_vllm_uv.py](skills/hugging-face-evaluation/scripts/inspect_vllm_uv.py) | setup_environment, run_inspect_vllm, run_inspect_hf, main | __future__, argparse, os, subprocess, sys, typing |
| [skills/hugging-face-evaluation/scripts/lighteval_vllm_uv.py](skills/hugging-face-evaluation/scripts/lighteval_vllm_uv.py) | setup_environment, run_lighteval_vllm, run_lighteval_accelerate, main | __future__, argparse, os, subprocess, sys, typing |
| [skills/hugging-face-evaluation/scripts/run_eval_job.py](skills/hugging-face-evaluation/scripts/run_eval_job.py) | create_eval_job, main | argparse, dotenv, huggingface_hub, os, pathlib, subprocess, sys, typing |
| [skills/hugging-face-evaluation/scripts/run_vllm_eval_job.py](skills/hugging-face-evaluation/scripts/run_vllm_eval_job.py) | estimate_hardware, create_lighteval_job, create_inspect_job, main | __future__, argparse, dotenv, huggingface_hub, os, pathlib, subprocess, sys |
| [skills/hugging-face-evaluation/scripts/test_extraction.py](skills/hugging-face-evaluation/scripts/test_extraction.py) | test_table_extraction, test_table_parsing, test_evaluation_detection, test_metric_extraction, test_model_index_format, main | evaluation_manager, yaml |
| [skills/hugging-face-jobs/scripts/cot-self-instruct.py](skills/hugging-face-jobs/scripts/cot-self-instruct.py) | check_gpu_availability, parse_thinking_output, extract_reasoning_output, extract_instruction_output, categorize_prompts, generate_synthetic_data, answer_consistency_filter, rip_filter, create_dataset_card, main | argparse, collections, datasets, datetime, huggingface_hub, json, logging, numpy |
| [skills/hugging-face-jobs/scripts/finepdfs-stats.py](skills/hugging-face-jobs/scripts/finepdfs-stats.py) | list_available_languages, compute_temporal_stats, compute_global_stats, format_temporal_stats, create_ascii_charts, create_readme, main | argparse, ascii_graph, datasets, huggingface_hub, logging, os, pathlib, polars |
| [skills/hugging-face-jobs/scripts/generate-responses.py](skills/hugging-face-jobs/scripts/generate-responses.py) | check_gpu_availability, create_dataset_card, main | argparse, datasets, datetime, huggingface_hub, logging, os, sys, torch |
| [skills/hugging-face-model-trainer/scripts/dataset_inspector.py](skills/hugging-face-model-trainer/scripts/dataset_inspector.py) | parse_args, api_request, get_splits, get_rows, find_columns, check_sft_compatibility, check_dpo_compatibility, check_grpo_compatibility, check_kto_compatibility, generate_mapping_code, format_value_preview, main | argparse, json, sys, typing, urllib |
| [skills/hugging-face-model-trainer/scripts/estimate_cost.py](skills/hugging-face-model-trainer/scripts/estimate_cost.py) | estimate_training_time, parse_args, extract_model_size, main | argparse |
| [skills/hugging-face-model-trainer/scripts/train_dpo_example.py](skills/hugging-face-model-trainer/scripts/train_dpo_example.py) | top-level workflow | datasets, trackio, trl |
| [skills/hugging-face-model-trainer/scripts/train_grpo_example.py](skills/hugging-face-model-trainer/scripts/train_grpo_example.py) | top-level workflow | datasets, trackio, trl |
| [skills/hugging-face-model-trainer/scripts/train_sft_example.py](skills/hugging-face-model-trainer/scripts/train_sft_example.py) | top-level workflow | datasets, peft, trackio, trl |
| [skills/hugging-face-paper-publisher/scripts/paper_manager.py](skills/hugging-face-paper-publisher/scripts/paper_manager.py) | PaperManager, main, index_paper, check_paper, link_paper_to_repo, create_research_article, get_arxiv_info, generate_citation | argparse, datetime, dotenv, huggingface_hub, json, os, pathlib, re |
| [skills/hugging-face-tool-builder/references/baseline_hf_api.py](skills/hugging-face-tool-builder/references/baseline_hf_api.py) | show_help, main | __future__, os, sys, urllib |
| [scripts/link-skills.sh](scripts/link-skills.sh) | backend/configuration source; inspect directly | .sh |
| [skills/hugging-face-tool-builder/references/baseline_hf_api.sh](skills/hugging-face-tool-builder/references/baseline_hf_api.sh) | backend/configuration source; inspect directly | .sh |
| [skills/hugging-face-tool-builder/references/find_models_by_paper.sh](skills/hugging-face-tool-builder/references/find_models_by_paper.sh) | backend/configuration source; inspect directly | .sh |
| [skills/hugging-face-tool-builder/references/hf_enrich_models.sh](skills/hugging-face-tool-builder/references/hf_enrich_models.sh) | backend/configuration source; inspect directly | .sh |
| [skills/hugging-face-tool-builder/references/hf_model_card_frontmatter.sh](skills/hugging-face-tool-builder/references/hf_model_card_frontmatter.sh) | backend/configuration source; inspect directly | .sh |
| [skills/hugging-face-tool-builder/references/hf_model_papers_auth.sh](skills/hugging-face-tool-builder/references/hf_model_papers_auth.sh) | backend/configuration source; inspect directly | .sh |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [apps/evals-leaderboard/collect_evals.py](apps/evals-leaderboard/collect_evals.py) | 63 | BenchmarkSpec | ClassDef |
| [apps/evals-leaderboard/collect_evals.py](apps/evals-leaderboard/collect_evals.py) | 104 | EvalsCollector | Collects evaluation scores from model-index metadata. |
| [apps/evals-leaderboard/collect_evals.py](apps/evals-leaderboard/collect_evals.py) | 427 | main | FunctionDef |
| [apps/evals-leaderboard/collect_evals.py](apps/evals-leaderboard/collect_evals.py) | 68 | matches | FunctionDef |
| [apps/evals-leaderboard/collect_evals.py](apps/evals-leaderboard/collect_evals.py) | 116 | log | Add a log message. |
| [apps/evals-leaderboard/collect_evals.py](apps/evals-leaderboard/collect_evals.py) | 121 | collect_all | Collect evaluation scores from trending models. |
| [apps/evals-leaderboard/collect_evals.py](apps/evals-leaderboard/collect_evals.py) | 360 | get_leaderboard | Get results sorted by score descending. |
| [apps/evals-leaderboard/collect_evals.py](apps/evals-leaderboard/collect_evals.py) | 364 | save_json | Save the leaderboard to a JSON file. |
| [apps/evals-leaderboard/collect_evals.py](apps/evals-leaderboard/collect_evals.py) | 377 | push_to_hub | Push the leaderboard data to a HF dataset. |
| [apps/hackers-leaderboard/collect_points.py](apps/hackers-leaderboard/collect_points.py) | 36 | UserStats | Tracks engagement stats for a single user. |
| [apps/hackers-leaderboard/collect_points.py](apps/hackers-leaderboard/collect_points.py) | 63 | PointsCollector | Collects engagement points from the hf-skills organization. |
| [apps/hackers-leaderboard/collect_points.py](apps/hackers-leaderboard/collect_points.py) | 461 | main | FunctionDef |
| [apps/hackers-leaderboard/collect_points.py](apps/hackers-leaderboard/collect_points.py) | 48 | total_points | FunctionDef |
| [apps/hackers-leaderboard/collect_points.py](apps/hackers-leaderboard/collect_points.py) | 51 | to_dict | FunctionDef |
| [apps/hackers-leaderboard/collect_points.py](apps/hackers-leaderboard/collect_points.py) | 75 | log | Add a log message. |
| [apps/hackers-leaderboard/collect_points.py](apps/hackers-leaderboard/collect_points.py) | 106 | collect_all | Collect points from all repos in the organization. |
| [apps/hackers-leaderboard/collect_points.py](apps/hackers-leaderboard/collect_points.py) | 143 | scan_external_repos | Scan trending repos across the Hub for PRs by org members. |
| [apps/hackers-leaderboard/collect_points.py](apps/hackers-leaderboard/collect_points.py) | 392 | get_leaderboard | Get the leaderboard sorted by total points. |
| [apps/hackers-leaderboard/collect_points.py](apps/hackers-leaderboard/collect_points.py) | 398 | save_json | Save the leaderboard to a JSON file. |
| [apps/hackers-leaderboard/collect_points.py](apps/hackers-leaderboard/collect_points.py) | 411 | push_to_hub | Push the leaderboard data to a HF dataset. |
| [scripts/generate_agents.py](scripts/generate_agents.py) | 31 | load_template | FunctionDef |
| [scripts/generate_agents.py](scripts/generate_agents.py) | 35 | parse_frontmatter | Parse a minimal YAML-ish frontmatter block without external deps. |
| [scripts/generate_agents.py](scripts/generate_agents.py) | 49 | collect_skills | FunctionDef |
| [scripts/generate_agents.py](scripts/generate_agents.py) | 68 | render | Very small Mustache-like renderer that only supports a single skills loop. |
| [scripts/generate_agents.py](scripts/generate_agents.py) | 87 | load_marketplace | Load marketplace.json and return parsed structure. |
| [scripts/generate_agents.py](scripts/generate_agents.py) | 94 | generate_readme_table | Generate the skills table for README.md using marketplace.json names. |
| [scripts/generate_agents.py](scripts/generate_agents.py) | 115 | update_readme | Update the README.md skills table between markers. |
| [scripts/generate_agents.py](scripts/generate_agents.py) | 154 | validate_marketplace | Validate marketplace.json against discovered skills. |
| [scripts/generate_agents.py](scripts/generate_agents.py) | 190 | main | FunctionDef |
| [scripts/generate_agents.py](scripts/generate_agents.py) | 70 | repl | FunctionDef |
| [skills/hugging-face-datasets/scripts/dataset_manager.py](skills/hugging-face-datasets/scripts/dataset_manager.py) | 39 | init_dataset | Initialize a new dataset repository on Hugging Face Hub. |
| [skills/hugging-face-datasets/scripts/dataset_manager.py](skills/hugging-face-datasets/scripts/dataset_manager.py) | 74 | define_config | Define a configuration for the dataset, including a system prompt. |
| [skills/hugging-face-datasets/scripts/dataset_manager.py](skills/hugging-face-datasets/scripts/dataset_manager.py) | 97 | load_dataset_template | Load dataset template configuration from templates directory. |
| [skills/hugging-face-datasets/scripts/dataset_manager.py](skills/hugging-face-datasets/scripts/dataset_manager.py) | 110 | validate_by_template | Validate data according to template schema. |
| [skills/hugging-face-datasets/scripts/dataset_manager.py](skills/hugging-face-datasets/scripts/dataset_manager.py) | 232 | validate_training_data | Validate training data structure according to template. |
| [skills/hugging-face-datasets/scripts/dataset_manager.py](skills/hugging-face-datasets/scripts/dataset_manager.py) | 255 | add_rows | Stream updates to the dataset by uploading a new chunk of rows. |
| [skills/hugging-face-datasets/scripts/dataset_manager.py](skills/hugging-face-datasets/scripts/dataset_manager.py) | 307 | load_template | Load a template file from the examples directory. |
| [skills/hugging-face-datasets/scripts/dataset_manager.py](skills/hugging-face-datasets/scripts/dataset_manager.py) | 317 | quick_setup | Quick setup for different dataset types using templates. |
| [skills/hugging-face-datasets/scripts/dataset_manager.py](skills/hugging-face-datasets/scripts/dataset_manager.py) | 360 | show_stats | Display statistics about the dataset. |
| [skills/hugging-face-datasets/scripts/dataset_manager.py](skills/hugging-face-datasets/scripts/dataset_manager.py) | 386 | list_available_templates | List all available dataset templates with descriptions. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 54 | HFDatasetSQL | Query Hugging Face datasets using DuckDB SQL. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 619 | main | CLI entry point. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 125 | query | Execute SQL query on a Hugging Face dataset. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 189 | query_raw | Execute raw SQL query without path substitution. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 216 | describe | Get schema/structure of a dataset. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 238 | sample | Get a random sample from a dataset. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 268 | count | Count rows in a dataset, optionally with filter. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 292 | unique_values | Get unique values in a column. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 315 | histogram | Get value distribution/histogram for a column. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 345 | filter_and_transform | Filter and transform dataset with SQL clauses. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 397 | join_datasets | Join two datasets. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 443 | export_to_parquet | Export query results to a local Parquet file. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 479 | export_to_jsonl | Export query results to JSONL format. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 509 | push_to_hub | Query a dataset and push results to a new Hub repository. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 564 | create_view | Create a DuckDB view for easier querying. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 578 | info | Get information about a dataset including available configs and splits. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 614 | close | Close the database connection. |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | 659 | add_common_args | FunctionDef |
| [skills/hugging-face-evaluation/examples/artificial_analysis_to_hub.py](skills/hugging-face-evaluation/examples/artificial_analysis_to_hub.py) | 53 | get_model_evaluations_data | FunctionDef |
| [skills/hugging-face-evaluation/examples/artificial_analysis_to_hub.py](skills/hugging-face-evaluation/examples/artificial_analysis_to_hub.py) | 65 | aa_evaluations_to_model_index | FunctionDef |
| [skills/hugging-face-evaluation/examples/artificial_analysis_to_hub.py](skills/hugging-face-evaluation/examples/artificial_analysis_to_hub.py) | 107 | main | FunctionDef |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 29 | load_env | Load .env if python-dotenv is available; keep help usable without it. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 38 | require_markdown_it | FunctionDef |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 49 | require_model_card | FunctionDef |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 60 | require_requests | FunctionDef |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 71 | require_yaml | FunctionDef |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 87 | extract_tables_from_markdown | Extract all markdown tables from content. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 95 | parse_markdown_table | Parse a markdown table string into headers and rows. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 123 | is_evaluation_table | Determine if a table contains evaluation results. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 154 | normalize_model_name | Normalize a model name for matching. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 176 | find_main_model_column | Identify the column index that corresponds to the main model. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 215 | find_main_model_row | Identify the row index that corresponds to the main model in a transposed table. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 262 | is_transposed_table | Determine if a table is transposed (models as rows, benchmarks as columns). |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 319 | extract_metrics_from_table | Extract metrics from parsed table data. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 489 | extract_evaluations_from_readme | Extract evaluation results from a model's README. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 609 | extract_tables_with_parser | Extract tables from markdown using markdown-it-py parser. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 656 | detect_table_format | Analyze a table to detect its format and identify model columns. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 720 | inspect_tables | Inspect and display all evaluation tables in a model's README. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 788 | get_open_prs | Fetch open pull requests for a Hugging Face model repository. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 826 | list_open_prs | Display open pull requests for a model repository. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 853 | get_aa_model_data | Fetch model evaluation data from Artificial Analysis API. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 893 | aa_data_to_model_index | Convert Artificial Analysis model data to model-index format. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 943 | import_aa_evaluations | Import evaluation results from Artificial Analysis for a model. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 973 | update_model_card_with_evaluations | Update a model card with evaluation results. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 1052 | show_evaluations | Display current evaluations in a model card. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 1100 | validate_model_index | Validate model-index format in a model card. |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | 1153 | main | FunctionDef |
| [skills/hugging-face-evaluation/scripts/inspect_eval_uv.py](skills/hugging-face-evaluation/scripts/inspect_eval_uv.py) | 43 | main | FunctionDef |
| [skills/hugging-face-evaluation/scripts/inspect_vllm_uv.py](skills/hugging-face-evaluation/scripts/inspect_vllm_uv.py) | 41 | setup_environment | Configure environment variables for HuggingFace authentication. |
| [skills/hugging-face-evaluation/scripts/inspect_vllm_uv.py](skills/hugging-face-evaluation/scripts/inspect_vllm_uv.py) | 49 | run_inspect_vllm | Run inspect-ai evaluation with vLLM backend. |
| [skills/hugging-face-evaluation/scripts/inspect_vllm_uv.py](skills/hugging-face-evaluation/scripts/inspect_vllm_uv.py) | 118 | run_inspect_hf | Run inspect-ai evaluation with HuggingFace Transformers backend. |
| [skills/hugging-face-evaluation/scripts/inspect_vllm_uv.py](skills/hugging-face-evaluation/scripts/inspect_vllm_uv.py) | 183 | main | FunctionDef |
| [skills/hugging-face-evaluation/scripts/lighteval_vllm_uv.py](skills/hugging-face-evaluation/scripts/lighteval_vllm_uv.py) | 37 | setup_environment | Configure environment variables for HuggingFace authentication. |
| [skills/hugging-face-evaluation/scripts/lighteval_vllm_uv.py](skills/hugging-face-evaluation/scripts/lighteval_vllm_uv.py) | 45 | run_lighteval_vllm | Run lighteval with vLLM backend for efficient GPU inference. |
| [skills/hugging-face-evaluation/scripts/lighteval_vllm_uv.py](skills/hugging-face-evaluation/scripts/lighteval_vllm_uv.py) | 113 | run_lighteval_accelerate | Run lighteval with accelerate backend for multi-GPU distributed inference. |
| [skills/hugging-face-evaluation/scripts/lighteval_vllm_uv.py](skills/hugging-face-evaluation/scripts/lighteval_vllm_uv.py) | 177 | main | FunctionDef |
| [skills/hugging-face-evaluation/scripts/run_eval_job.py](skills/hugging-face-evaluation/scripts/run_eval_job.py) | 32 | create_eval_job | Submit an evaluation job using the Hugging Face Jobs CLI. |
| [skills/hugging-face-evaluation/scripts/run_eval_job.py](skills/hugging-face-evaluation/scripts/run_eval_job.py) | 80 | main | FunctionDef |
| [skills/hugging-face-evaluation/scripts/run_vllm_eval_job.py](skills/hugging-face-evaluation/scripts/run_vllm_eval_job.py) | 54 | estimate_hardware | Estimate appropriate hardware based on model ID naming conventions. |
| [skills/hugging-face-evaluation/scripts/run_vllm_eval_job.py](skills/hugging-face-evaluation/scripts/run_vllm_eval_job.py) | 76 | create_lighteval_job | Submit a lighteval evaluation job on HuggingFace Jobs. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `Qwen/Qwen2.5-0.5B`
- `Qwen/Qwen2.5-0.5B-Instruct`

Detected import roots: `__future__`, `argparse`, `ascii_graph`, `collections`, `dataclasses`, `datasets`, `datetime`, `dotenv`, `duckdb`, `evaluation_manager`, `gradio`, `huggingface_hub`, `inspect_evals`, `json`, `logging`, `markdown_it`, `numpy`, `os`, `pathlib`, `peft`, `polars`, `random`, `re`, `requests`, `sklearn`, `subprocess`, `sys`, `textwrap`, `time`, `torch`, `tqdm`, `trackio`, `transformers`, `trl`, `typing`, `urllib`, `vllm`, `yaml`

Retained dependency manifests: [apps/evals-leaderboard/requirements.txt](apps/evals-leaderboard/requirements.txt), [apps/hackers-leaderboard/requirements.txt](apps/hackers-leaderboard/requirements.txt), [skills/hugging-face-evaluation/requirements.txt](skills/hugging-face-evaluation/requirements.txt)

Environment names detected from code/configuration:

- `AA_API_KEY`
- `ADAPTER_MODEL`
- `BASE_MODEL`
- `HF_HUB_ENABLE_HF_TRANSFER`
- `HF_TOKEN`
- `HF_USERNAME`
- `HF_XET_HIGH_PERFORMANCE`
- `OUTPUT_REPO`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [agents/AGENTS.upstream.md](agents/AGENTS.upstream.md) | Quarantined imported agent instructions as reference documentation. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [skills/hugging-face-evaluation/examples/.env.example](skills/hugging-face-evaluation/examples/.env.example) | Redacted 1 possible credential literals (values not retained). |
| [skills/hugging-face-evaluation/examples/artificial_analysis_to_hub.py](skills/hugging-face-evaluation/examples/artificial_analysis_to_hub.py) | Added explicit connection/read timeouts to 1 direct requests calls. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

| Source | Line | Rule | Review implication |
| --- | --- | --- | --- |
| [skills/hugging-face-model-trainer/scripts/convert_to_gguf.py](skills/hugging-face-model-trainer/scripts/convert_to_gguf.py) | 61 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |
| [skills/hugging-face-model-trainer/scripts/convert_to_gguf.py](skills/hugging-face-model-trainer/scripts/convert_to_gguf.py) | 79 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/hugging-face-skills); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
