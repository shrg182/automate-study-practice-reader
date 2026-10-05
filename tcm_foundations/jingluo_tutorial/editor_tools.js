(() => {
  const editor = document.getElementById("editor");
  const toolbar = document.querySelector(".toolbar");
  const storageKey = document.body.dataset.editorKey;
  const channelName = document.body.dataset.channelName;
  if (!editor || !toolbar || !storageKey) return;

  const canonicalOverview = editor.querySelector(".google-ai-overview")?.cloneNode(true);
  const saved = localStorage.getItem(storageKey);
  if (saved) {
    const savedDocument = new DOMParser().parseFromString(`<article>${saved}</article>`, "text/html");
    const savedChannelName = savedDocument.querySelector("h1")?.textContent.trim();
    if (!channelName || savedChannelName === channelName) {
      editor.innerHTML = saved;
      if (canonicalOverview && !editor.querySelector(".google-ai-overview")) {
        const memorySection = [...editor.querySelectorAll("section")].find(
          section => section.querySelector(":scope > h2")?.textContent.trim() === "记忆任务"
        );
        (memorySection || editor.querySelector(".safety"))?.before(canonicalOverview);
      }
    } else {
      localStorage.setItem(`${storageKey}-mismatched-backup`, saved);
      console.warn(`Ignored a mismatched local draft for ${channelName}: ${savedChannelName || "missing title"}`);
    }
  }

  function persist() {
    try {
      localStorage.setItem(storageKey, editor.innerHTML);
    } catch (error) {
      console.warn("Unable to save JingLuo editor content", error);
    }
  }

  function selectedRange(requireText = true) {
    const selection = getSelection();
    if (!selection?.rangeCount) return null;
    const range = selection.getRangeAt(0).cloneRange();
    const container = range.commonAncestorContainer.nodeType === 1
      ? range.commonAncestorContainer
      : range.commonAncestorContainer.parentElement;
    if (!editor.contains(container) || (requireText && !range.toString().trim())) return null;
    return range;
  }

  function wrapRange(range, node) {
    try {
      range.surroundContents(node);
    } catch {
      node.append(range.extractContents());
      range.insertNode(node);
    }
    persist();
  }

  function addNotation() {
    const range = selectedRange();
    if (!range) return alert("请先选择需要注音或简注的文字。");
    const term = range.toString();
    const reading = prompt(`“${term}”的拼音或读音（可留空）：`, "");
    if (reading === null) return;
    const note = prompt("简注（可留空）：", "");
    if (note === null) return;
    const span = document.createElement("span");
    const ruby = document.createElement("ruby");
    const rt = document.createElement("rt");
    span.className = "notation";
    span.dataset.term = term;
    span.dataset.note = note.trim();
    span.title = note.trim();
    ruby.textContent = term;
    rt.textContent = reading.trim();
    ruby.append(rt);
    span.append(ruby);
    range.deleteContents();
    range.insertNode(span);
    persist();
  }

  function addInterlinear() {
    const range = selectedRange();
    if (!range) return alert("请先选择需要行间注的文字。");
    const note = prompt("行间注（显示在原文上方）：", "");
    if (!note?.trim()) return;
    const ruby = document.createElement("ruby");
    const rt = document.createElement("rt");
    ruby.className = "interlinear-note";
    ruby.append(range.extractContents());
    rt.textContent = note.trim();
    ruby.append(rt);
    range.insertNode(ruby);
    persist();
  }

  function footnoteList() {
    let section = editor.querySelector(".reader-footnotes");
    if (!section) {
      section = document.createElement("section");
      section.className = "reader-footnotes";
      section.innerHTML = "<h2>脚注</h2><ol></ol>";
      editor.append(section);
    }
    return section.querySelector("ol");
  }

  function addFootnote() {
    const range = selectedRange(false);
    if (!range) return alert("请把光标放在正文中，或选择需要脚注的文字。");
    const note = prompt("脚注内容：", "");
    if (!note?.trim()) return;
    const list = footnoteList();
    const number = list.children.length + 1;
    const item = document.createElement("li");
    const ref = document.createElement("sup");
    item.textContent = note.trim();
    ref.className = "footnote-ref";
    ref.textContent = `〔${number}〕`;
    ref.title = note.trim();
    if (!range.collapsed) {
      const anchor = document.createElement("span");
      anchor.className = "comment-anchor";
      anchor.append(range.extractContents());
      anchor.append(ref);
      range.insertNode(anchor);
    } else {
      range.insertNode(ref);
    }
    list.append(item);
    persist();
  }

  function addComment() {
    const range = selectedRange(false);
    if (!range) return alert("请把光标放在正文中。");
    const note = prompt("按语或评论：", "");
    if (!note?.trim()) return;
    if (!range.collapsed) {
      const anchor = document.createElement("span");
      anchor.className = "comment-anchor";
      anchor.title = note.trim();
      wrapRange(range, anchor);
    }
    const block = document.createElement("p");
    block.className = "comment-block";
    block.textContent = note.trim();
    const start = range.startContainer.nodeType === 1
      ? range.startContainer
      : range.startContainer.parentElement;
    const paragraph = start?.closest?.("p");
    (paragraph || editor.lastElementChild).after(block);
    persist();
  }

  function addDoubt() {
    const range = selectedRange();
    if (!range) return alert("请先选择需要标记存疑的文字。");
    const note = prompt("存疑原因（可留空）：", "");
    if (note === null) return;
    const span = document.createElement("span");
    span.className = "doubt";
    span.dataset.issue = note.trim();
    span.title = note.trim() || "存疑";
    wrapRange(range, span);
  }

  editor.addEventListener("input", persist);
  toolbar.addEventListener("click", event => {
    const button = event.target.closest("button");
    if (!button) return;
    const command = button.dataset.command;
    const action = button.dataset.action;
    if (command) {
      document.execCommand(command, false, command === "hiliteColor" ? "#fff2a8" : null);
      editor.focus();
      persist();
    }
    if (action === "notation") addNotation();
    if (action === "interlinear") addInterlinear();
    if (action === "footnote") addFootnote();
    if (action === "comment") addComment();
    if (action === "doubt") addDoubt();
  });
})();
