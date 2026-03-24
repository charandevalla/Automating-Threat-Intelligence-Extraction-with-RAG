import re


def extract_cves(text: str):
    return list(set(re.findall(r"\bCVE-\d{4}-\d{4,7}\b", text, flags=re.IGNORECASE)))


def extract_ips(text: str):
    return list(set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)))


def extract_domains(text: str):
    return list(set(re.findall(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b", text)))


def extract_hashes(text: str):
    md5 = re.findall(r"\b[a-fA-F0-9]{32}\b", text)
    sha1 = re.findall(r"\b[a-fA-F0-9]{40}\b", text)
    sha256 = re.findall(r"\b[a-fA-F0-9]{64}\b", text)
    return list(set(md5 + sha1 + sha256))


def extract_mitre_techniques(text: str):
    return list(set(re.findall(r"\bT\d{4}(?:\.\d{3})?\b", text, flags=re.IGNORECASE)))


def extract_threat_actors(text: str):
    patterns = [
        r"\bAPT\d{1,3}\b",
        r"\bFIN\d{1,4}\b",
        r"\bLazarus\b",
        r"\bSandworm\b",
        r"\bCozy Bear\b",
        r"\bFancy Bear\b",
        r"\bLockBit\b",
        r"\bBlackCat\b",
        r"\bClop\b",
        r"\bVolt Typhoon\b",
        r"\bMuddyWater\b",
    ]

    matches = []
    for pattern in patterns:
        matches.extend(re.findall(pattern, text, flags=re.IGNORECASE))

    return list(set(matches))


def extract_iocs(text: str):
    return {
        "cves": extract_cves(text),
        "ips": extract_ips(text),
        "domains": extract_domains(text),
        "hashes": extract_hashes(text),
        "mitre_techniques": extract_mitre_techniques(text),
        "threat_actors": extract_threat_actors(text),
    }