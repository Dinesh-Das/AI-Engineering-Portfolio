"""Build a single offline interview handbook from maintained content and project evidence."""

import argparse
import base64
import csv
import hashlib
import html
import json
import posixpath
import re
import shlex
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

from .transform import redact_literals

ROOT = Path(__file__).resolve().parents[1]
AUTHORING = ROOT / "tools/interview"
OCR = {"Latex-OCR-Lama", "gemma3-ocr", "llama-ocr", "qwen-2.5VL-ocr"}
DOC_NAMES = {
    "README.md": "overview",
    "LEARNINGS.md": "learning",
    "EVALUATION.md": "evaluation",
    "ENHANCEMENTS.md": "engineering",
    "REVERSE_ENGINEERING.md": "source",
    "reverse-engineering.md": "source",
    "UPSTREAM_README.md": "author",
}
CATEGORY_TOPICS = {
    "rag": [
        "rag-design",
        "chunking-ingestion",
        "embeddings",
        "vector-indexes",
        "hybrid-search",
        "reranking",
        "rag-evaluation",
        "context-memory",
    ],
    "retrieval": ["embeddings", "vector-indexes", "hybrid-search", "reranking", "rag-evaluation"],
    "agents": ["agents-workflows", "tool-contracts", "multi-agent", "reliability", "system-design"],
    "memory": ["context-memory", "graph-rag", "sql-data", "security-privacy", "reliability"],
    "mcp": ["mcp-protocols", "tool-contracts", "security-privacy", "python-async"],
    "training": [
        "data-splitting",
        "neural-optimization",
        "finetuning-lora",
        "quantization",
        "eval-experiments",
    ],
    "evaluation": ["evaluation-metrics", "probability-stats", "eval-experiments", "cost-latency"],
    "voice": ["audio-voice", "python-async", "streaming-ux", "cost-latency"],
    "media": ["audio-voice", "agents-workflows", "reliability", "evaluation-metrics"],
    "structured": [
        "prompting-structured",
        "tool-contracts",
        "data-splitting",
        "evaluation-metrics",
    ],
    "interfaces": ["streaming-ux", "generation", "context-memory", "security-privacy"],
    "operations": ["deployment-mlops", "serving-capacity", "observability", "security-privacy"],
    "recipe": ["deployment-mlops", "reliability", "system-design", "security-privacy"],
    "ocr": ["multimodal-ocr", "evaluation-metrics", "vision-detection", "serving-capacity"],
}


def inline_json(value):
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def safe_link(target, base=""):
    target = html.unescape(target.strip().strip("<>"))
    parsed = urlsplit(target)
    if parsed.scheme:
        return target if parsed.scheme.lower() in {"https", "http"} else None
    if parsed.netloc or target.startswith(("\\", "/")):
        return None
    if target.startswith("#"):
        return None
    path = posixpath.normpath(posixpath.join(base, unquote(parsed.path)))
    if path == ".." or path.startswith("../"):
        return None
    parts = path.split("/")
    if (
        len(parts) >= 2
        and parts[-1] in DOC_NAMES
        and parts[0] not in {"docs", "tools", "workbench_core"}
    ):
        return (
            "#view=project&id=" + quote(parts[0], safe="") + "&tab=docs&doc=" + DOC_NAMES[parts[-1]]
        )
    return quote(path, safe="/") + ("#" + quote(parsed.fragment) if parsed.fragment else "")


