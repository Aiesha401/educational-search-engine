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