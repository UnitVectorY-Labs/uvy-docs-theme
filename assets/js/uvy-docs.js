// UnitVectorY-Labs Docs Theme enhancements: full-text search, code copy bars,
// table scroll regions and heading anchor links.
(function () {
  const scriptEl = document.currentScript;
  const searchIndexUrl =
    (scriptEl && scriptEl.dataset && scriptEl.dataset.searchIndex) ||
    "/assets/js/search-data.json";

  function enhanceCodeBlocks() {
    const article = document.querySelector(".uvy-docs-article");
    if (!article) return;

    const blocks = [];
    article.querySelectorAll("div.highlighter-rouge").forEach((div) => {
      if (div.closest(".uvy-code")) return;
      if (div.querySelector("code.language-mermaid")) return;
      blocks.push(div);
    });
    article.querySelectorAll("pre").forEach((pre) => {
      if (pre.closest(".uvy-code") || pre.closest("div.highlighter-rouge")) return;
      if (pre.querySelector("code.language-mermaid")) return;
      blocks.push(pre);
    });

    let seq = 0;
    blocks.forEach((node) => {
      const code = node.querySelector("code") || node;
      const cls = (node.className + " " + (code.className || "")).trim();
      const langMatch = cls.match(/language-([a-zA-Z0-9_+-]+)/);
      const lang = langMatch ? langMatch[1] : "text";
      if (lang === "mermaid") return;

      const codeId = "uvy-code-block-" + ++seq;
      code.id = code.id || codeId;
      const pre = node.tagName === "PRE" ? node : node.querySelector("pre");
      if (pre && !pre.hasAttribute("tabindex")) pre.setAttribute("tabindex", "0");

      const wrap = document.createElement("div");
      wrap.className = "uvy-code";

      const bar = document.createElement("div");
      bar.className = "uvy-code__bar";

      const label = document.createElement("span");
      label.textContent = lang;

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "uvy-button--quiet uvy-button--small uvy-copy";
      btn.dataset.copyTarget = code.id;
      btn.setAttribute("aria-label", "Copy " + lang + " code");
      btn.innerHTML =
        '<span data-copy class="with-icon">' +
        '<svg class="icon icon-small" aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><use href="#tabler-copy"></use></svg>' +
        "Copy</span>" +
        '<span data-copied class="with-icon">' +
        '<svg class="icon icon-small" aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><use href="#tabler-check"></use></svg>' +
        "Copied</span>";

      bar.append(label, btn);
      node.parentNode.insertBefore(wrap, node);
      wrap.append(bar, node);
    });
  }

  function enhanceTables() {
    const article = document.querySelector(".uvy-docs-article");
    if (!article) return;
    article.querySelectorAll("table").forEach((table) => {
      if (table.closest(".table-wrap")) return;
      const wrap = document.createElement("div");
      wrap.className = "table-wrap";
      wrap.setAttribute("role", "region");
      wrap.setAttribute("tabindex", "0");
      wrap.setAttribute("aria-label", "Scrollable table");
      table.parentNode.insertBefore(wrap, table);
      wrap.append(table);
    });
  }

  function enhanceHeadings() {
    const article = document.querySelector(".uvy-docs-article");
    if (!article) return;
    article.querySelectorAll("h2[id], h3[id], h4[id]").forEach((h) => {
      if (h.classList.contains("no_toc") || h.id === "section-pages-heading") return;
      if (h.querySelector(".uvy-heading-anchor")) return;
      const a = document.createElement("a");
      a.className = "uvy-heading-anchor";
      a.href = "#" + h.id;
      a.setAttribute("aria-label", "Link to section " + h.textContent.trim());
      a.textContent = "#";
      h.append(a);
    });
  }

  function highlightText(container, text, terms) {
    if (!text) return;
    const escaped = terms
      .filter(Boolean)
      .map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
    if (!escaped.length) {
      container.textContent = text;
      return;
    }
    const re = new RegExp("(" + escaped.join("|") + ")", "gi");
    const parts = text.split(re);
    parts.forEach((part, idx) => {
      if (idx % 2 === 1) {
        const m = document.createElement("mark");
        m.textContent = part;
        container.append(m);
      } else if (part) {
        container.append(document.createTextNode(part));
      }
    });
  }

  function decodeEntities(str) {
    if (!str || str.indexOf("&") === -1) return str || "";
    return str
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">")
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&apos;/g, "'")
      .replace(/&amp;/g, "&");
  }

  function buildSnippet(content, terms) {
    content = decodeEntities(content);
    if (!content) return "";
    const lower = content.toLowerCase();
    let bestPos = -1;
    for (const term of terms) {
      const p = lower.indexOf(term);
      if (p !== -1 && (bestPos === -1 || p < bestPos)) bestPos = p;
    }
    if (bestPos === -1) return content.slice(0, 120) + (content.length > 120 ? "…" : "");
    const start = Math.max(0, bestPos - 36);
    const end = Math.min(content.length, start + 128);
    let snippet = content.slice(start, end).trim();
    if (start > 0) snippet = "…" + snippet;
    if (end < content.length) snippet += "…";
    return snippet;
  }

  function initSearch() {
    const input = document.getElementById("docs-search");
    const resultsBox = document.getElementById("docs-search-results");
    const nav = document.getElementById("docs-nav");
    if (!input || !resultsBox || !nav) return;

    let docs = null;
    let loading = null;
    let activeIdx = -1;

    function loadIndex() {
      if (docs) return Promise.resolve(docs);
      if (loading) return loading;
      loading = fetch(searchIndexUrl)
        .then((res) => (res.ok ? res.json() : []))
        .then((data) => {
          docs = Array.isArray(data) ? data : [];
          return docs;
        })
        .catch(() => {
          docs = [];
          return docs;
        });
      return loading;
    }

    function setActive(index) {
      const items = [...resultsBox.querySelectorAll(".uvy-docs-search__item")];
      if (!items.length) {
        activeIdx = -1;
        return;
      }
      activeIdx = ((index % items.length) + items.length) % items.length;
      items.forEach((el, i) => {
        el.setAttribute("aria-selected", String(i === activeIdx));
      });
      items[activeIdx].scrollIntoView({ block: "nearest" });
    }

    function clearSearch() {
      resultsBox.hidden = true;
      resultsBox.textContent = "";
      nav.hidden = false;
      input.setAttribute("aria-expanded", "false");
      activeIdx = -1;
    }

    function renderResults(query, items) {
      const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
      const scored = [];

      items.forEach((doc) => {
        const title = doc.title || "";
        const titleL = title.toLowerCase();
        const content = doc.content || "";
        const contentL = content.toLowerCase();
        const headings = Array.isArray(doc.headings) ? doc.headings : [];

        let matchedAll = true;
        let score = 0;
        let matchedHeading = null;

        for (const term of terms) {
          let hit = false;
          if (titleL === term) {
            score += 40;
            hit = true;
          } else if (titleL.startsWith(term)) {
            score += 24;
            hit = true;
          } else if (titleL.includes(term)) {
            score += 16;
            hit = true;
          }

          for (const h of headings) {
            const hl = (h.text || "").toLowerCase();
            if (hl.includes(term)) {
              score += 10;
              hit = true;
              if (!matchedHeading) matchedHeading = h;
              break;
            }
          }

          if (contentL.includes(term)) {
            score += 4;
            hit = true;
          }

          if (!hit) {
            matchedAll = false;
            break;
          }
        }

        if (matchedAll && score > 0) {
          scored.push({ doc, score, matchedHeading });
        }
      });

      scored.sort((a, b) => b.score - a.score);
      const top = scored.slice(0, 12);

      resultsBox.textContent = "";
      nav.hidden = true;
      resultsBox.hidden = false;
      input.setAttribute("aria-expanded", "true");
      activeIdx = -1;

      if (!top.length) {
        const empty = document.createElement("p");
        empty.className = "uvy-docs-search__empty";
        empty.textContent = 'No matches for "' + query + '".';
        resultsBox.append(empty);
        return;
      }

      const meta = document.createElement("p");
      meta.className = "uvy-docs-search__meta";
      meta.textContent =
        scored.length === 1 ? "1 result" : scored.length + " results";

      const list = document.createElement("ul");
      list.className = "uvy-docs-search__list";
      list.setAttribute("role", "listbox");

      top.forEach(({ doc, matchedHeading }) => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.className = "uvy-docs-search__item";
        a.setAttribute("role", "option");
        a.setAttribute("aria-selected", "false");
        a.href = matchedHeading && matchedHeading.id
          ? doc.url + "#" + matchedHeading.id
          : doc.url;

        if (doc.parent) {
          const parentEl = document.createElement("span");
          parentEl.className = "uvy-docs-search__parent";
          parentEl.textContent = doc.parent;
          a.append(parentEl);
        }

        const titleEl = document.createElement("span");
        titleEl.className = "uvy-docs-search__title";
        const displayTitle = decodeEntities(
          matchedHeading ? doc.title + " — " + matchedHeading.text : doc.title
        );
        highlightText(titleEl, displayTitle, terms);
        a.append(titleEl);

        const snippet = buildSnippet(doc.content, terms);
        if (snippet) {
          const snipEl = document.createElement("span");
          snipEl.className = "uvy-docs-search__snippet";
          highlightText(snipEl, snippet, terms);
          a.append(snipEl);
        }

        li.append(a);
        list.append(li);
      });

      resultsBox.append(meta, list);
    }

    input.addEventListener("focus", () => {
      loadIndex();
    });

    input.addEventListener("input", async () => {
      const q = input.value.trim();
      if (!q) {
        clearSearch();
        return;
      }
      const items = await loadIndex();
      renderResults(q, items);
    });

    input.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        if (input.value) {
          event.preventDefault();
          event.stopPropagation();
          input.value = "";
          clearSearch();
        }
        return;
      }
      if (resultsBox.hidden) return;
      if (event.key === "ArrowDown") {
        event.preventDefault();
        setActive(activeIdx + 1);
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        setActive(activeIdx - 1);
      } else if (event.key === "Enter" && activeIdx >= 0) {
        const items = resultsBox.querySelectorAll(".uvy-docs-search__item");
        if (items[activeIdx]) {
          event.preventDefault();
          items[activeIdx].click();
        }
      }
    });

    // Global "/" shortcut to focus search
    document.addEventListener("keydown", (event) => {
      if (
        event.key !== "/" ||
        event.ctrlKey ||
        event.metaKey ||
        event.altKey
      )
        return;
      const tag = (document.activeElement && document.activeElement.tagName) || "";
      if (
        tag === "INPUT" ||
        tag === "TEXTAREA" ||
        tag === "SELECT" ||
        (document.activeElement && document.activeElement.isContentEditable)
      )
        return;
      event.preventDefault();
      const menu = document.getElementById("menu");
      if (menu && getComputedStyle(menu).display !== "none" && menu.getAttribute("aria-expanded") !== "true") {
        menu.click();
      }
      input.focus();
      input.select();
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    enhanceCodeBlocks();
    enhanceTables();
    enhanceHeadings();
    initSearch();
  });
})();
