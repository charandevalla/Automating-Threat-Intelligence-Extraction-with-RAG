from app.extractors import extract_iocs


def test_extract_iocs():
    text = """
    Exploitation of CVE-2024-12345 was observed from 192.168.1.10.
    Contact with malicious domain evil-example.com was detected.
    MITRE technique T1059 was referenced.
    Threat actor APT29 was mentioned.
    SHA256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    """

    iocs = extract_iocs(text)

    assert "CVE-2024-12345" in iocs["cves"]
    assert "192.168.1.10" in iocs["ips"]
    assert "evil-example.com" in iocs["domains"]
    assert "T1059" in [x.upper() for x in iocs["mitre_techniques"]]
    assert "APT29" in [x.upper() for x in iocs["threat_actors"]]
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" in iocs["hashes"]