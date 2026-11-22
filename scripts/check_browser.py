"""Playwright Chromium QA for uvy-docs-theme built sites."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import sys
import threading
from playwright.sync_api import sync_playwright, expect

REPO = Path(__file__).resolve().parents[1]
SITE_DIR = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else REPO / "_site"
BASEURL = sys.argv[2] if len(sys.argv) > 2 else "/uvy-docs-theme"
SEARCH_TERM = sys.argv[3] if len(sys.argv) > 3 else "mermaid"


class MountedHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        clean = path.split("?", 1)[0].split("#", 1)[0]
        if BASEURL and clean.startswith(BASEURL):
            clean = clean[len(BASEURL):] or "/"
        rel = clean.lstrip("/")
        candidate = SITE_DIR / rel
        if candidate.is_dir():
            if (candidate / "index.html").exists():
                candidate = candidate / "index.html"
            elif candidate.with_suffix(".html").exists():
                candidate = candidate.with_suffix(".html")
        elif not candidate.exists() and candidate.with_suffix(".html").exists():
            candidate = candidate.with_suffix(".html")
        return str(candidate)

    def log_message(self, format, *args):
        pass


def check_layout(page, check_footer_height=True):
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"Overflow: {page.url}"
    assert page.locator("h1").count() == 1, f"Expected 1 h1: {page.url}"
    assert page.locator(".site-header .uvy-mark polygon").count() == 3, page.url
    assert page.locator(".site-header nav").count() == 0, f"Unexpected top nav tabs: {page.url}"
    assert page.locator(".site-header .header-actions a.icon-button").count() == 1, page.url
    assert page.locator("#theme svg:visible").count() == 1, page.url
    if page.viewport_size["width"] >= 768:
        assert page.locator("#menu").is_hidden(), f"#menu visible on desktop: {page.url}"
        assert page.locator("#menu-close").is_hidden(), f"#menu-close visible on desktop: {page.url}"
    assert "UVY" not in page.title(), f"Unexpected UVY in title: {page.title()}"
    brand_text = page.locator(".site-header .brand").inner_text()
    assert "UVY" not in brand_text, f"Unexpected UVY in brand: {brand_text}"
    assert page.evaluate(
        "Math.abs(document.getElementById('theme').getBoundingClientRect().right - document.querySelector('.header-inner').getBoundingClientRect().right) < 2"
    ), page.url
    assert page.evaluate(
        "document.getElementById('theme').getBoundingClientRect().top < document.querySelector('.header-inner').getBoundingClientRect().top + 32"
    ), page.url
    foot = page.locator(".site-footer").evaluate(
        "el => { const r = el.getBoundingClientRect(); return { top: r.top, bottom: r.bottom, height: r.height, vh: window.innerHeight }; }"
    )
    assert foot["top"] >= 0 and foot["bottom"] <= foot["vh"] + 2, f"Footer not visible: {foot} ({page.url})"
    if check_footer_height:
        max_foot_h = 56 if page.viewport_size["width"] >= 768 else 96
        assert foot["height"] <= max_foot_h, f"Footer too tall: {foot['height']} ({page.url})"
    foot_text = page.locator(".site-footer").inner_text()
    assert "UnitVectorY-Labs" in foot_text, page.url
    assert "on GitHub" in foot_text, page.url
    sidebar_note = page.locator(".uvy-docs-sidebar-footer a")
    assert sidebar_note.count() == 1, f"Missing sidebar theme link: {page.url}"
    assert sidebar_note.get_attribute("href") == "https://github.com/UnitVectorY-Labs/uvy-docs-theme", page.url
    assert "uvy-docs-theme" in (sidebar_note.text_content() or ""), page.url


def contrast_ratios(page, selector):
    return page.locator(selector).evaluate_all(
        """elements => {
      const ctx = document.createElement('canvas').getContext('2d');
      function rgb(color){ctx.clearRect(0,0,1,1);ctx.fillStyle=color;ctx.fillRect(0,0,1,1);return [...ctx.getImageData(0,0,1,1).data].slice(0,3);}
      function lum(color){return rgb(color).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);}
      return elements.map(el => {
        const style = getComputedStyle(el);
        const a = lum(style.color), b = lum(style.backgroundColor);
        return (Math.max(a,b)+.05)/(Math.min(a,b)+.05);
      });
    }"""
    )


def discover_urls():
    urls = []
    for f in sorted(SITE_DIR.rglob("*.html")):
        rel = f.relative_to(SITE_DIR).as_posix()
        if rel == "index.html":
            urls.append(f"{BASEURL}/")
        elif rel.endswith("/index.html"):
            urls.append(f"{BASEURL}/{rel[:-len('index.html')]}")
        else:
            urls.append(f"{BASEURL}/{rel}")
    return urls


server = ThreadingHTTPServer(("127.0.0.1", 0), MountedHandler)
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
base = f"http://127.0.0.1:{port}"
urls = discover_urls()

try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        errors = []
        layout_count = 0

        for theme in ["light", "dark"]:
            context = browser.new_context(color_scheme=theme)
            page = context.new_page()
            page.on("pageerror", lambda err: errors.append(str(err)))
            for u in urls:
                for width in [320, 375, 1280]:
                    page.set_viewport_size({"width": width, "height": 900})
                    page.goto(base + u, wait_until="domcontentloaded")
                    check_layout(page)
                    layout_count += 1
            # Callout & sidebar contrast check
            for u in urls:
                page.set_viewport_size({"width": 1280, "height": 900})
                page.goto(base + u, wait_until="domcontentloaded")
                if page.locator("p.highlight, p.important, p.new, p.note, p.warning").count() > 0:
                    ratios = contrast_ratios(page, "p.highlight, p.important, p.new, p.note, p.warning")
                    assert min(ratios) >= 4.5, f"Low callout contrast ({theme}): {ratios}"
            # Sidebar heading prominence and sidebar footer contrast against --uvy-bg
            page.set_viewport_size({"width": 1280, "height": 900})
            page.goto(base + urls[0], wait_until="domcontentloaded")
            sidebar_checks = page.evaluate(
                """() => {
              const ctx = document.createElement('canvas').getContext('2d');
              function rgb(color){ctx.clearRect(0,0,1,1);ctx.fillStyle=color;ctx.fillRect(0,0,1,1);return [...ctx.getImageData(0,0,1,1).data].slice(0,3);}
              function lum(color){return rgb(color).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);}
              function ratio(fg, bg){const a=lum(fg), b=lum(bg); return (Math.max(a,b)+.05)/(Math.min(a,b)+.05);}
              const bg = getComputedStyle(document.body).backgroundColor;
              const groups = [...document.querySelectorAll('.sidebar .sidebar-group')].map(el => {
                const s = getComputedStyle(el);
                return { weight: parseInt(s.fontWeight, 10), borderBottom: parseFloat(s.borderBottomWidth), contrast: ratio(s.color, bg) };
              });
              const footerP = document.querySelector('.uvy-docs-sidebar-footer p');
              const footerA = document.querySelector('.uvy-docs-sidebar-footer a');
              return {
                groups,
                footerTextContrast: ratio(getComputedStyle(footerP).color, bg),
                footerLinkContrast: ratio(getComputedStyle(footerA).color, bg),
              };
            }"""
            )
            assert sidebar_checks["groups"], f"Expected sidebar groups ({theme})"
            for g in sidebar_checks["groups"]:
                assert g["weight"] >= 700, f"Sidebar group should be bold ({theme}): {g}"
                assert g["borderBottom"] >= 1, f"Sidebar group should be underlined ({theme}): {g}"
                assert g["contrast"] >= 4.5, f"Low sidebar group contrast ({theme}): {g}"
            assert sidebar_checks["footerTextContrast"] >= 4.5, f"Low sidebar footer text contrast ({theme}): {sidebar_checks}"
            assert sidebar_checks["footerLinkContrast"] >= 4.5, f"Low sidebar footer link contrast ({theme}): {sidebar_checks}"
            context.close()

        # Cookie theme persistence, hover logo stability, typography, search, copy button, zoom
        context = browser.new_context(viewport={"width": 1280, "height": 900}, color_scheme="light")
        page = context.new_page()
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.goto(base + urls[0], wait_until="domcontentloaded")

        # Logo colors must stay static on hover
        def logo_colors():
            return page.evaluate(
                """() => [...document.querySelectorAll('.site-header .uvy-mark polygon')].map(el => {
              const s = getComputedStyle(el); return [s.fill, s.stroke];
            })"""
            )
        before_hover = logo_colors()
        page.locator(".site-header .brand").hover()
        page.wait_for_timeout(150)
        assert logo_colors() == before_hover, "Logo mark colors changed on hover"

        # Monospace headings vs sans body
        h1_font = page.locator("h1").evaluate("el => getComputedStyle(el).fontFamily")
        p_font = page.locator(".uvy-docs-article p").first.evaluate("el => getComputedStyle(el).fontFamily")
        assert h1_font != p_font, (h1_font, p_font)

        # Theme toggle persists via cookie across pages
        page.locator("#theme").click()
        assert page.locator("html").get_attribute("data-theme") == "dark"
        cookies = {c["name"]: c["value"] for c in context.cookies()}
        assert cookies.get("uvy-theme") == "dark", cookies
        if len(urls) > 1:
            page.goto(base + urls[1], wait_until="domcontentloaded")
            assert page.locator("html").get_attribute("data-theme") == "dark"
        page.locator("#theme").click()
        assert page.locator("html").get_attribute("data-theme") == "light"

        # Full-text search
        search = page.locator("#docs-search")
        expect(search).to_be_visible()
        search.fill(SEARCH_TERM)
        expect(page.locator("#docs-search-results")).to_be_visible()
        assert page.locator("#docs-nav").is_hidden()
        assert page.locator("#docs-search-results .uvy-docs-search__item").count() >= 1
        search.press("Escape")
        expect(page.locator("#docs-nav")).to_be_visible()
        expect(page.locator("#docs-search-results")).to_be_hidden()

        # Code copy button
        if page.locator(".uvy-code .uvy-copy").count() > 0:
            btn = page.locator(".uvy-code .uvy-copy").first
            btn.click()
            expect(btn).to_have_class(re.compile(r"\bis-copied\b"))

        # Verify reveal-on-scroll-up header behavior on a tall page
        for u in urls:
            page.goto(base + u, wait_until="domcontentloaded")
            doc_h = page.evaluate("document.documentElement.scrollHeight")
            if doc_h > 1300:
                page.evaluate("window.scrollTo(0, 500)")
                page.wait_for_timeout(250)
                assert "is-hidden" in (page.locator(".site-header").get_attribute("class") or ""), f"Header should hide on scroll down ({u})"
                page.evaluate("window.scrollTo(0, 320)")
                page.wait_for_timeout(250)
                assert "is-hidden" not in (page.locator(".site-header").get_attribute("class") or ""), f"Header should reveal on scroll up ({u})"
                assert page.locator(".site-header").evaluate("el => el.getBoundingClientRect().top") >= -1
                break

        # 200% zoom
        page.set_viewport_size({"width": 640, "height": 900})
        page.evaluate("document.documentElement.style.fontSize = '200%'")
        check_layout(page, check_footer_height=False)
        context.close()

        # Mobile drawer interaction
        context = browser.new_context(viewport={"width": 375, "height": 900}, color_scheme="light")
        page = context.new_page()
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.goto(base + urls[0], wait_until="domcontentloaded")
        page.locator("#menu").click()
        assert page.locator("#sidebar").get_attribute("aria-modal") == "true"
        page.keyboard.press("Escape")
        assert page.locator("#menu").evaluate("el => el === document.activeElement")
        assert page.locator("#sidebar").evaluate("el => el.inert")
        context.close()

        # No-JS fallback
        context = browser.new_context(java_script_enabled=False, color_scheme="dark", viewport={"width": 320, "height": 900})
        page = context.new_page()
        for u in urls:
            page.goto(base + u, wait_until="domcontentloaded")
            assert page.locator("h1").count() == 1
            assert page.locator("#theme").is_hidden()
            assert page.locator("#sidebar").is_visible()
            assert page.locator("#docs-search").is_hidden()
            assert not page.evaluate("document.documentElement.scrollWidth > innerWidth"), f"No-JS overflow: {u}"
        context.close()

        assert not errors, errors
        browser.close()
        print(f"Passed {layout_count} theme/viewport checks across {len(urls)} pages; cookie theme, search, copy, drawer, contrast, zoom and no-JS verified")
finally:
    server.shutdown()
