class Searcher:
    def __init__(self, indexer):
        self.indexer = indexer

    def search(self, query):
        document_ids = self.indexer.inverted_index.get(query, set())

        results = []

        # for document in self.indexer.documents.values():
        for document_id in document_ids:
            document = self.indexer.get(document_id)

            if document is not None:
                results.append(document)

        return results