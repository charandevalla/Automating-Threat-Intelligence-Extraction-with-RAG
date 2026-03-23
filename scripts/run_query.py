from app.rag import ThreatIntelRAG


def main():
    rag = ThreatIntelRAG()

    while True:
        query = input("Ask a question (type exit to quit): ")
        if query.lower() == "exit":
            break

        answer, _ = rag.ask(query)
        print("\nAnswer:\n")
        print(answer)
        print()


if __name__ == "__main__":
    main()