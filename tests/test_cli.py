from src.search_engine.cli import SearchEngineCLI


def test_index_command():
    cli = SearchEngineCLI()

    assert cli.execute('index 1 "The quick brown fox"') is True

    assert cli.indexer.count() == 1
    assert cli.indexer.get("1").text == "The quick brown fox"


def test_search_command(capsys):
    cli = SearchEngineCLI()

    cli.execute('index 1 "The quick brown fox"')
    cli.execute('index 2 "The lazy dog"')

    cli.execute("search brown")

    captured = capsys.readouterr()

    assert "1: The quick brown fox" in captured.out


def test_search_with_no_results(capsys):
    cli = SearchEngineCLI()

    cli.execute('index 1 "The quick brown fox"')
    cli.execute("search elephant")

    captured = capsys.readouterr()

    assert "No results" in captured.out


def test_count_command(capsys):
    cli = SearchEngineCLI()

    cli.execute('index 1 "The quick brown fox"')
    cli.execute('index 2 "The lazy dog"')

    cli.execute("count")

    captured = capsys.readouterr()

    assert "Documents: 2" in captured.out


def test_unknown_command(capsys):
    cli = SearchEngineCLI()

    cli.execute("hello")

    captured = capsys.readouterr()

    assert "Unknown command: hello" in captured.out