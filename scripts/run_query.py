from app.rag import ThreatIntelRAG


def main():
    rag = ThreatIntelRAG()

    while True:
        query = input("Ask a question (type exit to quit): ")
        if query.lower() == "exit":
            break

        answer, _, sources = rag.ask(query)

        print("\nAnswer:\n")
        print(answer)

        print("\nSources:\n")
        for i, source in enumerate(sources, start=1):
            print(f"{i}. Page: {source['page']}")
            print(f"   Preview: {source['text_preview']}\n")


if __name__ == "__main__":
    main()