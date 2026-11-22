---
layout: default
title: Overview
nav_order: 1
permalink: /
---

# UnitVectorY-Labs Docs Theme

A standardized Jekyll remote theme implementing the [UnitVectorY-Labs Design Guide](https://unitvectory-labs.github.io/uvy-design/) for GitHub Pages documentation sites.

This documentation site is built with the theme itself and serves as the live reference for its layout, typography, callouts, code blocks, Mermaid diagrams, and full-text search.

## One-line setup

Switch any existing `just-the-docs` repository in `docs/_config.yml`:

```yaml
remote_theme: UnitVectorY-Labs/uvy-docs-theme@v0.2.0
plugins:
  - jekyll-remote-theme
```

Existing Markdown pages, frontmatter (`title`, `nav_order`, `parent`, `has_children`, `has_toc`, `permalink`), `{:toc}` outlines, callouts, Mermaid blocks, `nav_external_links`, and `gh_edit_*` settings continue working without edits.

## What the theme provides

- **UnitVectorY-Labs visual language:** Cool light surfaces (`#F5F7FA` / `#FFFFFF`), midnight blue-slate dark mode (`#090D16` / `#111827`), bright signal orange (`#F25C05` / `#FF7A1A`), fixed-width monospace headings and chrome paired with system sans prose, and zero external font dependencies.
- **Universal header and sticky footer:** `60px` top bar with the theme-adaptive isometric unit cube mark, a Tabler GitHub icon beside the direct sun/moon `uvy-theme` cookie toggle, reveal-on-scroll-up behavior, and an always-visible compact footer derived automatically from repository metadata.
- **Sticky navigation and mobile drawer:** Multi-level sidebar navigation ordered by `nav_order` and `parent`, collection groups, breadcrumbs, and an accessible focus-trapped mobile drawer below `768px`.
- **Client-side full-text search:** Build-time Liquid JSON index (`assets/js/search-data.json`) with keyboard navigation (`/` to focus, arrow keys, `Enter`, `Escape`) and zero external search libraries.
- **Documentation ergonomics:** Syntax-highlighted code blocks with copy bars, keyboard-scrollable tables, live-themed Mermaid diagrams, heading anchor links, and semantic callouts.

## Explore the documentation

- [Getting started](docs/getting-started.md) — Switch an existing repository or start a new docs site.
- [Configuration](docs/configuration.md) — Drop-in `just-the-docs` settings and optional `uvy_docs` keys.
- [Authoring](docs/authoring.md) — Page hierarchy, callouts, code blocks, tables, Mermaid diagrams, and search.
