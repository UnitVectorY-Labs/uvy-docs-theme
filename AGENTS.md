# Repository guidance

`uvy-docs-theme` is the standardized Jekyll remote theme (`jekyll-remote-theme`) implementing the [UnitVectorY-Labs Design Guide](https://github.com/UnitVectorY-Labs/uvy-design) for UnitVectorY-Labs GitHub Pages documentation sites. The repository also hosts its own documentation using itself.

## Design language and architecture

- **Single source of truth for base design:** `assets/css/uvy.css` and `assets/js/uvy.js` are copied verbatim from `UnitVectorY-Labs/uvy-design` (`site/uvy.css` and `site/uvy.js`). Keep theme-specific rules isolated in `assets/css/uvy-docs.css` and `assets/js/uvy-docs.js`, using `--uvy-*` custom properties and `light-dark()` exclusively.
- **Brand naming:** Always spell out `UnitVectorY-Labs` in user-facing titles, headers, headings, footers, and documentation prose. Reserve `uvy-` strictly for code identifiers, CSS tokens/classes, filenames, the `uvy-theme` cookie, and repository slugs (`uvy-docs-theme`, `uvy-design`).
- **Header and navigation conventions:**
  - Keep `.site-header` at `60px` desktop with the inline theme-adaptive isometric unit cube (`.uvy-mark`, static on hover) + monospace site title on the left, and `.header-actions` on the right holding the Tabler outline `brand-github` icon link (`a.icon-button`) immediately to the left of the `#theme` sun/moon cookie toggle.
  - Omit top-bar `<nav>` tabs by default on single-section documentation sites; only render `<nav>` when `uvy_docs.header_links` is explicitly configured.
  - Preserve reveal-on-scroll-up `.site-header` behavior (`.is-hidden` on downward scroll past the header, returning immediately on upward scroll, top of page, drawer open, or `:focus-within`), coordinated with desktop `.sidebar` sticky `top` offset so sidebar tools and search are never obscured.
  - Keep the compact always-visible sticky `.site-footer` (`UnitVectorY-Labs | <license> | <repo> on GitHub`, linking `LICENSE` to `<repo>/blob/<branch>/LICENSE` for `/docs` deployments).
- **Typography and content geometry:** Keep Markdown prose (`p`, `li`, `blockquote`, callouts) capped at `70ch` in `--uvy-font-sans`, with headings, navigation, controls, table headers, and code in `--uvy-font-mono`, while allowing `.table-wrap` tables, `.uvy-code` blocks, and `.uvy-mermaid` diagrams to use the full `.workspace` width.

## Jekyll and GitHub Pages constraints

- Consuming repositories build on classic GitHub Pages (`github-pages` gem / Jekyll 3.10 / Liquid 4.0.4) via `remote_theme: UnitVectorY-Labs/uvy-docs-theme@vX.Y.Z`.
- `jekyll-remote-theme` only exposes `_layouts/`, `_includes/`, `_sass/`, and `assets/` to consuming sites. Keep theme-supplied Liquid assets such as `assets/js/search-data.json` inside `assets/`.
- Keep all Liquid templates compatible with Liquid 4.0.4 (avoid Liquid 5 filters such as `find`, and guard `sort: "nav_order"` against `nil` values by splitting ordered and unordered pages).
- Preserve drop-in `just-the-docs` backwards compatibility (`layout: default`, `title`, `nav_order`, `parent`, `grand_parent`, `has_children`, `has_toc`, `permalink`, `just_the_docs.collections`, `{:toc}` / `.no_toc` / `.text-delta`, Kramdown callouts scoped strictly to `p`/`blockquote` so Rouge `div.highlight` is unaffected, `mermaid.version`, `nav_external_links`, `aux_links`, and `gh_edit_*`).

## Verification before shipping

1. Build locally with `bundle exec jekyll build`.
2. Run `python3 scripts/check_site.py` (links, assets, duplicate IDs, fragments, and valid `search-data.json`).
3. Run `python3 scripts/check_browser.py` (light/dark modes, `320px`/`375px`/`1280px`, `200%` zoom, reveal-on-scroll-up header, cookie theme persistence, mobile drawer, full-text search, copy buttons, contrast `>= 4.5:1`, and no-JS fallback).
4. Inspect rendered screenshots in both light and dark modes when changing visual styles or layouts.

## Release procedure (mandatory)

Whenever publishing a new theme version (`vX.Y.Z`):

1. Update version references in `uvy-docs-theme.gemspec`, `README.md`, `index.md`, and `docs/` examples.
2. Ensure `main` passes `.github/workflows/pages.yml` cleanly.
3. Create and push an annotated Git tag (`git tag -a vX.Y.Z -m "vX.Y.Z" && git push origin vX.Y.Z`).
4. **Always create a corresponding GitHub Release** for every tag using `gh release create vX.Y.Z --title "vX.Y.Z" --notes "..."` (or `--generate-notes`) so downstream automation and release tracking stay in sync.
