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