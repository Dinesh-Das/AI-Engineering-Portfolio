"""Keep the learning aspect explicit when project guides evolve."""

import re

REQUIRED_SECTIONS = (
    'The core lesson', 'Rebuild it yourself', 'Project-specific experiment',
    'What to measure', 'Failure modes to understand', 'Learn from every scenario', 'Better production deployment',
    'Deployment tradeoffs', 'Release and rollback evidence',
)


def validate_learning(text: str) -> list[str]:
    sections = {match.group(1).strip(): match.group(2).strip() for match in re.finditer(
        r'^## ([^\n]+)\n(.*?)(?=^## |\Z)', text, re.M | re.S)}
    return [f'Missing or empty learning section: {heading}' for heading in REQUIRED_SECTIONS
            if len(sections.get(heading, '')) < 30]
