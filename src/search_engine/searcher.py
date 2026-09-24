from src.search_engine.analyzer import Analyzer


class Searcher:
    def __init__(self, indexer):
        self.indexer = indexer
        self.analyzer = Analyzer()

    def search(self, query):
        terms = self.analyzer.analyze(query)

        if not terms:
            return []

        term = terms[0]

        postings = self.indexer.inverted_index.get(term, {})

        results = []

        for document_id in postings:
            document = self.indexer.get(document_id)

            if document is not None:
                results.append(document)

        return results