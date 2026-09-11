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


## Day 2 — Populate the Inverted Index

### Objective

Make the Indexer populate the inverted index when documents
are indexed.

### Implementation

The `Indexer` now maintains two structures:

documents:

document ID → Document

inverted_index:

term → document IDs

Terms are currently extracted using simple whitespace splitting.

Example:

"The quick brown fox"

becomes:

["The", "quick", "brown", "fox"]

The corresponding inverted-index entries are:

The → {"1"}
quick → {"1"}
brown → {"1"}
fox → {"1"}

### Multiple Documents

When multiple documents contain the same term, their document IDs
are stored in the same posting.

Example:

brown → {"1", "3"}
dog → {"2", "3"}

### Duplicate Terms

A set is used for document IDs.

Therefore, if a document contains:

"brown brown brown fox"

the inverted index contains:

brown → {"1"}
fox → {"1"}

rather than storing the same document ID multiple times.

Term frequency is intentionally not tracked yet.

### Current Architecture

                    Indexer
                   /       \
                  /         \
                 ▼           ▼
          Document Store   Inverted Index
                 │           │
                 │           └── term → document IDs
                 │
                 └───────────────┐
                                 ▼
                             Documents

The Searcher still uses the Week 1 brute-force implementation.

### Key Observation

The inverted index is now populated during indexing, but search
does not use it yet.

This creates the foundation for changing the search path on Day 3.

### Next Step

Day 3 — Replace brute-force search with inverted-index lookup.

## Day 3 — Search Using the Inverted Index

### Objective

Change search from scanning every document to using the inverted index to directly locate documents containing the queried term.

### Starting Point

The inverted index was populated during Day 2, but Searcher still used the Week 1 brute-force approach.

### Implementation

Searcher was changed to:

1. Look up the query term in the inverted index.
2. Retrieve matching document IDs.
3. Retrieve the corresponding Document objects.
4. Return the matching documents.

The new search path is:

    query
      |
      v
    inverted index
      |
      v
    document IDs
      |
      v
    documents

### Behavior Change

Week 1 used substring matching through:

    query in document.text

The new implementation uses exact term lookup.

For example, a document containing:

    dogmatic

does not match:

    dog

but does match:

    dogmatic

This is an intentional consequence of moving from brute-force substring search to term-based lookup.

### Case Sensitivity

Search remains case-sensitive.

For example:

    Beautiful

matches:

    Beautiful

but:

    beautiful

does not.

Normalization is intentionally deferred to Week 3.

### Important Observation

Searcher no longer needs to scan every indexed document.

The query is first resolved through the inverted index to obtain candidate document IDs.

### Known Issue

Duplicate document IDs can still leave stale postings in the inverted index.

This issue was intentionally left for Day 4.

### Status

Day 3 complete.

### Next Step

Day 4 will investigate and fix inverted-index consistency when an existing document ID is replaced.