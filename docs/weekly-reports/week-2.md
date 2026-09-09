# Week 2 — Inverted Index

## Day 1 — Inverted Index Structure

### Objective

Introduce the basic data structure required to replace the brute-force
search architecture from Week 1.

The goal for Day 1 was not to implement inverted-index searching yet,
but to introduce the structure that will eventually map:

term → document IDs

### Starting Architecture

The Week 1 Indexer stored documents in an in-memory dictionary:

documents

document ID → Document

The Searcher then scanned every stored document and performed
substring matching.

### Today's Change

Added an `inverted_index` structure to the `Indexer`.

The current `Indexer` now contains:

documents
    document ID → Document

inverted_index
    term → document IDs

At the end of Day 1, the inverted index is intentionally empty because
term extraction and inverted-index population will be implemented on
Day 2.

### Current Architecture

                    Indexer
                   /       \
                  /         \
                 ▼           ▼
          Document Store   Inverted Index
                │                │
                ▼                ▼
         ID → Document       Currently empty

The existing document store remains unchanged.

The Searcher still uses the Week 1 brute-force implementation.
Search behavior was not changed on Day 1.

### Data Structure Decision

The inverted index will eventually represent postings as a set of
document IDs.

Example:

brown → {"1", "3"}

A set is appropriate for the current Week 2 design because the current
goal is to represent document membership:

"Which documents contain this term?"

Term frequency and positional information are intentionally not part
of this day's implementation.

### Manual Experiments

Inspected the existing document store and confirmed that it is a
dictionary mapping string document IDs to `Document` objects.

For example:

"1" → Document("1", "The quick brown fox")

Attempting to access the dictionary as if it were a Document produced
an AttributeError.

Attempting to access integer keys such as `0` or `1` produced KeyError
because the document IDs are strings.

Accessing the correct string key successfully retrieved the document:

indexer.documents["1"].text

Result:

The quick brown fox

These experiments confirmed the current structure of the document
store.

### Testing

Ran the complete test suite:

    python -m pytest

Result:

    22 passed in 0.10s

All existing Week 1 tests continue to pass after introducing the
new inverted-index structure.

### Important Observation

The inverted index currently exists but is not populated.

For example:

documents
    {"1": Document(...)}

inverted_index
    {}

This is intentional.

Day 1 establishes the new structure. Day 2 will make document indexing
populate the inverted index.

### What I Learned

The current document store is a forward representation:

document ID → document

An inverted index introduces the opposite direction:

term → documents containing the term

This change is the foundation for moving away from scanning the entire
document collection during search.

### Day 1 Status

Completed.

- Added inverted index structure
- Preserved existing document storage
- Preserved Week 1 search behavior
- Added test coverage for the new structure
- Ran the complete test suite
- 22 tests passed

### Next Step

Day 2 — Populate the inverted index when documents are indexed.