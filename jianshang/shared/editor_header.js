class JianshangEditorHeader extends HTMLElement {
  connectedCallback() {
    if (this.dataset.rendered === "true") return;
    this.dataset.rendered = "true";
    if (!document.querySelector('link[data-workspace-theme]')) {
      const theme = document.createElement("link");
      theme.rel = "stylesheet";
      theme.href = "../../workspace_theme.css";
      theme.dataset.workspaceTheme = "true";
      document.head.append(theme);
    }
    if (!document.querySelector('script[src$="workspace_skin.js"]')) {
      const skin = document.createElement("script");
      skin.src = "../../workspace_skin.js";
      document.head.appendChild(skin);
    }
    this.innerHTML = `
      <header>
        <div class="topbar">
          <div><h1 class="shared-editor-title"></h1><div class="subtitle shared-editor-subtitle"></div></div>
          <div class="actions">
            <div class="header-tool-group view-tools" aria-label="导航与视图"><a class="action-link" href="../../index.html">返回首页</a><button id="viewToggleBtn" class="primary" type="button">切换为注音稿</button><span id="modeBadge" class="mode-badge">当前：清稿</span></div>
            <div class="header-tool-group annotation-tools" aria-label="标注工具"><div class="format-menu" id="formatMenu"><button type="button" class="format-menu-trigger" id="formatMenuBtn" aria-haspopup="menu" aria-expanded="false" title="高亮与划线"><span class="marker-icon" aria-hidden="true"></span><span class="hidden">高亮与划线</span></button><div class="format-popover" id="formatPopover" role="menu" aria-label="高亮与划线"><button type="button" class="format-option" role="menuitem" data-command="hiliteColor" data-value="#fff1a8" data-label="黄色高亮"><span class="format-dot" style="background:#f4c542"></span>黄色</button><button type="button" class="format-option" role="menuitem" data-command="hiliteColor" data-value="#dff0d2" data-label="绿色高亮"><span class="format-dot" style="background:#78c56b"></span>绿色</button><button type="button" class="format-option" role="menuitem" data-command="hiliteColor" data-value="#dcebf7" data-label="蓝色高亮"><span class="format-dot" style="background:#68afe0"></span>蓝色</button><button type="button" class="format-option" role="menuitem" data-command="hiliteColor" data-value="#f8d7e4" data-label="粉色高亮"><span class="format-dot" style="background:#ef78a6"></span>粉色</button><button type="button" class="format-option" role="menuitem" data-command="hiliteColor" data-value="#e7d8f2" data-label="紫色高亮"><span class="format-dot" style="background:#b879cc"></span>紫色</button><div class="format-divider" role="separator"></div><button type="button" class="format-option" role="menuitem" data-command="underline" data-label="下划线"><span class="format-symbol"><u>U</u></span>下划线</button><button type="button" class="format-option" role="menuitem" data-command="strikeThrough" data-label="删除线"><span class="format-symbol"><s>S</s></span>删除线</button></div></div><button id="boldBtn" type="button" title="加粗所选文字"><strong>B</strong><span class="hidden">粗体</span></button><button id="addNotationBtn" type="button">添加注音</button><button id="addFootnoteBtn" type="button">添加编者注</button><button id="addCommentBtn" type="button">插入按语</button><button id="markDoubtBtn" type="button">标为待核</button><button id="addUserNoteBtn" type="button">用户札记</button></div>
            <div class="header-tool-group speech-tools" aria-label="语音朗读"><button id="speakBtn" type="button">朗读所选/本页</button><button id="pauseSpeechBtn" type="button" disabled>暂停</button><button id="stopSpeechBtn" type="button" disabled>停止</button><select id="voiceSelect" aria-label="朗读声音"><option value="">系统默认声音</option></select><label class="speech-rate">语速<input id="speechRate" type="range" min="0.5" max="1.5" step="0.1" value="0.8"><span id="speechRateValue">0.8×</span></label></div>
            <div class="header-tool-group file-tools" aria-label="保存与文件"><button id="saveBtn" type="button">保存</button><button id="printPdfBtn" type="button">导出 PDF</button><button id="exportBtn" type="button">生成文本</button><button id="downloadBtn" type="button">下载 TXT</button><button id="backupBtn" type="button">导出备份</button><label for="importBackup" class="import-label">导入备份</label><input id="importBackup" class="hidden" type="file" accept="application/json,.json"></div>
            <div class="header-tool-group reference-tools" aria-label="词典、参考与札记"><button id="dictionaryHintsBtn" type="button" class="active" aria-pressed="true">词典提示：开</button><label>难度<select id="dictionaryDifficulty" aria-label="词语最低难度"><option value="1">全部</option><option value="2">2+ 进阶</option><option value="3" selected>3+ 高阶</option><option value="4">4+ 生僻</option><option value="5">5 专业</option></select></label><label>词库<select id="dictionaryDomain" aria-label="词典领域"><option value="all">全部词库</option><option value="general">普通词语</option><option value="bronze_vessel">青铜器</option><option value="archaeology">考古</option><option value="proper_name">专名</option><option value="phrase">短语</option></select></label><a class="action-link" href="../../../project_dictionary/index.html" target="_blank">项目词典</a><a class="action-link master-vocabulary-link" href="#" target="_blank">全书总词表</a><a class="action-link master-bronze-link" href="#" target="_blank">青铜器名总表</a><button type="button" data-target="notes">札记</button><button id="resetBtn" type="button">恢复 clean 原稿</button></div><div id="status" class="status">文本已显示</div>
          </div>
        </div>
      </header>`;
    this.querySelector(".shared-editor-title").textContent = this.getAttribute("page-title") || "《翦商》校读编辑器";
    this.querySelector(".shared-editor-subtitle").textContent = this.getAttribute("page-subtitle") || "";
    const annotationTools = this.querySelector(".annotation-tools");
    annotationTools.insertAdjacentHTML("beforeend", '<button id="insertImageBtn" type="button">插入图片</button><input id="editorImageInput" class="hidden" type="file" accept="image/jpeg,image/png,image/webp,image/gif">');
    const projectDictionaryLink = [...this.querySelectorAll(".reference-tools a")].find(link => link.textContent === "项目词典");
    if (projectDictionaryLink) projectDictionaryLink.textContent = "共享项目词典";
    const masterVocabularyLink = this.querySelector(".master-vocabulary-link");
    if (masterVocabularyLink) {
      masterVocabularyLink.textContent = "《翦商》总词表";
      masterVocabularyLink.insertAdjacentHTML("beforebegin", '<label for="dictionaryOverridesInput" class="import-label">导入词典修订</label><input id="dictionaryOverridesInput" class="hidden" type="file" accept="application/json,.json">');
    }
    const referenceHref = this.getAttribute("reference-href") || "../reference_tables.html";
    this.querySelector(".master-vocabulary-link").href = `${referenceHref}#vocabulary`;
    this.querySelector(".master-bronze-link").href = `${referenceHref}#bronze`;
    this.querySelector("#printPdfBtn").addEventListener("click", () => window.print());

    const header = this.querySelector("header");
    const updateHeaderHeight = () => {
      const height = Math.ceil(header.getBoundingClientRect().height);
      document.documentElement.style.setProperty("--editor-header-height", `${height}px`);
    };
    updateHeaderHeight();
    requestAnimationFrame(updateHeaderHeight);
    if ("ResizeObserver" in window) {
      this.headerResizeObserver = new ResizeObserver(updateHeaderHeight);
      this.headerResizeObserver.observe(header);
    }
  }

  disconnectedCallback() {
    this.headerResizeObserver?.disconnect();
  }
}

if (!customElements.get("jianshang-editor-header")) {
  customElements.define("jianshang-editor-header", JianshangEditorHeader);
}
