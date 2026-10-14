/* Versioned, device-local records. Documents are independent of their views. */
(() => {
  'use strict';
  const clone = (value) => structuredClone(value);
  function database() {
    return new Promise((resolve, reject) => {
      const r = indexedDB.open('open-books-offline', 2);
      r.onupgradeneeded = () => {
        for (const name of ['books', 'documents', 'workspaces'])
          if (!r.result.objectStoreNames.contains(name)) r.result.createObjectStore(name);
      };
      r.onsuccess = () => resolve(r.result);
      r.onerror = () => reject(r.error);
      r.onblocked = () =>
        reject(Error('Close other Open Books tabs, then reload to update storage.'));
    });
  }
  async function transaction(name, mode, operation) {
    const db = await database();
    try {
      return await new Promise((resolve, reject) => {
        const tx = db.transaction(name, mode),
          r = operation(tx.objectStore(name));
        tx.oncomplete = () => resolve(r?.result);
        tx.onerror = () => reject(tx.error);
        tx.onabort = () => reject(tx.error);
      });
    } finally {
      db.close();
    }
  }
  function format(file) {
    const name = file.name.toLowerCase();
    return name.endsWith('.pdf') ? 'pdf' : name.endsWith('.epub') ? 'epub' : null;
  }
  async function identify(file) {
    if (!format(file)) throw Error('Choose a PDF or EPUB file.');
    if (!crypto.subtle)
      throw Error(
        'Open the reader through HTTPS or the local reader service to identify and save books.',
      );
    const bytes = await file.arrayBuffer(),
      hash = await crypto.subtle.digest('SHA-256', bytes);
    return {
      id:
        'sha256-' + [...new Uint8Array(hash)].map((n) => n.toString(16).padStart(2, '0')).join(''),
      name: file.name,
      type: file.type,
      format: format(file),
      size: file.size,
      bytes,
    };
  }
  function toFile(record) {
    return record?.bytes ? new File([record.bytes], record.name, { type: record.type }) : null;
  }
  function validateWorkspace(value) {
    if (!value || value.version !== 1 || !Array.isArray(value.panes) || !value.panes.length)
      throw Error('Invalid workspace.');
    if (
      value.canvas !== undefined &&
      (!value.canvas ||
        !['fit', 'scroll'].includes(value.canvas.mode) ||
        !Number.isInteger(value.canvas.minHeight) ||
        value.canvas.minHeight < 240 ||
        value.canvas.minHeight > 1200 ||
        !Number.isInteger(value.canvas.minWidth) ||
        value.canvas.minWidth < 240 ||
        value.canvas.minWidth > 800)
    )
      throw Error('Invalid workspace dimensions.');
    const ids = new Set();
    for (const p of value.panes) {
      if (
        !p ||
        typeof p.id !== 'string' ||
        !/^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/.test(p.id) ||
        ids.has(p.id) ||
        !p.view ||
        (p.documentId !== null && !/^sha256-[a-f0-9]{64}$/.test(p.documentId))
      )
        throw Error('Invalid pane record.');
      ids.add(p.id);
      if (p.view.page !== undefined && (!Number.isInteger(p.view.page) || p.view.page < 1))
        throw Error('Invalid page position.');
      if (p.view.rotation !== undefined && ![0, 90, 180, 270].includes(p.view.rotation))
        throw Error('Invalid rotation.');
      if (
        p.view.fontSize !== undefined &&
        (!Number.isFinite(p.view.fontSize) || p.view.fontSize < 10 || p.view.fontSize > 72)
      )
        throw Error('Invalid EPUB text size.');
      if (
        p.view.scale !== undefined &&
        !(typeof p.view.scale === 'number' && p.view.scale >= 0.1 && p.view.scale <= 10) &&
        !['page-width', 'page-fit', 'auto', 'page-actual'].includes(p.view.scale)
      )
        throw Error('Invalid zoom.');
      if (p.view.cfi !== undefined && (typeof p.view.cfi !== 'string' || p.view.cfi.length > 10000))
        throw Error('Invalid EPUB location.');
    }
    const leaves = new Set();
    function visit(node, depth = 0) {
      if (!node || depth > 100) throw Error('Invalid pane layout.');
      if (node.height !== undefined && (!Number.isFinite(node.height) || node.height < 0))
        throw Error('Invalid pane height.');
      if (node.pane) {
        if (!ids.has(node.pane) || leaves.has(node.pane)) throw Error('Invalid pane layout.');
        leaves.add(node.pane);
        return;
      }
      if (
        !['cols', 'rows'].includes(node.axis) ||
        !Number.isFinite(node.ratio) ||
        node.ratio < 0.1 ||
        node.ratio > 0.9
      )
        throw Error('Invalid split.');
      visit(node.first, depth + 1);
      visit(node.second, depth + 1);
    }
    visit(value.tree);
    if (leaves.size !== ids.size || !ids.has(value.active)) throw Error('Invalid active pane.');
    if (typeof value.name !== 'string') throw Error('Invalid workspace name.');
    return clone(value);
  }
  window.OpenBooksStore = {
    identify,
    toFile,
    format,
    validateWorkspace,
    getDocument: (id) => transaction('documents', 'readonly', (s) => s.get(id)),
    putDocument: (record) => transaction('documents', 'readwrite', (s) => s.put(record, record.id)),
    async listDocuments() {
      const db = await database();
      try {
        return await new Promise((resolve, reject) => {
          const tx = db.transaction('documents'),
            r = tx.objectStore('documents').openCursor(),
            records = [];
          r.onsuccess = () => {
            const cursor = r.result;
            if (cursor) {
              const value = cursor.value;
              delete value.bytes;
              records.push(value);
              cursor.continue();
            }
          };
          tx.oncomplete = () => resolve(records);
          tx.onerror = () => reject(tx.error);
          tx.onabort = () => reject(tx.error);
        });
      } finally {
        db.close();
      }
    },
    getWorkspace: () => transaction('workspaces', 'readonly', (s) => s.get('current')),
    putWorkspace: (value) =>
      transaction('workspaces', 'readwrite', (s) => s.put(clone(value), 'current')),
    getLegacy: (key) => transaction('books', 'readonly', (s) => s.get(key)),
    async forgetFiles() {
      const db = await database();
      try {
        await new Promise((resolve, reject) => {
          const tx = db.transaction(['documents', 'books'], 'readwrite'),
            store = tx.objectStore('documents'),
            cursor = store.openCursor();
          cursor.onsuccess = () => {
            const c = cursor.result;
            if (c) {
              const value = c.value;
              delete value.bytes;
              c.update(value);
              c.continue();
            }
          };
          tx.objectStore('books').clear();
          tx.oncomplete = resolve;
          tx.onerror = () => reject(tx.error);
          tx.onabort = () => reject(tx.error);
        });
      } finally {
        db.close();
      }
    },
    async importWorkspace(workspace, records) {
      const db = await database();
      try {
        await new Promise((resolve, reject) => {
          const tx = db.transaction(['documents', 'workspaces'], 'readwrite'),
            store = tx.objectStore('documents');
          for (const record of records) store.put(record, record.id);
          tx.objectStore('workspaces').put(clone(workspace), 'current');
          tx.oncomplete = resolve;
          tx.onerror = () => reject(tx.error);
          tx.onabort = () => reject(tx.error);
        });
      } finally {
        db.close();
      }
    },
  };
})();
