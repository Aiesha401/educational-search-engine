from document import Document
from indexer import Indexer


def main():
    indexer = Indexer()

    documents = [
        Document("1", "The quick brown fox"),
        Document("2", "The lazy dog"),
        Document("3", "The brown dog jumps"),
    ]

    for document in documents:
        indexer.index(document)

    print(f"Indexed documents: {indexer.count()}")

    document = indexer.get("2")

    if document is not None:
        print(f"Document {document.id}: {document.text}")


if __name__ == "__main__":
    main()