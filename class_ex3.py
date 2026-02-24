import hashlib

class URLShortener:
    """
    Mini URL shortener.

    Stores:
    - code_to_url   : short_code -> long_url
    - url_to_code   : long_url -> short_code
    - click_counts  : short_code -> int
    """

    def __init__(self):
        self.code_to_url = {}
        self.url_to_code = {}
        self.click_counts = {}

    def _make_code(self, url, extra=""):
        """
        Create a short code using MD5 hash.
        Returns first 6 characters of hex digest.
        """
        digest = hashlib.md5((url + extra).encode()).hexdigest()
        return digest[:6]

    def shorten(self, url):
        """
        Shorten a URL and return a 6-character code.
        Handles collisions and returns the same code for same URL.
        """
        if url in self.url_to_code:
            return self.url_to_code[url]

        extra = 0
        code = self._make_code(url, str(extra))

        # Resolve collision if code already used for different URL
        while code in self.code_to_url and self.code_to_url[code] != url:
            extra += 1
            code = self._make_code(url, str(extra))

        # Save mappings and initialize click count
        self.code_to_url[code] = url
        self.url_to_code[url] = code
        self.click_counts[code] = 0

        return code

    def open_url(self, code):
        """
        Return the original URL for a short code and increment click count.
        Returns None if code not found.
        """
        if code in self.code_to_url:
            self.click_counts[code] += 1
            return self.code_to_url[code]
        return None

    def get_stats(self, code):
        """
        Return a dictionary: { "code": ..., "url": ..., "clicks": ... }
        Returns None if code not found.
        """
        if code in self.code_to_url:
            return {
                "code": code,
                "url": self.code_to_url[code],
                "clicks": self.click_counts[code]
            }
        return None


shortener = URLShortener()

url1 = "https://example.com/products/usb-cable"
url2 = "https://example.com/about"
url3 = "https://example.com/products/usb-cable"  # same as url1

# Shorten URLs
code1 = shortener.shorten(url1)
code2 = shortener.shorten(url2)
code3 = shortener.shorten(url3)  # should match code1

print("Codes:", code1, code2, code3)  # code1 and code3 should match

# Open URLs
print("Open code1:", shortener.open_url(code1))
print("Open code1 again:", shortener.open_url(code1))
print("Open code2:", shortener.open_url(code2))

# Check stats
print("Stats code1:", shortener.get_stats(code1))
print("Stats code2:", shortener.get_stats(code2))
print("Stats code3:", shortener.get_stats(code3))