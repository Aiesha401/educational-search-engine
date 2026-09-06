import shlex

from src.search_engine.document import Document
from src.search_engine.indexer import Indexer
from src.search_engine.searcher import Searcher


class SearchEngineCLI:
    def __init__(self):
        self.indexer = Indexer()
        self.searcher = Searcher(self.indexer)

    def run(self):
        print("Educational Search Engine")
        print('Type "help" for commands.')

        while True:
            try:
                command = input("> ")
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not self.execute(command):
                break

    def execute(self, command):
        parts = shlex.split(command)

        if not parts:
            return True

        action = parts[0].lower()

        if action == "help":
            self.print_help()

        elif action == "index":
            self.index_document(parts)

        elif action == "search":
            self.search_documents(parts)

        elif action == "count":
            print(f"Documents: {self.indexer.count()}")

        elif action == "exit":
            print("Goodbye!")
            return False

        else:
            print(f"Unknown command: {action}")

        return True

    def print_help(self):
        print("Commands:")
        print('  index <id> "<text>"')
        print("  search <query>")
        print("  count")
        print("  help")
        print("  exit")

    def index_document(self, parts):
        if len(parts) != 3:
            print('Usage: index <id> "<text>"')
            return

        document_id = parts[1]
        text = parts[2]

        document = Document(document_id, text)
        self.indexer.index(document)

        print(f"Indexed document {document_id}")

    def search_documents(self, parts):
        if len(parts) != 2:
            print("Usage: search <query>")
            return

        query = parts[1]
        results = self.searcher.search(query)

        if not results:
            print("No results")
            return
        for document in results:
            print(f"{document.id}: {document.text}")