(() => {
  "use strict";

  const BASE = Array.isArray(window.SHIJI_REFERENCES) ? window.SHIJI_REFERENCES.map(item => ({...item})) : [];
  const STORAGE_KEY = "shiji-reference-library-overrides-v1";
  const fields = ["id", "title", "url", "description", "tags", "citation", "added_from"];
  const baseById = new Map(BASE.map(item => [item.id, item]));
  const state = {query: "", tag: "all", sort: "title"};
  let local = loadLocal();
  let activeId = null;

  const elements = {
    grid: document.querySelector("#referenceGrid"), search: document.querySelector("#search"),
    tags: document.querySelector("#tagFilters"), summary: document.querySelector("#summary"),
    empty: document.querySelector("#empty"), count: document.querySelector("#entryCount"),
    dialog: document.querySelector("#editorDialog"), form: document.querySelector("#referenceForm"),
    reset: document.querySelector("#resetReference"), toast: document.querySelector("#toast")
  };

  function loadLocal() {
    try {
      const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{"overrides":{},"added":[]}');
      return {overrides: value.overrides || {}, added: Array.isArray(value.added) ? value.added : []};
    } catch { return {overrides: {}, added: []}; }
  }
  function persist() { localStorage.setItem(STORAGE_KEY, JSON.stringify(local)); }
  function entries() { return [...BASE.map(item => ({...item, ...(local.overrides[item.id] || {})})), ...local.added]; }
  function escapeHtml(value) { return String(value || "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"})[c]); }
  function safeUrl(value) { try { const url = new URL(value); return ["http:", "https:"].includes(url.protocol) ? url.href : "#"; } catch { return "#"; } }
  function tagList(entry) { return String(entry.tags || "").split(/[;；,，]/).map(tag => tag.trim()).filter(Boolean); }
  function citation(entry) { return entry.citation || `${entry.title || ""} ${entry.url || ""}`.trim(); }
  function filtered() {
    const query = state.query.trim().toLowerCase();
    return entries().filter(entry =>
      (state.tag === "all" || tagList(entry).includes(state.tag)) &&
      (!query || fields.map(field => entry[field] || "").join(" ").toLowerCase().includes(query))
    ).sort((a, b) => state.sort === "added"
      ? String(a.added_from || "").localeCompare(String(b.added_from || ""), "zh-CN")
      : String(a.title || "").localeCompare(String(b.title || ""), "zh-CN"));
  }
  function renderTags() {
    const tags = [...new Set(entries().flatMap(tagList))].sort((a, b) => a.localeCompare(b, "zh-CN"));
    elements.tags.innerHTML = ["all", ...tags].map(tag => `<button type="button" data-tag="${escapeHtml(tag)}" class="${state.tag === tag ? "active" : ""}">${tag === "all" ? "全部" : escapeHtml(tag)}</button>`).join("");
  }
  function render() {
    const all = entries(), shown = filtered();
    elements.count.textContent = all.length;
    elements.summary.textContent = `显示 ${shown.length} / ${all.length} 条资料`;
    elements.grid.innerHTML = shown.map(entry => `<article class="reference" data-id="${escapeHtml(entry.id)}">
      <div class="tags">${tagList(entry).map(tag => `<span>${escapeHtml(tag)}</span>`).join("")}</div>
      <h2>${escapeHtml(entry.title)}</h2><p>${escapeHtml(entry.description)}</p>
      <a class="url" href="${escapeHtml(safeUrl(entry.url))}" target="_blank" rel="noreferrer">${escapeHtml(entry.url)}</a>
      <div class="meta">${escapeHtml(entry.added_from || "共享资料")}</div>
      <div class="card-actions"><button type="button" data-action="open">打开来源</button><button type="button" data-action="copy">复制引用</button><button type="button" data-action="edit">编辑</button></div>
    </article>`).join("");
    elements.empty.hidden = shown.length !== 0;
    renderTags();
  }
  function notify(message) { elements.toast.textContent = message; elements.toast.classList.add("show"); setTimeout(() => elements.toast.classList.remove("show"), 1800); }
  async function copyText(text) {
    try { await navigator.clipboard.writeText(text); }
    catch { const area = document.createElement("textarea"); area.value = text; document.body.append(area); area.select(); document.execCommand("copy"); area.remove(); }
    notify("引用已复制");
  }
  function openForm(entry = null) {
    activeId = entry?.id || null;
    elements.form.reset();
    fields.forEach(field => { const control = elements.form.elements.namedItem(field); if (control) control.value = entry?.[field] || ""; });
    document.querySelector("#formMode").textContent = entry ? "编辑浏览器副本" : "添加浏览器资料";
    document.querySelector("#dialogTitle").textContent = entry?.title || "新参考资料";
    elements.reset.hidden = !entry || !baseById.has(entry.id);
    elements.dialog.showModal();
  }
  function closeForm() { elements.dialog.close(); activeId = null; }
  function csvCell(value) { const text = String(value || ""); return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text; }
  function exportCsv() {
    const content = "\ufeff" + [fields, ...entries().map(entry => fields.map(field => entry[field] || ""))].map(row => row.map(csvCell).join(",")).join("\n") + "\n";
    const link = document.createElement("a"); link.href = URL.createObjectURL(new Blob([content], {type:"text/csv;charset=utf-8"})); link.download = "shared_references_edited.csv"; link.click(); setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  }

  elements.search.addEventListener("input", event => { state.query = event.target.value; render(); });
  document.querySelector("#sort").addEventListener("change", event => { state.sort = event.target.value; render(); });
  elements.tags.addEventListener("click", event => { const button = event.target.closest("[data-tag]"); if (!button) return; state.tag = button.dataset.tag; render(); });
  elements.grid.addEventListener("click", event => {
    const card = event.target.closest(".reference"), action = event.target.closest("[data-action]"); if (!card || !action) return;
    const entry = entries().find(item => item.id === card.dataset.id); if (!entry) return;
    if (action.dataset.action === "open") window.open(safeUrl(entry.url), "_blank", "noopener");
    else if (action.dataset.action === "copy") copyText(citation(entry));
    else openForm(entry);
  });
  document.querySelector("#addReference").addEventListener("click", () => openForm());
  document.querySelector("#exportCsv").addEventListener("click", exportCsv);
  document.querySelector("#closeDialog").addEventListener("click", closeForm);
  document.querySelector("#cancelDialog").addEventListener("click", closeForm);
  elements.reset.addEventListener("click", () => {
    if (!activeId || !confirm("恢复此资料的项目原值？")) return;
    delete local.overrides[activeId]; persist(); closeForm(); render(); notify("已恢复项目原值");
  });
  elements.form.addEventListener("submit", event => {
    event.preventDefault();
    const values = Object.fromEntries(fields.map(field => [field, String(new FormData(elements.form).get(field) || "").trim()]));
    if (!values.title || safeUrl(values.url) === "#") { alert("请填写标题和有效的 http/https 网址。"); return; }
    if (activeId && baseById.has(activeId)) { values.id = activeId; local.overrides[activeId] = values; }
    else if (activeId) { const index = local.added.findIndex(item => item.id === activeId); values.id = activeId; local.added[index] = values; }
    else { values.id = `local-${Date.now()}`; local.added.push(values); }
    persist(); closeForm(); render(); notify("资料已保存到浏览器");
  });
  document.addEventListener("keydown", event => { if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") { event.preventDefault(); elements.search.focus(); } });
  render();
})();
