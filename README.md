# Educational Search Engine

An educational search engine built from scratch in Python.

The project explores the internal mechanisms behind search engines,
inspired by core ideas found in Elasticsearch and Lucene.

Neither Elasticsearch nor Lucene is used as an implementation dependency.

## Current Status

**Week 1 — Smallest Working Search Engine: Complete**

The current engine supports:

- Document creation
- Document indexing
- Document retrieval by ID
- Brute-force search
- Interactive command-line interface
- Automated tests
- Baseline search benchmarking

## Current Architecture

                         USER
                          |
                          v
                         CLI
                    /           \
                   /             \
                index           search
                  |                |
                  v                v
               Indexer          Searcher
                  |                |
                  v                v
          In-memory storage   Scan documents
                  |                |
                  v                v
              Documents       String matching
                                   |
                                   v
                                Results

## Search Flow

The current search implementation uses a brute-force approach.

For every query, the Searcher scans the indexed documents and checks whether the query occurs in each document's text.

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

This implementation is intentionally simple and serves as the baseline for future architectural improvements.

## Testing

The project currently has automated tests covering:

Document behavior
Indexer behavior
Search behavior
CLI behavior
Basic application smoke testing

Run the test suite with:

python -m pytest

Current Week 1 result:

21 passed

## Benchmarking

The Week 1 baseline benchmark measures brute-force search across:

10 documents
100 documents
1,000 documents
10,000 documents

Each query is executed 20 times.

### Baseline Results

| Documents | Present Query | Absent Query |
|----------:|--------------:|-------------:|
| 10        | 0.0033 ms     | 0.0010 ms    |
| 100       | 0.0127 ms     | 0.0077 ms    |
| 1,000     | 0.0945 ms     | 0.0992 ms    |
| 10,000    | 0.7853 ms     | 0.8213 ms    |

These measurements are a baseline from the development environment and are not intended as universal performance claims.

Benchmark results are stored in:

benchmarks/week1_search_baseline.csv

Run the benchmark with:

python -m benchmarks.benchmark_search

## What I Learned

A search engine can produce correct results while still having an inefficient internal architecture.

The current Indexer stores documents by ID, but the Searcher does not have a structure that tells it which documents contain a searched term.

Therefore, even a query with no matching documents requires scanning the document collection.

## Project Roadmap

The project is being built incrementally.

### Week 1

Smallest working search engine

### Week 2

Inverted index

### Week 3

Analysis pipeline and tokenization

### Week 4

Query engine and Boolean/phrase queries

### Week 5

TF-IDF and BM25 ranking

### Week 6

Persistence and immutable segments

### Week 7

Segment merging and refresh

### Week 8

Shards and deterministic routing

### Week 9

Distributed search

### Week 10

Primary/replica architecture and failure recovery

The implementation will evolve based on actual experiments and observations rather than trying to reproduce Elasticsearch itself.

## Project Structure

    educational-search-engine/
    ├── benchmarks/
    │   ├── benchmark_search.py
    │   └── week1_search_baseline.csv
    ├── docs/
    │   └── weekly-reports/
    │       └── week-1.md
    ├── src/
    │   └── search_engine/
    │       ├── __init__.py
    │       ├── cli.py
    │       ├── document.py
    │       ├── indexer.py
    │       ├── main.py
    │       └── searcher.py
    ├── tests/
    │   ├── test_cli.py
    │   ├── test_document.py
    │   ├── test_indexer.py
    │   ├── test_searcher.py
    │   └── test_smoke.py
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