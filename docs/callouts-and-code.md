---
layout: default
title: Callouts and code
parent: Authoring
nav_order: 1
permalink: /authoring/callouts-and-code
---

# Callouts and code
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

- TOC
{:toc}

---

## Callouts

Apply Kramdown attribute lists directly above a paragraph or blockquote. Callout styles map to UnitVectorY-Labs semantic status colors with a `3px` left accent bar.

{: .highlight }
**Highlight:** Use `{: .highlight }` to emphasize an important constraint or operational rule.

{: .important }
Use `{: .important }` for required configuration steps or prerequisites.

{: .new }
Use `{: .new }` to call out newly added flags, options, or behaviors.

{: .note }
Use `{: .note }` for helpful context or cross-references that supplement the main flow.

{: .warning }
Use `{: .warning }` for destructive operations, breaking changes, or security caveats.

## Code blocks

Fenced code blocks are enhanced automatically with a language header bar, syntax highlighting calibrated for light and dark contrast, and a clipboard copy button.

```yaml
title: example-service
remote_theme: UnitVectorY-Labs/uvy-docs-theme@v0.1.0
plugins:
  - jekyll-remote-theme
```

```bash
git clone https://github.com/UnitVectorY-Labs/uvy-docs-theme.git
cd uvy-docs-theme
```

```go
package main

import "fmt"

func main() {
	fmt.Println("UnitVectorY-Labs Docs Theme")
}
```

## Tables

Markdown tables automatically receive keyboard-focusable horizontal scrolling (`.table-wrap`) so dense flag and configuration references never overflow narrow viewports.

| Flag | Environment variable | Default | Description |
|---|---|---|---|
| `--config` | `APP_CONFIG` | `.config.yaml` | Path to the YAML configuration file |
| `--workers` | `APP_WORKERS` | `8` | Maximum concurrent repository operations |
| `--dry-run` | — | `false` | Report planned changes without mutating local files |
| `--verbose` | — | `false` | Emit diagnostic request and command details |
