# Week 1 — Smallest Working Search Engine

## Day 1 — Project Setup

### Objective

Initialize the project structure and development environment.

### Environment

- Python: 3.14.4
- Testing: pytest 9.1.1
- Implementation: Python standard library

### Completed

- Initialized Git repository
- Created source structure
- Created test structure
- Created initial Python entry point
- Configured .gitignore
- Created initial README
- Verified application runs
- Verified pytest runs

### Current Architecture

Project
   |
   v
Python Application

## Day 2 — Document Model

### Objective

Implement the first domain object representing a searchable document.

### What I Built

Implemented the `Document` class with:

- document ID
- document text

### Current Architecture

Application
    |
    v
Document
    |
    ├── id
    └── text

## Day 3 — Indexer and Document Storage

### Objective

Implement the component responsible for accepting and storing
documents.

### What I Built

Implemented an `Indexer` with:

- document indexing
- document retrieval by ID
- document counting
- replacement behavior for duplicate document IDs

### Current Architecture

Application
    |
    v
  Indexer
    |
    v
Dictionary
    |
    v
Documents

## Day 4 — Basic Brute-Force Search

### Objective

Implement the first working search component.

### What I Built

Implemented a `Searcher` that scans the documents stored
by the `Indexer` and returns documents whose text contains
the query.

### Search Algorithm

Query
  |
  v
Searcher
  |
  v
Scan every document
  |
  +-- match --> result
  |
  +-- no match

### current architecture

                         APPLICATION
                              │
                ┌─────────────┴─────────────┐
                │                           │
             INDEX                        SEARCH
                │                           │
                ▼                           ▼
             Indexer                    Searcher
                │                           │
                ▼                           │
        In-memory dictionary ◄──────────────┘
                │
                ▼
           Documents

## Day 5 — Interactive CLI

### Objective

Make the search engine usable through an interactive command-line
interface.

### What I Built

Implemented a CLI supporting:

- indexing documents
- searching documents
- counting documents
- displaying help
- exiting the application

### Current Architecture

               USER
                │
                ▼
                CLI
          ┌─────┴─────┐
          │           │
        index        search
          │           │
          ▼           ▼
        Indexer     Searcher
          │           │
          └─────┬─────┘
                ▼
        In-memory storage
                │
                ▼
            Documents
#### Supported Commands

- index <id> "<text>"
- search <query>
- count
- help
- exit