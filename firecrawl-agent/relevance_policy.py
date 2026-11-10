"""A strict relevance gate shared by context selection and fallback routing."""


def is_relevant_grade(grade: str) -> bool:
    return isinstance(grade, str) and grade.strip().lower() == 'yes'


def needs_web_search(grades) -> bool:
    """No evidence or an invalid grader response must trigger evidence recovery."""
    return not any(is_relevant_grade(grade) for grade in grades)
