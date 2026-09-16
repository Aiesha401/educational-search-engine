from src.search_engine.analyzer import Analyzer


def test_tokenize_splits_text_into_tokens():
    analyzer = Analyzer()

    result = analyzer.tokenize("The quick brown fox")

    assert result == ["The", "quick", "brown", "fox"]


def test_normalize_lowercases_tokens():
    analyzer = Analyzer()

    result = analyzer.normalize(["The", "QUICK", "Brown"])

    assert result == ["the", "quick", "brown"]


def test_analyze_tokenizes_and_normalizes():
    analyzer = Analyzer()

    result = analyzer.analyze("The QUICK Brown Fox")

    assert result == ["the", "quick", "brown", "fox"]


def test_analyze_handles_multiple_spaces():
    analyzer = Analyzer()

    result = analyzer.analyze("The   quick    fox")

    assert result == ["the", "quick", "fox"]


def test_analyze_handles_empty_text():
    analyzer = Analyzer()

    result = analyzer.analyze("")

    assert result == []


def test_normalization_does_not_remove_tokens():
    analyzer = Analyzer()

    result = analyzer.analyze("DOG dog DoG")

    assert result == ["dog", "dog", "dog"]