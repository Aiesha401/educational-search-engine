class Analyzer:
    def tokenize(self, text: str) -> list[str]:
        return text.split()

    def normalize(self, tokens: list[str]) -> list[str]:
        return [token.lower() for token in tokens]

    def analyze(self, text: str) -> list[str]:
        tokens = self.tokenize(text)
        return self.normalize(tokens)

tokens = Analyzer().tokenize("The Quick Brown Fox")
print(tokens)

print(Analyzer().analyze("Dog dog DOG dOg"))