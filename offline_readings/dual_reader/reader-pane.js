/* One view controller per pane. Hidden views release their rendering resources. */
(() => {
  'use strict';
  class OpenBooksPane {
    constructor(record, callbacks) {
      this.record = record;
      this.callbacks = callbacks;
      this.element = document
        .querySelector('#paneTemplate')
        .content.firstElementChild.cloneNode(true);
      this.element.id = record.id;
      this.element.setAttribute('aria-labelledby', 'tab-' + record.id);
      this.q = (s) => this.element.querySelector(s);
      this.generation = 0;
      this.mounted = false;
      this.ready = false;
      this.contents = [];
      this.speechRequests = new Map();
      this.disposeDrag = callbacks.drag(this.q('.paneDrag'), record.id);
      this.q('.activate').onclick = () => callbacks.activate(record.id);
      this.element.addEventListener('pointerdown', () => callbacks.activate(record.id));
      this.element.addEventListener('focusin', () => callbacks.activate(record.id, 'focus'));
      this.q('.paneMax').onclick = () => callbacks.maximize(record.id);
      this.q('.paneClose').onclick = () => callbacks.close(record.id);
      this.q('.paneFile').onchange = (e) => {
        const file = e.target.files[0];
        e.target.value = '';
        if (file) callbacks.open(record.id, file);
      };
      this.q('.paneBooks').onclick = () => {
        callbacks.activate(record.id);
        callbacks.books();
      };
      this.message = (e) => {
        if (
          e.source !== this.q('.pdf').contentWindow ||
          e.origin !== location.origin ||
          !this.mounted
        )
          return;
        const d = e.data;
        if (d?.type === 'PDF_READY') {
          this.send({
            type: 'OPEN_PDF',
            file: this.file,
            view: this.record.view,
            session: this.session,
          });
        } else if (d?.type === 'PDF_READ_TEXT' && d.session === this.session) {
          this.speechRequests.get(d.requestId)?.(d);
        } else if (d?.type === 'PDF_LOCATION'  && d.session === this.session) {
          this.ready = true;
          Object.assign(this.record.view, d.view || { page: d.page });
          this.total = d.total;
          this.q('.status').textContent = `Page ${d.page} of ${d.total}`;
          callbacks.changed(record.id);
        } else if (d?.type === 'PDF_FOCUS' && d.session === this.session)
          callbacks.activate(record.id, d.intent || 'focus');
        else if (d?.type === 'PDF_ERROR' && d.session === this.session) {
          this.q('.status').textContent = d.message;
          callbacks.notice(d.message);
        }
      };
      window.addEventListener('message', this.message);
      this.observer = new ResizeObserver(() => {
        if (this.document?.format === 'image' && this.ready) this.renderImage();
        if (
          this.rendition?.manager?.isRendered() &&
          this.rendition.location &&
          this.q('.epub').clientWidth
        )
          this.rendition.resize(this.q('.epub').clientWidth, this.q('.epub').clientHeight);
      });
      this.observer.observe(this.q('.epub'));
      this.observer.observe(this.q('.image-view'));
      this.q('.text-reader').addEventListener('scroll', () => {
        if (!this.ready) return;
        const host = this.q('.text-reader');
        this.record.view.textOffset = host.scrollTop / Math.max(1, host.scrollHeight - host.clientHeight);
        clearTimeout(this.textTimer);
        this.textTimer = setTimeout(() => { if (this.ready) this.callbacks.changed(this.record.id); }, 150);
      });
    }
    send(data) {
      this.q('.pdf').contentWindow?.postMessage(data, location.origin);
    }
    label(index, document) {
      this.index = index;
      this.document = document;
      this.q('.activate').textContent = `${index + 1} · ${document?.name || 'Empty pane'}`;
      this.q('.pdf').title = `Pane ${index + 1} · ${document?.name || 'PDF'}`;
    }
    unmount() {
      ++this.generation;
      clearTimeout(this.textTimer);
      for (const resolve of this.speechRequests.values()) resolve({error: 'The document was closed.'});
      this.speechRequests.clear();
      this.mounted = false;
      this.ready = false;
      // epub.js does not cancel its queued start when destroy() clears book.
      // Stop those queues before disposal, including views closed during startup.
      this.rendition?.q?.stop();
      this.rendition?.manager?.q?.stop();
      this.rendition?.destroy();
      const oldBook = this.book;
      if (oldBook) {
        oldBook.opened
          .then(() => oldBook.loaded.navigation)
          .then(
            () => oldBook.destroy(),
            () => oldBook.destroy(),
          )
          .catch(() => {});
      }
      this.rendition = this.book = null;
      if (this.url) URL.revokeObjectURL(this.url);
      this.url = null;
      this.q('.pdf').removeAttribute('src');
      this.q('.pdf').hidden = true;
      this.q('.epub').replaceChildren();
      this.q('.epub').hidden = true;
      this.q('.text-reader').replaceChildren();
      this.q('.text-reader').hidden = true;
      this.q('.image-view img').removeAttribute('src');
      this.q('.image-view').hidden = true;
      this.q('.empty').hidden = false;
      this.file = null;
    }
    destroy() {
      this.disposeDrag();
      this.unmount();
      this.observer.disconnect();
      window.removeEventListener('message', this.message);
      this.element.remove();
    }
    async mount(file) {
      if (this.mounted) return;
      this.mounted = true;
      const version = ++this.generation;
      this.file = file;
      this.session = crypto.randomUUID();
      this.contents = [];
      this.total = undefined;
      if (!file) {
        this.q('.empty strong').textContent = this.record.documentId
          ? 'Reattach this book'
          : 'Open a document or image';
        this.q('.empty p').textContent = this.record.documentId
          ? 'Choose the original file to restore this view.'
          : 'Choose a file, or reopen a saved book.';
        this.q('.status').textContent = this.record.documentId
          ? 'Book file is not stored in this browser'
          : 'No book attached';
        return;
      }
      this.q('.empty').hidden = true;
      this.q('.status').textContent = 'Opening book…';
      const view = this.record.view;
      try {
        if (this.document.format === 'pdf') {
          this.q('.pdf').hidden = false;
          if (location.protocol === 'file:') {
            this.url = URL.createObjectURL(file);
            this.q('.pdf').src = this.url + `#page=${view.page || 1}&view=FitH`;
            this.q('.status').textContent =
              'Native PDF view · use the hosted reader for workspace zoom controls';
            this.ready = true;
            this.callbacks.changed(this.record.id);
          } else this.q('.pdf').src = 'pdf-viewer.html?v=reader-1.28.19';
          return;
        }
        if (['text', 'markdown'].includes(this.document.format)) {
          const text = await file.text();
          if (version !== this.generation) return;
          const host = this.q('.text-reader');
          if (this.document.format === 'markdown') host.replaceChildren(OpenBooksContent.markdown(text));
          else { const pre = document.createElement('pre'); pre.textContent = text; host.replaceChildren(pre); }
          host.hidden = false;
          this.setFont(view.fontSize || 18);
          host.scrollTop = (view.textOffset || 0) * Math.max(0, host.scrollHeight - host.clientHeight);
          this.ready = true;
          this.q('.status').textContent = this.document.format === 'markdown' ? 'Markdown · reading view' : 'Text document · UTF-8';
          this.callbacks.changed(this.record.id);
          return;
        }
        if (this.document.format === 'image') {
          const image = this.q('.image-view img');
          this.url = URL.createObjectURL(file);
          this.q('.image-view').hidden = false;
          image.alt = file.name;
          await new Promise((resolve, reject) => {
            image.onload = resolve;
            image.onerror = () => reject(Error('Could not decode this image.'));
            image.src = this.url;
          });
          if (version !== this.generation) return;
          this.ready = true; this.renderImage();
          this.q('.status').textContent = `Image · ${image.naturalWidth} × ${image.naturalHeight}`;
          this.callbacks.changed(this.record.id);
          return;
        }
        this.q('.epub').hidden = false;
        const bytes = await file.arrayBuffer();
        if (version !== this.generation) return;
        const book = ePub();
        this.book = book;
        await book.open(bytes, 'binary');
        if (version !== this.generation) return;
        const navigation = await book.loaded.navigation;
        if (version !== this.generation) return;
        const add = (items, depth = 0) => {
          for (const item of items) {
            this.contents.push({ label: '  '.repeat(depth) + item.label.trim(), href: item.href });
            add(item.subitems || [], depth + 1);
          }
        };
        add(navigation.toc || []);
        for (const [i, section] of book.spine.spineItems.entries())
          if (!this.contents.some((item) => item.href === section.href))
            this.contents.push({ label: `Section ${i + 1}`, href: section.href });
        this.total = book.spine.spineItems.length;
        const rendition = book.renderTo(this.q('.epub'), {
          width: '100%',
          height: '100%',
          manager: 'continuous',
          flow: 'scrolled',
          spread: 'none',
        });
        this.rendition = rendition;
        this.setFont(view.fontSize || 18);
        rendition.hooks.content.register((content) => {
          content.document.addEventListener('pointerdown', () =>
            this.callbacks.activate(this.record.id, 'pointer'),
          );
          content.document.addEventListener('focusin', () =>
            this.callbacks.activate(this.record.id, 'focus'),
          );
          content.document.addEventListener('keydown', () =>
            this.callbacks.activate(this.record.id, 'keyboard'),
          );
        });
        rendition.on('relocated', (where) => {
          if (version !== this.generation) return;
          this.ready = true;
          view.cfi = where.start.cfi;
          view.page = where.start.index + 1;
          view.href = book.spine.get(where.start.index)?.href;
          this.q('.status').textContent = `Section ${view.page} of ${this.total}`;
          this.callbacks.changed(this.record.id);
        });
        try {
          await rendition.display(view.cfi || undefined);
        } catch {
          if (version !== this.generation) return;
          await rendition.display();
        }
        if (version !== this.generation) return;
        this.callbacks.changed(this.record.id);
      } catch (error) {
        if (version !== this.generation) return;
        this.q('.empty').hidden = false;
        this.q('.status').textContent = 'Could not open this book. Reattach a valid file.';
        this.callbacks.notice('Could not open ' + file.name);
        console.warn(error);
      }
    }
    go(page) {
      if (!this.file) return;
      const n = Math.max(1, Math.min(this.total || Number.MAX_SAFE_INTEGER, Number(page) || 1));
      this.record.view.page = n;
      if (this.document.format === 'epub') {
        const section = this.book?.spine.get(n - 1);
        if (section) this.rendition?.display(section.href);
      } else if (location.protocol === 'file:') {
        this.q('.pdf').src = this.url + `#page=${n}&view=FitH`;
        this.callbacks.changed(this.record.id);
      } else this.send({ type: 'PDF_PAGE', page: n });
    }
    navigate(delta) {
      if (['text', 'markdown'].includes(this.document?.format)) { this.q('.text-reader').scrollTop += delta * this.q('.text-reader').clientHeight * 0.8; return; }
      if (this.document?.format === 'image') return;
      if (this.document?.format === 'epub') this.rendition?.[delta < 0 ? 'prev' : 'next']();
      else this.go((this.record.view.page || 1) + delta);
    }
    zoom(scale) {
      this.record.view.scale = scale;
      if (this.document?.format === 'image') this.renderImage();
      else this.send({ type: 'PDF_VIEW', view: { scale } });
    }
    rotate() {
      this.record.view.rotation = ((this.record.view.rotation || 0) + 90) % 360;
      if (this.document?.format === 'image') this.renderImage();
      else this.send({ type: 'PDF_VIEW', view: { rotation: this.record.view.rotation } });
    }
    renderImage() {
      const host = this.q('.image-view'), image = this.q('.image-view img'), stage = this.q('.image-stage');
      if (!image.naturalWidth || !host.clientWidth) return;
      const rotation = this.record.view.rotation || 0, swapped = rotation % 180 !== 0;
      const w = swapped ? image.naturalHeight : image.naturalWidth, h = swapped ? image.naturalWidth : image.naturalHeight;
      const setting = this.record.view.scale || 'page-fit';
      const scale = Number.isFinite(Number(setting)) ? Number(setting) : setting === 'page-actual' ? 1 : setting === 'page-width' ? host.clientWidth / w : Math.min(host.clientWidth / w, host.clientHeight / h);
      stage.style.width = w * scale + 'px'; stage.style.height = h * scale + 'px';
      image.style.width = image.naturalWidth * scale + 'px'; image.style.height = image.naturalHeight * scale + 'px';
      image.style.transform = `translate(-50%, -50%) rotate(${rotation}deg)`;
    }
    async readableText() {
      if (['text', 'markdown'].includes(this.document?.format)) return this.q('.text-reader').innerText;
      if (this.document?.format === 'epub') {
        const current = this.rendition?.getContents().find(content => content.sectionIndex === (this.record.view.page || 1) - 1) || this.rendition?.getContents()[0];
        return current?.document?.body?.innerText || '';
      }
      if (this.document?.format === 'pdf' && location.protocol !== 'file:') {
        const requestId = crypto.randomUUID();
        return new Promise((resolve, reject) => {
          const timer = setTimeout(() => { this.speechRequests.delete(requestId); reject(Error('PDF text is not ready. Try again.')); }, 15000);
          this.speechRequests.set(requestId, result => {
            clearTimeout(timer); this.speechRequests.delete(requestId);
            if (result.error) reject(Error(result.error)); else resolve(result.text || '');
          });
          this.send({type: 'PDF_READ_TEXT', requestId, session: this.session});
        });
      }
      return '';
    }
    setFont(size) {
      this.record.view.fontSize = Number(size);
      this.q('.text-reader').style.fontSize = size + 'px';
      this.rendition?.themes.default({
        body: {
          'font-size': size + 'px',
          'line-height': '1.6',
          padding: '20px',
          color: '#24241f',
          background: '#fff',
        },
        img: { 'max-width': '100%' },
      });
    }
  }
  window.OpenBooksPane = OpenBooksPane;
})();
