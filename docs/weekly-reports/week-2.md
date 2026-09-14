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

# Week 2 — Inverted Index

## 1. Objective

Replace the Week 1 brute-force search approach with an inverted index.

The goal was to change the search engine from scanning every indexed document for every query to using a term-to-document mapping for direct lookup.

The intended Week 2 search flow was:

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

---

## 2. Starting Architecture

At the beginning of Week 2, the search engine from Week 1 contained:

- Document model
- In-memory document storage
- Brute-force search
- Interactive CLI
- Automated tests
- Baseline benchmark

The Week 1 search flow was:

    Query
      |
      v
    Searcher
      |
      v
    Scan every document
      |
      v
    String matching
      |
      v
    Results

The Indexer stored:

    document ID → Document

but did not have a structure for:

    term → documents containing that term

This meant every query required scanning the document collection.

---

## 3. What I Built

During Week 2, I implemented an in-memory inverted index.

The current Indexer maintains:

    documents
        document ID → Document

    inverted_index
        term → document IDs

For example:

    brown → {"1", "3"}
    dog   → {"2", "3"}

The inverted index is populated during document indexing.

Searcher was then changed to use the inverted index rather than scanning every document.

---

## 4. Day 1 — Add the Inverted Index Structure

The first change was adding an empty inverted-index structure to the Indexer.

The initial architecture became:

    Indexer
    ├── documents
    │     └── document ID → Document
    │
    └── inverted_index
          └── term → document IDs

At this stage the inverted index existed but was not populated.

The existing test suite continued to pass.

---

## 5. Day 2 — Populate the Inverted Index

The Indexer was changed to extract terms from document text using simple whitespace splitting.

For example:

    "The quick brown fox"

becomes:

    ["The", "quick", "brown", "fox"]

The resulting postings are:

    The   → {"1"}
    quick → {"1"}
    brown → {"1"}
    fox   → {"1"}

Multiple documents add their IDs to the same postings.

Repeated terms do not duplicate a document ID because postings are stored as sets.

For example:

    "brown brown brown fox"

produces:

    brown → {"1"}
    fox   → {"1"}

Analysis and normalization were intentionally not introduced at this stage.

---

## 6. Day 3 — Search Using the Inverted Index

Searcher was changed from document scanning to inverted-index lookup.

The new search path is:

    query
      |
      v
    inverted_index[query]
      |
      v
    document IDs
      |
      v
    Indexer.get()
      |
      v
    matching documents

This means Searcher no longer scans the complete document collection to locate matches.

### Behavior Change

Week 1 used substring matching.

For example:

    "dog" in "dogmatic fox"

was considered a match.

The new implementation performs exact term lookup.

Therefore:

    search("dog")

does not match:

    "dogmatic"

while:

    search("dogmatic")

does match.

This was an intentional consequence of moving from brute-force string matching to term-based inverted-index lookup.

Search also remains case-sensitive.

For example:

    Beautiful

matches:

    Beautiful

but:

    beautiful

does not.

Normalization is intentionally deferred to Week 3.

---

## 7. Day 4 — Fix Inverted Index Consistency

While testing document replacement, I encountered a consistency bug.

For example:

    index 1 "brown fox"

created:

    brown → {"1"}
    fox   → {"1"}

Then replacing the same document ID:

    index 1 "red dog"

updated the document store but originally left the old postings behind.

This could produce:

    brown → {"1"}
    fox   → {"1"}
    red   → {"1"}
    dog   → {"1"}

even though document 1 now contained only "red dog".

### Solution

When an existing document ID is replaced:

1. Retrieve the old document.
2. Extract its old terms.
3. Remove the document ID from those postings.
4. Delete postings that become empty.
5. Store the new document.
6. Add the new document's terms.

The document store and inverted index are now kept consistent during replacement.

### Additional Case

I also tested shared terms.

For example:

    document 1 → "brown fox"
    document 2 → "brown dog"

After replacing document 1 with:

    "red dog"

the result should be:

    brown → {"2"}
    dog   → {"1", "2"}
    red   → {"1"}

The shared `brown` posting remains for document 2.

---

## 8. Tests

The final test suite contains 30 tests.

Final result:

    30 passed in 0.13s

Tests cover:

- Document behavior
- Document indexing
- Document retrieval
- Document replacement
- Inverted-index initialization
- Inverted-index population
- Multiple documents
- Repeated terms
- Independent postings
- Empty documents
- Stale-posting removal
- Replacement with empty text
- Shared terms
- Exact-term search
- Unknown terms
- Case-sensitive search
- CLI behavior
- Application smoke testing

---

## 9. Experiments

### Inverted Index Inspection

The index was manually inspected after indexing multiple documents.

Example:

    The   → {"1", "2", "3"}
    quick → {"1"}
    brown → {"1", "3"}
    fox   → {"1"}
    lazy  → {"2"}
    dog   → {"2", "3"}

### Exact-Term Experiment

A document containing:

    dogmatic fox

was indexed.

Searching:

    dog

returned no result.

Searching:

    dogmatic

returned the document.

### Replacement Experiment

A document was first indexed as:

    brown fox

and then replaced with:

    red dog

The original stale postings were initially observed and later removed as part of the Day 4 fix.

---

## 10. Benchmark

