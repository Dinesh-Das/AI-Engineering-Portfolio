# GitHub publication

The target is one public GitHub repository per project, plus [AI-Engineering-Portfolio](https://github.com/Dinesh-Das/AI-Engineering-Portfolio) as its main directory. All 113 local publication repositories are prepared on `main`. **All 113 project repositories are uploaded and their remote heads are verified.** The main repository is published and GitHub Pages is configured. The [publication report](publication-report.json) records the completed set.

- [Live searchable portfolio](https://dinesh-das.github.io/AI-Engineering-Portfolio/portfolio.html)
- [Live interactive HTML interview handbook](https://dinesh-das.github.io/AI-Engineering-Portfolio/)
- [Complete repository directory](REPOSITORIES.md)
- [Machine-readable repository manifest](../repositories.json)

## Repository contents and commit dates

The 109 collection projects are exported as independent repositories with commits for source and upstream provenance, learning and evaluation documentation, and standalone CPU learning tools plus validation. The four OCR projects preserve their existing Git histories and add three publication commits. The already-published repositories keep their published dates. Every commit prepared after the November 14 handoff uses the actual preparation date in Asia/Kolkata (UTC+05:30). Push events retain their actual GitHub timestamps.

At the user's request, the 58 already-pushed project histories stay unchanged. The remaining 55 projects resume after midnight IST on November 14. Their three unpublished commits are dated on the actual date they are prepared, while the three-commit count and original OCR history are preserved. Main repository updates also use their actual commit date. Per-project dates and commit hashes are recorded in the publication report.

The main portfolio retains the collection's existing history and adds the directory, website and publication evidence in separate commits. Original copyright notices and source manifests remain in place. Source-backed learning ports are attributed in each project's README; these repositories do not imply independently authored upstream implementations or production model qualification.

## Independent clones

Each independent project includes a local `workbench_core` package and an adapted `enhance.py` launcher. It does not need a sibling collection checkout for its CPU checks:

```sh
git clone https://github.com/Dinesh-Das/agentic_rag.git
cd agentic_rag
python enhance.py check
python enhance.py doctor
```

Use Python 3.12 or newer. Original SDK, model, hardware and service requirements are documented in each project's setup guide. Each repository includes `publication-validation.json` with the executed CPU scenario results. Its enhancement Dockerfile accepts this independent repository as its build context.

The original source folders stay in the local collection. Independent publication checkouts are retained under the ignored `.publication/repos/` directory; the four original local OCR repositories are preserved. Further independent changes and pushes should use those publication checkouts.

## Verification

Before publication, the collection's 79 standard-library tests and four ColBERT tests passed. Collection verification checked 109 learning contracts, seven independent UI bundles, 113 enhancement profiles with 630 scenarios, and the handbook's 113 projects, 46 chapters and 477 answered questions.

Each independent checkout was executed with `python -I <absolute-path-to-enhance.py> check` from outside the project directory. Its full reachable Git history was scanned for common credential patterns before pushing. This pattern scan is limited and does not establish exhaustive security review.

The independent OCR exports also passed 130 native pytest tests across the four projects. The Gemma, Llama and Qwen exports pass their repository lint and format checks plus 15 bundled-core tests each. [OCR export verification](OCR_PUBLICATION_VALIDATION.json) records the results and the sequential rerun after a parallel UI test timed out; test limits were preserved. Export corrections remain within each affected export's publication commits, retaining the original project history and three-commit publication count.

Remote `main` commit hashes are verified against the prepared local heads after every push. [Publication evidence](publication-report.json) records the project repositories and requested dated commit hashes. Live provider inference and GPU training are outside these checks.

The report's `date` and `last_updated_at` use the actual publication run time in Asia/Kolkata. Its `commit_dates` include the dates actually assigned to each prepared project, including November 14 for the spillover. The publisher checks the configured GitHub destination and prepared `main` commit before pushing. Portfolio commits stay on `main` and exclude unrelated staged files.

## Resuming after GitHub's cooldown

The prepared local checkouts and completed upload state are retained. From this workstation, run the following after GitHub permits content creation again:

```powershell
& 'C:\Users\dines\AppData\Roaming\uv\python\cpython-3.12.15-windows-x86_64-none\python.exe' 'D:\MyProjects\AI Projects\.publication\resume.py'
```

The script creates the main repository first, pushes the collection and portfolio, enables GitHub Pages, then uploads pending project repositories. It skips verified uploads and refuses to overwrite a different existing remote head. New repository creations are spaced 2–4 minutes apart with variable pauses and capped at eight creations per rolling hour; other writes have a smaller separate delay. Pacing deadlines and creation timestamps persist across restarts. Initial timestamps use successful push times as conservative upper bounds for the prior creation times. Rate-limit responses trigger a cooldown of at least 30 minutes, increasing exponentially on repeated failures, while honoring any longer server-provided retry interval. Transient connection errors use shorter increasing retries with a repository existence check before retrying creation. After three failed attempts the publisher stops with progress retained. Other API errors stop immediately. These measures reduce request pressure but cannot guarantee the absence of GitHub limits. [GitHub's guidance](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api#exceeding-the-rate-limit) requires backing off rather than continuing requests.
