# Interactive AI engineering interview handbook

## Objective and scope

Create the collection's root `index.html` as a complete offline revision entry point for every current project. Cover beginners through advanced AI engineering interviews with explanations, worked examples, implementation reasoning, practical commands, failure analysis, production tradeoffs and answer rubrics. Embed the substantive project guides so reading them does not require opening Markdown files or a network connection. Interview readiness is demonstrated through explanation and experiments, never a promised hiring result.

## Capabilities and build order

| Capability | Responsibility | Depends on |
| --- | --- | --- |
| content | Reconcile project folders, curate technical chapters and sources, derive commands from retained manifests/entries | Existing repository evidence |
| reader | Offline search, project/topic navigation, learning paths, embedded guide reader and command copying | content |
| practice | Question bank, revealable model answers, confidence and interactive metric/capacity examples | content, reader |
| revision | Local notes/bookmarks/progress with validated JSON export/import and storage-failure recovery | reader |
| verification | Content/security checks and real-browser functional, responsive and accessibility evidence | All above |

## Design contract

An editorial field manual: warm paper, dark forest navigation, restrained amber accents, serif reading titles and compact tabular project lists. Reference structure comes from the repository's existing learning workspaces and documentation sites: persistent table of contents, explicit active location, visible reading hierarchy and progressive disclosure. Avoid a decorative dashboard/card grid. Primary action is choosing a project or subject to revise. Search, empty results, unknown links, copy failure, saved notes and unavailable storage all need explicit states.

Use system-installed Georgia/Cambria, Trebuchet/Verdana and Consolas so fonts require no download. At small widths the navigation becomes an accessible disclosure and all content fits 320px. Respect reduced motion. Keyboard focus, labeled controls, headings, current navigation and status announcements are required. Print the current reading view. No remote fonts, scripts, styles, images, analytics or inference calls.

## Implementation and boundaries

Maintain authoring sources under `tools/interview/`; a stdlib Python builder produces one self-contained root HTML file. Embed escaped JSON and render only a bounded, escaped Markdown subset. Source content and imported notes cannot become executable HTML. A restrictive CSP permits only the bundled hashed script and local inline styling; no connections or form submissions. Browser-local study data has no authentication role and contains only explicitly typed notes/status. Do not read or embed personal journals, environment values, user-edited verification files or Git metadata.

Command blocks distinguish collection-root offline checks, environment preparation, original application/notebook candidates, fixture UI and live inference. Enumerate all original entry candidates; retain setup and compatibility limits instead of inventing missing dependency manifests. Native OCR commands use their real project directories and local virtual environments. The four OCR repositories and pre-existing modified enhancement report remain untouched.

## Commands and verification

- Build: `python -m tools.build_interview`
- Verify generated file: `python -m tools.build_interview --check`
- Unit tests: `python -m unittest discover -s tests -p test_interview_handbook.py -v`
- Browser: `node tools/browser-tests/interview.mjs` using existing pinned Playwright/axe and an isolated Chrome profile.
- Collection regressions: `.\run.ps1 test`.

Acceptance: all 113 current projects represented and folder inventory reconciled; substantive explanations and commands embedded; at least 40 structured technical chapters and 3 answered questions per chapter/project; beginner/intermediate/advanced paths; useful metric/capacity calculators; working search/filter/deep-link/back navigation; local notes/bookmarks/progress and safe export/import; no external requests during offline use; correct formulas; no console errors, automated accessibility violations or horizontal page overflow at 320/768/1024/1440px. Verify direct `file://` opening and loopback HTTP. Preserve the user's existing changes and commit only this task on main.
