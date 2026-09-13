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

## Day 4 — Fix Inverted Index Consistency

### Objective

Fix stale postings when an existing document ID is replaced.

### Problem

When a document was indexed using an existing ID, the document store replaced the old document but the inverted index retained postings belonging to the old document.

For example:

    index 1 "brown fox"
    index 1 "red dog"

Previously this could leave:

    brown → {"1"}
    fox → {"1"}
    red → {"1"}
    dog → {"1"}

This was inconsistent because document 1 no longer contained brown or fox.

### Implementation

When replacing an existing document:

1. Retrieve the old document.
2. Extract its terms.
3. Remove the document ID from each old term's postings.
4. Remove terms whose postings become empty.
5. Store the new document.
6. Add the new document's terms to the inverted index.

### Invariant

The inverted index should only associate a document ID with terms that occur in the current version of that document.

### Important Observation

The document store and inverted index represent related but separate pieces of state.

Updating one without updating the other creates inconsistent search behavior.

### Status

Day 4 complete.

### Next Step

Day 5 will benchmark brute-force search against inverted-index search using the same methodology as the Week 1 baseline.

## Day 5 — Benchmark Brute-Force vs Inverted-Index Search

### Objective

Measure the performance difference between the Week 1 brute-force search implementation and the Week 2 inverted-index search implementation.

### Methodology

The benchmark compares both approaches using the same indexed document collections.

Document counts:

- 10
- 100
- 1,000
- 10,000
- 20,000

Each measurement uses 20 repetitions.

Queries:

- `needle` — present in one document
- `notpresent` — absent from the collection

Search time is measured using Python's `time.perf_counter()`.

### Implementations Compared

#### Brute Force

    query
      |
      v
    scan every document
      |
      v
    check document text

#### Inverted Index

    query
      |
      v
    inverted index lookup
      |
      v
    document IDs
      |
      v
    documents

### Correctness Verification

Before measuring performance, the benchmark compares the document IDs returned by both implementations.

The benchmark asserts that both implementations return the same set of matching document IDs.

### Results

Results are stored in:

    benchmarks/week2_search_comparison.csv

### Observations

Record observations based on the actual benchmark results.

Questions considered:

- How does brute-force search time change as document count increases?
- How does inverted-index search time change?
- Is the difference noticeable at small document counts?
- Does the difference become more noticeable at larger document counts?
- How do present and absent queries compare?

### Key Engineering Observation

The inverted index changes the search operation from scanning the document collection to directly locating documents associated with a term.

The benchmark provides experimental evidence for the effect of this architectural change.

### Status

Day 5 complete.

### Next Step

Day 6 will review the entire Week 2 implementation, compare planned work with completed work, run the final test suite and benchmark, finalize documentation, and prepare the Week 2 publication.