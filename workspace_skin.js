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
    style.textContent += `html[data-workspace-skin="sheet"] body.reading-immersive .paper,html[data-workspace-skin="sheet"] body.reading-immersive .editor-panel{width:100%!important;max-width:none!important;padding:clamp(18px,2vw,32px)!important}html[data-workspace-skin="sheet"] body.reading-immersive .civil-war-table-wrap,html[data-workspace-skin="sheet"] body.reading-immersive .chinese-war-table-wrap{max-width:100%;overflow-x:auto;scrollbar-gutter:stable}`;
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

  function installReadingEnvironment() {
    if (document.querySelector(".reading-environment")) return;
    const content = document.querySelector(".editor, .rich-editor");
    const host = document.querySelector(".toolbar") || document.querySelector("jianshang-editor-header .view-tools") || document.querySelector(".actions");
    if (!content || !host) return;
    const key = "reading-workspace-environment-v1";
    const defaults = { fontSize: Number.parseFloat(getComputedStyle(content).fontSize) || 18, lineHeight: 1.85, background: "#fffdfa" };
    let settings = defaults;
    try { settings = { ...defaults, ...JSON.parse(localStorage.getItem(key) || "{}") }; } catch {}
    const style = document.createElement("style");
    style.textContent = `.editor,.rich-editor{font-size:var(--reading-content-font-size)!important;line-height:var(--reading-content-line-height)!important;background:var(--reading-content-background)!important}.paper,.editor-panel,.page-card{background:var(--reading-content-background,#fffdfa)!important}.reading-environment{position:relative;display:inline-flex}.reading-environment-trigger{min-height:30px!important;padding:4px 9px!important;border:1px solid #c9d2df!important;border-radius:5px!important;background:#fff!important;color:#202124!important;cursor:pointer}.reading-environment-panel{position:absolute;z-index:340;top:calc(100% + 6px);left:0;right:auto;display:none;width:min(260px,calc(100vw - 24px));padding:14px;border:1px solid #dadce0;border-radius:10px;background:#fff;color:#202124;box-shadow:0 10px 30px #0003;font:12px/1.4 Arial,"PingFang SC",sans-serif}.reading-environment.open .reading-environment-panel{display:grid;gap:12px}.reading-setting{display:grid;grid-template-columns:70px 1fr 42px;gap:8px;align-items:center}.reading-setting input{min-width:0;width:100%}.reading-colors{display:flex;gap:8px}.reading-color{width:30px;height:30px!important;min-height:30px!important;padding:0!important;border:2px solid #dadce0!important;border-radius:50%!important}.reading-color.active{border-color:#1a73e8!important;box-shadow:0 0 0 2px #d2e3fc}.reading-reset{justify-self:start}@media print{.reading-environment{display:none!important}}`;
    document.head.appendChild(style);
    const controls = document.createElement("div");
    controls.className = "reading-environment";
    controls.innerHTML = `<button type="button" class="reading-environment-trigger" aria-expanded="false">阅读设置</button><div class="reading-environment-panel"><label class="reading-setting"><span>字号</span><input data-reading-setting="fontSize" type="range" min="12" max="34" step="1"><output data-reading-output="fontSize"></output></label><label class="reading-setting"><span>行距</span><input data-reading-setting="lineHeight" type="range" min="1.3" max="2.6" step="0.05"><output data-reading-output="lineHeight"></output></label><div><div style="margin-bottom:7px">背景颜色</div><div class="reading-colors"><button class="reading-color" data-reading-color="#ffffff" style="background:#fff" title="白色"></button><button class="reading-color" data-reading-color="#fffdfa" style="background:#fffdfa" title="米白"></button><button class="reading-color" data-reading-color="#f3eedf" style="background:#f3eedf" title="羊皮纸"></button><button class="reading-color" data-reading-color="#eaf2e7" style="background:#eaf2e7" title="护眼绿"></button><button class="reading-color" data-reading-color="#e9f0f5" style="background:#e9f0f5" title="浅蓝"></button></div></div><button type="button" class="reading-reset">恢复默认</button></div>`;
    const trigger = controls.querySelector(".reading-environment-trigger");
    const panel = controls.querySelector(".reading-environment-panel");
    const positionPanel = () => {
      panel.style.left = "0px";
      const rect = panel.getBoundingClientRect();
      const left = Math.max(12 - rect.left, Math.min(0, innerWidth - 12 - rect.right));
      panel.style.left = `${left}px`;
    };
    const apply = (persist = true) => {
      settings.fontSize = Math.max(12, Math.min(34, Number(settings.fontSize) || defaults.fontSize));
      settings.lineHeight = Math.max(1.3, Math.min(2.6, Number(settings.lineHeight) || defaults.lineHeight));
      document.documentElement.style.setProperty("--reading-content-font-size", `${settings.fontSize}px`);
      document.documentElement.style.setProperty("--reading-content-line-height", String(settings.lineHeight));
      document.documentElement.style.setProperty("--reading-content-background", settings.background);
      controls.querySelector('[data-reading-setting="fontSize"]').value = settings.fontSize;
      controls.querySelector('[data-reading-setting="lineHeight"]').value = settings.lineHeight;
      controls.querySelector('[data-reading-output="fontSize"]').textContent = `${settings.fontSize}px`;
      controls.querySelector('[data-reading-output="lineHeight"]').textContent = settings.lineHeight.toFixed(2);
      controls.querySelectorAll("[data-reading-color]").forEach(button => button.classList.toggle("active", button.dataset.readingColor === settings.background));
      if (persist) localStorage.setItem(key, JSON.stringify(settings));
    };
    controls.addEventListener("input", event => { const name = event.target.dataset.readingSetting; if (name) { settings[name] = Number(event.target.value); apply(); } });
    controls.addEventListener("click", event => {
      const triggerButton = event.target.closest(".reading-environment-trigger");
      if (triggerButton) { const open = controls.classList.toggle("open"); triggerButton.setAttribute("aria-expanded", String(open)); if (open) requestAnimationFrame(positionPanel); }
      const color = event.target.closest("[data-reading-color]"); if (color) { settings.background = color.dataset.readingColor; apply(); }
      if (event.target.closest(".reading-reset")) { settings = { ...defaults }; apply(); }
    });
    document.addEventListener("click", event => { if (!controls.contains(event.target)) { controls.classList.remove("open"); trigger.setAttribute("aria-expanded", "false"); } });
    window.addEventListener("resize", () => { if (controls.classList.contains("open")) positionPanel(); });
    host.appendChild(controls); apply(false);
    window.ReadingWorkspace ||= {}; window.ReadingWorkspace.openSettings = () => controls.querySelector(".reading-environment-trigger").click();
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
    style.textContent = `.workspace-file-menu{position:relative;display:inline-flex;align-items:center}.workspace-file-trigger{min-height:30px!important;padding:4px 9px!important;border:1px solid #c9d2df!important;border-radius:5px!important;background:#fff!important;color:#202124!important;white-space:nowrap;cursor:pointer}.workspace-file-trigger::after{content:" ▾";font-size:10px}.workspace-file-popover{position:absolute;z-index:100;top:calc(100% + 5px);left:0;right:auto;display:none;width:min(210px,calc(100vw - 24px));padding:6px;border:1px solid #dadce0;border-radius:8px;background:#fff;box-shadow:0 8px 24px #3c404333}.workspace-file-menu.open .workspace-file-popover{display:grid;gap:2px}.workspace-file-popover button,.workspace-file-popover label{display:flex!important;width:100%;min-height:32px!important;padding:6px 9px!important;align-items:center;border:0!important;border-radius:4px!important;background:#fff!important;color:#202124!important;text-align:left;font:12px/1.3 Arial,"PingFang SC",sans-serif!important;cursor:pointer}.workspace-file-popover button:hover,.workspace-file-popover label:hover{background:#edf2fa!important}.workspace-file-popover .export-all-action{margin-bottom:5px;border-bottom:1px solid #e3e7ed!important;border-radius:4px 4px 0 0!important;background:#e8f0fe!important;color:#174ea6!important;font-weight:700!important}.workspace-file-popover .danger-action{margin-top:5px;border-top:1px solid #eee!important;border-radius:0 0 4px 4px!important;color:#b3261e!important}.workspace-file-popover input{display:none!important}@media print{.workspace-file-menu{display:none!important}}`;
    document.head.appendChild(style);
    const menu = document.createElement("div"), trigger = document.createElement("button"), popover = document.createElement("div");
    menu.className = "workspace-file-menu"; trigger.className = "workspace-file-trigger"; trigger.type = "button"; trigger.textContent = "文件与备份"; trigger.setAttribute("aria-haspopup", "menu"); trigger.setAttribute("aria-expanded", "false");
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
    const positionPopover = () => {
      popover.style.left = "0px";
      const rect = popover.getBoundingClientRect();
      const offset = Math.max(12 - rect.left, Math.min(0, innerWidth - 12 - rect.right));
      popover.style.left = `${offset}px`;
    };
    trigger.addEventListener("click", (event) => {
      event.stopPropagation();
      const open = menu.classList.toggle("open");
      trigger.setAttribute("aria-expanded", String(open));
      if (open) requestAnimationFrame(positionPopover);
    });
    popover.addEventListener("click", (event) => { if (!event.target.closest("label")) { menu.classList.remove("open"); trigger.setAttribute("aria-expanded", "false"); } });
    importInput?.addEventListener("change", () => { menu.classList.remove("open"); trigger.setAttribute("aria-expanded", "false"); });
    document.addEventListener("click", (event) => { if (!menu.contains(event.target)) { menu.classList.remove("open"); trigger.setAttribute("aria-expanded", "false"); } });
    document.addEventListener("keydown", (event) => { if (event.key === "Escape") { menu.classList.remove("open"); trigger.setAttribute("aria-expanded", "false"); } });
    window.addEventListener("resize", () => { if (menu.classList.contains("open")) positionPopover(); });
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
    shortcut.addEventListener("click", () => {
      window.BilingualStudyPane?.activateTab?.("notes");
      section.scrollIntoView({ behavior: "smooth", block: "start" });
    });
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

  function installImmersiveMode() {
    if (!document.querySelector(".editor, .rich-editor")) return;
    const style = document.createElement("style");
    style.textContent = `body.reading-immersive{background:var(--reading-content-background,#fffdfa)!important}body.reading-immersive .toolbar,body.reading-immersive .topbar,body.reading-immersive .masthead,body.reading-immersive jianshang-editor-header,body.reading-immersive .sidebar,body.reading-immersive .notes-dock,body.reading-immersive .export-dock{display:none!important}body.reading-immersive .workspace,body.reading-immersive .main-content,body.reading-immersive .editor-shell,body.reading-immersive .content-grid{display:block!important;width:100%!important;max-width:none!important;margin:0!important;padding:0!important}body.reading-immersive .paper,body.reading-immersive .editor-panel{width:min(900px,100%)!important;max-width:900px!important;min-height:100vh!important;margin:0 auto!important;padding:clamp(24px,5vw,64px)!important;border:0!important;box-shadow:none!important}body.reading-immersive .editor,body.reading-immersive .rich-editor{min-height:100vh!important;border:0!important;box-shadow:none!important}`;
    document.head.appendChild(style);
    const contextualHome = [...document.querySelectorAll("a[href]")].find(link => /返回首页|返回目录|书目|篇目/.test(link.textContent || ""));
    const directoryHref = window.ReadingWorkspace?.directoryHref || contextualHome?.href || new URL("index.html", workspaceRoot).href;
    const setImmersive = async enabled => {
      document.body.classList.toggle("reading-immersive", enabled);
      const button = document.querySelector('[data-mobile-action="immersive"]');
      if (button) { button.classList.toggle("active", enabled); button.setAttribute("aria-pressed", String(enabled)); button.textContent = enabled ? "退出沉浸" : "沉浸"; }
      if (enabled && document.documentElement.requestFullscreen && !document.fullscreenElement) await document.documentElement.requestFullscreen().catch(() => {});
      if (!enabled && document.fullscreenElement) await document.exitFullscreen().catch(() => {});
    };
    document.addEventListener("fullscreenchange", () => { if (!document.fullscreenElement && document.body.classList.contains("reading-immersive")) setImmersive(false); });
    document.addEventListener("keydown", event => { if (event.key === "Escape" && document.body.classList.contains("reading-immersive")) setImmersive(false); });
    window.ReadingWorkspace ||= {};
    window.ReadingWorkspace.directoryHref = directoryHref;
    window.ReadingWorkspace.toggleImmersive = () => setImmersive(!document.body.classList.contains("reading-immersive"));
  }

  function installAnnotationSync() {
    if (!document.querySelector(".editor, .rich-editor") || document.querySelector(".reading-sync-dialog")) return;
    const configKey = "reading-workspace-sync-config-v1";
    const syncable = key => /(notes?|annotation|highlight|marker|editor-v\d|reading-lexicon-entry-overrides)/i.test(key) && !/(log|history|difficulty|environment|sync-config)/i.test(key);
    const snapshot = () => { const data = {}; for (let i = 0; i < localStorage.length; i++) { const key = localStorage.key(i); if (key && syncable(key)) data[key] = localStorage.getItem(key); } return data; };
    const style = document.createElement("style"); style.textContent = `.reading-sync-dialog{width:min(520px,calc(100% - 28px));padding:0;border:0;border-radius:12px;box-shadow:0 18px 60px #0005;color:#202124}.reading-sync-dialog::backdrop{background:#0006}.reading-sync-form{display:grid;gap:12px;padding:20px;font:13px/1.45 Arial,"PingFang SC",sans-serif}.reading-sync-form h2{margin:0;font-size:18px}.reading-sync-form p{margin:0;color:#5f6368}.reading-sync-form label{display:grid;gap:5px}.reading-sync-form input{width:100%;min-width:0;padding:9px;border:1px solid #bdc1c6;border-radius:6px;font:inherit}.reading-sync-actions{display:flex;flex-wrap:wrap;gap:8px}.reading-sync-actions button{min-height:34px;padding:7px 11px;border:1px solid #c7d3e3;border-radius:6px;background:#fff;color:#174ea6;cursor:pointer}.reading-sync-actions .primary{background:#1a73e8;color:#fff}.reading-sync-status{min-height:20px;color:#137333!important}@media print{.reading-sync-dialog{display:none!important}}`; document.head.appendChild(style);
    const dialog = document.createElement("dialog"); dialog.className = "reading-sync-dialog";
    dialog.innerHTML = `<form class="reading-sync-form" method="dialog"><h2>跨设备批注同步</h2><p>填写支持 GET 和 PUT 的 WebDAV 或 JSON 文件地址。数据仅在此地址与您的设备之间传输。</p><label>同步文件地址<input name="url" type="url" placeholder="https://cloud.example.com/reader-notes.json"></label><label>Bearer 令牌（可选）<input name="token" type="password" autocomplete="off"></label><label><span><input name="automatic" type="checkbox" style="width:auto"> 打开阅读器时自动下载，编辑后定期上传</span></label><p class="reading-sync-status" role="status"></p><div class="reading-sync-actions"><button type="button" data-sync="pull">从云端下载</button><button type="button" data-sync="push" class="primary">上传到云端</button><button type="button" data-sync="save">保存设置</button><button value="close">关闭</button></div></form>`;
    document.body.appendChild(dialog); const form = dialog.querySelector("form"), status = dialog.querySelector(".reading-sync-status");
    const getConfig = () => { try { return JSON.parse(localStorage.getItem(configKey) || "{}"); } catch { return {}; } };
    const readForm = () => ({ url: form.elements.url.value.trim(), token: form.elements.token.value.trim(), automatic: form.elements.automatic.checked });
    const headers = config => ({ "Content-Type": "application/json", ...(config.token ? { Authorization: `Bearer ${config.token}` } : {}) });
    const pull = async (quiet = false) => { const config = readForm(); if (!config.url) throw new Error("请先填写同步文件地址"); status.textContent = "正在下载…"; const response = await fetch(config.url, { headers: headers(config), cache: "no-store" }); if (!response.ok) throw new Error(`下载失败（HTTP ${response.status}）`); const payload = await response.json(); Object.entries(payload.data || {}).forEach(([key, value]) => { if (syncable(key) && typeof value === "string") localStorage.setItem(key, value); }); localStorage.setItem("reading-workspace-last-sync", new Date().toISOString()); status.textContent = "下载完成；刷新页面后显示云端批注。"; if (!quiet) setTimeout(() => location.reload(), 700); };
    const push = async () => { const config = readForm(); if (!config.url) throw new Error("请先填写同步文件地址"); status.textContent = "正在上传…"; const response = await fetch(config.url, { method: "PUT", headers: headers(config), body: JSON.stringify({ version: 1, updatedAt: new Date().toISOString(), data: snapshot() }) }); if (!response.ok) throw new Error(`上传失败（HTTP ${response.status}）`); localStorage.setItem("reading-workspace-last-sync", new Date().toISOString()); status.textContent = "批注与高亮已上传。"; };
    dialog.addEventListener("click", async event => { const action = event.target.closest("[data-sync]")?.dataset.sync; if (!action) return; try { if (action === "save") { localStorage.setItem(configKey, JSON.stringify(readForm())); status.textContent = "同步设置已保存。"; } if (action === "pull") await pull(); if (action === "push") await push(); } catch (error) { status.textContent = error.message; } });
    const open = () => { const config = getConfig(); form.elements.url.value = config.url || ""; form.elements.token.value = config.token || ""; form.elements.automatic.checked = Boolean(config.automatic); status.textContent = ""; dialog.showModal(); };
    window.ReadingWorkspace ||= {}; window.ReadingWorkspace.openSync = open;
    const config = getConfig(); if (config.automatic && config.url) { form.elements.url.value = config.url; form.elements.token.value = config.token || ""; form.elements.automatic.checked = true; pull(true).catch(error => console.warn("Reader sync pull failed", error)); window.setInterval(() => push().catch(error => console.warn("Reader sync push failed", error)), 60000); }
  }

  function installContextNavigation() {
    const editor = document.querySelector(".editor, .rich-editor");
    if (!editor) return;
    const relativePath = decodeURIComponent(location.pathname).replace(decodeURIComponent(workspaceRoot.pathname), "").replace(/^\/+/, "");
    const collection = relativePath.split("/")[0];
    const menuHref = collection && !collection.endsWith(".html")
      ? new URL(`index.html#${encodeURIComponent(collection)}`, workspaceRoot).href
      : new URL("index.html", workspaceRoot).href;
    window.ReadingWorkspace ||= {};
    window.ReadingWorkspace.directoryHref = menuHref;
    const homeLink = [...document.querySelectorAll("a[href]")].find(link => /返回首页|返回目录|书目|篇目/.test(link.textContent || ""));
    if (!homeLink) return;
    const toolbar = homeLink.closest(".toolbar") || document.querySelector(".toolbar");
    const bookContentsLink = [...(toolbar?.querySelectorAll("a[href]") || [])].find(link =>
      link !== homeLink && /Reading Plan|Course|本书目录|阅读计划|完整目录/i.test(link.textContent || "")
    );
    window.ReadingWorkspace.bookDirectoryHref = bookContentsLink?.href || homeLink.href;
    homeLink.remove();
  }

  function installExpandingReviewFields() {
    const selector = ".annotation-register .register-row textarea";
    const style = document.createElement("style");
    style.textContent = `${selector}{min-height:96px!important;overflow-y:hidden;resize:vertical}`;
    document.head.appendChild(style);
    const resize = (area) => {
      area.style.height = "auto";
      area.style.height = `${Math.max(area.scrollHeight + 2, 96)}px`;
    };
    const resizeWithin = (root) => {
      if (root.matches?.(selector)) resize(root);
      root.querySelectorAll?.(selector).forEach(resize);
    };
    document.addEventListener("input", (event) => {
      if (event.target.matches?.(selector)) resize(event.target);
    });
    new MutationObserver((changes) => {
      changes.forEach((change) => change.addedNodes.forEach((node) => {
        if (node.nodeType === Node.ELEMENT_NODE) resizeWithin(node);
      }));
    }).observe(document.body, { childList: true, subtree: true });
    resizeWithin(document);
  }

  function installAllNotesView() {
    const footnotes = document.getElementById("footnotes");
    const registers = [
      ["行间注", document.getElementById("interlinearList")],
      ["按语", document.getElementById("commentList")],
      ["待核", document.getElementById("doubtList")],
    ];
    if (!footnotes && !registers.some(([, list]) => list)) return;
    if (!document.getElementById("allNotesStyle")) {
      const style = document.createElement("style");
      style.id = "allNotesStyle";
      style.textContent = `.all-notes-card h2{display:flex;gap:7px;align-items:center}.all-notes-card h2 small{color:var(--muted);font-size:11px}.all-notes-total,.all-notes-group h3 b{display:inline-grid;min-width:22px;height:22px;padding:0 5px;place-items:center;border-radius:12px;background:#e8f0fe;color:#174ea6;font:700 11px system-ui,sans-serif}.all-notes-return{margin:0 0 9px}.all-notes-groups{display:grid;gap:10px}.all-notes-group{padding-top:9px;border-top:1px solid var(--line)}.all-notes-group h3{display:flex;gap:6px;align-items:center;margin:0 0 7px;font:700 13px/1.4 system-ui,sans-serif}.all-notes-row{display:grid;grid-template-columns:minmax(60px,.5fr) minmax(120px,1fr);gap:6px;margin:6px 0;padding:7px;border:1px solid #d8e0e5;border-radius:6px;background:#fff}.all-notes-register-row{grid-template-columns:minmax(90px,.65fr) minmax(120px,1fr) auto}.all-notes-row textarea{width:100%;min-height:64px;padding:6px;border:1px solid var(--line);resize:vertical;font:12px/1.5 system-ui,sans-serif}.all-notes-source{min-width:0;padding:5px 7px;overflow-wrap:anywhere;text-align:left;font:12px/1.45 system-ui,sans-serif}.all-notes-actions{display:flex;flex-direction:column;gap:5px}.all-notes-empty{margin:0!important;padding:7px;color:var(--muted);background:var(--panel);font:12px system-ui,sans-serif}.study-panel #allNotesMount .all-notes-card{margin:0;box-shadow:none}@media(max-width:620px){.all-notes-row,.all-notes-register-row{grid-template-columns:1fr}.all-notes-actions{flex-direction:row}}`;
      document.head.append(style);
    }

    document.querySelectorAll(".study-panel .chinese-support-card details").forEach(details => details.open = true);
    let mount = document.getElementById("allNotesMount");
    if (!mount) {
      const sidebar = document.querySelector(".sidebar");
      if (!sidebar) return;
      mount = document.createElement("div");
      mount.id = "allNotesMount";
      sidebar.prepend(mount);
    }
    const card = document.createElement("section");
    card.className = "card all-notes-card";
    card.innerHTML = '<h2>全部注释 <small>All Notes</small> <b class="all-notes-total">0</b></h2><button type="button" class="all-notes-return" data-all-notes-return hidden>返回正文</button><div class="all-notes-groups"></div>';
    mount.replaceChildren(card);
    const groups = card.querySelector(".all-notes-groups");
    let rendering = false;

    function proxyTextarea(source) {
      const area = document.createElement("textarea");
      area.value = source.value;
      area.setAttribute("aria-label", source.getAttribute("aria-label") || "注释内容");
      area.addEventListener("input", () => {
        source.value = area.value;
        const event = new Event("input", { bubbles: true });
        event.allNotesProxy = true;
        source.dispatchEvent(event);
      });
      return area;
    }
    function actionButton(label, source, className = "") {
      const button = document.createElement("button");
      button.type = "button"; button.textContent = label; button.className = className;
      button.addEventListener("click", () => { source?.click(); queueMicrotask(render); });
      return button;
    }
    function section(title, rows) {
      const block = document.createElement("section");
      block.className = "all-notes-group";
      block.innerHTML = `<h3>${title} <b>${rows.length}</b></h3>`;
      if (!rows.length) block.insertAdjacentHTML("beforeend", '<p class="all-notes-empty">暂无</p>');
      rows.forEach(row => block.append(row));
      groups.append(block);
    }
    function render() {
      if (rendering) return;
      rendering = true; groups.innerHTML = ""; let total = 0;
      const footnoteRows = [...(document.getElementById("footnoteList")?.querySelectorAll(".footnote-item") || [])].map((sourceRow, index) => {
        const row = document.createElement("div"); row.className = "all-notes-row";
        const jump = actionButton(`${index + 1}.`, sourceRow.querySelector(".footnote-number"), "all-notes-source");
        const sourceArea = sourceRow.querySelector("textarea");
        row.append(jump, sourceArea ? proxyTextarea(sourceArea) : document.createTextNode(""));
        return row;
      });
      total += footnoteRows.length; section("脚注", footnoteRows);
      registers.forEach(([title, list]) => {
        const rows = [...(list?.querySelectorAll(".register-row") || [])].map(sourceRow => {
          const row = document.createElement("div"); row.className = "all-notes-row all-notes-register-row";
          const sourceButton = sourceRow.querySelector(".register-source");
          const jump = actionButton(sourceButton?.textContent.trim() || "定位正文", sourceButton, "all-notes-source");
          const sourceArea = sourceRow.querySelector("textarea");
          const actions = document.createElement("div"); actions.className = "all-notes-actions";
          sourceRow.querySelectorAll(".register-actions button").forEach(button => actions.append(actionButton(button.textContent, button, button.classList.contains("register-delete") ? "all-notes-delete" : "")));
          row.append(jump, sourceArea ? proxyTextarea(sourceArea) : document.createTextNode(""), actions);
          return row;
        });
        total += rows.length; section(title, rows);
      });
      card.querySelector(".all-notes-total").textContent = String(total);
      const returnButton = card.querySelector(".all-notes-return");
      returnButton.hidden = !document.querySelector(".study-pane");
      rendering = false;
    }
    let pending = false;
    const schedule = () => { if (!pending) { pending = true; requestAnimationFrame(() => { pending = false; render(); }); } };
    [document.getElementById("footnoteList"), ...registers.map(([, list]) => list)].filter(Boolean).forEach(list => {
      new MutationObserver(schedule).observe(list, { childList: true, subtree: true, attributes: true });
      list.addEventListener("input", event => { if (!event.allNotesProxy) schedule(); });
    });
    render();
  }

  function installGoogleVoicePriority() {
    const select = document.getElementById("voiceSelect");
    if (!select) return;
    let arranging = false;
    const arrange = () => {
      if (arranging) return;
      const options = [...select.options];
      if (options.length < 2) return;
      const first = options.shift();
      const google = options.filter(option => /^google\b/i.test(option.textContent.trim()));
      const others = options.filter(option => !/^google\b/i.test(option.textContent.trim()));
      const ordered = [first, ...google, ...others];
      if (ordered.every((option, index) => select.options[index] === option)) return;
      const selected = select.value;
      arranging = true;
      select.replaceChildren(...ordered);
      select.value = selected;
      arranging = false;
    };
    new MutationObserver(arrange).observe(select, { childList: true });
    arrange();
  }

  function installWorkspaceControls() { installContextNavigation(); installSwitch(); installReadingEnvironment(); installFileMenu(); installInsertMenu(); installUserNotesAccess(); installExpandingReviewFields(); installAnnotationSync(); installAllNotesView(); installImmersiveMode(); installGoogleVoicePriority(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", installWorkspaceControls);
  else installWorkspaceControls();
})();
