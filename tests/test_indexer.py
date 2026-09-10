from src.search_engine.document import Document
from src.search_engine.indexer import Indexer


def test_index_document():
    indexer = Indexer()
    document = Document("1", "The quick brown fox")

    indexer.index(document)

    assert indexer.get("1") is document

def test_index_multiple_documents():
    indexer = Indexer()

    document1 = Document("1", "The quick brown fox")
    document2 = Document("2", "The lazy dog")

    indexer.index(document1)
    indexer.index(document2)

    assert indexer.get("1") is document1
    assert indexer.get("2") is document2

def test_get_unknown_document_returns_none():
    indexer = Indexer()

    assert indexer.get("does-not-exist") is None

def test_document_count():
    indexer = Indexer()

    indexer.index(Document("1", "The quick brown fox"))
    indexer.index(Document("2", "The lazy dog"))

    assert indexer.count() == 2

def test_indexing_same_id_replaces_document():
    indexer = Indexer()

    first = Document("1", "The quick brown fox")
    second = Document("1", "The slow red fox")

    indexer.index(first)
    indexer.index(second)

    assert indexer.get("1") is second
    assert indexer.count() == 1

def test_inverted_index_starts_empty():
    indexer = Indexer()

    assert indexer.inverted_index == {}

def test_index_creates_inverted_index_entries():
    indexer = Indexer()

    document = Document("1", "The quick brown fox")
    indexer.index(document)

    assert indexer.inverted_index["The"] == {"1"}
    assert indexer.inverted_index["quick"] == {"1"}
    assert indexer.inverted_index["brown"] == {"1"}
    assert indexer.inverted_index["fox"] == {"1"}

def test_inverted_index_tracks_multiple_documents():
    indexer = Indexer()

    document1 = Document("1", "The quick brown fox")
    document2 = Document("2", "The lazy dog")
    document3 = Document("3", "The brown dog")

    indexer.index(document1)
    indexer.index(document2)
    indexer.index(document3)

    assert indexer.inverted_index["The"] == {"1", "2", "3"}
    assert indexer.inverted_index["brown"] == {"1", "3"}
    assert indexer.inverted_index["dog"] == {"2", "3"}

def test_repeated_term_does_not_duplicate_document_id():
    indexer = Indexer()

    document = Document("1", "brown brown brown fox")
    indexer.index(document)

    assert indexer.inverted_index["brown"] == {"1"}
    assert indexer.inverted_index["fox"] == {"1"}

def test_terms_have_independent_postings():
    indexer = Indexer()

    document1 = Document("1", "brown fox")
    document2 = Document("2", "red dog")

    indexer.index(document1)
    indexer.index(document2)

    assert indexer.inverted_index["brown"] == {"1"}
    assert indexer.inverted_index["fox"] == {"1"}
    assert indexer.inverted_index["red"] == {"2"}
    assert indexer.inverted_index["dog"] == {"2"}

def test_indexing_empty_document_creates_no_postings():
    indexer = Indexer()

    document = Document("1", "")
    indexer.index(document)

    assert indexer.inverted_index == {}
    assert indexer.get("1") is document