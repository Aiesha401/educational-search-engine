from document import Document


def main():
    document = Document("1", "The quick brown fox")

    print(document.id)
    print(document.text)


if __name__ == "__main__":
    main()