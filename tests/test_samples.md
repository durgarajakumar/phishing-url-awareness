# Test Results

Python version used: 3.13.5 | Operating system: linux | Date: 27-10-2026


| # | Input | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| 1 | https://www.example.com/login | No listed warning signs; not a safety guarantee. | No listed warning signs found. This does NOT prove safety. | PASS |
| 2 | http://192.0.2.10/account | IP-address hostname and HTTP. | Uses an IP address instead of a familiar domain. \| Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 3 | http://example.com@sample.invalid/login | @ symbol and HTTP. | Contains an @ symbol; inspect carefully. \| Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 4 | https://a.b.c.d.e.example.invalid/path | Many hostname segments. | Contains many hostname segments/subdomains. | PASS |
| 5 | https://xn--example.invalid/ | Punycode-style hostname. | Contains a punycode-style hostname. | PASS |

## Notes

- The checker reads URL text only; it does not visit any website or send network requests.
- The tests demonstrate that the selected rules work on these examples, not that the tool can identify every phishing URL.

## Automated Unit Tests

Run from the project root:

```bash
python -m unittest discover -s tests -v
```
