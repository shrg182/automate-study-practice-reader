/* Device-local reading workspaces in the main library. No source files are read. */
(() => {
  'use strict';
  const section = document.getElementById('reading-workspaces');
  if (!section || !window.OpenBooksStore) return;
  const cards = section.querySelector('[data-workspace-cards]');
  const status = section.querySelector('[data-workspace-status]');
  const refreshButton = section.querySelector('[data-workspace-refresh]');
  let entries = [], query = '', category = 'all', refreshing = false, again = false, loadError = false, timer;
  function filter(nextQuery = query, nextCategory = category) {
    query = nextQuery; category = nextCategory;
    const categoryMatch = !!query || ['all', 'offline', 'workspaces'].includes(category);
    let count = 0;
    for (const card of cards.children) {
      card.hidden = !categoryMatch || (!!query && !card.dataset.search.includes(query));
      if (!card.hidden) count++;
    }
    section.hidden = !categoryMatch || (!!query && count === 0 && category !== 'workspaces');
    if (!loadError && entries.length) status.textContent = count ? '' : '没有匹配的工作区 · No matching workspaces.';
    return count;
  }
  function render() {
    cards.replaceChildren();
    for (const item of entries) {
      const card = document.createElement('article'); card.className = 'workspace-library-card';
      card.dataset.workspaceId = item.id;
      card.dataset.search = `${item.name} workspace reading workspaces 阅读工作区`.toLocaleLowerCase();
      const badge = document.createElement('span'); badge.className = 'workspace-library-badge'; badge.textContent = '▦ 阅读工作区 · Workspace';
      const heading = document.createElement('h3'), link = document.createElement('a');
      const url = new URL('offline_readings/dual_reader/editor.html', location.href);
      url.searchParams.set('view', 'annotated'); url.searchParams.set('workspace', item.id);
      link.href = url.href; link.textContent = item.name; heading.append(link);
      const summary = document.createElement('p');
      summary.textContent = `${item.paneCount} 个窗格 · ${item.documentCount} 个文档`;
      const last = document.createElement('p'); last.className = 'workspace-library-last';
      const date = new Date(item.lastOpenedAt || '');
      last.textContent = Number.isFinite(date.getTime()) ? `最近打开：${new Intl.DateTimeFormat(undefined, {dateStyle:'medium',timeStyle:'short'}).format(date)}` : '尚无打开时间记录';
      const action = document.createElement('a'); action.className = 'workspace-library-open'; action.href = url.href; action.textContent = '打开工作区 · Open workspace';
      card.append(badge, heading, summary, last, action); cards.append(card);
    }
    document.getElementById('workspaceLibraryCount').textContent = entries.length;
    status.textContent = entries.length ? '' : '此浏览器尚无已保存工作区。打开 Open Books 创建工作区。';
    filter();
    window.filterCatalog?.();
  }
  async function refresh() {
    if (refreshing) { again = true; return; }
    refreshing = true; refreshButton.disabled = true;
    try {
      // Upgrade the original single-workspace record without changing its contents.
      await OpenBooksStore.getWorkspace();
      loadError = false;
      entries = (await OpenBooksStore.listWorkspaces()).filter(item => /^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/.test(item.id) && typeof item.name === 'string');
      entries.sort((a,b) => String(b.lastOpenedAt || '').localeCompare(String(a.lastOpenedAt || '')) || a.name.localeCompare(b.name));
      render();
    } catch {
      loadError = true;
      status.textContent = '无法读取此浏览器的工作区。请在 Open Books 中查看；不同浏览器或地址的保存内容可能不同。';
      filter();
    } finally {
      refreshing = false; refreshButton.disabled = false;
      if (again) { again = false; refresh(); }
    }
  }
  const schedule = () => { clearTimeout(timer); timer = setTimeout(refresh, 150); };
  refreshButton.onclick = refresh;
  window.addEventListener('focus', schedule);
  window.addEventListener('pageshow', schedule);
  window.addEventListener('storage', event => { if (event.key === 'open-books-workspaces-changed-v1') schedule(); });
  document.addEventListener('visibilitychange', () => { if (!document.hidden) schedule(); });
  window.ReadingWorkspaceLibrary = {filter, refresh};
  refresh();
})();
