(function () {
  const mobile = matchMedia("(max-width: 760px)");
  const isEditor = /\/editor\.html$/.test(location.pathname);
  const isBookPage = /\/(?:marxist_classics\/(?:capital|anti_duhring)\/select_readings|tcm_foundations\/index)\.html$/.test(location.pathname);
  const englishFirst = /English-First Reader/i.test(document.title);
  const scriptRoot = document.currentScript?.src ? new URL(".", document.currentScript.src) : new URL("./", location.href);
  let installPrompt = null;
  let registration = null;
  let reloadingForUpdate = false;
  let editing = false;
  let originalEditable = [];

  function style() {
    const element = document.createElement("style");
    element.textContent = `
      .mobile-pwa-bar,.mobile-pwa-toast{display:none}
      .mobile-pwa-update{position:fixed;z-index:500;top:calc(env(safe-area-inset-top,0px) + 10px);left:50%;display:none;max-width:calc(100% - 28px);padding:10px 12px 10px 16px;align-items:center;gap:12px;border:1px solid #aecbfa;border-radius:24px;background:#e8f0fe;color:#174ea6;box-shadow:0 5px 20px #0003;font:13px/1.35 Arial,"PingFang SC",sans-serif;transform:translateX(-50%)}
      .mobile-pwa-update.show{display:flex}.mobile-pwa-update button{min-height:32px;padding:6px 11px;border:0;border-radius:16px;background:#1a73e8;color:#fff;cursor:pointer;font:inherit;font-weight:700;white-space:nowrap}
      @media(max-width:760px){
        html,body.mobile-pwa{max-width:100%!important;overflow-x:hidden!important}
        body.mobile-pwa{padding-bottom:64px!important}
        body.mobile-pwa .masthead-inner,body.mobile-pwa .workspace,body.mobile-pwa .main-content,body.mobile-pwa .editor-shell,body.mobile-pwa .content-grid{display:block!important;width:100%!important;min-width:0!important;max-width:100%!important;padding-left:0!important;padding-right:0!important}
        body.mobile-pwa .paper{box-sizing:border-box!important;width:100%!important;min-width:0!important;max-width:100%!important;min-height:100vh!important;padding:24px 18px 88px!important;border:0!important;box-shadow:none!important}
        body.mobile-pwa .editor,body.mobile-pwa .rich-editor{box-sizing:border-box!important;width:100%!important;min-width:0!important;max-width:100%!important;font-size:var(--reading-content-font-size,18px)!important;line-height:var(--reading-content-line-height,1.9)!important;overflow-wrap:anywhere!important}
        body.mobile-pwa.mobile-read-mode .toolbar{display:none!important}
        body.mobile-pwa.mobile-read-mode .sidebar{display:none!important}
        body.mobile-pwa.mobile-panel-open .sidebar{display:flex!important;position:fixed!important;z-index:220;inset:54px 0 62px!important;width:auto!important;min-width:0!important;max-width:none!important;max-height:none!important;margin:0!important;padding:12px;background:#f8f9fa;overflow:auto;visibility:visible!important;transform:none!important}
        body.mobile-pwa.mobile-panel-open .study-pane{flex-direction:column!important}
        body.mobile-pwa.mobile-edit-mode .toolbar{display:flex!important;position:fixed!important;z-index:210;inset:0 0 auto!important;max-height:52vh;overflow:auto;box-shadow:0 5px 20px #0003}
        body.mobile-pwa.mobile-edit-mode .workspace{padding-top:54px!important}
        .mobile-pwa-bar{box-sizing:border-box!important;position:fixed;z-index:300;left:0;right:auto;bottom:0;display:flex;width:100vw!important;min-width:0!important;max-width:100vw!important;min-height:58px;padding:max(4px,env(safe-area-inset-bottom)) 4px env(safe-area-inset-bottom);border-top:1px solid #dadce0;background:#fff;color:#3c4043;box-shadow:0 -2px 12px #0002;overflow-x:auto}
        .mobile-pwa-bar.mobile-home-bar{grid-template-columns:repeat(3,minmax(0,1fr))}
        .mobile-pwa-bar button{display:grid!important;flex:1 0 62px;place-items:center;min-width:62px!important;min-height:48px!important;padding:4px 2px!important;border:0!important;background:transparent!important;color:inherit!important;font:11px/1.2 Arial,"PingFang SC",sans-serif!important}
        .mobile-pwa-bar button.active{color:#137333!important;background:#e6f4ea!important;border-radius:12px!important;font-weight:700!important}
        .mobile-pwa-toast{position:fixed;z-index:400;left:50%;bottom:74px;display:block;max-width:calc(100% - 32px);padding:9px 14px;border-radius:18px;background:#202124;color:#fff;font:12px/1.4 Arial,"PingFang SC",sans-serif;transform:translateX(-50%);opacity:0;pointer-events:none;transition:opacity .2s}
        .mobile-pwa-toast.show{opacity:1}
      }
      @media(min-width:761px){
        body.mobile-pwa{padding-bottom:64px!important}
        .mobile-pwa-bar{box-sizing:border-box!important;position:fixed;z-index:300;left:50%;bottom:14px;display:flex;max-width:min(760px,calc(100vw - 28px));padding:5px;border:1px solid #dadce0;border-radius:24px;background:#fff;color:#3c4043;box-shadow:0 4px 18px #0002;transform:translateX(-50%)}
        .mobile-pwa-bar.mobile-home-bar{max-width:260px}.mobile-pwa-bar button{display:grid!important;flex:1 1 auto;place-items:center;min-width:66px!important;min-height:38px!important;padding:5px 8px!important;border:0!important;border-radius:16px!important;background:transparent!important;color:inherit!important;font:11px/1.2 Arial,"PingFang SC",sans-serif!important}.mobile-pwa-bar button.active{color:#137333!important;background:#e6f4ea!important;font-weight:700!important}
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
    const paneButton = document.querySelector('[data-mobile-action="pane"]');
    if (paneButton) { paneButton.classList.remove("active"); paneButton.textContent = englishFirst ? "Pane" : "窗格"; paneButton.setAttribute("aria-pressed", "false"); }
    const nodes = editableNodes();
    if (!originalEditable.length) originalEditable = nodes.map(node => node.getAttribute("contenteditable"));
    nodes.forEach((node, index) => {
      if (node.matches(".reader-editable-cell")) {
        node.setAttribute("contenteditable", "true");
        return;
      }
      node.setAttribute("contenteditable", enabled ? (originalEditable[index] || "true") : "false");
    });
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

  async function bookUrls(manifestPath = "book_manifest.json") {
    const manifestUrl = new URL(manifestPath, location.href);
    const response = await fetch(manifestUrl, {cache: "no-store"});
    if (!response.ok) throw new Error("无法读取本书离线清单");
    const manifest = await response.json();
    const urls = [location.href, manifestUrl.href];
    (manifest.units || []).forEach(unit => urls.push(new URL(unit.path, manifestUrl).href));
    Object.values(manifest.components || {}).forEach(component => {
      if (component?.path) urls.push(new URL(component.path, manifestUrl).href);
    });
    ["workspace_theme.css", "workspace_skin.js", "mobile_pwa.js", "index.html"].forEach(path => urls.push(new URL(path, scriptRoot).href));
    return [...new Set(urls)];
  }

  async function manageOfflineBook(remove = false, manifestPath = "book_manifest.json", bookName = "") {
    if (!navigator.serviceWorker?.controller) return toast("离线书库将在重新打开应用后可用");
    try {
      if (!remove) {
        await navigator.storage?.persist?.();
        toast("正在保存整本书，请保持页面开启…");
      }
      navigator.serviceWorker.controller.postMessage({type: remove ? "REMOVE_BOOK" : "CACHE_BOOK", urls: await bookUrls(manifestPath), book: bookName || document.querySelector("h1")?.textContent?.trim() || "本书"});
    } catch (error) {
      toast(`离线书库操作失败：${error.message}`);
    }
  }

  function showPanel(kind) {
    document.body.classList.add("mobile-panel-open");
    document.body.classList.remove("mobile-edit-mode");
    const paneButton = document.querySelector('[data-mobile-action="pane"]');
    if (paneButton) { paneButton.classList.add("active"); paneButton.textContent = englishFirst ? "Text" : "正文"; paneButton.setAttribute("aria-pressed", "true"); }
    if (window.BilingualStudyPane) {
      window.BilingualStudyPane.activateTab(kind === "notes" ? "notes" : kind === "chinese" ? "chinese" : "dictionary");
      document.querySelector(".study-pane")?.scrollIntoView({block: "start"});
      return;
    }
    const selector = kind === "notes" ? "#user-notes,.notes-dock,#notes" : ".sidebar,.term-list";
    document.querySelector(selector)?.scrollIntoView({block: "start"});
  }

  function toggleStudyPane() {
    if (!document.body.classList.contains("mobile-panel-open")) return showPanel("chinese");
    document.body.classList.remove("mobile-panel-open");
    const paneButton = document.querySelector('[data-mobile-action="pane"]');
    if (paneButton) { paneButton.classList.remove("active"); paneButton.textContent = englishFirst ? "Pane" : "窗格"; paneButton.setAttribute("aria-pressed", "false"); }
    document.querySelector(".paper,.editor-panel")?.scrollIntoView({block: "start"});
  }

  async function install() {
    if (installPrompt) {
      installPrompt.prompt(); await installPrompt.userChoice; installPrompt = null; return;
    }
    const ios = /iphone|ipad|ipod/i.test(navigator.userAgent);
    alert(ios ? "请在 Safari 中点按“分享”，再选择“添加到主屏幕”。" : "请打开浏览器菜单并选择“安装应用”或“添加到主屏幕”。");
  }

  function waitForInstalled(worker) {
    if (!worker || worker.state === "installed") return Promise.resolve(worker);
    return new Promise(resolve => worker.addEventListener("statechange", () => {
      if (worker.state === "installed" || worker.state === "redundant") resolve(worker);
    }));
  }

  async function updateApp() {
    if (!registration) return toast("更新服务正在启动，请稍后再试");
    toast("正在检查并刷新应用…");
    try {
      await registration.update();
      const installing = registration.installing;
      if (installing) await waitForInstalled(installing);
      const waiting = registration.waiting;
      if (waiting) {
        reloadingForUpdate = true;
        waiting.postMessage({type: "SKIP_WAITING"});
        return;
      }
      if (navigator.serviceWorker.controller) {
        reloadingForUpdate = true;
        navigator.serviceWorker.controller.postMessage({type: "REFRESH_APP"});
        return;
      }
      location.reload();
    } catch (error) {
      reloadingForUpdate = false;
      toast(navigator.onLine ? "更新失败，请稍后再试" : "当前离线，联网后再更新");
    }
  }

  function mount() {
    if (document.querySelector(".mobile-pwa-bar")) return;
    style(); document.body.classList.add("mobile-pwa");
    const buttons = isEditor
      ? englishFirst
        ? '<button data-mobile-action="home">Home</button><button data-mobile-action="book">Books</button><button data-mobile-action="pane" aria-pressed="false">Pane</button><button data-mobile-action="immersive">Focus</button><button data-mobile-action="settings">Settings</button><button data-mobile-action="notes">Notes</button><button data-mobile-action="sync">Sync</button><button data-mobile-action="edit">Edit</button><button data-mobile-action="offline">Offline</button><button data-mobile-action="install">Install</button>'
        : '<button data-mobile-action="home">目录</button><button data-mobile-action="book">书目</button><button data-mobile-action="pane" aria-pressed="false">窗格</button><button data-mobile-action="immersive">沉浸</button><button data-mobile-action="settings">设置</button><button data-mobile-action="notes">札记</button><button data-mobile-action="sync">同步</button><button data-mobile-action="edit">编辑</button><button data-mobile-action="offline">离线</button><button data-mobile-action="install">安装</button>'
      : isBookPage
        ? '<button data-mobile-action="home">目录</button><button data-mobile-action="book-offline">保存本书</button><button data-mobile-action="book-remove">移除离线</button><button data-mobile-action="update">更新</button><button data-mobile-action="install">安装</button>'
        : '<button data-mobile-action="home" class="active">目录</button><button data-mobile-action="update">更新</button><button data-mobile-action="install">安装</button>';
    document.body.insertAdjacentHTML("beforeend", `<div class="mobile-pwa-toast" role="status"></div><div class="mobile-pwa-update" role="status"><span>${englishFirst ? "A Mobile Reader update is available" : "发现新版 Mobile Reader"}</span><button type="button">${englishFirst ? "Update now" : "立即更新"}</button></div><nav class="mobile-pwa-bar${isEditor ? "" : " mobile-home-bar"}" aria-label="${englishFirst ? "Reader tools" : "阅读工具"}">${buttons}</nav>`);
    if (registration?.waiting && navigator.serviceWorker.controller) document.querySelector(".mobile-pwa-update").classList.add("show");
    document.querySelector(".mobile-pwa-update button").addEventListener("click", updateApp);
    document.querySelector(".mobile-pwa-bar").addEventListener("click", async event => {
      const action = event.target.closest("button")?.dataset.mobileAction;
      if (action === "home") location.href = window.ReadingWorkspace?.directoryHref || new URL("index.html", scriptRoot).href;
      if (action === "book") location.href = window.ReadingWorkspace?.bookDirectoryHref || window.ReadingWorkspace?.directoryHref || new URL("index.html", scriptRoot).href;
      if (action === "pane") toggleStudyPane();
      if (action === "immersive") window.ReadingWorkspace?.toggleImmersive?.();
      if (action === "settings") window.ReadingWorkspace?.openSettings?.();
      if (action === "notes") showPanel("notes");
      if (action === "sync") window.ReadingWorkspace?.openSync?.();
      if (action === "edit") setEditing(!editing);
      if (action === "offline") cacheArticle();
      if (action === "book-offline") manageOfflineBook(false);
      if (action === "book-remove") manageOfflineBook(true);
      if (action === "update") updateApp();
      if (action === "install") install();
    });
    if (isEditor) setEditing(false, true);
    storageLabel().then(value => {
      const offlineButton = document.querySelector('[data-mobile-action="offline"]');
      if (value && offlineButton) offlineButton.title = `已用空间 ${value}`;
    });
  }

  window.addEventListener("beforeinstallprompt", event => { event.preventDefault(); installPrompt = event; });
  document.addEventListener("click", event => {
    const button = event.target.closest("[data-offline-manifest]");
    if (button) manageOfflineBook(button.dataset.offlineRemove === "true", button.dataset.offlineManifest, button.dataset.offlineBook);
  });
  navigator.serviceWorker?.addEventListener("message", async event => {
    if (event.data?.type === "ARTICLE_CACHED") toast(`本篇已保存离线 · ${await storageLabel()}`);
    if (event.data?.type === "BOOK_CACHED") toast(`${event.data.book || "本书"}已保存到离线书库 · ${await storageLabel()}`);
    if (event.data?.type === "BOOK_REMOVED") toast(`${event.data.book || "本书"}的离线副本已移除`);
    if (event.data?.type === "CACHE_ERROR") toast(`离线保存失败：${event.data.message}`);
    if (event.data?.type === "APP_REFRESHED") location.reload();
    if (event.data?.type === "APP_REFRESH_ERROR") { reloadingForUpdate = false; toast("更新失败，请稍后再试"); }
  });
  function announceUpdate(worker) { if (worker && navigator.serviceWorker.controller) document.querySelector(".mobile-pwa-update")?.classList.add("show"); }
  if ("serviceWorker" in navigator && /^(https?:)$/.test(location.protocol)) {
    navigator.serviceWorker.register(new URL("service-worker.js", scriptRoot), {scope: scriptRoot.pathname, updateViaCache: "none"}).then(value => {
      registration = value; announceUpdate(registration.waiting);
      registration.addEventListener("updatefound", () => { const worker = registration.installing; worker?.addEventListener("statechange", () => { if (worker.state === "installed") announceUpdate(worker); }); });
      window.setInterval(() => registration.update().catch(() => {}), 60 * 60 * 1000);
    }).catch(error => console.warn("PWA service worker registration failed", error));
    navigator.serviceWorker.addEventListener("controllerchange", () => { if (reloadingForUpdate) location.reload(); });
    document.addEventListener("visibilitychange", () => { if (document.visibilityState === "visible") registration?.update().catch(() => {}); });
    window.addEventListener("pageshow", () => registration?.update().catch(() => {}));
    window.addEventListener("online", () => registration?.update().catch(() => {}));
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount); else mount();
})();
