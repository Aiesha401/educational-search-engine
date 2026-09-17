# from src.search_engine.cli import SearchEngineCLI


# def main():
#     cli = SearchEngineCLI()
#     cli.run()


# if __name__ == "__main__":
#     main()

from src.search_engine.document import Document
from src.search_engine.indexer import Indexer

indexer = Indexer()

indexer.index(Document("1", "the dog chased the dog"))
indexer.index(Document("2", "the dog"))

print(vars(indexer.inverted_index["dog"]["1"]))
# print(indexer.inverted_index)