def inline(value, base=""):
    pattern = r"`([^`]+)`|!?\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*"
    result, cursor = [], 0
    for match in re.finditer(pattern, value):
        result.append(html.escape(value[cursor : match.start()]))
        if match[1] is not None:
            result.append("<code>" + html.escape(match[1]) + "</code>")
        elif match[2] is not None:
            url = safe_link(match[3], base)
            label = html.escape(match[2])
            if match[0].startswith("!"):
                result.append(
                    '<span class="asset-label">[Source illustration: ' + label + "]</span>"
                )
            elif url:
                result.append(
                    '<a href="'
                    + html.escape(url, quote=True)
                    + '"'
                    + (
                        ' target="_blank" rel="noopener noreferrer"'
                        if url.startswith(("http:", "https:"))
                        else ""
                    )
                    + ">"
                    + label
                    + "</a>"
                )
            else:
                result.append(label)
        else:
            result.append("<strong>" + html.escape(match[4]) + "</strong>")
        cursor = match.end()
    result.append(html.escape(value[cursor:]))
    return "".join(result)


def markdown(text, base=""):
    """Escape-first subset: headings, paragraphs, lists, tables, links and fenced code."""
    lines, out, index = text.splitlines(), [], 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("```"):
            language, code = line[3:].strip(), []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            out.append(
                '<div class="code-block"><div class="code-bar"><span>'
                + html.escape(language or "Code")
                + '</span><button type="button" data-action="copy" aria-label="Copy code block">Copy</button></div><pre tabindex="0"><code>'
                + html.escape("\n".join(code))
                + "</code></pre></div>"
            )
            index += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level = min(6, len(heading[1]) + 2)
            out.append(f"<h{level}>" + inline(heading[2], base) + f"</h{level}>")
            index += 1
            continue
        if index + 1 < len(lines) and "|" in line and re.fullmatch(r"[\s|:\-]+", lines[index + 1]):

            def cells(row):
                return re.split(r"(?<!\\)\|", row.strip().strip("|"))

            headers = cells(line)
            out.append(
                '<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable reference table"><table><thead><tr>'
                + "".join('<th scope="col">' + inline(c.strip(), base) + "</th>" for c in headers)
                + "</tr></thead><tbody>"
            )
            index += 2
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                out.append(
                    "<tr>"
                    + "".join(
                        "<td>" + inline(c.strip().replace("\\|", "|"), base) + "</td>"
                        for c in cells(lines[index])
                    )
                    + "</tr>"
                )
                index += 1
            out.append("</tbody></table></div>")
            continue
        if re.match(r"^([-*]|\d+\.)\s+", line):
            ordered = bool(re.match(r"^\d+\.", line))
            tag = "ol" if ordered else "ul"
            out.append("<" + tag + ">")
            while index < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[index]):
                item = re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[index])
                out.append("<li>" + inline(item, base) + "</li>")
                index += 1
            out.append("</" + tag + ">")
            continue
        if re.fullmatch(r"[-_*]{3,}", line):
            out.append("<hr>")
            index += 1
            continue
        paragraph = [line]
        index += 1
        while (
            index < len(lines)
            and lines[index].strip()
            and not re.match(r"^(#|```|[-*]\s|\d+\.\s|\|)", lines[index].strip())
        ):
            paragraph.append(lines[index].strip())
            index += 1
        out.append("<p>" + inline(" ".join(paragraph), base) + "</p>")
    return "\n".join(out)


def topics(root):
    source_map = json.loads((root / "tools/interview/sources.json").read_text(encoding="utf-8"))
    text = (root / "tools/interview/handbook.md").read_text(encoding="utf-8")
    matches = list(re.finditer(r"^# (.+) \{#([a-z0-9-]+)\}\s*$", text, re.MULTILINE))
    result = []
    for number, match in enumerate(matches):
        content = text[
            match.end() : matches[number + 1].start() if number + 1 < len(matches) else len(text)
        ].strip()
        group = re.search(r"^Group: (.+)$", content, re.MULTILINE)[1]
        source_ids = re.search(r"^Sources: (.+)$", content, re.MULTILINE)[1].split(",")
        body = re.sub(r"^(Group|Sources): .+\n?", "", content, flags=re.MULTILINE).strip()
        questions = []
        for question in re.finditer(
            r"^### (Foundation|Applied|Advanced): ([^\n]+)\n(.*?)(?=^### |\Z)",
            body,
            re.MULTILINE | re.DOTALL,
        ):
            questions.append(
                {
                    "id": match[2] + "-" + str(len(questions)),
                    "level": question[1],
                    "question": question[2].strip(),
                    "answer": question[3].strip(),
                    "answer_html": markdown(question[3].strip()),
                }
            )
        reading = body.split("## Interview questions")[0].strip()
        reading = re.sub(r"^(#{2,6}) ", lambda m: m[1][1:] + " ", reading, flags=re.MULTILINE)
        result.append(
            {
                "id": match[2],
                "title": match[1],
                "group": group,
                "number": number + 1,
                "body": body,
                "html": markdown(reading),
                "questions": questions,
                "sources": [source_map[key.strip()] for key in source_ids],
                "summary": re.sub(r"^## .+\n", "", reading).split("\n\n")[0].strip(),
            }
        )
    return result


