# Offline interview handbook verification

The root `index.html` is the reader-facing deliverable. It is self-contained and works by direct file opening, with optional source/reference links. Its maintained authoring source is described in [the maintenance guide](../tools/interview/README.md). This page records UI/content evidence, not live model or hiring outcomes.

## Coverage

- All 113 current project folders are reconciled against the catalog and local OCR repositories.
- 46 technical chapters cover foundations, training, retrieval, agents/tools, evaluation/operations, multimodal work and interview craft.
- 477 answered questions include Foundation, Applied and Advanced prompts for every chapter and project.
- 574 annotated command blocks distinguish offline contracts, diagnostics, setup, fixtures, notebooks, original source candidates and live application paths.
- Six substantive guide views per project are embedded, using the existing setup/source/learning/evaluation/enhancement material, pinned author instructions where retained, or documented native implementation contracts/local setup fallbacks. Personal journals and environment values are excluded.
- Four revision paths, project/topic search and filters, deep links/history, mock practice/timer, local notes/bookmarks/progress and validated JSON backup/import are included.
- Four interactive examples calculate confusion-matrix metrics, ranking quality, simplified KV/attention storage and illustrative token economics/concurrency.

## Evidence

The [browser report](interview-browser-validation.json) is fingerprinted to the exact generated HTML. It records 12 passing scenario groups using the repository's pinned Playwright/axe dependencies and an isolated Chrome profile. Tests open both `file://` and loopback HTTP, visit all 113 project readers and command panels, exercise representative embedded guides/chapters and confirm search/filter/back/forward behavior. They test notes persistence, copy behavior, mock answers/confidence/timer, independently known arithmetic, invalid imports, hostile note text and unavailable storage. Displayed AI commands are never executed by the page or browser suite.

Responsive checks cover 320, 768, 1024 and 1440px with no horizontal page overflow. Automated WCAG A/AA checks pass on the home, chapter, command, practice, calculator, revision and mobile calculator views. Keyboard search/menu behavior and visual screenshots were reviewed. The report records zero console errors and zero external requests. This is automated and selected manual verification, not a formal accessibility certification.

Content/security tests verify full inventory, answered depth at all three levels, command annotations, private-file exclusion, escaped Markdown/links, data-script termination defense and absence of remote script/style dependencies. `.\run.ps1 handbook --check` verifies regeneration freshness. `.\run.ps1 verify` checks both current content and browser evidence. The one-extra-argument PowerShell forwarding case was corrected and verified through the real `handbook --check` command.

## Reproduce

```powershell
.\run.ps1 handbook
.\run.ps1 handbook --check
node tools/browser-tests/interview.mjs
.\run.ps1 test
.\run.ps1 verify
```

Browser testing requires the already configured Node dependencies and Chrome; reading `index.html` does not. Original applications still need their own compatible dependencies, models, credentials/hardware and integration/quality tests. Proposed deployment designs and sample prices are labeled. Existing journals, OCR work and the user's modified enhancement report/verification files are preserved.

Final collection regression result: 82 tests passed with one existing Windows symlink-permission skip. The seven handbook content/security tests also passed after the final author-guide/redaction changes. Preservation hashes confirm all 113 existing personal journals plus the three pre-existing user-edited report/verification files are byte-identical.
