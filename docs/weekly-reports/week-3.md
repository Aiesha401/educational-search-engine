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