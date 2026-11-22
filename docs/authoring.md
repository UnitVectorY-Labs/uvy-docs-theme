---
layout: default
title: Authoring
nav_order: 4
permalink: /authoring/
has_children: true
---

# Authoring

Write documentation in standard GitHub-flavored Markdown with Kramdown frontmatter. Every page uses `layout: default` and includes a single `# H1` heading at the top of the document.

## Frontmatter fields

| Field | Type | Description |
|---|---|---|
| `layout` | string | Always `default` |
| `title` | string | Label in the sidebar, breadcrumbs, search results, and `<title>` |
| `nav_order` | number | Sort order among sibling pages (pages without `nav_order` sort alphabetically afterward) |
| `permalink` | string | Stable page path such as `/usage` or `/configuration/workspace` |
| `parent` | string | Exact `title` of the parent page for nested navigation and breadcrumbs |
| `grand_parent` | string | Optional grandparent `title` for three-level hierarchies |
| `has_children` | boolean | Renders the automatic section index at the bottom of the page |
| `has_toc` | boolean | Set to `false` on a parent page to suppress the automatic child index |
| `nav_exclude` | boolean | Excludes the page from sidebar navigation |
| `search_exclude` | boolean | Excludes the page from `assets/js/search-data.json` |

## Page hierarchy

When a page sets `parent: Authoring`, it appears indented under **Authoring** in the left sidebar and displays monospace breadcrumbs (`UnitVectorY-Labs Docs Theme / Authoring / Page`) above its title.

Setting `has_children: true` on the parent page automatically generates the directory list below unless `has_toc: false` is specified.
