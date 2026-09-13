import csv
import time

from src.search_engine.document import Document
from src.search_engine.indexer import Indexer
from src.search_engine.searcher import Searcher


def brute_force_search(documents, query):
    results = []

    for document in documents.values():
        if query in document.text:
            results.append(document)

    return results


def build_indexer(document_count):
    indexer = Indexer()

    for i in range(document_count):
        text = f"document {i} contains common words"

        if i == document_count // 2:
            text += " needle"

        indexer.index(Document(str(i), text))

    return indexer


def benchmark_search(search_function, query, repetitions=20):
    times = []

    for _ in range(repetitions):
        start = time.perf_counter()

        search_function(query)

        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000
        times.append(elapsed_ms)

    return sum(times) / len(times)


def main():
    sizes = [10, 100, 1000, 10000, 20000]
    queries = ["needle", "notpresent"]

    rows = []

    for size in sizes:
        indexer = build_indexer(size)
        searcher = Searcher(indexer)

        for query in queries:
            brute_force_results = brute_force_search(
                indexer.documents,
                query,
            )

            inverted_index_results = searcher.search(query)

            brute_force_ids = {
                document.id for document in brute_force_results
            }

            inverted_index_ids = {
                document.id for document in inverted_index_results
            }

            assert brute_force_ids == inverted_index_ids

            brute_force_ms = benchmark_search(
                lambda q: brute_force_search(
                    indexer.documents,
                    q,
                ),
                query,
            )

            inverted_index_ms = benchmark_search(
                searcher.search,
                query,
            )

            rows.append(
                {
                    "documents": size,
                    "query": query,
                    "brute_force_ms": brute_force_ms,
                    "inverted_index_ms": inverted_index_ms,
                }
            )

    output_file = "benchmarks/week2_search_comparison.csv"

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "documents",
                "query",
                "brute_force_ms",
                "inverted_index_ms",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Benchmark results written to {output_file}")
    print()

    for row in rows:
        print(
            f"{row['documents']:>6} docs | "
            f"{row['query']:<10} | "
            f"brute force: {row['brute_force_ms']:.6f} ms | "
            f"inverted index: {row['inverted_index_ms']:.6f} ms"
        )


if __name__ == "__main__":
    main()