# Educational Search Engine

An educational search engine built from scratch in Python.

The project explores the internal mechanisms behind search engines,
inspired by core ideas found in Elasticsearch and Lucene.

Neither Elasticsearch nor Lucene is used as an implementation dependency.

## Current Status

### Week 2 — Inverted Index: Complete**

The current engine supports:

- Document creation
- Document indexing
- Document retrieval by ID
- In-memory document storage
- In-memory inverted index
- Exact-term search
- Interactive command-line interface
- Automated tests
- Search benchmarking
- Document replacement with inverted-index consistency
- Weekly engineering documentation

Final Week 2 test result:

```text
  30 passed in 0.13s
  ```

## Current Architecture

```text
                         USER
                           |
                           v
                          CLI
                     /           \
                    /             \
                 index           search
                   |               |
                   v               v
                Indexer         Searcher
                   |               |
          +--------+--------+      |
          |                 |      |
          v                 v      v
      Documents      Inverted Index
          |                 |      |
          |           term → IDs   |
          |                 |      |
          +---------+-------+------+
                    |
                    v
                Documents
  ```

## Search Flow

Week 1 used brute-force search:

```text
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
```
Week 2 changed the search path to use the inverted index:

Query
  |
  v
Inverted Index
  |
  v
Document IDs
  |
  v
Documents
  |
  v
Results

For example, the inverted index can contain:

brown → {"1", "3"}
dog   → {"2", "3"}

A search for brown can therefore locate the matching document IDs directly instead of scanning the entire document collection.

## Current Search Semantics

Search currently uses exact terms rather than substring matching.

For example, a document containing:

The dogmatic fox

contains the term dogmatic, but not the term dog.

Therefore:

search dog

does not match the document, while:

search dogmatic

does.

Search is also currently case-sensitive.

For example:

Beautiful

and:

beautiful

are treated as different terms.

Tokenization and normalization are intentionally deferred to Week 3.

## Example

Start the engine with:

python -m src.search_engine.main

Example session:

> index 1 "The quick brown fox"
Indexed document 1

> index 2 "The lazy dog"
Indexed document 2

> index 3 "The brown dog"
Indexed document 3

> search brown
1: The quick brown fox
3: The brown dog

> search dog
2: The lazy dog
3: The brown dog

> count
Documents: 3

> exit
Goodbye!

## Testing

The project currently has automated tests covering:

Document behavior
Indexer behavior
Inverted-index population
Document replacement
Stale-posting cleanup
Search behavior
Exact-term matching
Case sensitivity
CLI behavior
Basic application smoke testing

Run the test suite with:

python -m pytest

Final Week 2 result:

30 passed in 0.13s

## Benchmarking

Week 1 established the brute-force search baseline.

Week 2 compares the original brute-force implementation with the new inverted-index implementation.

The Week 2 benchmark uses:

10 documents
100 documents
1,000 documents
10,000 documents
20,000 documents
20 repetitions per measurement
Present query: needle
Absent query: notpresent

## Week 2 Results

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

The benchmark verifies that both implementations return the same logical set of matching document IDs before comparing their search times.

The measurements show that brute-force search time generally increases as the document collection grows, while inverted-index lookup remains approximately within the same small range across the tested sizes.

These measurements are from the development environment and are not intended as universal performance claims.

Week 1 baseline results are stored in:

benchmarks/week1_search_baseline.csv

Week 2 comparison results are stored in:

benchmarks/week2_search_comparison.csv

Run the Week 1 benchmark with:

python -m benchmarks.benchmark_search

Run the Week 2 comparison with:

python -m benchmarks.week2_search_comparison

## What I Learned

A search engine can produce correct results while still having an inefficient internal architecture.

In Week 1, the Indexer stored documents by ID, but the Searcher had no structure that told it which documents contained a searched term.

Therefore, even a query with no matching documents required scanning the document collection.

Week 2 introduced an inverted index:

term → document IDs

This changed the search operation from scanning documents to looking up the documents associated with a term.

I also encountered a consistency problem when replacing an existing document.

The document store was updated, but the inverted index could retain postings belonging to the old document.

This created stale index entries and could produce incorrect search results.

The problem was fixed by removing the old document's postings before adding the new document's terms, and regression tests were added for the behavior.


## Current Limitations

The current implementation is intentionally small.

It does not yet support:

Advanced tokenization
Lowercase normalization
Stemming
Stop words
Term frequency
Document frequency
Positional information
Boolean queries
Phrase queries
Ranking
BM25
Persistence
Segments
Segment merging
Refresh
Shards
Distributed search
Replication
Failure recovery

These capabilities will be introduced incrementally as the project progresses.

## Project Roadmap

The project is being built incrementally.

Week 1 — Complete

Smallest working search engine

Week 2 — Complete

Inverted index

Week 3 — Next

Analysis pipeline, tokenization, normalization, term frequency, document frequency, and positions

Week 4

Query engine and Boolean/phrase queries

Week 5

TF-IDF and BM25 ranking

Week 6

Persistence and immutable segments

Week 7

Segment merging and refresh

Week 8

Shards and deterministic routing

Week 9

Distributed search

Week 10

Primary/replica architecture and failure recovery

The implementation will evolve based on actual experiments and observations rather than trying to reproduce Elasticsearch itself.

## Project Structure

educational-search-engine/
│
├── benchmarks/
│   ├── benchmark_search.py
│   ├── week1_search_baseline.csv
│   ├── week2_search_comparison.py
│   └── week2_search_comparison.csv
│
├── docs/
│   └── weekly-reports/
│       ├── week-1.md
│       └── week-2.md
│
├── examples/
│
├── src/
│   └── search_engine/
│       ├── cli.py
│       ├── document.py
│       ├── indexer.py
│       ├── main.py
│       └── searcher.py
│
├── tests/
│   ├── test_cli.py
│   ├── test_document.py
│   ├── test_indexer.py
│   ├── test_searcher.py
│   └── test_smoke.py
│
├── .gitignore
└── README.md

## Development Philosophy

The project follows:

BUILD
  ↓
RUN
  ↓
BREAK
  ↓
UNDERSTAND WHY
  ↓
FIX
  ↓
TEST
  ↓
OBSERVE
  ↓
DOCUMENT
  ↓
COMMIT
  ↓
PUBLISH

The goal is not to implement every feature found in Elasticsearch.

The goal is to understand the mechanisms that make a search engine work.

The implementation is intentionally built incrementally so that architectural decisions can be tested, measured, and changed as the system evolves.