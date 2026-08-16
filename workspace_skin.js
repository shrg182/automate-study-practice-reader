(function () {
  const workspaceRoot = document.currentScript?.src
    ? new URL(".", document.currentScript.src)
    : new URL("./", location.href);
  const key = "reading-workspace-skin";
  const requested = new URLSearchParams(location.search).get("skin");
  const saved = localStorage.getItem(key);
  const fallback = /目录/.test(document.title) ? "sheet" : "reading";
  const initial = requested === "reading" || requested === "sheet"
    ? requested
    : (saved === "reading" || saved === "sheet" ? saved : fallback);

  function applySkin(skin, persist) {
    document.documentElement.dataset.workspaceSkin = skin;
    const theme = document.querySelector('link[href$="workspace_theme.css"]');
    if (theme) theme.disabled = skin === "reading";
    document.querySelectorAll("[data-skin-choice]").forEach((button) => {
      const active = button.dataset.skinChoice === skin;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    if (persist) localStorage.setItem(key, skin);
  }

  applySkin(initial, false);

  function installPwaAssets() {
    if (!document.querySelector('meta[name="viewport"]')) {
      const viewport = document.createElement("meta");
      viewport.name = "viewport"; viewport.content = "width=device-width,initial-scale=1,viewport-fit=cover";
      document.head.appendChild(viewport);
    }
    if (!document.querySelector('link[rel="manifest"]')) {
      const manifest = document.createElement("link");
      manifest.rel = "manifest"; manifest.href = new URL("manifest.webmanifest", workspaceRoot).href;
      document.head.appendChild(manifest);
    }
    if (!document.querySelector('meta[name="theme-color"]')) {
      const theme = document.createElement("meta");
      theme.name = "theme-color"; theme.content = "#188038"; document.head.appendChild(theme);
    }
    if (!document.querySelector('link[rel="apple-touch-icon"]')) {
      const touchIcon = document.createElement("link");
      touchIcon.rel = "apple-touch-icon";
      touchIcon.href = new URL("icons/reading-room-192.png", workspaceRoot).href;
      document.head.appendChild(touchIcon);
    }
    if (!document.querySelector('script[src$="mobile_pwa.js"]')) {
      const script = document.createElement("script");
      script.src = new URL("mobile_pwa.js", workspaceRoot).href; script.defer = true;
      document.head.appendChild(script);
    }
  }

  installPwaAssets();

  function recordReading() {
    const match = decodeURIComponent(location.pathname).match(/\/practice\/(.+\/editor\.html)$/);
    if (!match) return;
    const editorPath = match[1];
    const historyKey = "reading-workspace-history-v1";
    const sessionKey = `reading-workspace-counted:${editorPath}`;
    let history = {};
    try { history = JSON.parse(localStorage.getItem(historyKey) || "{}"); } catch { history = {}; }
    const previous = history[editorPath] || {};
    history[editorPath] = {
      count: (Number(previous.count) || 0) + (sessionStorage.getItem(sessionKey) ? 0 : 1),
      firstRead: previous.firstRead || new Date().toISOString(),
      lastRead: new Date().toISOString()
    };
    localStorage.setItem(historyKey, JSON.stringify(history));
    sessionStorage.setItem(sessionKey, "1");
  }

  recordReading();

  function installEditingHistory() {
    const match = decodeURIComponent(location.pathname).match(/\/practice\/(.+\/editor\.html)$/);
    if (!match) return;
    const editorPath = match[1];
    const historyKey = "reading-workspace-editing-history-v1";
    const sessionKey = `reading-workspace-edited:${editorPath}`;
    let timer = 0;
    const classify = (target) => {
      if (target.closest(".rich-editor,#editor.editor,.editor[contenteditable]")) return "正文";
      if (target.closest(".footnote-item,.annotation-register,.marker-composer")) return "注释";
      if (target.closest("#user-notes,.notes-dock,.chapter-note-entry")) return "札记";
      if (target.closest(".global-edit-form,.dictionary-actions,.term-list")) return "词典";
      return "";
    };
    const save = (kind) => {
      let history = {};
      try { history = JSON.parse(localStorage.getItem(historyKey) || "{}"); } catch { history = {}; }
      const previous = history[editorPath] || {};
      const now = new Date().toISOString();
      const kinds = new Set(previous.kinds || []); kinds.add(kind);
      history[editorPath] = {
        sessions: (Number(previous.sessions) || 0) + (sessionStorage.getItem(sessionKey) ? 0 : 1),
        changes: (Number(previous.changes) || 0) + 1,
        firstEdited: previous.firstEdited || now,
        lastEdited: now,
        kinds: [...kinds]
      };
      localStorage.setItem(historyKey, JSON.stringify(history));
      sessionStorage.setItem(sessionKey, "1");
    };
    document.addEventListener("input", (event) => {
      const kind = classify(event.target);
      if (!kind) return;
      window.clearTimeout(timer);
      timer = window.setTimeout(() => save(kind), 700);
    }, true);
  }

  installEditingHistory();

  function installSwitch() {
    if (document.querySelector(".workspace-skin-switch")) return;
    const host = document.querySelector(".masthead-inner") || document.querySelector(".topbar");
    if (!host) return;
    const style = document.createElement("style");
    style.textContent = `.workspace-skin-switch{display:inline-flex;flex:0 0 auto;gap:2px;margin-left:auto;padding:3px;border:1px solid #c9c3b7;border-radius:18px;background:#fff;color:#3c4043;font:12px/1.2 Arial,"PingFang SC",sans-serif;box-shadow:0 1px 2px #00000010}.workspace-skin-switch button{min-height:28px;margin:0;padding:5px 10px;border:0;border-radius:14px;background:transparent;color:inherit;cursor:pointer;font:inherit;white-space:nowrap}.workspace-skin-switch button:hover{background:#f1f3f4}.workspace-skin-switch button.active{background:#e6f4ea;color:#137333;font-weight:700}html[data-workspace-skin=reading] .workspace-skin-switch button.active{background:#eee5d2;color:#71352e}@media(max-width:700px){.workspace-skin-switch{width:100%;margin-left:0;justify-content:center}}@media print{.workspace-skin-switch{display:none!important}}`;
    document.head.appendChild(style);
    const control = document.createElement("div");
    control.className = "workspace-skin-switch";
    control.setAttribute("role", "group");
    control.setAttribute("aria-label", "界面风格");
    control.innerHTML = '<button type="button" data-skin-choice="reading" title="适合长时间阅读的温暖书卷风格">阅读模式</button><button type="button" data-skin-choice="sheet" title="适合目录管理和密集编辑的表格风格">表格模式</button>';
    control.addEventListener("click", (event) => {
      const button = event.target.closest("[data-skin-choice]");
      if (button) applySkin(button.dataset.skinChoice, true);
    });
    host.appendChild(control);
    applySkin(document.documentElement.dataset.workspaceSkin || initial, false);

    document.addEventListener("click", (event) => {
      const link = event.target.closest("a[href]");
      if (!link || link.target === "_blank" || /^(https?:|mailto:|#)/i.test(link.getAttribute("href"))) return;
      const url = new URL(link.href, location.href);
      if (!/\.html$/i.test(url.pathname)) return;
      url.searchParams.set("skin", document.documentElement.dataset.workspaceSkin);
      link.href = url.href;
    });
  }

  function installContentFontControls() {
    if (document.querySelector(".content-font-controls")) return;
    const content = document.querySelector(".editor, .rich-editor");
    const host = document.querySelector(".toolbar") || document.querySelector("jianshang-editor-header .view-tools") || document.querySelector(".actions");
    if (!content || !host) return;
    const key = "reading-workspace-content-font-size";
    const defaultSize = Number.parseFloat(getComputedStyle(content).fontSize) || 18;
    let size = Number(localStorage.getItem(key)) || defaultSize;
    const minimum = 12, maximum = 34;
    const style = document.createElement("style");
    style.textContent = `.editor,.rich-editor{font-size:var(--reading-content-font-size)!important}.content-font-controls{display:inline-flex;align-items:center;gap:2px;padding:2px;border:1px solid #c9d2df;border-radius:6px;background:#fff;color:#3c4043;font:12px/1 Arial,"PingFang SC",sans-serif}.content-font-controls button{min-width:29px;min-height:27px!important;padding:3px 6px!important;border:0!important;border-radius:4px!important;background:transparent!important;color:inherit!important;font:inherit!important;cursor:pointer}.content-font-controls button:hover{background:#edf2fa!important}.content-font-size{min-width:34px;text-align:center;color:#5f6368;font-variant-numeric:tabular-nums}@media print{.content-font-controls{display:none!important}}`;
    style.textContent += ".workspace{width:100%!important;max-width:none!important}";
    document.head.appendChild(style);
    const controls = document.createElement("div");
    controls.className = "content-font-controls";
    controls.setAttribute("role", "group");
    controls.setAttribute("aria-label", "正文字号");
    controls.innerHTML = '<button type="button" data-font-change="-1" title="减小正文字号">A−</button><span class="content-font-size"></span><button type="button" data-font-change="1" title="增大正文字号">A+</button><button type="button" data-font-reset title="恢复默认正文字号">重置</button>';
    const apply = (next, persist = true) => {
      size = Math.max(minimum, Math.min(maximum, next));
      document.documentElement.style.setProperty("--reading-content-font-size", `${size}px`);
      controls.querySelector(".content-font-size").textContent = `${size}px`;
      if (persist) localStorage.setItem(key, String(size));
    };
    controls.addEventListener("click", (event) => {
      const change = event.target.closest("[data-font-change]");
      if (change) apply(size + Number(change.dataset.fontChange));
      if (event.target.closest("[data-font-reset]")) { localStorage.removeItem(key); apply(defaultSize, false); }
    });
    host.appendChild(controls);
    apply(size, false);
  }

  function installFileMenu() {
    if (document.querySelector(".workspace-file-menu")) return;
    const pdf = document.getElementById("printPdfBtn");
    if (!pdf) return;
    pdf.textContent = "PDF 草稿";
    const ids = ["saveBtn", "exportTxtBtn", "exportHtmlBtn", "exportJsonBtn", "exportLogBtn", "exportTermsBtn", "exportNotesBtn", "exportBtn", "downloadBtn", "backupBtn", "resetBtn"];
    const controls = ids.map((id) => document.getElementById(id)).filter(Boolean);
    const importInput = document.getElementById("importJson") || document.getElementById("importBackup");
    const importLabel = importInput ? document.querySelector(`label[for="${importInput.id}"]`) : null;
    if (!controls.length) return;
    const style = document.createElement("style");
    style.textContent = `.workspace-file-menu{position:relative;display:inline-flex;align-items:center}.workspace-file-trigger{min-height:30px!important;padding:4px 9px!important;border:1px solid #c9d2df!important;border-radius:5px!important;background:#fff!important;color:#202124!important;white-space:nowrap;cursor:pointer}.workspace-file-trigger::after{content:" ▾";font-size:10px}.workspace-file-popover{position:absolute;z-index:100;top:calc(100% + 5px);right:0;display:none;width:210px;padding:6px;border:1px solid #dadce0;border-radius:8px;background:#fff;box-shadow:0 8px 24px #3c404333}.workspace-file-menu.open .workspace-file-popover{display:grid;gap:2px}.workspace-file-popover button,.workspace-file-popover label{display:flex!important;width:100%;min-height:32px!important;padding:6px 9px!important;align-items:center;border:0!important;border-radius:4px!important;background:#fff!important;color:#202124!important;text-align:left;font:12px/1.3 Arial,"PingFang SC",sans-serif!important;cursor:pointer}.workspace-file-popover button:hover,.workspace-file-popover label:hover{background:#edf2fa!important}.workspace-file-popover .export-all-action{margin-bottom:5px;border-bottom:1px solid #e3e7ed!important;border-radius:4px 4px 0 0!important;background:#e8f0fe!important;color:#174ea6!important;font-weight:700!important}.workspace-file-popover .danger-action{margin-top:5px;border-top:1px solid #eee!important;border-radius:0 0 4px 4px!important;color:#b3261e!important}.workspace-file-popover input{display:none!important}@media print{.workspace-file-menu{display:none!important}}`;
    document.head.appendChild(style);
    const menu = document.createElement("div"), trigger = document.createElement("button"), popover = document.createElement("div");
    menu.className = "workspace-file-menu"; trigger.className = "workspace-file-trigger"; trigger.type = "button"; trigger.textContent = "文件与备份"; trigger.setAttribute("aria-expanded", "false");
    popover.className = "workspace-file-popover"; popover.setAttribute("role", "menu");
    const exportAll = document.createElement("button");
    exportAll.type = "button"; exportAll.className = "export-all-action"; exportAll.textContent = "一键导出全部";
    exportAll.addEventListener("click", () => {
      const downloadIds = ["exportTxtBtn", "exportHtmlBtn", "exportJsonBtn", "exportTermsBtn", "exportNotesBtn", "downloadBtn", "backupBtn", "downloadLogBtn"];
      const downloadLog = document.getElementById("downloadLogBtn");
      if (!downloadLog) downloadIds.push("exportLogBtn");
      downloadIds.map((id) => document.getElementById(id)).filter(Boolean).forEach((control) => control.click());
    });
    popover.appendChild(exportAll);
    controls.forEach((control) => { if (control.id === "resetBtn") control.classList.add("danger-action"); popover.appendChild(control); });
    if (importLabel) popover.insertBefore(importLabel, popover.querySelector(".danger-action"));
    if (importInput) popover.appendChild(importInput);
    menu.append(trigger, popover); pdf.insertAdjacentElement("afterend", menu);
    trigger.addEventListener("click", (event) => { event.stopPropagation(); const open = menu.classList.toggle("open"); trigger.setAttribute("aria-expanded", String(open)); });
    popover.addEventListener("click", (event) => { if (!event.target.closest("label")) { menu.classList.remove("open"); trigger.setAttribute("aria-expanded", "false"); } });
    importInput?.addEventListener("change", () => { menu.classList.remove("open"); trigger.setAttribute("aria-expanded", "false"); });
    document.addEventListener("click", (event) => { if (!menu.contains(event.target)) { menu.classList.remove("open"); trigger.setAttribute("aria-expanded", "false"); } });
    document.addEventListener("keydown", (event) => { if (event.key === "Escape") { menu.classList.remove("open"); trigger.setAttribute("aria-expanded", "false"); } });
  }

  function installInsertMenu() {
    if (document.querySelector(".workspace-insert-menu")) return;
    const ids = ["notationBtn", "interlinearBtn", "footnoteBtn", "commentBtn", "insertImageBtn", "doubtBtn"];
    const controls = ids.map((id) => document.getElementById(id)).filter(Boolean);
    if (controls.length < 2) return;
    const firstControl = controls[0];
    const host = firstControl.parentNode;
    const style = document.createElement("style");
    style.textContent = `.workspace-insert-menu{position:relative;display:inline-flex;align-items:center}.workspace-insert-trigger{min-height:30px!important;padding:4px 9px!important;border:1px solid #c9d2df!important;border-radius:5px!important;background:#fff!important;color:#202124!important;white-space:nowrap;cursor:pointer}.workspace-insert-trigger::after{content:" ▾";font-size:10px}.workspace-insert-popover{position:absolute;z-index:101;top:calc(100% + 5px);left:0;display:none;width:190px;padding:6px;border:1px solid #dadce0;border-radius:8px;background:#fff;box-shadow:0 8px 24px #3c404333}.workspace-insert-menu.open .workspace-insert-popover{display:grid;gap:2px}.workspace-insert-popover button{display:flex!important;width:100%;min-height:32px!important;padding:6px 9px!important;align-items:center;border:0!important;border-radius:4px!important;background:#fff!important;color:#202124!important;text-align:left;font:12px/1.3 Arial,"PingFang SC",sans-serif!important;cursor:pointer}.workspace-insert-popover button:hover,.workspace-insert-popover button:focus-visible{background:#edf2fa!important}@media print{.workspace-insert-menu{display:none!important}}`;
    document.head.appendChild(style);
    const menu = document.createElement("div"), trigger = document.createElement("button"), popover = document.createElement("div");
    menu.className = "workspace-insert-menu";
    trigger.className = "workspace-insert-trigger"; trigger.type = "button"; trigger.textContent = "插入与注释";
    trigger.setAttribute("aria-haspopup", "menu"); trigger.setAttribute("aria-expanded", "false");
    popover.className = "workspace-insert-popover"; popover.setAttribute("role", "menu");
    host.insertBefore(menu, firstControl);
    menu.append(trigger, popover);
    controls.forEach((control) => { control.setAttribute("role", "menuitem"); popover.appendChild(control); });
    const editor = document.querySelector("#editor, .rich-editor, .editor");
    let preservedRange = null;
    let preservedTextSelection = null;
    const preserveSelection = () => {
      preservedRange = null; preservedTextSelection = null;
      const active = document.activeElement;
      if (active?.matches(".footnote-item textarea") && active.selectionStart !== active.selectionEnd) {
        preservedTextSelection = {
          input: active,
          start: active.selectionStart,
          end: active.selectionEnd,
          text: active.value.slice(active.selectionStart, active.selectionEnd)
        };
        return;
      }
      const selection = getSelection();
      if (selection?.rangeCount && editor?.contains(selection.getRangeAt(0).commonAncestorContainer)) {
        preservedRange = selection.getRangeAt(0).cloneRange();
      }
    };
    const restoreSelection = () => {
      if (!preservedRange) return;
      const selection = getSelection();
      selection.removeAllRanges(); selection.addRange(preservedRange.cloneRange());
    };
    const close = () => { menu.classList.remove("open"); trigger.setAttribute("aria-expanded", "false"); };
    const addFootnoteNotation = () => {
      const selected = preservedTextSelection;
      if (!selected?.input.isConnected || !selected.text.trim()) return false;
      const term = selected.text;
      const pronunciation = prompt(`“${term}”的拼音或读音（可留空）：`, "");
      if (pronunciation === null) return true;
      const pinyin = pronunciation.trim();
      const note = prompt("简注（可留空；保存在本篇词典）：", "");
      if (note === null) return true;
      const replacement = pinyin ? `${term}（${pinyin}）` : term;
      selected.input.setRangeText(replacement, selected.start, selected.end, "select");
      selected.input.dispatchEvent(new Event("input", { bubbles: true }));
      selected.input.focus({ preventScroll: true });
      if (typeof window.upsertRuntimeTerm === "function") window.upsertRuntimeTerm(term, pinyin, note);
      if (typeof window.addLog === "function") window.addLog("添加脚注注音/简注", term);
      preservedTextSelection = null;
      return true;
    };
    menu.addEventListener("mousedown", (event) => {
      if (!event.target.closest("button")) return;
      if (event.target === trigger) preserveSelection();
      event.preventDefault();
    });
    popover.addEventListener("click", (event) => {
      if (event.target.closest("#notationBtn") && addFootnoteNotation()) {
        event.preventDefault(); event.stopPropagation(); close(); return;
      }
      restoreSelection();
    }, true);
    trigger.addEventListener("click", (event) => {
      event.stopPropagation();
      const open = menu.classList.toggle("open");
      trigger.setAttribute("aria-expanded", String(open));
    });
    popover.addEventListener("click", close);
    document.addEventListener("click", (event) => { if (!menu.contains(event.target)) close(); });
    document.addEventListener("keydown", (event) => { if (event.key === "Escape") { close(); trigger.focus(); } });
  }

  function installUserNotesAccess() {
    const input = document.getElementById("userNoteInput");
    const list = document.getElementById("userNoteList");
    const addButton = document.getElementById("addUserNoteBtn");
    const host = document.querySelector(".toolbar") || document.querySelector(".actions");
    if (!input || !list || !addButton || !host || document.querySelector(".user-notes-shortcut")) return;
    const section = list.closest("section") || list;
    section.id ||= "user-notes";
    const style = document.createElement("style");
    style.textContent = `.user-notes-shortcut{min-height:30px!important;padding:4px 9px!important;border:1px solid #c9d2df!important;border-radius:5px!important;background:#fff!important;color:#174ea6!important;font-weight:700!important;white-space:nowrap;cursor:pointer}.note-item.duplicate-note-highlight{outline:3px solid #f9ab00;outline-offset:2px;background:#fef7e0!important;animation:noteDuplicatePulse .8s ease-in-out 2}@keyframes noteDuplicatePulse{50%{outline-color:#fdd663;background:#fff8d8!important}}@media print{.user-notes-shortcut{display:none!important}}`;
    document.head.appendChild(style);
    const shortcut = document.createElement("button");
    shortcut.type = "button"; shortcut.className = "user-notes-shortcut"; shortcut.textContent = "札记（0）";
    shortcut.title = "查看本篇用户札记";
    const rows = () => [...list.querySelectorAll(".note-item")];
    const updateCount = () => { shortcut.textContent = `札记（${rows().length}）`; };
    shortcut.addEventListener("click", () => section.scrollIntoView({ behavior: "smooth", block: "start" }));
    host.appendChild(shortcut);
    new MutationObserver(updateCount).observe(list, { childList: true, subtree: true });
    updateCount();
    const normalize = (value) => value.replace(/\s+/g, " ").trim();
    addButton.addEventListener("click", (event) => {
      const draft = normalize(input.value);
      const hasDraftMedia = Boolean(document.querySelector("#userNoteMedia > *"));
      if (!draft || hasDraftMedia) return;
      const duplicate = rows().find((row) => normalize(row.firstElementChild?.textContent || "") === draft);
      if (!duplicate) return;
      event.preventDefault(); event.stopImmediatePropagation();
      rows().forEach((row) => row.classList.remove("duplicate-note-highlight"));
      duplicate.classList.add("duplicate-note-highlight");
      duplicate.scrollIntoView({ behavior: "smooth", block: "center" });
      window.setTimeout(() => duplicate.classList.remove("duplicate-note-highlight"), 3500);
      window.alert("此札记已经保存，现已为您定位到原札记。");
    }, true);
  }

  function installWorkspaceControls() { installSwitch(); installContentFontControls(); installFileMenu(); installInsertMenu(); installUserNotesAccess(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", installWorkspaceControls);
  else installWorkspaceControls();
})();
