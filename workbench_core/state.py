"""Durable reference jobs and scoped memory, with transactional ownership checks."""

import hashlib
import json
import sqlite3
import time

TRANSITIONS = {
    "pending": {"running", "cancelled"},
    "running": {"completed", "failed", "cancelled"},
    "failed": {"running", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}


def identity(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise ValueError("Identity must be nonempty text below 200 characters")
    return value


class StateStore:
    def __init__(self, path):
        self.connection = sqlite3.connect(path, timeout=5)
        self.connection.row_factory = sqlite3.Row
        self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, owner TEXT NOT NULL, payload_hash TEXT NOT NULL,
                payload TEXT NOT NULL, status TEXT NOT NULL, version INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS memory (owner TEXT NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL,
                expires REAL, version INTEGER NOT NULL, PRIMARY KEY(owner,key));
        """)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.connection.close()

    def create_job(self, identifier, owner, payload):
        identity(identifier)
        identity(owner)
        text = json.dumps(payload, sort_keys=True, allow_nan=False)
        if len(text) > 64000:
            raise ValueError("Job payload budget exceeded")
        fingerprint = hashlib.sha256(text.encode()).hexdigest()
        with self.connection:
            self.connection.execute("BEGIN IMMEDIATE")
            row = self.connection.execute("SELECT * FROM jobs WHERE id=?", (identifier,)).fetchone()
            if row:
                if row["owner"] != owner:
                    raise PermissionError("Job not found or not owned by caller")
                if row["payload_hash"] != fingerprint:
                    raise ValueError("Idempotency conflict: run ID already has another payload")
                return False
            self.connection.execute(
                "INSERT INTO jobs VALUES (?,?,?,?,?,?)",
                (identifier, owner, fingerprint, text, "pending", 1),
            )
        return True

    def job(self, identifier, owner):
        identity(identifier)
        identity(owner)
        row = self.connection.execute(
            "SELECT * FROM jobs WHERE id=? AND owner=?", (identifier, owner)
        ).fetchone()
        if row is None:
            raise PermissionError("Job not found or not owned by caller")
        return {**dict(row), "payload": json.loads(row["payload"])}

    def transition(self, identifier, owner, status):
        with self.connection:
            self.connection.execute("BEGIN IMMEDIATE")
            row = self.job(identifier, owner)
            if status not in TRANSITIONS[row["status"]]:
                raise ValueError("Invalid or repeated job transition")
            self.connection.execute(
                "UPDATE jobs SET status=?,version=version+1 WHERE id=? AND owner=? AND version=?",
                (status, identifier, owner, row["version"]),
            )
        return self.job(identifier, owner)

    def remember(self, owner, key, value, now=None, ttl=None):
        identity(owner)
        identity(key)
        text = json.dumps(value, allow_nan=False)
        if len(text) > 16000:
            raise ValueError("Memory value budget exceeded")
        now = time.time() if now is None else now
        if ttl is not None and (type(ttl) not in {int, float} or not 0 < ttl <= 31_536_000):
            raise ValueError("TTL must be positive and at most one year")
        expires = None if ttl is None else now + ttl
        with self.connection:
            self.connection.execute(
                """INSERT INTO memory VALUES (?,?,?,?,1) ON CONFLICT(owner,key)
                DO UPDATE SET value=excluded.value, expires=excluded.expires, version=memory.version+1""",
                (owner, key, text, expires),
            )

    def recall(self, owner, key, now=None):
        identity(owner)
        identity(key)
        now = time.time() if now is None else now
        row = self.connection.execute(
            "SELECT * FROM memory WHERE owner=? AND key=? AND (expires IS NULL OR expires>?)",
            (owner, key, now),
        ).fetchone()
        return None if row is None else {**dict(row), "value": json.loads(row["value"])}

    def forget(self, owner, key):
        identity(owner)
        identity(key)
        with self.connection:
            self.connection.execute("DELETE FROM memory WHERE owner=? AND key=?", (owner, key))