The Week 2 benchmark compares:

### Brute Force

    query
      |
      v
    scan every document
      |
      v
    string matching

### Inverted Index

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

The benchmark uses:

- 10 documents
- 100 documents
- 1,000 documents
- 10,000 documents
- 20,000 documents
- 20 repetitions per measurement
- `needle` as a present query
- `notpresent` as an absent query

Before measuring performance, the benchmark verifies that both implementations return the same set of document IDs.

### Final Results

| Documents | Query | Brute Force (ms) | Inverted Index (ms) |
|----------:|:------|-----------------:|--------------------:|
| 10 | needle | 0.001460 | 0.000670 |
| 10 | notpresent | 0.000980 | 0.000415 |
| 100 | needle | 0.006240 | 0.000605 |
| 100 | notpresent | 0.006915 | 0.000375 |
| 1,000 | needle | 0.057215 | 0.000560 |
| 1,000 | notpresent | 0.063585 | 0.000425 |
| 10,000 | needle | 0.571915 | 0.000705 |
| 10,000 | notpresent | 0.619440 | 0.000505 |
| 20,000 | needle | 1.139140 | 0.000770 |
| 20,000 | notpresent | 1.226350 | 0.000485 |

Benchmark results are stored in:

    benchmarks/week2_search_comparison.csv

The benchmark implementation is:

    benchmarks/week2_search_comparison.py

---

## 11. Key Observations

The brute-force search time generally increased as the document collection grew.

For the present query:

    10 documents    → 0.001460 ms
    20,000 documents → 1.139140 ms

For the absent query:

    10 documents    → 0.000980 ms
    20,000 documents → 1.226350 ms

The inverted-index measurements remained approximately within the same small range across the tested document counts.

The absent-query experiment was particularly useful.

With brute-force search, a missing term still requires the Searcher to inspect the document collection.

With the inverted index, a missing term can be resolved through direct dictionary lookup and produce an empty postings set.

The important result is not a universal speed claim based on these small measurements.

The important observation is the difference in scaling behavior between the two search strategies.

---

## 12. Engineering Decisions

### Use an In-Memory Dictionary

The inverted index is currently implemented as:

    term → set(document IDs)

This is intentionally simple and keeps the internal mechanism visible.

### Keep the Inverted Index Inside Indexer

The inverted index currently lives alongside the document store.

This avoids introducing additional abstractions before they are necessary.

Later storage and segment architecture may justify separating these responsibilities.

### Use Sets for Postings

Sets prevent duplicate document IDs when a term occurs multiple times in the same document.

### Keep Analysis Out of Week 2

Tokenization beyond simple whitespace splitting, normalization, term frequency, document frequency, and positions were intentionally deferred.

These are part of the next analysis/postings stage.

### Preserve Meaningful Git History

Week 2 was developed through meaningful implementation, fix, and benchmark commits rather than artificial commit creation.

---

## 13. Problems / Errors Encountered

The main unexpected problem was stale postings during document replacement.

The document store correctly replaced an existing document ID, but the inverted index initially retained terms belonging to the old document.

This produced inconsistent internal state and could cause incorrect search results.

The problem was deliberately investigated and then fixed.

Another behavior change was discovered when the new exact-term search no longer matched substrings such as `dog` inside `dogmatic`.

This was not treated as a bug because the new search model is term-based.

---

## 14. What I Would Change

The current implementation is intentionally small.

Potential future improvements include:

- Dedicated analysis/tokenization pipeline
- Normalization
- Term frequency
- Document frequency
- Positional postings
- Better query execution
- Ranking
- Persistence
- Segments

These are not being added yet because they belong to later stages of the project.

---

## 15. Current Architecture

    USER
      |
      v
     CLI
      |
      +----------------+
      |                |
      v                v
   Indexer          Searcher
      |                |
      |                v
      |         inverted index lookup
      |                |
      |                v
      |          document IDs
      |                |
      +-------+--------+
              |
              v
          Documents

Indexer:

    documents
        document ID → Document

    inverted_index
        term → document IDs

Current search:

    query
      ↓
    inverted index
      ↓
    document IDs
      ↓
    documents

---

## 16. Week 2 Planned vs Actually Completed

### Planned

- Create inverted index
- Populate inverted index
- Replace brute-force search
- Benchmark both approaches
- Document observations

### Actually Completed

All planned work was completed.

Additionally, implementation exposed a document-replacement consistency bug that was investigated, fixed, and covered with regression tests.

The project therefore did not simply implement the planned data structure; it also tested the relationship between the document store and its derived inverted-index state.

---

## 17. Week 2 Outcome

Week 2 successfully moved the search engine from document-oriented brute-force scanning to term-oriented inverted-index lookup.

The engine now has a basic internal search structure that can directly map terms to documents.

The implementation remains intentionally simple and in-memory so that the mechanism can still be understood completely.

---

## 18. Next Week

Week 3 will introduce the analysis and postings layer.

Planned areas include:

- Tokenization
- Lowercase/normalization
- Term frequency
- Document frequency
- Positional information

The next architectural progression is:

    raw text
       ↓
    tokenizer
       ↓
    normalization
       ↓
    tokens
       ↓
    postings
       ↓
    positions

Week 3 will build on the inverted index created during this week.