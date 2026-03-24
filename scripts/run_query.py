from app.rag import ThreatIntelRAG


def main():
    rag = ThreatIntelRAG()

    while True:
        query = input("Ask a question (type exit to quit): ")
        if query.lower() == "exit":
            break

        answer, _, sources, metadata_summary = rag.ask(query)

        print("\nAnswer:\n")
        print(answer)

        print("\nMetadata Summary:\n")
        print(f"CVEs: {metadata_summary['cves']}")
        print(f"IPs: {metadata_summary['ips']}")
        print(f"Domains: {metadata_summary['domains']}")
        print(f"Hashes: {metadata_summary['hashes']}")
        print(f"MITRE Techniques: {metadata_summary['mitre_techniques']}")
        print(f"Threat Actors: {metadata_summary['threat_actors']}")

        print("\nSources:\n")
        for i, source in enumerate(sources, start=1):
            print(f"{i}. Page: {source['page']}")
            print(f"   Preview: {source['text_preview']}\n")


if __name__ == "__main__":
    main()