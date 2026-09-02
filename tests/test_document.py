from src.search_engine.document import Document


def test_document_has_id_and_text():
    document = Document("1", "The quick brown fox")

    assert document.id == "1"
    assert document.text == "The quick brown fox"

def test_multiple_documents_have_different_ids():
    document1 = Document("1", "The quick brown fox")
    document2 = Document("2", "The lazy dog")

    assert document1.id != document2.id

def test_document_can_have_empty_text():
    document = Document("1", "")

    assert document.id == "1"
    assert document.text == ""

def test_document_id_is_string():
    document = Document("123", "Some text")

    assert isinstance(document.id, str)