"""A lexical BM25 baseline with versioned provenance and pre-ranking tenant filters.

This is a CPU reference, not a replacement for the projects' multimodal/embedding models.
"""

import hashlib
import math
import re
from collections import Counter

from .io import read_json, write_json


def terms(text):
    return re.findall(r"\w+", text.casefold(), flags=re.UNICODE)


class EvidenceIndex:
    def __init__(self, documents):
        if not isinstance(documents, list) or len(documents) > 10000:
            raise ValueError("Evidence corpus must be a list with at most 10000 documents")
        self.documents = []
        identifiers, total = set(), 0
        for document in documents:
            if not isinstance(document, dict):
                raise ValueError("Each document must be an object")
            for key in ("id", "tenant", "text"):
                if not isinstance(document.get(key), str) or not document[key].strip():
                    raise ValueError("Every document needs a nonempty id, tenant and text")
            if document["id"] in identifiers:
                raise ValueError(
                    "Duplicate document IDs are not accepted; update the source explicitly"
                )
            identifiers.add(document["id"])
            total += len(document["text"])
            if len(document["text"]) > 100000 or total > 4_000_000:
                raise ValueError("Evidence corpus text budget exceeded")
            record = dict(document)
            record["content_hash"] = hashlib.sha256(record["text"].encode()).hexdigest()
            self.documents.append(record)

    def search(self, query, tenant, k=5, context_chars=4000):
        if not isinstance(query, str) or not query.strip() or len(query) > 4000:
            raise ValueError("Query must contain 1–4000 characters")
        if not isinstance(tenant, str) or not tenant.strip():
            raise ValueError("Tenant is required")
        if (
            type(k) is not int
            or not 1 <= k <= 100
            or type(context_chars) is not int
            or not 1 <= context_chars <= 100000
        ):
            raise ValueError("Invalid retrieval/context budget")
        # Scope both the result set and scoring statistics, avoiding cross-tenant score leakage.
        corpus = [d for d in self.documents if d["tenant"] == tenant]
        if not corpus:
            return []
        counts = [Counter(terms(d["text"])) for d in corpus]
        lengths = [sum(count.values()) for count in counts]
        average = sum(lengths) / len(lengths) or 1
        query_terms = set(terms(query))
        frequency = {term: sum(term in count for count in counts) for term in query_terms}
        ranked = []
        for document, count, length in zip(corpus, counts, lengths):
            score = 0.0
            for term in query_terms:
                tf = count[term]
                if tf:
                    inverse = math.log(
                        1 + (len(corpus) - frequency[term] + 0.5) / (frequency[term] + 0.5)
                    )
                    score += inverse * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * length / average))
            if score > 0:
                ranked.append({**document, "score": score})
        ranked.sort(key=lambda d: (-d["score"], d["id"]))
        selected, remaining = [], context_chars
        for document in ranked[:k]:
            text = document["text"][:remaining]
            if not text:
                break
            selected.append(
                {**document, "text": text, "truncated": len(text) < len(document["text"])}
            )
            remaining -= len(text)
        return selected

    def save(self, path):
        write_json(
            path,
            {
                "schema_version": 1,
                "retrieval": "lexical-bm25-reference",
                "documents": self.documents,
            },
        )

    @classmethod
    def load(cls, path):
        data = read_json(path)
        if data.get("schema_version") != 1 or data.get("retrieval") != "lexical-bm25-reference":
            raise ValueError("Index version or retrieval method is incompatible")
        for record in data.get("documents", []):
            if record.get("content_hash") != hashlib.sha256(record["text"].encode()).hexdigest():
                raise ValueError("Document hash mismatch")
        return cls(data["documents"])
