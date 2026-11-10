"""Dependency-free reference implementation of token-level MaxSim reranking.

Uses dot products without implicit normalization. Supply identically preprocessed
query/document vectors. Padding must be masked out, especially with negative scores.
The original PyTorch tutorial remains in colbert.py for comparison.
"""

import math
from collections.abc import Sequence


def _vectors(values, dimension=None):
    if not isinstance(values, Sequence) or not values:
        raise ValueError('At least one token vector is required')
    result = []
    for vector in values:
        if not isinstance(vector, Sequence) or not vector:
            raise ValueError('Token vectors must be nonempty sequences')
        if dimension is None:
            dimension = len(vector)
        if len(vector) != dimension:
            raise ValueError('All query/document vector dimensions must agree')
        if any(type(v) not in {int, float} or not math.isfinite(v) for v in vector):
            raise ValueError('Embedding values must be finite numbers')
        result.append(tuple(float(v) for v in vector))
    return result


def score_document(query, document, mask=None) -> float:
    """Sum each query token's best real document-token dot product."""
    query_vectors = _vectors(query)
    document_vectors = _vectors(document, len(query_vectors[0]))
    if mask is None:
        mask = [True] * len(document_vectors)
    if len(mask) != len(document_vectors) or any(type(value) is not bool for value in mask):
        raise ValueError('Mask must contain one boolean per document token')
    real_tokens = [vector for vector, keep in zip(document_vectors, mask) if keep]
    if not real_tokens:
        raise ValueError('Document must have at least one unmasked token')
    total = sum(max(sum(q * d for q, d in zip(query_token, token)) for token in real_tokens)
                for query_token in query_vectors)
    if not math.isfinite(total):
        raise ValueError('Similarity score overflowed; normalize or bound the input vectors')
    return total


def rank_documents(query, documents, k, masks=None):
    """Return (original_index, score) pairs for top k, with stable index tie breaks."""
    if type(k) is not int or not 1 <= k <= len(documents):
        raise ValueError('k must be between 1 and the number of documents')
    if masks is None:
        masks = [None] * len(documents)
    if len(masks) != len(documents):
        raise ValueError('Supply one mask per document')
    scores = [(index, score_document(query, document, mask))
              for index, (document, mask) in enumerate(zip(documents, masks))]
    return sorted(scores, key=lambda item: (-item[1], item[0]))[:k]


if __name__ == '__main__':
    print(rank_documents([[1, 0], [0, 1]], [[[2, 0]], [[2, 0], [0, 3]]], k=2))
