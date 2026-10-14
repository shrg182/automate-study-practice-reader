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
        } else if (d?.type === 'PDF_LOCATION' && d.session === this.session) {
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
        if (
          this.rendition?.manager?.isRendered() &&
          this.rendition.location &&
          this.q('.epub').clientWidth
        )
          this.rendition.resize(this.q('.epub').clientWidth, this.q('.epub').clientHeight);
      });
      this.observer.observe(this.q('.epub'));
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
      this.mounted = false;
      this.ready = false;
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
          : 'Open a PDF or EPUB';
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
          } else this.q('.pdf').src = 'pdf-viewer.html?v=workspace-2';
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
      if (this.document?.format === 'epub') this.rendition?.[delta < 0 ? 'prev' : 'next']();
      else this.go((this.record.view.page || 1) + delta);
    }
    zoom(scale) {
      this.record.view.scale = scale;
      this.send({ type: 'PDF_VIEW', view: { scale } });
    }
    rotate() {
      this.record.view.rotation = ((this.record.view.rotation || 0) + 90) % 360;
      this.send({ type: 'PDF_VIEW', view: { rotation: this.record.view.rotation } });
    }
    setFont(size) {
      this.record.view.fontSize = Number(size);
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
