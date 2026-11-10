"""Allowlisted tool contracts and stream lifecycle validation."""

from .validation import validate_schema


class ToolRegistry:
    """Local contract boundary; caller permissions must come from trusted application code."""

    def __init__(self):
        self.tools = {}

    def register(self, name, schema, function, write=False):
        if (
            not isinstance(name, str)
            or not name
            or len(name) > 100
            or name in self.tools
            or not callable(function)
        ):
            raise ValueError("Invalid or duplicate tool registration")
        self.tools[name] = {"schema": schema, "function": function, "write": write}

    def call(self, name, arguments, allow_write=False):
        if not isinstance(name, str) or name not in self.tools:
            raise ValueError("Unknown tool")
        tool = self.tools[name]
        if tool["write"] and allow_write is not True:
            raise PermissionError("Write tool requires explicit application authorization")
        errors = validate_schema(arguments, tool["schema"])
        if errors:
            raise ValueError("; ".join(errors))
        return tool["function"](**arguments)


def stream_state(events):
    if not isinstance(events, list) or not 1 <= len(events) <= 10000:
        raise ValueError("Supply a bounded stream-event list")
    state, answer, thinking, fixture = "idle", "", "", None
    for event in events:
        if not isinstance(event, dict):
            raise ValueError("Stream events must be objects")
        kind = event.get("type")
        if state in {"completed", "failed"}:
            raise ValueError("Event arrived after a terminal state")
        if kind == "start" and state == "idle":
            state = "streaming"
            fixture = event.get("fixture")
        elif kind == "delta" and state == "streaming":
            if event.get("channel") not in {"answer", "thinking"} or not isinstance(
                event.get("text"), str
            ):
                raise ValueError("Invalid stream delta")
            if event["channel"] == "answer":
                answer += event["text"]
            else:
                thinking += event["text"]
            if len(answer) + len(thinking) > 200000:
                raise ValueError("Stream output budget exceeded")
        elif kind in {"done", "error"} and state == "streaming":
            if "fixture" in event and fixture is not None and event["fixture"] != fixture:
                raise ValueError("Stream source label changed during generation")
            state = "completed" if kind == "done" else "failed"
        else:
            raise ValueError("Invalid stream lifecycle transition")
    return {
        "status": state if state != "streaming" else "interrupted",
        "answer": answer,
        "thinking": thinking,
        "can_commit_history": state == "completed" and bool(answer.strip()),
        "fixture": fixture,
    }
