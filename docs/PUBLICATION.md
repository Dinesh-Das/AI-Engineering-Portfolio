# GitHub publication

The target is one public GitHub repository per project, plus [AI-Engineering-Portfolio](https://github.com/Dinesh-Das/AI-Engineering-Portfolio) as its main directory. All 113 local publication repositories are prepared on `main`. **Ten project repositories are uploaded and verified; 103 project repositories await the slow sequential publication.** The main repository has been created. The [publication report](publication-report.json) records the verified project set. Publication resumed with persistent pacing and automatic backoff.

- [Live searchable portfolio](https://dinesh-das.github.io/AI-Engineering-Portfolio/portfolio.html)
- [Live interactive HTML interview handbook](https://dinesh-das.github.io/AI-Engineering-Portfolio/)
- [Complete repository directory](REPOSITORIES.md)
- [Machine-readable repository manifest](../repositories.json)

## Repository contents and commit dates

The 109 collection projects are exported as independent repositories in three substantive commits: source and upstream provenance on November 11, learning and evaluation documentation on November 12, and standalone CPU learning tools plus validation on November 13, 2026. The four OCR projects preserve their existing Git histories and add three publication commits across the same dates. Both author and committer dates use Asia/Kolkata (UTC+05:30), as requested. Push events retain their actual GitHub timestamps.

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

Remote `main` commit hashes are verified against the prepared local heads after every push. [Publication evidence](publication-report.json) records the project repositories and requested dated commit hashes. Live provider inference and GPU training are outside these checks.

## Resuming after GitHub's cooldown

The prepared local checkouts and completed upload state are retained. From this workstation, run the following after GitHub permits content creation again:

```powershell
& 'C:\Users\dines\AppData\Roaming\uv\python\cpython-3.12.15-windows-x86_64-none\python.exe' 'D:\MyProjects\AI Projects\.publication\resume.py'
```

The script creates the main repository first, pushes the collection and portfolio, enables GitHub Pages, then uploads pending project repositories. It skips verified uploads and refuses to overwrite a different existing remote head. New repository creations are spaced 2–4 minutes apart with variable pauses; other writes have a smaller separate delay. Pacing deadlines persist across restarts. Rate-limit responses trigger a cooldown of at least 30 minutes, increasing exponentially on repeated failures, while honoring any longer server-provided retry interval. After three failed attempts the publisher stops with progress retained. Other API errors stop immediately. These measures reduce request pressure but cannot guarantee the absence of GitHub limits. [GitHub's guidance](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api#exceeding-the-rate-limit) requires backing off rather than continuing requests.
