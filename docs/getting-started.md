---
layout: default
title: Getting started
nav_order: 2
permalink: /getting-started
---

# Getting started

`uvy-docs-theme` works directly with GitHub Pages branch publishing (`docs/` on `main`) via `jekyll-remote-theme`, requiring no custom GitHub Actions workflow in consuming repositories.

## Migrating from just-the-docs

1. Open `docs/_config.yml` in the target repository.
2. Replace `remote_theme: just-the-docs/just-the-docs@...` with a pinned `uvy-docs-theme` tag:

```yaml
title: ghorgsync
description: "Clone and update all organization repositories in one folder."

remote_theme: UnitVectorY-Labs/uvy-docs-theme@v0.3.0
plugins:
  - jekyll-remote-theme
```

3. Push to `main`. GitHub Pages rebuilds the site automatically using `jekyll-remote-theme`.

{: .note }
Because `uvy-docs-theme` keeps nested navigation sections expanded by default and styles Mermaid diagrams live for both light and dark modes, repository-local overrides such as `_sass/custom/custom.scss` or `_includes/mermaid_config.js` can usually be removed once migrated.

## Minimal configuration example

A complete `docs/_config.yml` for a UnitVectorY-Labs repository looks like this:

```yaml
title: my-tool
description: "Concise one-sentence summary of the repository."

remote_theme: UnitVectorY-Labs/uvy-docs-theme@v0.3.0
plugins:
  - jekyll-remote-theme

callouts:
  highlight:
    color: yellow
  important:
    title: Important
    color: blue
  new:
    title: New
    color: green
  note:
    title: Note
    color: purple
  warning:
    title: Warning
    color: red

mermaid:
  version: "12.3.0" # MERMAIDVERSION

nav_external_links:
  - title: my-tool on GitHub
    url: https://github.com/UnitVectorY-Labs/my-tool

gh_edit_link: true
gh_edit_link_text: "Edit this page on GitHub."
gh_edit_repository: "https://github.com/UnitVectorY-Labs/my-tool"
gh_edit_branch: "main"
gh_edit_source: "docs"
gh_edit_view_mode: "tree"
```

## Updating versions with repver

If the repository manages pinned versions with `repver`, point the target pattern in `.repver` at `uvy-docs-theme`:

```yaml
 - name: "docsthemeversion"
   params:
   - name: "version"
     pattern: "^v(?P<major>0|[1-9]\\d*)\\.(?P<minor>0|[1-9]\\d*)\\.(?P<patch>0|[1-9]\\d*)$"
   targets:
   - path: "docs/_config.yml"
     pattern: "^remote_theme: UnitVectorY-Labs/uvy-docs-theme@(?P<version>.*)$"
```
