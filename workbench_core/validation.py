"""Strict schema subset and bounded read-only SQLite, independent of an LLM."""

import math
import sqlite3
import time
from pathlib import Path

KEYWORDS = {
    "type",
    "properties",
    "required",
    "additionalProperties",
    "items",
    "enum",
    "minimum",
    "maximum",
    "minLength",
    "maxLength",
    "minItems",
    "maxItems",
}


def validate_schema(value, schema):
    """Validate an explicit JSON Schema subset; reject unsupported schema keywords."""
    errors, visited = [], 0

    def schema_check(contract, depth=0):
        nonlocal visited
        visited += 1
        if depth > 12 or visited > 10000:
            raise ValueError("Schema validation budget exceeded")
        if not isinstance(contract, dict) or set(contract) - KEYWORDS:
            raise ValueError("Unsupported schema keyword or schema shape")
        if "type" in contract and (
            not isinstance(contract["type"], str)
            or contract["type"]
            not in {"object", "array", "string", "integer", "number", "boolean", "null"}
        ):
            raise ValueError("Unsupported schema type")
        if "enum" in contract and (
            not isinstance(contract["enum"], list) or not 1 <= len(contract["enum"]) <= 1000
        ):
            raise ValueError("Enum requires a bounded nonempty list")
        if (
            "additionalProperties" in contract
            and type(contract["additionalProperties"]) is not bool
        ):
            raise ValueError("Only boolean additionalProperties is supported")
        for key in ("minimum", "maximum"):
            if key in contract and (
                type(contract[key]) not in {int, float} or not -1e100 <= contract[key] <= 1e100
            ):
                raise ValueError("Numeric schema bounds must be finite and bounded")
        for key in ("minLength", "maxLength", "minItems", "maxItems"):
            if key in contract and (
                type(contract[key]) is not int or not 0 <= contract[key] <= 100000
            ):
                raise ValueError("Length schema bounds must be nonnegative integers")
        properties, required = contract.get("properties", {}), contract.get("required", [])
        if (
            not isinstance(properties, dict)
            or not all(isinstance(key, str) for key in properties)
            or not isinstance(required, list)
            or not all(isinstance(key, str) for key in required)
        ):
            raise ValueError("Invalid object schema")
        for child in properties.values():
            schema_check(child, depth + 1)
        if "items" in contract:
            schema_check(contract["items"], depth + 1)

    def check(item, contract, pointer="$", depth=0):
        nonlocal visited
        visited += 1
        if depth > 12 or visited > 10000:
            raise ValueError("Schema validation budget exceeded")
        if not isinstance(contract, dict) or set(contract) - KEYWORDS:
            raise ValueError("Unsupported schema keyword or schema shape")
        kind = contract.get("type")
        types = {
            "object": lambda x: isinstance(x, dict),
            "array": lambda x: isinstance(x, list),
            "string": lambda x: isinstance(x, str),
            "integer": lambda x: type(x) is int,
            "number": lambda x: type(x) is int or type(x) is float and math.isfinite(x),
            "boolean": lambda x: type(x) is bool,
            "null": lambda x: x is None,
        }
        if kind is not None and (not isinstance(kind, str) or kind not in types):
            raise ValueError("Unsupported schema type")
        if kind is not None and not types[kind](item):
            errors.append(pointer + ": expected " + kind)
            return
        if "enum" in contract and not any(
            type(item) is type(v) and item == v for v in contract["enum"]
        ):
            errors.append(pointer + ": value outside enum")
        if isinstance(item, dict):
            properties = contract.get("properties", {})
            required = contract.get("required", [])
            if (
                not isinstance(properties, dict)
                or not isinstance(required, list)
                or not all(isinstance(k, str) for k in required)
            ):
                raise ValueError("Invalid object schema")
            errors.extend(pointer + ": missing " + key for key in required if key not in item)
            if contract.get("additionalProperties") is False:
                errors.extend(
                    pointer + ": unexpected " + str(key) for key in item if key not in properties
                )
            for key, child in item.items():
                if key in properties:
                    check(child, properties[key], pointer + "." + key, depth + 1)
        elif isinstance(item, list):
            if len(item) > 10000:
                raise ValueError("Array validation budget exceeded")
            for index, child in enumerate(item):
                if "items" in contract:
                    check(child, contract["items"], f"{pointer}[{index}]", depth + 1)
            for key, passed in (
                ("minItems", len(item) >= contract.get("minItems", 0)),
                ("maxItems", len(item) <= contract.get("maxItems", 10000)),
            ):
                if not passed:
                    errors.append(pointer + ": " + key + " failed")
        elif isinstance(item, str):
            if len(item) < contract.get("minLength", 0) or len(item) > contract.get(
                "maxLength", 100000
            ):
                errors.append(pointer + ": string length outside schema bounds")
        elif type(item) in {int, float}:
            if (
                (type(item) is float and not math.isfinite(item))
                or item < contract.get("minimum", -math.inf)
                or item > contract.get("maximum", math.inf)
            ):
                errors.append(pointer + ": numeric value outside schema bounds")

    schema_check(schema)
    visited = 0
    check(value, schema)
    return errors


def readonly_query(path, statement, parameters=(), max_rows=100, timeout=1):
    if not isinstance(statement, str) or not statement.strip() or len(statement) > 8000:
        raise ValueError("Query must contain 1–8000 characters")
    if type(max_rows) is not int or not 1 <= max_rows <= 1000 or not 0 < timeout <= 5:
        raise ValueError("Invalid query resource limit")
    path = Path(path).resolve(strict=True)
    connection = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=timeout)
    connection.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 1_000_000)
    connection.setlimit(sqlite3.SQLITE_LIMIT_COLUMN, 100)
    deadline = time.monotonic() + timeout
    allowed_functions = {
        "count",
        "sum",
        "avg",
        "min",
        "max",
        "length",
        "lower",
        "upper",
        "coalesce",
        "round",
        "abs",
    }

    def authorize(action, first, second, *_):
        if action in {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_RECURSIVE}:
            return sqlite3.SQLITE_OK
        if action == sqlite3.SQLITE_FUNCTION and second in allowed_functions:
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY

    connection.set_authorizer(authorize)
    connection.set_progress_handler(lambda: int(time.monotonic() > deadline), 1000)
    try:
        cursor = connection.execute(statement, parameters)
        rows = cursor.fetchmany(max_rows + 1)
        return {
            "columns": [column[0] for column in cursor.description],
            "rows": [list(row) for row in rows[:max_rows]],
            "truncated": len(rows) > max_rows,
        }
    except sqlite3.Error as error:
        raise ValueError(
            "Read-only query rejected or its budget was exceeded: " + str(error)
        ) from None
    finally:
        connection.close()
