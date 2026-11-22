<p align="left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/uvy-standalone-mark-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="assets/uvy-standalone-mark-light.svg" />
    <img src="assets/uvy-standalone-mark-light.svg" alt="UnitVectorY-Labs" width="48" height="48" />
  </picture>
</p>

# uvy-docs-theme

Standardized Jekyll remote theme implementing the [UnitVectorY-Labs Design Guide](https://unitvectory-labs.github.io/uvy-design/) for GitHub Pages documentation sites.

Live documentation (hosted with this theme): [unitvectory-labs.github.io/uvy-docs-theme](https://unitvectory-labs.github.io/uvy-docs-theme/)

## Quick start

In your repository's `docs/_config.yml`:

```yaml
remote_theme: UnitVectorY-Labs/uvy-docs-theme@v0.3.0
plugins:
  - jekyll-remote-theme
```

`uvy-docs-theme` is drop-in compatible with existing `just-the-docs` frontmatter (`title`, `nav_order`, `parent`, `has_children`, `has_toc`, `permalink`), `{:toc}`, callouts, Mermaid blocks, `nav_external_links`, `aux_links`, `just_the_docs.collections`, and `gh_edit_*` settings.

## Local preview and checks

```sh
bundle install
bundle exec jekyll build
python3 scripts/check_site.py
```

For browser regression checks (light/dark modes, mobile drawer, search, copy buttons, contrast, and no-JS fallback):

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-browser.txt
.venv/bin/python -m playwright install --with-deps chromium
.venv/bin/python scripts/check_browser.py
```
