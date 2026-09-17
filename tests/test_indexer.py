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

    assert indexer.inverted_index["The"]["1"].document_id == "1"
    assert indexer.inverted_index["The"]["1"].term_frequency == 1

    assert indexer.inverted_index["quick"]["1"].document_id == "1"
    assert indexer.inverted_index["quick"]["1"].term_frequency == 1

    assert indexer.inverted_index["brown"]["1"].document_id == "1"
    assert indexer.inverted_index["brown"]["1"].term_frequency == 1

    assert indexer.inverted_index["fox"]["1"].document_id == "1"
    assert indexer.inverted_index["fox"]["1"].term_frequency == 1

def test_inverted_index_tracks_multiple_documents():
    indexer = Indexer()

    document1 = Document("1", "The quick brown fox")
    document2 = Document("2", "The lazy dog")
    document3 = Document("3", "The brown dog")

    indexer.index(document1)
    indexer.index(document2)
    indexer.index(document3)

    assert set(indexer.inverted_index["The"].keys()) == {"1", "2", "3"}
    assert set(indexer.inverted_index["brown"].keys()) == {"1", "3"}
    assert set(indexer.inverted_index["dog"].keys()) == {"2", "3"}

def test_repeated_term_does_not_duplicate_document_id():
    indexer = Indexer()

    document = Document("1", "brown brown brown fox")
    indexer.index(document)

    assert set(indexer.inverted_index["brown"].keys()) == {"1"}
    assert indexer.inverted_index["brown"]["1"].term_frequency == 3

    assert set(indexer.inverted_index["fox"].keys()) == {"1"}
    assert indexer.inverted_index["fox"]["1"].term_frequency == 1

def test_terms_have_independent_postings():
    indexer = Indexer()

    document1 = Document("1", "brown fox")
    document2 = Document("2", "red dog")

    indexer.index(document1)
    indexer.index(document2)

    assert set(indexer.inverted_index["brown"].keys()) == {"1"}
    assert set(indexer.inverted_index["fox"].keys()) == {"1"}
    assert set(indexer.inverted_index["red"].keys()) == {"2"}
    assert set(indexer.inverted_index["dog"].keys()) == {"2"}

def test_indexing_empty_document_creates_no_postings():
    indexer = Indexer()

    document = Document("1", "")
    indexer.index(document)

    assert indexer.inverted_index == {}
    assert indexer.get("1") is document

def test_replacing_document_removes_old_postings():
    indexer = Indexer()

    indexer.index(Document("1", "brown fox"))

    indexer.index(Document("1", "red dog"))

    assert "brown" not in indexer.inverted_index
    assert "fox" not in indexer.inverted_index
    assert indexer.inverted_index["red"].keys() == {"1"}
    assert indexer.inverted_index["dog"].keys() == {"1"}


def test_replacing_document_preserves_shared_terms():
    indexer = Indexer()

    indexer.index(Document("1", "brown fox"))
    indexer.index(Document("2", "brown dog"))

    indexer.index(Document("1", "red dog"))

    assert set(indexer.inverted_index["brown"].keys()) == {"2"}
    assert "fox" not in indexer.inverted_index
    assert set(indexer.inverted_index["red"].keys()) == {"1"}
    assert set(indexer.inverted_index["dog"].keys()) == {"1", "2"}

def test_replacing_document_with_empty_text_removes_old_postings():
    indexer = Indexer()

    indexer.index(Document("1", "brown fox"))

    indexer.index(Document("1", ""))

    assert indexer.get("1").text == ""
    assert indexer.inverted_index == {}

def test_posting_contains_term_frequency():
    from src.search_engine.document import Document
    from src.search_engine.indexer import Indexer

    indexer = Indexer()
    document = Document("1", "dog cat dog")

    indexer.index(document)

    posting = indexer.inverted_index["dog"]["1"]

    assert posting.document_id == "1"
    assert posting.term_frequency == 2


def test_each_document_has_its_own_posting():
    from src.search_engine.document import Document
    from src.search_engine.indexer import Indexer

    indexer = Indexer()

    indexer.index(Document("1", "dog dog"))
    indexer.index(Document("2", "dog"))

    assert indexer.inverted_index["dog"]["1"].term_frequency == 2
    assert indexer.inverted_index["dog"]["2"].term_frequency == 1


def test_replacing_document_updates_term_frequencies():
    from src.search_engine.document import Document
    from src.search_engine.indexer import Indexer

    indexer = Indexer()

    indexer.index(Document("1", "brown dog dog"))
    indexer.index(Document("1", "red fox"))

    assert "brown" not in indexer.inverted_index
    assert "dog" not in indexer.inverted_index

    assert indexer.inverted_index["red"]["1"].term_frequency == 1
    assert indexer.inverted_index["fox"]["1"].term_frequency == 1