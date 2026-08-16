const JIANSHANG_CHAPTERS = [
  {
    "chapter": "intro",
    "title": "引子",
    "printedStart": 1,
    "printedEnd": 22,
    "available": true
  },
  {
    "chapter": "chapter_01",
    "title": "第一章 新石器时代的社会升级",
    "printedStart": 23,
    "printedEnd": 34,
    "available": true
  },
  {
    "chapter": "chapter_02",
    "title": "第二章 大禹治水真相：稻与龙",
    "printedStart": 35,
    "printedEnd": 48,
    "available": true
  },
  {
    "chapter": "chapter_03",
    "title": "第三章 二里头：青铜铸造王权",
    "printedStart": 49,
    "printedEnd": 74,
    "available": true
  },
  {
    "chapter": "chapter_04",
    "title": "第四章 异族占领二里头",
    "printedStart": 75,
    "printedEnd": 88,
    "available": true
  },
  {
    "chapter": "chapter_05",
    "title": "第五章 商族来源之谜",
    "printedStart": 89,
    "printedEnd": 102,
    "available": true
  },
  {
    "chapter": "chapter_06",
    "title": "第六章 早商：仓城奇观",
    "printedStart": 103,
    "printedEnd": 116,
    "available": true
  },
  {
    "chapter": "chapter_07",
    "title": "第七章 人祭繁荣与宗教改革运动",
    "printedStart": 117,
    "printedEnd": 144,
    "available": true
  },
  {
    "chapter": "chapter_08",
    "title": "第八章 武德沦丧南土：盘龙城",
    "printedStart": 145,
    "printedEnd": 160,
    "available": true
  },
  {
    "chapter": "chapter_09",
    "title": "第九章 3300年前的军营：台西",
    "printedStart": 161,
    "printedEnd": 180,
    "available": true
  },
  {
    "chapter": "chapter_10",
    "title": "第十章 殷都王室的人祭",
    "printedStart": 181,
    "printedEnd": 208,
    "available": true
  },
  {
    "chapter": "chapter_11",
    "title": "第十一章 商人的思维与国家",
    "printedStart": 209,
    "printedEnd": 228,
    "available": true
  },
  {
    "chapter": "chapter_12",
    "title": "第十二章 王后的社交圈",
    "printedStart": 229,
    "printedEnd": 248,
    "available": true
  },
  {
    "chapter": "chapter_13",
    "title": "第十三章 大学与王子",
    "printedStart": 249,
    "printedEnd": 268,
    "available": true
  },
  {
    "chapter": "chapter_14",
    "title": "第十四章 西土拉锯战：老牛坡",
    "printedStart": 269,
    "printedEnd": 286,
    "available": true
  },
  {
    "chapter": "chapter_15",
    "title": "第十五章 周族的起源史诗与考古",
    "printedStart": 287,
    "printedEnd": 310,
    "available": true
  },
  {
    "chapter": "chapter_16",
    "title": "第十六章 成为商朝爪牙：去周原",
    "printedStart": 311,
    "printedEnd": 326,
    "available": true
  },
  {
    "chapter": "chapter_17",
    "title": "第十七章 周文王地窖里的秘密",
    "printedStart": 327,
    "printedEnd": 340,
    "available": true
  },
  {
    "chapter": "chapter_18",
    "title": "第十八章 《易经》里的猎俘与献俘",
    "printedStart": 341,
    "printedEnd": 356,
    "available": true
  },
  {
    "chapter": "chapter_19",
    "title": "第十九章 羑里牢狱记忆",
    "printedStart": 357,
    "printedEnd": 374,
    "available": true
  },
  {
    "chapter": "chapter_20",
    "title": "第二十章 翦商与《易经》的世界观",
    "printedStart": 375,
    "printedEnd": 392,
    "available": true
  },
  {
    "chapter": "chapter_21",
    "title": "第二十一章 殷都民间的人祭",
    "printedStart": 393,
    "printedEnd": 414,
    "available": true
  },
  {
    "chapter": "chapter_22",
    "title": "第二十二章 纣王的东南战争",
    "printedStart": 415,
    "printedEnd": 428,
    "available": true
  },
  {
    "chapter": "chapter_23",
    "title": "第二十三章 姜太公与周方伯",
    "printedStart": 429,
    "printedEnd": 450,
    "available": true
  },
  {
    "chapter": "chapter_24",
    "title": "第二十四章 西土之人",
    "printedStart": 451,
    "printedEnd": 480,
    "available": true
  },
  {
    "chapter": "chapter_25",
    "title": "第二十五章 牧野鹰扬",
    "printedStart": 481,
    "printedEnd": 508,
    "available": true
  },
  {
    "chapter": "chapter_26",
    "title": "第二十六章 周公新时代",
    "printedStart": 509,
    "printedEnd": 548,
    "available": true
  },
  {
    "chapter": "chapter_27",
    "title": "第二十七章 诸神远去之后",
    "printedStart": 549,
    "printedEnd": 558,
    "available": true
  },
  {
    "chapter": "epilogue",
    "title": "尾声：周公到孔子",
    "printedStart": 559,
    "printedEnd": 574,
    "available": true
  },
  {
    "chapter": "afterword",
    "title": "后记",
    "printedStart": 575,
    "printedEnd": 579,
    "available": true
  }
];

class JianshangEditorToc extends HTMLElement {
  connectedCallback() {
    if (this.dataset.rendered === "true") return;
    this.dataset.rendered = "true";
    const current = this.getAttribute("current-chapter") || "";
    const section = document.createElement("section");
    section.className = "toc-page";
    section.id = "toc";
    section.innerHTML = `<div class="toc-head"><h2>目录</h2><span>手工校订工作台</span></div>
      <div class="toc-body"><div><h3>章节</h3><div class="toc-legend"><span class="legend-current">当前章节</span><span class="legend-available">可打开</span><span class="legend-unavailable">尚未生成</span></div><div class="toc-links"></div></div>
      <div><h3>工作说明</h3><p>左侧文字来自已处理的 clean 文本，并按段落近似切分到 PDF 页。右侧为源 PDF 页面图像。手工修改后请使用“生成文本”或“下载 TXT”，作为 manual edition 输出。</p><p>浏览器自动保存只保存在本机 localStorage；长期保存请下载 TXT 和日志。</p></div></div>`;
    const links = section.querySelector(".toc-links");
    for (const item of JIANSHANG_CHAPTERS) {
      const link = document.createElement("a");
      const isCurrent = item.chapter === current;
      link.className = `toc-link ${isCurrent ? "current" : item.available ? "available" : "unavailable"}`;
      if (item.available) {
        link.href = isCurrent ? "editor.html" : `../${item.chapter}/editor.html`;
      } else {
        link.setAttribute("aria-disabled", "true");
        link.title = "此章 editor.html 尚未生成";
      }
      const title = document.createElement("span");
      title.textContent = item.title;
      const pages = document.createElement("span");
      pages.textContent = `${item.printedStart}-${item.printedEnd}`;
      link.append(title, pages);
      links.append(link);
    }
    this.replaceChildren(section);
  }
}

if (!customElements.get("jianshang-editor-toc")) {
  customElements.define("jianshang-editor-toc", JianshangEditorToc);
}
