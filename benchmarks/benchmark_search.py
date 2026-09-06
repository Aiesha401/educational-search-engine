import csv
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.search_engine.document import Document
from src.search_engine.indexer import Indexer
from src.search_engine.searcher import Searcher


DATASET_SIZES = [10, 100, 1_000, 10_000]
REPETITIONS = 20


def build_searcher(document_count):
    indexer = Indexer()

    for i in range(document_count):
        text = (
            f"document {i} contains ordinary search content "
            f"with several words for benchmarking"
        )

        if i % 100 == 0:
            text += " needle"

        indexer.index(Document(str(i), text))

    return Searcher(indexer)


def measure_search(searcher, query):
    times = []

    for _ in range(REPETITIONS):
        start = time.perf_counter()
        searcher.search(query)
        end = time.perf_counter()

        times.append(end - start)

    average = sum(times) / len(times)

    return {
        "average_ms": average * 1000,
        "min_ms": min(times) * 1000,
        "max_ms": max(times) * 1000,
    }


def main():
    output_file = Path(__file__).with_name("week1_search_baseline.csv")

    rows = []

    print("Week 1 Search Benchmark")
    print("=======================")
    print(f"Repetitions per measurement: {REPETITIONS}")
    print()

    for size in DATASET_SIZES:
        searcher = build_searcher(size)

        present = measure_search(searcher, "needle")
        absent = measure_search(searcher, "notpresent")

        print(f"Documents: {size}")
        print(
            f"  Present query: "
            f"{present['average_ms']:.4f} ms average "
            f"(min {present['min_ms']:.4f}, "
            f"max {present['max_ms']:.4f})"
        )
        print(
            f"  Absent query:  "
            f"{absent['average_ms']:.4f} ms average "
            f"(min {absent['min_ms']:.4f}, "
            f"max {absent['max_ms']:.4f})"
        )
        print()

        rows.append(
            {
                "documents": size,
                "query": "needle",
                "query_type": "present",
                "repetitions": REPETITIONS,
                "average_ms": present["average_ms"],
                "min_ms": present["min_ms"],
                "max_ms": present["max_ms"],
            }
        )

        rows.append(
            {
                "documents": size,
                "query": "notpresent",
                "query_type": "absent",
                "repetitions": REPETITIONS,
                "average_ms": absent["average_ms"],
                "min_ms": absent["min_ms"],
                "max_ms": absent["max_ms"],
            }
        )

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "documents",
                "query",
                "query_type",
                "repetitions",
                "average_ms",
                "min_ms",
                "max_ms",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()