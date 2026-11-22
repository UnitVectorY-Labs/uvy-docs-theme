---
layout: default
title: Configuration
nav_order: 3
permalink: /configuration
---

# Configuration
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

- TOC
{:toc}

---

## Drop-in configuration keys

`uvy-docs-theme` reads existing `just-the-docs` keys in `_config.yml` so repositories require only a single `remote_theme` change.

| Key | Purpose | Default |
|---|---|---|
| `title` | Product title displayed in `.site-header` and `<title>` | `Documentation` |
| `description` | HTML `<meta name="description">` fallback | *(omitted)* |
| `callouts` | Maps Kramdown class names to semantic colors and optional titles | Built-in `highlight`, `important`, `new`, `note`, `warning` |
| `mermaid.version` | Enables Mermaid rendering using jsDelivr at the pinned version | *(disabled)* |
| `nav_external_links` | External links appended under `Links` in the sidebar (`title`, `url`, `opens_in_new_tab`) | *(none)* |
| `aux_links` | GitHub URL fallback for the header repository icon and footer | Derived from `gh_edit_repository` |
| `gh_edit_link` | Displays an edit link beneath article content when `true` | `false` |
| `gh_edit_link_text` | Link text for the bottom edit link | `Edit this page on GitHub.` |
| `gh_edit_repository` | Repository URL used for edit links, header `GitHub` link, and footer attribution | Derived from `nav_external_links` or GitHub metadata |
| `gh_edit_branch` | Git branch used in edit and `LICENSE` links | `main` |
| `gh_edit_source` | Optional subdirectory containing Markdown sources (such as `docs`) | *(repo root)* |
| `gh_edit_view_mode` | GitHub path segment (`tree`, `blob`, or `edit`) | `blob` |
| `just_the_docs.collections` | Renders configured Jekyll collections as named sidebar groups | *(none)* |
| `search_enabled` | Set to `false` to disable sidebar full-text search | `true` |

## Optional `uvy_docs` keys

For new repositories or explicit overrides, you may set keys under `uvy_docs:` in `_config.yml`:

```yaml
uvy_docs:
  repository: "https://github.com/UnitVectorY-Labs/example-repo"
  repository_name: "example-repo"
  branch: "main"
  license: "Apache-2.0 License"
  license_url: "https://github.com/UnitVectorY-Labs/example-repo/blob/main/LICENSE"
  search_enabled: true
  wide: false
  header_links:
    - title: Docs
      url: "/"
      current: true
    - title: GitHub
      url: "https://github.com/UnitVectorY-Labs/example-repo"
```

| Key | Purpose | Fallback |
|---|---|---|
| `uvy_docs.repository` | GitHub repository URL for header and footer | `gh_edit_repository`, then first GitHub `nav_external_links` entry |
| `uvy_docs.repository_name` | Bold monospace repository slug in the footer | Last path segment of `repository` |
| `uvy_docs.branch` | Branch for generated `LICENSE` URL | `gh_edit_branch`, then `main` |
| `uvy_docs.license` | License label shown in the sticky footer | `MIT License` |
| `uvy_docs.license_url` | Explicit license destination URL | `<repository>/blob/<branch>/LICENSE` |
| `uvy_docs.search_enabled` | Toggle full-text search | `search_enabled` (`true`) |
| `uvy_docs.wide` | Opt into fluid `.page--wide` layout | `false` |
| `uvy_docs.header_links` | Optional top-bar navigation links (omitted by default so single-section docs stay free of redundant tabs) | *(none)* |

## Footer attribution

The sticky `.site-footer` always follows the UnitVectorY-Labs compact pattern:

`UnitVectorY-Labs | MIT License | <repository> on GitHub`

Because documentation sites typically publish from `/docs` rather than the repository root, the license link automatically points to `<repository>/blob/<branch>/LICENSE` unless overridden via `uvy_docs.license_url`.
