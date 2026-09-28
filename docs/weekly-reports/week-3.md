# Week 3

## Day 1: Analysis Pipeline

Today I introduced the first analysis layer of the search engine.

### What I did

- Created `src/search_engine/analyzer.py`
- Added `Analyzer` with:
  - `tokenize()`
  - `normalize()`
  - `analyze()`
- Tokenization currently uses whitespace splitting.
- Added lowercase normalization.
- Created `tests/test_analyzer.py`
- Added tests for tokenization, normalization, empty text, spaces, and capitalization.
- Tested punctuation behavior and confirmed it is currently preserved.
- Fixed a couple of initial errors while manually running the analyzer.
- Ran the complete test suite.

### Result

36 passed, The existing Week 2 functionality still works.

### Git

Created and pushed:

week-3-analysis-postings

### Current Architecture

Raw Text
   ↓
Analyzer
   ↓
Tokens

The Analyzer is not connected to the Indexer yet.

### Next

Day 2 — Introduce Postings + Term Frequency.

## Day 2: Postings + Term Frequency

Today I changed the inverted index to store posting objects instead of only document IDs.

### What I did
Created src/search_engine/posting.py
Added Posting with:
document_id
term_frequency
Changed the inverted index structure from:
term → set(document IDs)
To:
term → document ID → Posting
Added term frequency calculation during indexing.
Updated existing indexer tests to work with the new posting structure.
Added tests for:
term frequency
multiple documents having separate postings
replacing documents and removing old postings
Ran the complete test suite.

### Result

39 passed.

The existing Week 2 indexing behavior still works with the new posting structure.

### Current Architecture

Raw Text
   ↓
Indexer
   ↓
Inverted Index
   ↓
Posting
   ├── document_id
   └── term_frequency

### Important Observation

The index can now store information about how often a term appears in each document.

### Next

Day 3 — Introduce Positions into postings.

## Day 3 — Positions

Today I extended postings to store term positions.

### What I did
Added positions to Posting.
Stored the zero-based position of every term occurrence.
Kept term frequency and positions consistent.
Added tests for repeated terms and position tracking.
Verified document replacement still removes old postings.
Result

Postings now contain:

document_id
term_frequency
positions

## Day 4 — Analyzer Integration

Today I connected the Analyzer to both indexing and searching.

### What I did
Indexing now uses Analyzer.analyze().
Search queries also use the Analyzer.
Added lowercase normalization to the complete indexing/search flow.
Updated tests for case-insensitive searching.
Verified TF and positions still work after normalization.

### Result
"Python", "PYTHON", "python"

are treated as the same term.

## Day 5 — Document Frequency

Today I added Document Frequency (DF).

### What I did
Added document_frequency() to the Indexer.
DF counts how many different documents contain a term.
Verified repeated occurrences in one document count only once.
Added tests for unknown terms, normalization, and document replacement.

### Result

The index can now provide:

TF → occurrences within a document
DF → documents containing the term

## Day 6 — Integration + Final Review

Today I focused on integrating and testing the complete Week 3 pipeline.

### What I did
Added Analyzer edge-case tests.
Added empty and whitespace query tests.
Added integration tests for normalization + TF + positions.
Added integration tests for normalization + DF.
Ran the complete test suite.
Committed and pushed the final Week 3 changes.
Merged week-3-analysis-postings into main.
Ran the complete test suite again after the merge.

### Final Result
57 passed

Week 3 is now complete.

## week 3 Architecture:

                    Document
                       │
                       ▼
                    Analyzer
                 ┌─────┴─────┐
                 │           │
            Tokenize      Normalize
                 │           │
                 └─────┬─────┘
                       │
                     Tokens
                       │
                       ▼
                    Indexer
                       │
                       ▼
                Inverted Index
                       │
             ┌─────────┴─────────┐
             │                   │
           Term              Postings
                                 │
                         ┌───────┼───────┐
                         │       │       │
                    Document ID  TF   Positions