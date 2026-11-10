# UI learning design contract

The new interfaces are small inference notebooks for studying the original projects. They retain each project's model/capability focus and preserve the original Chainlit, Streamlit or Motia source as reference. Their working local implementation separates transport, stream parsing and presentation so a learner can trace each boundary.

The upstream chat screens are the supplied visual references: one conversation surface, model context and expandable model-provided trace. The improved direction is a quiet paper-and-ink workspace: warm neutral background, dark text, restrained green actions, compact monospace experiment labels and generous reading width. Avoid promotional heroes, decorative gradients and large card grids.

Primary action: submit a prompt (and an image for vision projects). The conversation is the main column. A collapsible experiment desk exposes the project's learning goal, a controlled experiment, sampling controls and observed timing/token metadata. The model-provided trace is collapsed and labeled as generated output, never evidence of correctness.

Required states: initial guidance, generation in progress, complete response, failed response, interrupted response, cleared conversation and explicit fixture mode. Incomplete responses never enter future model history. Separate browser tabs keep separate in-memory histories; no conversation is automatically persisted in local storage.

Responsive rules: one column at narrow widths; two columns only when both remain readable. Test 320, 768, 1024 and 1440 pixels. Controls wrap, text never forces horizontal page scrolling, and the composer remains reachable without overlapping content.

Accessibility: semantic headings and landmarks, visible input labels, visible keyboard focus, text status alongside color, polite status announcements, buttons for actions, an accessible file input and reduced-motion support. Render generated content as text rather than executable HTML.

Verification uses an isolated Chrome profile through Playwright because a Chrome DevTools MCP connector is not configured. Fixture responses are labeled and do not establish model quality. Read-only model discovery and any actual local inference are recorded separately.