def ps_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def wrapped(identifier, command, relative=""):
    folder = "./" + identifier + ("/" + relative if relative else "")
    return (
        "Push-Location -LiteralPath "
        + ps_quote(folder)
        + "\ntry {\n    "
        + command.replace("\n", "\n    ")
        + "\n} finally { Pop-Location }"
    )


def commands(root, project, category):
    identifier, directory = project["id"], root / project["id"]
    output = []

    def add(label, command, kind, note, language="PowerShell"):
        output.append(
            {
                "label": label,
                "command": command,
                "kind": kind,
                "note": note,
                "language": language,
                "cwd": "Collection root: AI Projects",
            }
        )

    add(
        "Run the CPU learning checks",
        ".\\run.ps1 enhance --project " + ps_quote(identifier),
        "offline",
        "Runs this project’s synthetic CPU contracts. No model/provider calls, training or application verification.",
    )
    add(
        "Inspect this environment",
        wrapped(identifier, "& .\\.venv\\Scripts\\python.exe enhance.py doctor"),
        "diagnostic",
        "Prepare a project-local virtual environment first. Reports package presence and variable names/set flags; version and model compatibility are unverified.",
    )
    manifests = project.get("analysis", {}).get("manifests", [])
    if identifier in OCR:
        manifests = [
            p.name
            for p in directory.iterdir()
            if p.name in {"pyproject.toml", "requirements.txt", "uv.lock"}
        ]
    setup = "python -m venv .venv\n& .\\.venv\\Scripts\\python.exe -m pip install --upgrade pip"
    if (directory / "uv.lock").exists() and (directory / "pyproject.toml").exists():
        add(
            "Prepare the locked environment",
            wrapped(identifier, "uv sync --frozen"),
            "setup",
            "Requires uv and the Python/platform supported by the retained lockfile. Optional model/GPU extras may be needed; inspect the embedded setup guide.",
        )
    elif (directory / "requirements.txt").exists():
        add(
            "Prepare an isolated environment",
            wrapped(
                identifier,
                setup + "\n& .\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt",
            ),
            "setup",
            "Installs the retained requirements, which may include optional paths. Model weights and external services remain separate. Resolve compatibility before real inference.",
        )
    else:
        add(
            "Create an isolated environment",
            wrapped(identifier, setup),
            "setup",
            "No universal dependency install is inferred. Read the embedded setup guide and the declared manifests: "
            + (", ".join(manifests) or "no root dependency manifest retained")
            + ".",
        )
    if project.get("learning_ui"):
        add(
            "Open the labeled learning UI fixture",
            ".\\run.ps1 ui --project "
            + ps_quote(identifier)
            + " --execute --timeout 3600 --entry-args --fixture --port 8765",
            "fixture",
            "Open http://127.0.0.1:8765. This uses the bundled stdlib UI; its fixture is not model inference.",
        )
        add(
            "Use an installed local model in the learning UI",
            ".\\run.ps1 ui --project "
            + ps_quote(identifier)
            + " --execute --timeout 3600 --entry-args --port 8765",
            "live",
            "Requires running local Ollama and the already installed model in lab.json. This command does not provision or download the model.",
        )
    entries = [
        e for e in project.get("entries", []) if e["path"] not in {"enhance.py", "learning_app.py"}
    ]
    ui_entries = [e for e in project.get("ui_entries", []) if e.get("kind") != "learning-ui"]
    if identifier in OCR:
        entries = []
        ui_entries = [{"path": "app.py", "kind": "streamlit"}]
    seen = set()
    for entry in ui_entries:
        path, kind = entry["path"], entry["kind"]
        seen.add(path)
        if kind in {"streamlit", "chainlit"}:
            module = "streamlit run" if kind == "streamlit" else "chainlit run"
            flags = " --server.address 127.0.0.1" if kind == "streamlit" else " --host 127.0.0.1"
            add(
                "Launch original UI: " + path,
                wrapped(
                    identifier,
                    "& .\\.venv\\Scripts\\python.exe -m " + module + " " + ps_quote(path) + flags,
                ),
                "live",
                "Uses this folder’s environment and configuration. Prepare dependencies, installed models and selected credentials/services first. Inference may consume resources or provider credits; this integration is not certified by CPU checks.",
            )
        elif kind == "npm":
            package = json.loads((directory / path).read_text(encoding="utf-8-sig"))
            script = entry["script"]
            relative = Path(path).parent.as_posix()
            relative = "" if relative == "." else relative
            shell_specific = bool(
                re.search(r"\bsource\b|\bexport\b|/bin/|\.\/.*\.sh", package["scripts"][script])
            )
            if shell_specific:
                add(
                    "Launch original Node workflow (Bash / WSL): " + path,
                    "cd "
                    + shlex.quote("./" + identifier + ("/" + relative if relative else ""))
                    + "\n"
                    + "npm run "
                    + script,
                    "live",
                    "The retained npm script uses a POSIX shell. Prepare its documented Node/Python environment in WSL/Linux first; it is not a native PowerShell command.",
                    "Bash / WSL",
                )
            else:
                add(
                    "Launch original Node UI: " + path,
                    wrapped(identifier, "npm run " + script, relative),
                    "live",
                    "Install the manifest-owning subproject according to its embedded guide first. Review lifecycle scripts and required services before running.",
                )
    for entry in entries:
        path = entry["path"]
        if path in seen or entry.get("ui"):
            continue
        if entry["kind"] == "notebook":
            add(
                "Inspect notebook: " + path,
                wrapped(
                    identifier, "& .\\.venv\\Scripts\\python.exe -m jupyter lab " + ps_quote(path)
                ),
                "notebook",
                "Requires JupyterLab in this project environment. Opening is for inspection; review cells before execution. Original notebooks may assume Colab/Linux, GPU packages, downloads or paid providers.",
            )
        elif entry["kind"] == "python":
            add(
                "Original Python candidate: " + path,
                wrapped(identifier, "& .\\.venv\\Scripts\\python.exe " + ps_quote(path)),
                "candidate",
                "Discovered source entry; inspect the embedded source map before running. Some files are helpers, servers or workers and need arguments, another process or external setup. No successful end-to-end run is implied.",
            )
    if not entries and not ui_entries:
        add(
            "Study the original deployment recipe / schemas",
            ".\\run.ps1 show --project " + ps_quote(identifier),
            "inspection",
            "No original standalone application entry is retained. The CPU extension is runnable; actual deployment follows the embedded guide and external prerequisites.",
        )
    return output


