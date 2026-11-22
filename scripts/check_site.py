"""Validate built Jekyll output: links, assets, duplicate IDs, fragments and search index."""
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

REPO = Path(__file__).resolve().parents[1]
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else REPO / "_site"
BASEURL = sys.argv[2] if len(sys.argv) > 2 else "/uvy-docs-theme"


class Page(HTMLParser):
    def __init__(self, path: Path):
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f"{tag}: Duplicate ID {attrs['id']}"
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])


def resolve_local_target(page_path: Path, raw_path: str) -> Path | None:
    path = unquote(raw_path)
    if BASEURL and path.startswith(BASEURL + "/"):
        path = path[len(BASEURL):]
    elif BASEURL and path == BASEURL:
        path = "/"
    if path.startswith("/"):
        candidate = (ROOT / path.lstrip("/")).resolve()
    else:
        candidate = (page_path.parent / path).resolve() if path else page_path

    if candidate.is_dir():
        idx = candidate / "index.html"
        if idx.exists():
            return idx
        if candidate.with_suffix(".html").exists():
            return candidate.with_suffix(".html")
        return None
    if candidate.exists():
        return candidate
    if candidate.with_suffix(".html").exists():
        return candidate.with_suffix(".html")
    idx = candidate / "index.html"
    if idx.exists():
        return idx
    return None


html_files = sorted(ROOT.rglob("*.html"))
assert html_files, f"No built HTML pages found under {ROOT}"
pages = {path: Page(path) for path in html_files}

errors: list[str] = []
for path, page in pages.items():
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        if not url.path and not url.fragment:
            continue
        if not url.path:
            if unquote(url.fragment) not in page.ids:
                errors.append(f"{path}: missing local fragment #{url.fragment}")
            continue
        target = resolve_local_target(path, url.path)
        if target is None or not target.is_relative_to(ROOT):
            errors.append(f"{path}: broken link {link}")
            continue
        if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f"{path}: missing fragment {link}")

# Verify generated search index JSON
search_file = ROOT / "assets" / "js" / "search-data.json"
assert search_file.exists(), f"Missing search index: {search_file}"
search_data = json.loads(search_file.read_text(encoding="utf-8"))
assert isinstance(search_data, list) and len(search_data) >= 1, "Empty search index"
for entry in search_data:
    for key in ("title", "url", "headings", "content"):
        assert key in entry, f"Missing key {key} in search entry: {entry}"

assert not errors, "\n".join(errors)
print(f"Checked {len(pages)} HTML pages and {len(search_data)} search entries under {ROOT}")
