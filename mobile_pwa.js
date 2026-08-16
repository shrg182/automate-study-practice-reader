(function () {
  const mobile = matchMedia("(max-width: 760px)");
  const isEditor = /\/editor\.html$/.test(location.pathname);
  const scriptRoot = document.currentScript?.src ? new URL(".", document.currentScript.src) : new URL("./", location.href);
  let installPrompt = null;
  let editing = false;
  let originalEditable = [];

  function style() {
    const element = document.createElement("style");
    element.textContent = `
      .mobile-pwa-bar,.mobile-pwa-toast{display:none}
      @media(max-width:760px){
        html,body.mobile-pwa{max-width:100%!important;overflow-x:hidden!important}
        body.mobile-pwa{padding-bottom:64px!important}
        body.mobile-pwa .masthead-inner,body.mobile-pwa .workspace,body.mobile-pwa .main-content,body.mobile-pwa .editor-shell,body.mobile-pwa .content-grid{display:block!important;width:100%!important;min-width:0!important;max-width:100%!important;padding-left:0!important;padding-right:0!important}
        body.mobile-pwa .paper{box-sizing:border-box!important;width:100%!important;min-width:0!important;max-width:100%!important;min-height:100vh!important;padding:24px 18px 88px!important;border:0!important;box-shadow:none!important}
        body.mobile-pwa .editor,body.mobile-pwa .rich-editor{box-sizing:border-box!important;width:100%!important;min-width:0!important;max-width:100%!important;font-size:var(--reading-content-font-size,18px)!important;line-height:1.9!important;overflow-wrap:anywhere!important}
        body.mobile-pwa.mobile-read-mode .toolbar{display:none!important}
        body.mobile-pwa.mobile-read-mode .sidebar{display:none!important}
        body.mobile-pwa.mobile-panel-open .sidebar{display:flex!important;position:fixed!important;z-index:220;inset:54px 0 62px!important;max-height:none!important;padding:12px;background:#f8f9fa;overflow:auto}
        body.mobile-pwa.mobile-edit-mode .toolbar{display:flex!important;position:fixed!important;z-index:210;inset:0 0 auto!important;max-height:52vh;overflow:auto;box-shadow:0 5px 20px #0003}
        body.mobile-pwa.mobile-edit-mode .workspace{padding-top:54px!important}
        .mobile-pwa-bar{box-sizing:border-box!important;position:fixed;z-index:300;left:0;right:auto;bottom:0;display:grid;width:100vw!important;min-width:0!important;max-width:100vw!important;grid-template-columns:repeat(5,minmax(0,1fr));min-height:58px;padding:max(4px,env(safe-area-inset-bottom)) 4px env(safe-area-inset-bottom);border-top:1px solid #dadce0;background:#fff;color:#3c4043;box-shadow:0 -2px 12px #0002}
        .mobile-pwa-bar.mobile-home-bar{grid-template-columns:repeat(2,minmax(0,1fr))}
        .mobile-pwa-bar button{display:grid!important;place-items:center;min-width:0!important;min-height:48px!important;padding:4px 2px!important;border:0!important;background:transparent!important;color:inherit!important;font:11px/1.2 Arial,"PingFang SC",sans-serif!important}
        .mobile-pwa-bar button.active{color:#137333!important;background:#e6f4ea!important;border-radius:12px!important;font-weight:700!important}
        .mobile-pwa-toast{position:fixed;z-index:400;left:50%;bottom:74px;display:block;max-width:calc(100% - 32px);padding:9px 14px;border-radius:18px;background:#202124;color:#fff;font:12px/1.4 Arial,"PingFang SC",sans-serif;transform:translateX(-50%);opacity:0;pointer-events:none;transition:opacity .2s}
        .mobile-pwa-toast.show{opacity:1}
      }
      @media print{.mobile-pwa-bar,.mobile-pwa-toast{display:none!important}}
    `;
    document.head.appendChild(element);
  }

  function toast(message) {
    const node = document.querySelector(".mobile-pwa-toast");
    if (!node) return;
    node.textContent = message; node.classList.add("show");
    clearTimeout(toast.timer); toast.timer = setTimeout(() => node.classList.remove("show"), 2600);
  }

  function editableNodes() { return [...document.querySelectorAll("#editor,[contenteditable],.rich-editor")]; }

  function setEditing(enabled, silent = false) {
    editing = enabled;
    document.body.classList.toggle("mobile-edit-mode", enabled);
    document.body.classList.toggle("mobile-read-mode", !enabled);
    document.body.classList.remove("mobile-panel-open");
    const nodes = editableNodes();
    if (!originalEditable.length) originalEditable = nodes.map(node => node.getAttribute("contenteditable"));
    nodes.forEach((node, index) => node.setAttribute("contenteditable", enabled ? (originalEditable[index] || "true") : "false"));
    document.querySelector('[data-mobile-action="edit"]')?.classList.toggle("active", enabled);
    if (!silent) toast(enabled ? "已进入轻编辑模式" : "已返回受保护的阅读模式");
  }

  function articleUrls() {
    const urls = [new URL(location.pathname, location.href).href];
    document.querySelectorAll('link[rel="stylesheet"],script[src],img[src]').forEach(node => {
      const source = node.href || node.src;
      if (source && new URL(source, location.href).origin === location.origin && !source.startsWith("data:")) urls.push(source);
    });
    return [...new Set(urls)];
  }

  async function storageLabel() {
    if (!navigator.storage?.estimate) return "";
    const {usage = 0, quota = 0} = await navigator.storage.estimate();
    return `${(usage / 1048576).toFixed(1)} MB / ${(quota / 1073741824).toFixed(1)} GB`;
  }

  async function cacheArticle() {
    if (!navigator.serviceWorker?.controller) return toast("离线功能将在重新打开应用后可用");
    navigator.serviceWorker.controller.postMessage({type: "CACHE_ARTICLE", urls: articleUrls()});
    toast("正在保存本篇供离线阅读…");
  }

  function showPanel(kind) {
    document.body.classList.add("mobile-panel-open");
    document.body.classList.remove("mobile-edit-mode");
    const selector = kind === "notes" ? "#user-notes,.notes-dock,#notes" : ".sidebar,.term-list";
    document.querySelector(selector)?.scrollIntoView({block: "start"});
  }

  async function install() {
    if (installPrompt) {
      installPrompt.prompt(); await installPrompt.userChoice; installPrompt = null; return;
    }
    const ios = /iphone|ipad|ipod/i.test(navigator.userAgent);
    alert(ios ? "请在 Safari 中点按“分享”，再选择“添加到主屏幕”。" : "请打开浏览器菜单并选择“安装应用”或“添加到主屏幕”。");
  }

  function mount() {
    if (!mobile.matches || document.querySelector(".mobile-pwa-bar")) return;
    style(); document.body.classList.add("mobile-pwa");
    const buttons = isEditor
      ? '<button data-mobile-action="home">首页</button><button data-mobile-action="notes">札记</button><button data-mobile-action="edit">编辑</button><button data-mobile-action="offline">离线</button><button data-mobile-action="install">安装</button>'
      : '<button data-mobile-action="home" class="active">目录</button><button data-mobile-action="install">安装</button>';
    document.body.insertAdjacentHTML("beforeend", `<div class="mobile-pwa-toast" role="status"></div><nav class="mobile-pwa-bar${isEditor ? "" : " mobile-home-bar"}" aria-label="移动阅读工具">${buttons}</nav>`);
    document.querySelector(".mobile-pwa-bar").addEventListener("click", async event => {
      const action = event.target.closest("button")?.dataset.mobileAction;
      if (action === "home") location.href = new URL("index.html", scriptRoot).href;
      if (action === "notes") showPanel("notes");
      if (action === "edit") setEditing(!editing);
      if (action === "offline") cacheArticle();
      if (action === "install") install();
    });
    if (isEditor) setEditing(false, true);
    storageLabel().then(value => { if (value) document.querySelector('[data-mobile-action="offline"]').title = `已用空间 ${value}`; });
  }

  window.addEventListener("beforeinstallprompt", event => { event.preventDefault(); installPrompt = event; });
  navigator.serviceWorker?.addEventListener("message", async event => {
    if (event.data?.type === "ARTICLE_CACHED") toast(`本篇已保存离线 · ${await storageLabel()}`);
    if (event.data?.type === "CACHE_ERROR") toast(`离线保存失败：${event.data.message}`);
  });
  if ("serviceWorker" in navigator && /^(https?:)$/.test(location.protocol)) navigator.serviceWorker.register(new URL("service-worker.js", scriptRoot), {scope: scriptRoot.pathname}).catch(error => console.warn("PWA service worker registration failed", error));
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount); else mount();
})();
