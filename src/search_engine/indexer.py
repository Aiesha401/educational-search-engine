from src.search_engine.analyzer import Analyzer
from src.search_engine.posting import Posting


class Indexer:
    def __init__(self):
        self.documents = {}
        self.inverted_index = {}
        self.analyzer = Analyzer()

    def index(self, document):
        old_document = self.documents.get(document.id)

        if old_document is not None:
            old_terms = self.analyzer.analyze(old_document.text)

            for term in old_terms:
                postings = self.inverted_index.get(term)

                if postings is not None:
                    postings.pop(document.id, None)

                    if not postings:
                        del self.inverted_index[term]

        self.documents[document.id] = document

        terms = self.analyzer.analyze(document.text)

        term_data = {}

        for position, term in enumerate(terms):
            if term not in term_data:
                term_data[term] = {
                    "frequency": 0,
                    "positions": [],
                }

            term_data[term]["frequency"] += 1
            term_data[term]["positions"].append(position)

        for term, data in term_data.items():
            if term not in self.inverted_index:
                self.inverted_index[term] = {}

            self.inverted_index[term][document.id] = Posting(
                document.id,
                data["frequency"],
                data["positions"],
            )

    def get(self, document_id):
        return self.documents.get(document_id)

    def count(self):
        return len(self.documents)