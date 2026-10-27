import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from phishing_checker import inspect_url, has_warnings


class PhishingCheckerTests(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(inspect_url("   "), ["No URL entered."])
        self.assertFalse(has_warnings(inspect_url("")))

    def test_ip_and_http(self):
        result = inspect_url("http://192.0.2.10/account")
        self.assertTrue(any("IP address" in item for item in result))
        self.assertTrue(any("Uses HTTP" in item for item in result))
        self.assertTrue(has_warnings(result))

    def test_at_symbol_and_http(self):
        result = inspect_url("http://example.com@sample.invalid/login")
        self.assertTrue(any("@ symbol" in item for item in result))
        self.assertTrue(any("Uses HTTP" in item for item in result))

    def test_many_hostname_segments(self):
        result = inspect_url("https://a.b.c.d.e.example.invalid/path")
        self.assertTrue(any("many hostname segments" in item for item in result))

    def test_punycode_marker(self):
        result = inspect_url("https://xn--example.invalid/")
        self.assertTrue(any("punycode-style" in item for item in result))

    def test_long_url(self):
        url = "https://example.invalid/" + ("a" * 101)
        self.assertTrue(any("Unusually long URL" in item for item in inspect_url(url)))

    def test_malformed_url_does_not_crash(self):
        self.assertEqual(
            inspect_url("http://[bad"),
            ["This text is not a valid URL format."]
        )

    def test_no_warning_is_not_a_safety_claim(self):
        result = inspect_url("https://www.example.com/login")
        self.assertIn(
            "No listed warning signs found. This does NOT prove safety.",
            result
        )
        self.assertFalse(has_warnings(result))


if __name__ == "__main__":
    unittest.main()