def build_data(root=ROOT):
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    with (root / "tools/project_notes.psv").open(encoding="utf-8", newline="") as stream:
        notes = {row["id"]: row for row in csv.DictReader(stream, delimiter="|")}
    categories = json.loads((root / "tools/category_notes.json").read_text(encoding="utf-8"))
    chapters = topics(root)
    topic_ids = {t["id"] for t in chapters}
    projects = []
    catalog_by_id = {p["id"]: p for p in catalog["projects"]}
    ids = (
        set(catalog_by_id)
        | OCR
        | {p.name for p in root.iterdir() if p.is_dir() and (p / "project.json").is_file()}
    )
    for identifier in sorted(ids, key=str.casefold):
        directory = root / identifier
        if not directory.is_dir() or not directory.resolve().is_relative_to(root.resolve()):
            raise ValueError("Project directory missing or outside the collection: " + identifier)
        project = catalog_by_id.get(identifier, {"id": identifier})
        profile_path = directory / "enhancement/profile.json"
        profile = (
            json.loads(profile_path.read_text(encoding="utf-8")) if profile_path.exists() else {}
        )
        note = notes.get(identifier, profile)
        category = project.get("category", "ocr")
        category_note = categories.get(
            category,
            {
                "lesson": "Separate faithful transcription, formatting and region localization, then measure against human references.",
                "pipeline": "validated image/page -> normalized pixels -> vision inference -> parsed text/regions -> human reference metrics",
                "metrics": "CER/WER edit counts, per-page exact fields, region precision/recall, empty output, failure rate and measured inference latency.",
                "failure": "Hallucinated digits, missed lines, duplicate regions, coordinate mismatches, stale results and incompatible model/service setup.",
                "tradeoff": "Local vision inference controls data location but needs measured memory/concurrency; external providers require explicit processing authorization and retention/cost controls.",
            },
        )
        analysis_path = directory / "analysis.json"
        analysis = (
            json.loads(analysis_path.read_text(encoding="utf-8")) if analysis_path.exists() else {}
        )
        docs, embedded = {}, []
        candidates = {
            "overview": ["README.md"],
            "source": [
                "REVERSE_ENGINEERING.md",
                "docs/REVERSE_ENGINEERING.md",
                "docs/reverse-engineering.md",
                "SPEC.md",
                "README.md",
            ],
            "learning": ["LEARNINGS.md", "ENHANCEMENTS.md", "README.md"],
            "evaluation": ["EVALUATION.md", "ENHANCEMENTS.md"],
            "engineering": ["ENHANCEMENTS.md"],
        }
        for key, choices in candidates.items():
            path = next(
                (directory / choice for choice in choices if (directory / choice).is_file()), None
            )
            if path is None:
                raise ValueError(f"{identifier}: missing {key} documentation")
            content = path.read_text(encoding="utf-8-sig")
            # Relocated native guides may retain their old checkout path; use this actual collection path in the embedded copy.
            content = content.replace("D:\\MyProjects\\" + identifier, str(directory))
            docs[key] = markdown(
                redact_literals(content)[0], path.parent.relative_to(root).as_posix()
            )
            embedded.append(path.relative_to(directory).as_posix())
        author = directory / "UPSTREAM_README.md"
        if author.is_file():
            docs["author"] = markdown(
                redact_literals(author.read_text(encoding="utf-8-sig"))[0], identifier
            )
            embedded.append("UPSTREAM_README.md")
            license_path = directory / "UPSTREAM_LICENSE"
            if license_path.is_file():
                docs["author"] += (
                    '<details><summary>Retained upstream source license</summary><div class="code-block"><pre tabindex="0">'
                    + html.escape(license_path.read_text(encoding="utf-8-sig"))
                    + "</pre></div></details>"
                )
        else:
            docs["author"] = (
                "<p>No separate upstream author README is retained in this folder. The local setup guide is included below.</p>"
                + docs["overview"]
            )
        related = list(CATEGORY_TOPICS.get(category, []))
        special = {
            "distill": "distillation",
            "grpo": "preference-grpo",
            "reasoning": "preference-grpo",
            "yolo": "vision-detection",
            "code": "coding-agents",
            "graph": "graph-rag",
            "colbert": "reranking",
            "sql": "sql-data",
            "sdv": "data-splitting",
            "siamese": "embeddings",
        }
        related.extend(topic for word, topic in special.items() if word in identifier.casefold())
        related = list(dict.fromkeys(t for t in related if t in topic_ids))
        questions = [
            {
                "id": identifier + "-explain",
                "level": "Foundation",
                "question": f"Explain {identifier} in 90 seconds. What problem does it solve and how does information flow?",
                "answer": note["purpose"]
                + " "
                + note["mechanism"]
                + " Trace a concrete input through each boundary, state the output contract and separate the original model path from the added CPU engineering lab.",
            },
            {
                "id": identifier + "-experiment",
                "level": "Applied",
                "question": f"How would you prove that {identifier} works, and diagnose a plausible failure?",
                "answer": note["experiment"]
                + " Freeze the inputs, independently checked expected labels, model/dependency versions and one changed variable. Measure "
                + category_note["metrics"]
                + " Retain missing/failed cases rather than dropping them; inspect the first boundary where observed evidence differs from the contract.",
            },
            {
                "id": identifier + "-production",
                "level": "Advanced",
                "question": f"How would you evolve {identifier} into a shared production service, and what would you trade off?",
                "answer": note["production"]
                + " "
                + category_note["tradeoff"]
                + " Derive scope from verified identity; test cross-user isolation, budgets, failure recovery and rollback. Report the deployment design as a proposal until load, quality and live integration evidence exist.",
            },
        ]
        for q in questions:
            q["answer_html"] = markdown(q["answer"])
        projects.append(
            {
                "id": identifier,
                "category": category,
                "purpose": note["purpose"],
                "mechanism": note["mechanism"],
                "lesson": category_note["lesson"],
                "pipeline": category_note["pipeline"],
                "metrics": category_note["metrics"],
                "risks": category_note["failure"],
                "experiment": note["experiment"],
                "production": note["production"],
                "tradeoff": category_note["tradeoff"],
                "family": profile.get("family", "reference"),
                "models": analysis.get("models", []),
                "environment": analysis.get("environment", []),
                "imports": analysis.get("imports", []),
                "commands": commands(root, project, category),
                "docs": docs,
                "embedded_files": embedded,
                "questions": questions,
                "topics": related,
                "source_url": project.get("source_url", catalog["repository"]),
                "local_ocr": identifier in OCR,
                "source_files": [
                    r["path"]
                    for r in project.get("files", [])
                    if Path(r["path"]).suffix
                    in {".py", ".ipynb", ".ts", ".tsx", ".js", ".json", ".toml"}
                ][:35],
            }
        )
    return {
        "schema_version": 1,
        "edition": "11 November 2026",
        "revision": catalog["revision"],
        "projects": projects,
        "topics": chapters,
        "categories": sorted({p["category"] for p in projects}),
        "coverage": {
            "projects": len(projects),
            "topics": len(chapters),
            "questions": sum(len(p["questions"]) for p in projects)
            + sum(len(t["questions"]) for t in chapters),
        },
    }


def render(root=ROOT):
    data = build_data(root)
    directory = root / "tools/interview"
    css = (directory / "site.css").read_text(encoding="utf-8")
    code = "\n".join(
        (directory / name).read_text(encoding="utf-8")
        for name in ("state.js", "views.js", "app.js")
    )
    script = "(() => {\n'use strict';\n" + code + "\n})();"
    digest = base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
    template = (directory / "template.html").read_text(encoding="utf-8")
    rendered = (
        template.replace("@@CSS@@", css)
        .replace("@@PAYLOAD@@", inline_json(data))
        .replace("@@SCRIPT@@", script)
        .replace("@@SCRIPT_HASH@@", digest)
    )
    return rendered, data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    rendered, data = render()
    output = ROOT / "index.html"
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != rendered:
            print("index.html is stale; run .\\run.ps1 handbook")
            return 1
        print("Handbook matches maintained content and all current project guides.")
    else:
        output.write_text(rendered, encoding="utf-8", newline="\n")
        print(
            json.dumps(
                {**data["coverage"], "bytes": output.stat().st_size, "output": str(output)},
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
