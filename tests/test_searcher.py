from src.search_engine.document import Document
from src.search_engine.indexer import Indexer
from src.search_engine.searcher import Searcher


def test_search_finds_matching_document():
    indexer = Indexer()

    document = Document("1", "The quick brown fox")
    indexer.index(document)

    searcher = Searcher(indexer)

    results = searcher.search("brown")

    assert results == [document]

def test_search_finds_multiple_documents():
    indexer = Indexer()

    document1 = Document("1", "The quick brown fox")
    document2 = Document("2", "The lazy dog")
    document3 = Document("3", "The brown dog jumps")

    indexer.index(document1)
    indexer.index(document2)
    indexer.index(document3)

    searcher = Searcher(indexer)

    results = searcher.search("brown")

    assert results == [document1, document3]

def test_search_returns_empty_list_when_no_document_matches():
    indexer = Indexer()

    indexer.index(Document("1", "The quick brown fox"))
    indexer.index(Document("2", "The lazy dog"))

    searcher = Searcher(indexer)

    results = searcher.search("elephant")

    assert results == []

def test_search_on_empty_index_returns_empty_list():
    indexer = Indexer()
    searcher = Searcher(indexer)

    results = searcher.search("brown")

    assert results == []

def test_search_is_case_sensitive():
    indexer = Indexer()

    document = Document("1", "The brown fox")
    indexer.index(document)

    searcher = Searcher(indexer)

    assert searcher.search("brown") == [document]
    assert searcher.search("Brown") == []

def test_search_currently_uses_substring_matching():
    indexer = Indexer()

    document = Document("1", "The dogmatic approach")
    indexer.index(document)

    searcher = Searcher(indexer)

    assert searcher.search("dog") == [document]