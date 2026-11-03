"""Prüft die statische Website ohne zusätzliche Abhängigkeiten."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.language = None
        self.headings = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.language = attrs.get("lang")
        if tag == "h1":
            self.headings += 1
        if "id" in attrs:
            assert attrs["id"] not in self.ids, "Doppelte HTML-ID"
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])


parser = SiteParser()
parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
parser.close()
assert parser.language == "de", "Die Seitensprache muss Deutsch sein"
assert parser.headings == 1, "Genau eine Hauptüberschrift erforderlich"
for link in parser.links:
    url = urlsplit(link)
    if url.scheme or url.netloc:
        assert url.scheme in ("https", "mailto", "tel"), "Unsicherer externer Link"
        continue
    if url.path:
        assert (ROOT / url.path).is_file(), f"Lokale Datei fehlt: {link}"
    if url.fragment and not url.path:
        assert url.fragment in parser.ids, f"Sprungziel fehlt: {link}"
assert "https://maps.app.goo.gl/HhwFWJqcy7rDhzZF8" in parser.links
assert "https://maps.app.goo.gl/fwjNqAUkVC915Zmy9" in parser.links
assert "https://maps.app.goo.gl/ZvrrkcyxLTmNJi4U7" in parser.links
assert "https://www.kolping-ebnit.at/" in parser.links
assert (ROOT / "style.css").stat().st_size > 0
print("Website erfolgreich geprüft: Sprache, Hauptüberschrift, IDs und lokale Links.")
