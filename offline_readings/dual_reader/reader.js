(() => {
  'use strict';
  const $ = (s) => document.querySelector(s),
    store = OpenBooksStore,
    controllers = new Map(),
    documents = new Map(),
    files = new Map(),
    unsavedBooks = new Set();
  const uid = () => crypto.randomUUID(),
    copy = (value) => structuredClone(value),
    leaf = (id) => ({ pane: id });
  let workspace,
    toolbar,
    maximized = null,
    renderedKey = '',
    saveTimer,
    saveQueue = Promise.resolve(),
    ready = false,
    loading = 0,
    noticeTimer,
    libraryGeneration = 0;
  let remember = true;
  try {
    remember = localStorage.getItem('open-books-remember') !== 'false';
  } catch {}
  $('#remember').checked = remember;
  function notice(text) {
    clearTimeout(noticeTimer);
    $('#notice').textContent = text;
    if (text) noticeTimer = setTimeout(() => ($('#notice').textContent = ''), 12000);
  }
  function failed(error) {
    $('#saveStatus').textContent = 'Not saved · export a workspace backup';
    notice(
      error?.message || 'Browser storage is unavailable. Keep this tab open and export a backup.',
    );
    console.warn(error);
  }
  function paneRecord(id = workspace.active) {
    return workspace.panes.find((p) => p.id === id);
  }
  function active() {
    return controllers.get(workspace.active);
  }
  function newPane(documentId = null, view = {}) {
    return {
      id: uid(),
      documentId,
      view: { page: 1, scale: 'page-width', rotation: 0, ...copy(view) },
    };
  }
  function saveSoon() {
    if (!ready) return;
    $('#saveStatus').textContent = 'Saving…';
    clearTimeout(saveTimer);
    saveTimer = setTimeout(flushSave, 300);
  }
  function flushSave() {
    clearTimeout(saveTimer);
    if (!workspace) return Promise.resolve();
    const snapshot = copy(workspace);
    saveQueue = saveQueue
      .catch(() => {})
      .then(() => store.putWorkspace(snapshot))
      .then(() => {
        $('#saveStatus').textContent = unsavedBooks.size
          ? 'Workspace saved · book file not saved'
          : 'Workspace saved on this device';
      })
      .catch(failed);
    return saveQueue;
  }
  function find(node, id) {
    if (node.pane === id) return node;
    if (node.pane) return null;
    return find(node.first, id) || find(node.second, id);
  }
  function replace(node, id, value) {
    if (node.pane === id) return value;
    if (node.pane) return node;
    return {
      ...node,
      first: replace(node.first, id, value),
      second: replace(node.second, id, value),
    };
  }
  function without(node, id) {
    if (node.pane) return node.pane === id ? null : node;
    const first = without(node.first, id),
      second = without(node.second, id);
    return first && second ? { ...node, first, second } : first || second;
  }
  function order(node, result = []) {
    if (node.pane) result.push(node.pane);
    else {
      order(node.first, result);
      order(node.second, result);
    }
    return result;
  }
  function balance(ids, axis) {
    if (ids.length === 1) return leaf(ids[0]);
    const n = Math.ceil(ids.length / 2);
    return {
      axis,
      ratio: n / ids.length,
      first: balance(ids.slice(0, n), axis),
      second: balance(ids.slice(n), axis),
    };
  }
  function minimum(node) {
    if (node.pane) return { width: 280, height: 230 };
    const a = minimum(node.first),
      b = minimum(node.second);
    return node.axis === 'cols'
      ? { width: a.width + b.width + 9, height: Math.max(a.height, b.height) }
      : { width: Math.max(a.width, b.width), height: a.height + b.height + 9 };
  }
  function focused() {
    const size = minimum(workspace.tree),
      host = $('#panes');
    return (
      !!maximized ||
      workspace.layout === 'tabs' ||
      host.clientWidth < size.width ||
      host.clientHeight < size.height
    );
  }
  function build(node) {
    if (node.pane) return controllers.get(node.pane).element;
    const split = document.createElement('div');
    split.className = 'split ' + node.axis;
    const first = document.createElement('div'),
      second = document.createElement('div');
    first.className = second.className = 'slot';
    first.style.flex = `${node.ratio} 1 0`;
    second.style.flex = `${1 - node.ratio} 1 0`;
    first.append(build(node.first));
    second.append(build(node.second));
    const divider = document.createElement('div');
    divider.className = 'divider';
    divider.tabIndex = 0;
    divider.setAttribute('role', 'separator');
    divider.setAttribute('aria-label', node.axis === 'cols' ? 'Resize columns' : 'Resize rows');
    divider.setAttribute('aria-orientation', node.axis === 'cols' ? 'vertical' : 'horizontal');
    const update = (ratio) => {
      node.ratio = Math.max(0.15, Math.min(0.85, ratio));
      first.style.flex = `${node.ratio} 1 0`;
      second.style.flex = `${1 - node.ratio} 1 0`;
      divider.setAttribute('aria-valuenow', String(Math.round(node.ratio * 100)));
    };
    divider.setAttribute('aria-valuemin', '15');
    divider.setAttribute('aria-valuemax', '85');
    update(node.ratio);
    divider.onpointerdown = (event) => {
      event.preventDefault();
      divider.setPointerCapture(event.pointerId);
      document.body.classList.add('resizing');
      const cover = document.createElement('div');
      cover.className = 'drag-cover';
      cover.style.cursor = node.axis === 'cols' ? 'col-resize' : 'row-resize';
      document.body.append(cover);
      const rect = split.getBoundingClientRect();
      const move = (e) =>
        update(
          node.axis === 'cols'
            ? (e.clientX - rect.left) / rect.width
            : (e.clientY - rect.top) / rect.height,
        );
      const finish = () => {
        document.body.classList.remove('resizing');
        cover.remove();
        divider.removeEventListener('pointermove', move);
        divider.removeEventListener('pointerup', finish);
        divider.removeEventListener('pointercancel', finish);
        saveSoon();
      };
      divider.addEventListener('pointermove', move);
      divider.addEventListener('pointerup', finish);
      divider.addEventListener('pointercancel', finish);
    };
    divider.onkeydown = (event) => {
      if (['ArrowLeft', 'ArrowUp', 'ArrowRight', 'ArrowDown', 'Home'].includes(event.key)) {
        event.preventDefault();
        update(
          event.key === 'Home'
            ? 0.5
            : node.ratio + (['ArrowLeft', 'ArrowUp'].includes(event.key) ? -0.05 : 0.05),
        );
        saveSoon();
      }
    };
    split.append(first, divider, second);
    return split;
  }
  async function getFile(id) {
    if (files.has(id)) return files.get(id);
    const record = await store.getDocument(id);
    if (!record) return null;
    const file = store.toFile(record);
    if (file) files.set(id, file);
    return file;
  }
  function syncControllers() {
    for (const [id, c] of controllers)
      if (!workspace.panes.some((p) => p.id === id)) {
        c.destroy();
        controllers.delete(id);
      }
    for (const p of workspace.panes)
      if (!controllers.has(p.id))
        controllers.set(
          p.id,
          new OpenBooksPane(p, {
            activate,
            close: closePane,
            maximize,
            toggle: render,
            open: attach,
            books: showBooks,
            notice,
            changed: (id) => {
              if (id === workspace.active) updateControls();
              saveSoon();
            },
          }),
        );
  }
  function labels() {
    const ids = order(workspace.tree);
    workspace.panes.sort((a, b) => ids.indexOf(a.id) - ids.indexOf(b.id));
    for (const [i, p] of workspace.panes.entries()) {
      const c = controllers.get(p.id),
        doc = documents.get(p.documentId);
      c.label(i, doc);
      c.element.classList.toggle('active', p.id === workspace.active);
    }
  }
  function updateTabs() {
    const tabs = $('#paneTabs');
    tabs.replaceChildren();
    for (const [i, p] of workspace.panes.entries()) {
      const button = document.createElement('button');
      button.type = 'button';
      button.id = 'tab-' + p.id;
      button.setAttribute('role', 'tab');
      button.setAttribute('aria-controls', p.id);
      button.setAttribute('aria-selected', String(p.id === workspace.active));
      button.tabIndex = p.id === workspace.active ? 0 : -1;
      button.textContent = `${i + 1} · ${documents.get(p.documentId)?.name || 'Empty pane'}`;
      button.onclick = () => activate(p.id);
      button.onkeydown = (event) => {
        if (['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) {
          event.preventDefault();
          const index =
            event.key === 'Home'
              ? 0
              : event.key === 'End'
                ? workspace.panes.length - 1
                : (i + (event.key === 'ArrowLeft' ? -1 : 1) + workspace.panes.length) %
                  workspace.panes.length;
          activate(workspace.panes[index].id);
          document.getElementById('tab-' + workspace.active)?.focus();
        }
      };
      tabs.append(button);
    }
  }
  function render(force = false) {
    if (!workspace) return;
    syncControllers();
    labels();
    const focus = focused(),
      visible = focus ? [maximized || workspace.active] : order(workspace.tree),
      key = JSON.stringify({ tree: workspace.tree, visible });
    $('#layoutHint').hidden = !focus || !!maximized || workspace.layout === 'tabs';
    $('#layout').value = workspace.layout || 'custom';
    if (document.activeElement !== $('#workspaceName')) $('#workspaceName').value = workspace.name;
    if (force || key !== renderedKey) {
      renderedKey = key;
      for (const c of controllers.values()) c.unmount();
      $('#panes').replaceChildren();
      if (focus) $('#panes').append(controllers.get(visible[0]).element);
      else $('#panes').append(build(workspace.tree));
      for (const id of visible) {
        const c = controllers.get(id),
          docId = c.record.documentId,
          version = c.generation;
        if (!docId) c.mount(null);
        else
          getFile(docId)
            .then((file) => {
              if (controllers.has(id) && c.generation === version && c.element.isConnected)
                c.mount(file);
            })
            .catch((error) => {
              failed(error);
              if (controllers.get(id) === c && c.element.isConnected) c.mount(null);
            });
      }
    }
    updateTabs();
    updateControls();
  }
  function activate(id) {
    if (!ready || !paneRecord(id)) return;
    if (workspace.active === id) {
      updateControls();
      return;
    }
    workspace.active = id;
    if (maximized) maximized = id;
    render();
    toolbar.setContext(documents.get(paneRecord().documentId)?.format, paneRecord().documentId);
    saveSoon();
  }
  function updateControls() {
    if (!workspace) return;
    const p = paneRecord(),
      c = active(),
      doc = documents.get(p.documentId),
      hasFile = !!c?.file && c.ready;
    $('#activeTarget').textContent =
      `Active: Pane ${workspace.panes.indexOf(p) + 1} · ${doc?.name || 'Empty pane'}`;
    if (document.activeElement !== $('#activePage')) $('#activePage').value = p.view.page || 1;
    $('#activePage').max = c?.total || '';
    $('#positionLabel').textContent = c?.total ? `of ${c.total}` : '';
    $('#pageForm').hidden = doc?.format === 'epub';
    $('#contentsLabel').hidden = doc?.format !== 'epub';
    const toc = $('#activeContents'),
      signature = p.id + ':' + c.contents.length;
    if (toc.dataset.signature !== signature) {
      toc.replaceChildren(...c.contents.map((item) => new Option(item.label, item.href)));
      toc.dataset.signature = signature;
    }
    if (p.view.href) toc.value = p.view.href;
    for (const id of [
      'previous',
      'next',
      'activePage',
      'activeContents',
      'zoom',
      'rotate',
      'fontSize',
    ])
      $('#' + id).disabled = !hasFile;
    // Native file:// PDF viewers do not implement our view-state message protocol.
    if (doc?.format === 'pdf' && location.protocol === 'file:') {
      $('#zoom').disabled = true;
      $('#rotate').disabled = true;
    }
    $('#zoomLabel').hidden = doc?.format === 'epub';
    $('#rotate').hidden = doc?.format !== 'pdf';
    $('#fontLabel').hidden = doc?.format !== 'epub';
    $('#zoom').value = String(p.view.scale || 'page-width');
    $('#fontSize').value = String(p.view.fontSize || 18);
    $('#maximize').textContent = maximized ? 'Restore layout' : 'Maximize pane';
    $('#moveEarlier').disabled = workspace.panes.indexOf(p) === 0;
    $('#moveLater').disabled = workspace.panes.indexOf(p) === workspace.panes.length - 1;
    if (toolbar) toolbar.setContext(doc?.format, p.documentId);
  }
  function addPane(axis = 'cols', duplicate = false) {
    if (!ready) return;
    const old = paneRecord(),
      p = newPane(duplicate ? old.documentId : null, duplicate ? old.view : {});
    workspace.panes.push(p);
    workspace.tree = replace(workspace.tree, old.id, {
      axis,
      ratio: 0.5,
      first: leaf(old.id),
      second: leaf(p.id),
    });
    workspace.active = p.id;
    workspace.layout = 'custom';
    maximized = null;
    render(true);
    saveSoon();
    return p;
  }
  function closePane(id = workspace.active) {
    if (!ready) return;
    const index = workspace.panes.findIndex((p) => p.id === id);
    if (workspace.panes.length === 1) {
      controllers.get(id).destroy();
      controllers.delete(id);
      const p = newPane();
      workspace.panes = [p];
      workspace.tree = leaf(p.id);
      workspace.active = p.id;
    } else {
      workspace.tree = without(workspace.tree, id);
      workspace.panes.splice(index, 1);
      if (workspace.active === id) workspace.active = workspace.panes[Math.max(0, index - 1)].id;
    }
    maximized = null;
    render(true);
    saveSoon();
  }
  function maximize(id = workspace.active) {
    if (!ready) return;
    workspace.active = id;
    maximized = maximized === id ? null : id;
    render();
    saveSoon();
  }
  function move(delta) {
    const ids = order(workspace.tree),
      i = ids.indexOf(workspace.active),
      j = i + delta;
    if (j < 0 || j >= ids.length) return;
    const other = ids[j];
    function swap(node) {
      if (node.pane)
        return leaf(
          node.pane === workspace.active
            ? other
            : node.pane === other
              ? workspace.active
              : node.pane,
        );
      return { ...node, first: swap(node.first), second: swap(node.second) };
    }
    workspace.tree = swap(workspace.tree);
    render(true);
    saveSoon();
  }
  function preset(layout) {
    workspace.layout = layout;
    maximized = null;
    if (layout !== 'tabs' && layout !== 'custom') {
      const ids = workspace.panes.map((p) => p.id),
        count = Math.min(ids.length, layout === 'columns3' ? 3 : 2),
        columns = Array.from({ length: count }, () => []);
      ids.forEach((id, i) => columns[i % count].push(id));
      const subtrees = columns.map((ids) => balance(ids, 'rows'));
      function combine(nodes) {
        if (nodes.length === 1) return nodes[0];
        return {
          axis: 'cols',
          ratio: 1 / nodes.length,
          first: nodes[0],
          second: combine(nodes.slice(1)),
        };
      }
      workspace.tree = combine(subtrees);
    }
    render(true);
    saveSoon();
  }
  async function attach(id, file) {
    if (!ready) return;
    const p = paneRecord(id);
    if (!p) return;
    const ticket = uid();
    p.openTicket = ticket;
    loading++;
    notice('Identifying ' + file.name + '…');
    try {
      const record = await store.identify(file);
      if (paneRecord(id) !== p || p.openTicket !== ticket) return;
      delete p.openTicket;
      const prior = documents.get(record.id);
      if (prior) record.name = prior.name;
      files.set(record.id, file);
      const meta = { ...record };
      delete meta.bytes;
      documents.set(record.id, meta);
      const sameDocument = p.documentId === record.id;
      p.documentId = record.id;
      if (!sameDocument) p.view = { page: 1, scale: 'page-width', rotation: 0 };
      try {
        if (remember) await store.putDocument(record);
        else await store.putDocument(meta);
        unsavedBooks.delete(record.id);
      } catch (error) {
        unsavedBooks.add(record.id);
        failed(error);
      }
      // A user may close this view while its source is being saved.
      if (paneRecord(id) !== p) return;
      workspace.active = id;
      render(true);
      saveSoon();
      notice('Opened ' + record.name);
    } catch (error) {
      notice(error.message);
    } finally {
      loading--;
    }
  }
  async function showBooks() {
    const version = ++libraryGeneration,
      dialog = $('#booksDialog'),
      list = $('#bookList');
    list.replaceChildren();
    if (!dialog.open) dialog.showModal();
    const ids = [...documents.keys()];
    if (!ids.length) {
      list.textContent = 'No saved books yet. Open a PDF or EPUB to begin.';
      return;
    }
    for (const id of ids) {
      const doc = documents.get(id),
        row = document.createElement('div');
      row.className = 'saved-book';
      const title = document.createElement('strong');
      title.textContent = doc.name;
      const info = document.createElement('span');
      info.textContent = doc.format.toUpperCase() + ' · ' + (doc.size / 1048576).toFixed(1) + ' MB';
      const open = document.createElement('button'),
        another = document.createElement('button');
      open.textContent = 'Open in active pane';
      another.textContent = 'Add view';
      const use = async (add) => {
        if (version !== libraryGeneration) return;
        const p = add ? addPane() : paneRecord();
        p.documentId = id;
        p.view = { page: 1, scale: 'page-width', rotation: 0 };
        dialog.close();
        render(true);
        saveSoon();
      };
      open.onclick = () => use(false);
      another.onclick = () => use(true);
      row.append(title, info, open, another);
      list.append(row);
    }
  }
  function base64(bytes) {
    const array = new Uint8Array(bytes),
      chunks = [];
    for (let i = 0; i < array.length; i += 32768)
      chunks.push(String.fromCharCode(...array.subarray(i, i + 32768)));
    return btoa(chunks.join(''));
  }
  function fromBase64(text) {
    const binary = atob(text),
      bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    return bytes.buffer;
  }
  async function exportWorkspace() {
    if (loading) return notice('Wait for the current file to finish opening before exporting.');
    await flushSave();
    const records = [];
    try {
      for (const id of new Set(workspace.panes.map((p) => p.documentId).filter(Boolean))) {
        const meta = documents.get(id),
          record = { ...meta };
        delete record.bytes;
        if ($('#includeFiles').checked) {
          const file = await getFile(id);
          if (!file) throw Error('Reattach ' + meta.name + ' before exporting with book files.');
          record.base64 = base64(await file.arrayBuffer());
        }
        records.push(record);
      }
      const backup = {
        format: 'open-books-workspace',
        version: 1,
        exportedAt: new Date().toISOString(),
        workspace: copy(workspace),
        documents: records,
        toolbar: toolbar.preferences,
        includesFiles: $('#includeFiles').checked,
      };
      const url = URL.createObjectURL(
          new Blob([JSON.stringify(backup)], { type: 'application/json' }),
        ),
        link = document.createElement('a');
      link.href = url;
      link.download = 'open-books-workspace-' + new Date().toISOString().slice(0, 10) + '.json';
      link.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      notice(
        backup.includesFiles
          ? 'Workspace exported with book files.'
          : 'Workspace exported. Original book files are required when restoring on another device.',
      );
    } catch (error) {
      notice(error.message);
    }
  }
  async function importWorkspace(file) {
    if (!file) return;
    if (loading) return notice('Wait for the current book to finish opening before importing.');
    try {
      const backup = JSON.parse(await file.text());
      if (
        backup.format !== 'open-books-workspace' ||
        backup.version !== 1 ||
        !Array.isArray(backup.documents)
      )
        throw Error('Choose an Open Books workspace backup.');
      const next = store.validateWorkspace(backup.workspace),
        preferences = backup.toolbar ? OpenBooksToolbar.validate(backup.toolbar) : null,
        records = [],
        seen = new Set();
      for (const item of backup.documents) {
        if (
          !item ||
          !/^sha256-[a-f0-9]{64}$/.test(item.id) ||
          seen.has(item.id) ||
          typeof item.name !== 'string' ||
          !['pdf', 'epub'].includes(item.format)
        )
          throw Error('Invalid book record.');
        seen.add(item.id);
        let record = {
          id: item.id,
          name: item.name,
          type: typeof item.type === 'string' ? item.type : '',
          format: item.format,
          size: Number(item.size) || 0,
        };
        if (item.base64) {
          const source = new File([fromBase64(item.base64)], record.name, { type: record.type }),
            identified = await store.identify(source);
          if (identified.id !== record.id || identified.format !== record.format)
            throw Error('Backup book contents do not match their identity.');
          record = identified;
        } else {
          const existing = await store.getDocument(item.id);
          if (existing?.bytes) record = existing;
        }
        records.push(record);
      }
      if (next.panes.some((p) => p.documentId && !seen.has(p.documentId)))
        throw Error('Backup is missing a referenced book.');
      if (
        !confirm(
          'Replace the current pane arrangement with this workspace? Saved books will remain in your library.',
        )
      )
        return;
      await flushSave();
      await store.importWorkspace(
        next,
        records.map((record) => {
          if (remember) return record;
          const meta = { ...record };
          delete meta.bytes;
          return meta;
        }),
      );
      for (const record of records) {
        const meta = { ...record };
        delete meta.bytes;
        documents.set(record.id, meta);
        if (record.bytes) files.set(record.id, store.toFile(record));
      }
      for (const c of controllers.values()) c.destroy();
      controllers.clear();
      workspace = next;
      if (preferences) {
        toolbar.preferences = preferences;
        toolbar.persist();
      }
      maximized = null;
      renderedKey = '';
      render(true);
      notice('Workspace restored. Reattach any books not included in the backup.');
      $('#saveStatus').textContent = unsavedBooks.size
        ? 'Workspace saved · book file not saved'
        : 'Workspace saved on this device';
    } catch (error) {
      notice(error.message);
    }
  }
  function wire() {
    toolbar = new OpenBooksToolbar($('#toolbars'), notice);
    $('#configureTools').onclick = () => $('#toolbarDialog').showModal();
    $('#addPane').onclick = () => addPane();
    $('#splitCols').onclick = () => addPane('cols');
    $('#splitRows').onclick = () => addPane('rows');
    $('#duplicate').onclick = () => addPane('cols', true);
    $('#closePane').onclick = () => closePane();
    $('#moveEarlier').onclick = () => move(-1);
    $('#moveLater').onclick = () => move(1);
    $('#maximize').onclick = () => maximize();
    $('#layout').onchange = (e) => preset(e.target.value);
    $('#previous').onclick = () => {
      active().navigate(-1);
      toolbar.closeUnpinned();
    };
    $('#next').onclick = () => {
      active().navigate(1);
      toolbar.closeUnpinned();
    };
    $('#pageForm').onsubmit = (e) => {
      e.preventDefault();
      active().go($('#activePage').value);
    };
    $('#activeContents').onchange = (e) => active().rendition?.display(e.target.value);
    $('#zoom').onchange = (e) => {
      const value = e.target.value;
      active().zoom(Number.isFinite(Number(value)) ? Number(value) : value);
      saveSoon();
    };
    $('#rotate').onclick = () => {
      active().rotate();
      saveSoon();
    };
    $('#fontSize').onchange = (e) => {
      active().setFont(e.target.value);
      saveSoon();
    };
    $('#activeFile').onchange = (e) => {
      const file = e.target.files[0];
      e.target.value = '';
      if (file) attach(workspace.active, file);
    };
    $('#showBooks').onclick = showBooks;
    $('#fullScreen').onclick = async () => {
      try {
        if (document.fullscreenElement) await document.exitFullscreen();
        else await active().element.requestFullscreen();
      } catch {
        notice('Full screen is unavailable in this browser.');
      }
    };
    $('#workspaceName').onchange = (e) => {
      workspace.name = e.target.value.trim() || 'My reading workspace';
      e.target.value = workspace.name;
      saveSoon();
    };
    $('#remember').onchange = async (e) => {
      remember = e.target.checked;
      try {
        localStorage.setItem('open-books-remember', String(remember));
        if (!remember) {
          await store.forgetFiles();
          notice('Saved book bytes cleared. Open views remain available for this session.');
        } else {
          for (const [id, file] of files) {
            const meta = documents.get(id);
            await store.putDocument({ ...meta, bytes: await file.arrayBuffer() });
          }
          notice('Open book files saved on this device.');
        }
      } catch (error) {
        failed(error);
      }
    };
    $('#exportWorkspace').onclick = exportWorkspace;
    $('#importWorkspace').onchange = (e) => {
      const file = e.target.files[0];
      e.target.value = '';
      importWorkspace(file);
    };
    window.addEventListener('resize', () => {
      if (ready) render();
    });
    new ResizeObserver(() => {
      if (ready) render();
    }).observe($('#panes'));
    window.addEventListener('pagehide', () => flushSave());
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) flushSave();
    });
  }
  async function initialize() {
    try {
      for (const record of await store.listDocuments()) {
        const meta = { ...record };
        delete meta.bytes;
        documents.set(record.id, meta);
      }
      const saved = await store.getWorkspace();
      if (saved) workspace = store.validateWorkspace(saved);
      else {
        const panes = [newPane(), newPane()];
        workspace = {
          version: 1,
          name: 'My reading workspace',
          panes,
          active: panes[0].id,
          tree: { axis: 'cols', ratio: 0.5, first: leaf(panes[0].id), second: leaf(panes[1].id) },
          layout: 'custom',
        };
        if (remember)
          for (const [i, key] of ['left', 'right'].entries()) {
            const old = await store.getLegacy(key),
              file = old instanceof File ? old : store.toFile(old);
            if (file) {
              const record = await store.identify(file);
              await store.putDocument(record);
              const meta = { ...record };
              delete meta.bytes;
              documents.set(record.id, meta);
              files.set(record.id, file);
              panes[i].documentId = record.id;
            }
          }
      }
    } catch (error) {
      failed(error);
      const p = newPane();
      workspace = {
        version: 1,
        name: 'My reading workspace',
        panes: [p],
        active: p.id,
        tree: leaf(p.id),
        layout: 'custom',
      };
    }
    wire();
    ready = true;
    render(true);
    saveSoon();
    cacheOffline();
  }
  async function cacheOffline() {
    if (location.protocol === 'file:' || !('serviceWorker' in navigator)) return;
    navigator.serviceWorker.addEventListener('message', (event) => {
      if (event.data?.type === 'ARTICLE_CACHED')
        $('#offlineStatus').textContent = 'Available offline';
      if (event.data?.type === 'CACHE_ERROR')
        $('#offlineStatus').textContent = 'Offline setup incomplete';
    });
    try {
      await navigator.serviceWorker.register(new URL('../../service-worker.js', location.href), {
        scope: new URL('../../', location.href).pathname,
        updateViaCache: 'none',
      });
      const registration = await navigator.serviceWorker.ready;
      const response = await fetch('../../vendor/pdfjs/assets.json');
      if (!response.ok) throw Error();
      const assets = await response.json(),
        paths = [
          'editor.html',
          location.pathname + location.search,
          'reader.css?v=workspace-1',
          'reader.js?v=workspace-1',
          'reader-pane.js?v=workspace-1',
          'workspace-store.js?v=workspace-1',
          'workspace-toolbar.js?v=workspace-1',
          'pdf-viewer.html?v=workspace-1',
          'pdf-viewer.js?v=workspace-1',
          '../../vendor/jszip/jszip.min.js',
          '../../vendor/epubjs/epub.min.js',
          '../../vendor/pdfjs/assets.json',
          ...assets.map((path) => '../../vendor/pdfjs/' + path),
        ];
      registration.active?.postMessage({
        type: 'CACHE_ARTICLE',
        urls: [...new Set(paths.map((path) => new URL(path, location.href).href))],
      });
    } catch {
      $('#offlineStatus').textContent = 'Offline setup unavailable';
    }
  }
  initialize();
})();
