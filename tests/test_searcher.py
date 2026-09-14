from src.search_engine.document import Document
from src.search_engine.indexer import Indexer
from src.search_engine.searcher import Searcher


def test_search_returns_matching_document():
    indexer = Indexer()

    document = Document("1", "The quick brown fox")
    indexer.index(document)

    searcher = Searcher(indexer)

    results = searcher.search("brown")

    assert results == [document]


def test_search_returns_multiple_matching_documents():
    indexer = Indexer()

    document1 = Document("1", "The quick brown fox")
    document2 = Document("2", "The brown dog")
    document3 = Document("3", "The lazy dog")

    indexer.index(document1)
    indexer.index(document2)
    indexer.index(document3)

    searcher = Searcher(indexer)

    results = searcher.search("brown")

    assert {document.id for document in results} == {"1", "2"}


def test_search_returns_no_results_for_unknown_term():
    indexer = Indexer()

    document = Document("1", "The quick brown fox")
    indexer.index(document)

    searcher = Searcher(indexer)

    results = searcher.search("elephant")

    assert results == []


def test_search_empty_index_returns_no_results():
    indexer = Indexer()

    searcher = Searcher(indexer)

    results = searcher.search("brown")

    assert results == []


def test_search_is_case_sensitive():
    indexer = Indexer()

    document = Document("1", "Beautiful fox")
    indexer.index(document)

    searcher = Searcher(indexer)

    assert searcher.search("Beautiful") == [document]
    assert searcher.search("beautiful") == []


def test_search_uses_exact_terms_not_substrings():
    indexer = Indexer()

    document = Document("1", "The dogmatic fox")
    indexer.index(document)

    searcher = Searcher(indexer)

    assert searcher.search("dog") == []
    assert searcher.search("dogmatic") == [document]