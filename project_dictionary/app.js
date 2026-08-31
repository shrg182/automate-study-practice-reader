(() => {
  "use strict";

  const entries = Array.isArray(window.DICTIONARY_ENTRIES) ? window.DICTIONARY_ENTRIES : [];
  const PAGE_SIZE = 50;
  const languageNames = { zh: "Chinese", en: "English", ru: "Russian" };
  const difficultyNames = {
    1: "Common",
    2: "Intermediate",
    3: "Advanced",
    4: "Rare",
    5: "Specialist"
  };
  const STORAGE_KEY = "reading-lexicon-entry-overrides-v1";
  const entryKeys = entries.map((entry) => `${entry.language}\u0000${entry.term}`);
  let activeEntry = null;
  let overrides = {};
  const state = { query: "", language: "all", minDifficulty: 0, sort: "term", page: 1 };

  const elements = {
    grid: document.querySelector("#dictionary-grid"),
    table: document.querySelector("#dictionary-table"),
    search: document.querySelector("#search"),
    difficulty: document.querySelector("#difficulty-filter"),
    sort: document.querySelector("#sort"),
    summary: document.querySelector("#results-summary"),
    pagination: document.querySelector("#pagination"),
    empty: document.querySelector("#empty-state"),
    clear: document.querySelector("#clear-search"),
    panel: document.querySelector("#detail-panel"),
    detail: document.querySelector("#detail-content"),
    close: document.querySelector("#close-panel"),
    scrim: document.querySelector("#scrim")
  };

  const collator = new Intl.Collator(["zh-Hans-CN", "en"], { sensitivity: "base", numeric: true });
  const escapeHtml = (value) => String(value || "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  })[character]);

  try {
    overrides = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
  } catch (_error) {
    overrides = {};
  }
  entries.forEach((entry, index) => Object.assign(entry, overrides[entryKeys[index]] || {}));

  function searchable(entry) {
    return [entry.term, entry.pinyin, entry.type, entry.definition, entry.example, entry.sources, entry.source_details]
      .join(" ").toLocaleLowerCase();
  }

  function filteredEntries() {
    const query = state.query.trim().toLocaleLowerCase();
    const filtered = entries.filter((entry) =>
      (state.language === "all" || entry.language === state.language) &&
      Number(entry.difficulty || 3) >= state.minDifficulty &&
      (!query || searchable(entry).includes(query))
    );
    return filtered.sort((a, b) => {
      if (state.sort === "frequency") {
        return Number(b.occurrence_count) - Number(a.occurrence_count) || collator.compare(a.term, b.term);
      }
      if (state.sort === "difficulty-desc") {
        return Number(b.difficulty) - Number(a.difficulty) || collator.compare(a.pinyin || a.term, b.pinyin || b.term);
      }
      if (state.sort === "difficulty-asc") {
        return Number(a.difficulty) - Number(b.difficulty) || collator.compare(a.pinyin || a.term, b.pinyin || b.term);
      }
      if (state.sort === "entry-time") {
        return String(b.entry_time || "").localeCompare(String(a.entry_time || "")) ||
          collator.compare(a.pinyin || a.term, b.pinyin || b.term);
      }
      if (state.sort === "source") return collator.compare(a.sources, b.sources);
      return collator.compare(a.pinyin || a.term, b.pinyin || b.term);
    });
  }

  function render() {
    const filtered = filteredEntries();
    const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
    state.page = Math.min(state.page, pageCount);
    const start = (state.page - 1) * PAGE_SIZE;
    const shown = filtered.slice(start, start + PAGE_SIZE);
    elements.grid.innerHTML = shown.map((entry, rowIndex) => {
      const index = entries.indexOf(entry);
      const sourceDetails = entry.source_details || entry.sources || "Source unavailable";
      const difficulty = Number(entry.difficulty) || 3;
      const targets = String(entry.source_targets || entry.sources || "").split("; ").filter(Boolean);
      const sourceLinks = targets.slice(0, 2).map((target, targetIndex) =>
        `<a href="../${escapeHtml(location.protocol === "file:" ? target : target.replace(/^practice\//, ""))}" target="_blank" aria-label="Open source ${targetIndex + 1} for ${escapeHtml(entry.term)}">${targetIndex ? "Open 2" : "Open"}</a>`
      ).join("");
      return `
        <div class="entry-row" role="row" tabindex="0" data-index="${index}" aria-label="View ${escapeHtml(entry.term)}">
          <span class="cell-index" role="cell">${start + rowIndex + 1}</span>
          <span class="entry-term" role="cell">${escapeHtml(entry.term)}</span>
          <span class="pinyin" role="cell">${escapeHtml(entry.pinyin || "—")}</span>
          <span role="cell"><span class="language-tag">${escapeHtml(entry.language)}</span></span>
          <span class="entry-type" role="cell">${escapeHtml(entry.type || "term")}</span>
          <span role="cell"><span class="difficulty difficulty-${difficulty}"><b>${difficulty}</b> ${difficultyNames[difficulty]}</span></span>
          <span class="definition" role="cell">${escapeHtml(entry.definition || "Definition pending source review.")}</span>
          <span class="source-cell" role="cell" title="${escapeHtml(sourceDetails)}">${escapeHtml(sourceDetails)}</span>
          <span class="cell-open" role="cell">${sourceLinks || "—"}${targets.length > 2 ? `<small>+${targets.length - 2}</small>` : ""}</span>
          <span class="cell-count" role="cell">${entry.occurrence_count}<span aria-hidden="true"> ↗</span></span>
        </div>`;
    }).join("");

    const end = Math.min(start + shown.length, filtered.length);
    elements.summary.textContent = filtered.length
      ? `Showing ${start + 1}–${end} of ${filtered.length.toLocaleString()} matching entries`
      : "Showing 0 matching entries";
    elements.empty.hidden = filtered.length !== 0;
    elements.table.hidden = filtered.length === 0;
    renderPagination(pageCount, filtered.length);
    elements.clear.hidden = !state.query;
  }

  function renderPagination(pageCount, resultCount) {
    if (!resultCount || pageCount <= 1) {
      elements.pagination.hidden = true;
      elements.pagination.innerHTML = "";
      return;
    }
    const candidates = new Set([1, pageCount, state.page - 2, state.page - 1, state.page, state.page + 1, state.page + 2]);
    const pages = [...candidates].filter((page) => page >= 1 && page <= pageCount).sort((a, b) => a - b);
    const parts = [`<button type="button" data-page="${state.page - 1}" ${state.page === 1 ? "disabled" : ""} aria-label="Previous page">←</button>`];
    pages.forEach((page, index) => {
      if (index && page - pages[index - 1] > 1) parts.push(`<span class="page-gap" aria-hidden="true">…</span>`);
      parts.push(`<button type="button" data-page="${page}" ${page === state.page ? 'class="active" aria-current="page"' : ""}>${page}</button>`);
    });
    parts.push(`<button type="button" data-page="${state.page + 1}" ${state.page === pageCount ? "disabled" : ""} aria-label="Next page">→</button>`);
    elements.pagination.innerHTML = parts.join("");
    elements.pagination.hidden = false;
  }

  function renderDetail(entry, editing = false) {
    const sources = String(entry.source_details || entry.sources || "").split("; ").filter(Boolean);
    const difficulty = Number(entry.difficulty) || 3;
    if (editing) {
      elements.detail.innerHTML = `
        <form id="entry-edit-form" class="entry-edit-form">
          <p class="detail-language">Editing local browser copy</p>
          <div class="edit-grid">
            <label>Term<input name="term" required value="${escapeHtml(entry.term)}"></label>
            <label>Reading<input name="pinyin" value="${escapeHtml(entry.pinyin)}"></label>
            <label>Type<input name="type" value="${escapeHtml(entry.type)}"></label>
            <label>Difficulty
              <select name="difficulty">
                ${Object.entries(difficultyNames).map(([level, name]) =>
                  `<option value="${level}" ${Number(level) === difficulty ? "selected" : ""}>${level} · ${name}</option>`
                ).join("")}
              </select>
            </label>
          </div>
          <label>Meaning & notes<textarea name="definition" rows="6">${escapeHtml(entry.definition)}</textarea></label>
          <label>Example / context<textarea name="example" rows="4">${escapeHtml(entry.example)}</textarea></label>
          <label>Source details<textarea name="source_details" rows="4">${escapeHtml(entry.source_details || entry.sources)}</textarea></label>
          <p class="edit-note">Edits are saved in this browser. Source-file links are preserved separately.</p>
          <div class="edit-actions">
            <button class="save-edit" type="submit">Save changes</button>
            <button id="cancel-edit" type="button">Cancel</button>
            <button id="reset-edit" class="reset-edit" type="button">Reset local edits</button>
          </div>
        </form>`;
      return;
    }
    elements.detail.innerHTML = `
      <div class="detail-heading">
        <p class="detail-language">${escapeHtml(languageNames[entry.language] || entry.language)} · ${escapeHtml(entry.type)} · Level ${difficulty} ${escapeHtml(difficultyNames[difficulty])}</p>
        <button id="edit-entry" class="edit-entry" type="button">Edit entry</button>
      </div>
      <h2 id="detail-term">${escapeHtml(entry.term)}</h2>
      ${entry.pinyin ? `<p class="detail-pinyin">${escapeHtml(entry.pinyin)}</p>` : ""}
      <section class="detail-section">
        <h3>Meaning & notes</h3>
        <p>${escapeHtml(entry.definition || "Definition pending source review.")}</p>
      </section>
      ${entry.example ? `<section class="detail-section"><h3>In context</h3><p>“${escapeHtml(entry.example)}”</p></section>` : ""}
      <section class="detail-section">
        <h3>${entry.occurrence_count} ${Number(entry.occurrence_count) === 1 ? "occurrence" : "occurrences"}</h3>
        <ul class="source-list">${sources.map((source) => `<li>${escapeHtml(source)}</li>`).join("")}</ul>
      </section>`;
  }

  function persistEntry(entry) {
    const index = entries.indexOf(entry);
    overrides[entryKeys[index]] = {
      term: entry.term,
      pinyin: entry.pinyin,
      type: entry.type,
      difficulty: entry.difficulty,
      definition: entry.definition,
      example: entry.example,
      source_details: entry.source_details
    };
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(overrides));
      return true;
    } catch (_error) {
      return false;
    }
  }

  function openPanel(entry) {
    activeEntry = entry;
    renderDetail(entry);
    elements.panel.classList.add("open");
    document.body.classList.add("panel-open");
    elements.panel.setAttribute("aria-hidden", "false");
    elements.scrim.hidden = true;
    elements.close.focus();
  }

  function closePanel() {
    activeEntry = null;
    elements.panel.classList.remove("open");
    document.body.classList.remove("panel-open");
    elements.panel.setAttribute("aria-hidden", "true");
    elements.scrim.hidden = true;
  }

  document.querySelector("#entry-count").textContent = entries.length.toLocaleString();
  ["all", "zh", "en", "ru"].forEach((language) => {
    const count = language === "all" ? entries.length : entries.filter((entry) => entry.language === language).length;
    document.querySelector(`#count-${language}`).textContent = count.toLocaleString();
  });

  elements.search.addEventListener("input", (event) => {
    state.query = event.target.value;
    state.page = 1;
    render();
  });
  elements.sort.addEventListener("change", (event) => {
    state.sort = event.target.value;
    state.page = 1;
    render();
  });
  elements.difficulty.addEventListener("change", (event) => {
    state.minDifficulty = Number(event.target.value);
    state.page = 1;
    render();
  });
  document.querySelectorAll(".filter").forEach((button) => button.addEventListener("click", () => {
    document.querySelector(".filter.active").classList.remove("active");
    button.classList.add("active");
    state.language = button.dataset.language;
    state.page = 1;
    render();
  }));
  elements.pagination.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-page]");
    if (!button || button.disabled) return;
    state.page = Number(button.dataset.page);
    render();
    elements.table.scrollTop = 0;
    elements.table.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  elements.clear.addEventListener("click", () => {
    elements.search.value = "";
    state.query = "";
    state.page = 1;
    elements.search.focus();
    render();
  });
  elements.grid.addEventListener("click", (event) => {
    if (event.target.closest("a")) return;
    const row = event.target.closest(".entry-row");
    if (row) openPanel(entries[Number(row.dataset.index)]);
  });
  elements.grid.addEventListener("keydown", (event) => {
    if ((event.key === "Enter" || event.key === " ") && !event.target.closest("a")) {
      event.preventDefault();
      const row = event.target.closest(".entry-row");
      if (row) openPanel(entries[Number(row.dataset.index)]);
    }
  });
  elements.close.addEventListener("click", closePanel);
  elements.detail.addEventListener("click", (event) => {
    if (!activeEntry) return;
    if (event.target.closest("#edit-entry")) {
      renderDetail(activeEntry, true);
      elements.detail.querySelector('input[name="term"]').focus();
    } else if (event.target.closest("#cancel-edit")) {
      renderDetail(activeEntry);
    } else if (event.target.closest("#reset-edit")) {
      const index = entries.indexOf(activeEntry);
      delete overrides[entryKeys[index]];
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(overrides));
      } catch (_error) {
        // The in-memory reset still applies until the page is refreshed.
      }
      window.location.reload();
    }
  });
  elements.detail.addEventListener("submit", (event) => {
    if (event.target.id !== "entry-edit-form" || !activeEntry) return;
    event.preventDefault();
    const values = new FormData(event.target);
    activeEntry.term = String(values.get("term") || "").trim();
    activeEntry.pinyin = String(values.get("pinyin") || "").trim();
    activeEntry.type = String(values.get("type") || "").trim();
    activeEntry.difficulty = Number(values.get("difficulty")) || 3;
    activeEntry.definition = String(values.get("definition") || "").trim();
    activeEntry.example = String(values.get("example") || "").trim();
    activeEntry.source_details = String(values.get("source_details") || "").trim();
    const persisted = persistEntry(activeEntry);
    render();
    renderDetail(activeEntry);
    if (!persisted) {
      elements.detail.insertAdjacentHTML("afterbegin", '<p class="edit-warning">Saved for this session, but browser storage is unavailable.</p>');
    }
  });
  elements.scrim.addEventListener("click", closePanel);
  document.querySelector("#export-overrides").addEventListener("click", () => {
    const blob = new Blob([JSON.stringify({ version: 1, storage_key: STORAGE_KEY, exported_at: new Date().toISOString(), overrides }, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob), link = document.createElement("a");
    link.href = url; link.download = "reading_lexicon_local_edits.json"; link.click(); URL.revokeObjectURL(url);
  });
  document.querySelector("#import-overrides").addEventListener("change", async (event) => {
    const file = event.target.files[0]; if (!file) return;
    try {
      const data = JSON.parse(await file.text()), imported = data.overrides || data;
      if (!imported || typeof imported !== "object" || Array.isArray(imported)) throw new Error("Invalid dictionary edit file");
      overrides = { ...overrides, ...imported }; localStorage.setItem(STORAGE_KEY, JSON.stringify(overrides)); window.location.reload();
    } catch (error) { window.alert(`Could not import dictionary edits: ${error.message}`); }
    finally { event.target.value = ""; }
  });
  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLocaleLowerCase() === "k") {
      event.preventDefault();
      elements.search.focus();
    }
    if (event.key === "Escape" && elements.panel.classList.contains("open")) closePanel();
  });

  render();
})();
