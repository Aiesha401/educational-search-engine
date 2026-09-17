from src.search_engine.posting import Posting


class Indexer:
    def __init__(self):
        self.documents = {}
        self.inverted_index = {}

    def index(self, document):
        old_document = self.documents.get(document.id)

        if old_document is not None:
            old_terms = old_document.text.split()

            for term in old_terms:
                postings = self.inverted_index.get(term)

                if postings is not None:
                    postings.pop(document.id, None)

                    if not postings:
                        del self.inverted_index[term]

        self.documents[document.id] = document

        terms = document.text.split()

        term_frequencies = {}

        for term in terms:
            term_frequencies[term] = term_frequencies.get(term, 0) + 1

        for term, frequency in term_frequencies.items():
            if term not in self.inverted_index:
                self.inverted_index[term] = {}

            self.inverted_index[term][document.id] = Posting(
                document.id,
                frequency,
            )

    def get(self, document_id):
        return self.documents.get(document_id)

    def count(self):
        return len(self.documents)