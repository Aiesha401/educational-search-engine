class Posting:
    def __init__(
        self,
        document_id: str,
        term_frequency: int,
        positions: list[int],
    ):
        self.document_id = document_id
        self.term_frequency = term_frequency
        self.positions = positions