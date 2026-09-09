class Indexer:
    def __init__(self):
        self.documents = {}
        self.inverted_index = {}

    def index(self, document):
        self.documents[document.id] = document

    def get(self, document_id):
        return self.documents.get(document_id)

    def count(self):
        return len(self.documents)