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