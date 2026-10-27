"""EWB Phishing URL Awareness Checker.

Defensive learning tool: inspects URL text only. It never opens URLs
or sends data over the network.
"""
import re
from urllib.parse import urlparse


INFO_PREFIXES = (
    "No URL entered.",
    "Could not identify a hostname.",
    "This text is not a valid URL format.",
    "No listed warning signs found.",
)


def inspect_url(raw_url):
    """Return a list of warning or information messages for URL text."""
    url = raw_url.strip()
    if not url:
        return ["No URL entered."]

    candidate = url if "://" in url else "http://" + url

    try:
        parsed = urlparse(candidate)
        host = (parsed.hostname or "").lower()
    except ValueError:
        return ["This text is not a valid URL format."]

    if not host:
        return ["Could not identify a hostname."]

    findings = []

    if "@" in candidate:
        findings.append("Contains an @ symbol; inspect carefully.")

    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")

    # This checks the shape of an IPv4 address; it is a simple text heuristic.
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append("Uses an IP address instead of a familiar domain.")

    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append("Contains many hostname segments/subdomains.")

    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")

    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP. HTTPS alone does not prove trust.")

    if not findings:
        findings.append(
            "No listed warning signs found. This does NOT prove safety."
        )

    return findings


def has_warnings(findings):
    """Distinguish actual warning findings from informational messages."""
    if not findings:
        return False
    return not findings[0].startswith(INFO_PREFIXES)


def main():
    """Interactive command-line loop; type q, quit or exit to stop."""
    print("EWB Phishing URL Awareness Checker")
    print("Text checks only - this program does not open URLs.")
    while True:
        try:
            raw_url = input("\nEnter a sample URL (or type q to quit): ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Stay alert online.")
            break

        if raw_url.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye! Stay alert online.")
            break

        findings = inspect_url(raw_url)
        print("\nResult:")
        for item in findings:
            print("- " + item)

        if has_warnings(findings):
            print(
                "\nREVIEW CAREFULLY: "
                f"{len(findings)} warning sign(s) found."
            )

        print("Never enter passwords from unexpected links.")


if __name__ == "__main__":
    main()
