class Searcher:
    def __init__(self, indexer):
        self.indexer = indexer

    def search(self, query):
        results = []

        for document in self.indexer.documents.values():
            if query in document.text:
                results.append(document)

        return results