from document import Document
from indexer import Indexer
from searcher import Searcher


def main():
    indexer = Indexer()

    documents = [
        Document("1", "The quick brown fox"),
        Document("2", "The lazy dog"),
        Document("3", "The brown dog jumps"),
    ]

    for document in documents:
        indexer.index(document)

    searcher = Searcher(indexer)

    query = "brown"
    results = searcher.search(query)

    print(f"Query: {query}")
    print("Results:")

    for document in results:
        print(f"{document.id}: {document.text}")


if __name__ == "__main__":
    main()