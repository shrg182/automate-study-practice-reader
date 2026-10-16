/* Shared functional toolbar groups; document-type adapters supply the actions. */
(() => {
  'use strict';
  class OpenBooksToolbar {
    constructor(root, onError) {
      this.root = root;
      this.onError = onError;
      this.context = { format: null, documentId: null };
      this.key = 'open-books-toolbar-v1';
      this.defaults = {
        preset: 'advanced',
        groups: {
          read: { visible: true, open: true, pinned: true },
          view: { visible: true, open: false, pinned: false },
          panes: { visible: true, open: false, pinned: false },
          save: { visible: true, open: false, pinned: false },
        },
      };
      try {
        this.preferences = JSON.parse(localStorage.getItem(this.key)) || {
          version: 1,
          library: this.defaults,
          formats: {},
          documents: {},
        };
        this.preferences = OpenBooksToolbar.validate(this.preferences);
      } catch {
        this.preferences = { version: 1, library: this.defaults, formats: {}, documents: {} };
      }
      this.preferences.formats ||= {};
      this.preferences.documents ||= {};
      this.scope = 'library';
      this.applying = false;
      this.ribbonKey = 'open-books-ribbon-v1';
      try { this.ribbon = JSON.parse(localStorage.getItem(this.ribbonKey)) || {}; }
      catch { this.ribbon = {}; }
      this.selected = ['read', 'view', 'panes', 'save'].includes(this.ribbon.selected) ? this.ribbon.selected : 'read';
      this.keepOpen = this.ribbon.keepOpen !== false;
      this.expanded = this.keepOpen && this.ribbon.expanded !== false;
      this.tabs = [...document.querySelectorAll('[data-ribbon-tab]')];
      for (const tab of this.tabs) {
        tab.onclick = () => {
          this.selected = tab.dataset.ribbonTab;
          this.expanded = true;
          this.apply();
          this.saveRibbon();
        };
        tab.onkeydown = (event) => {
          const tabs = this.tabs.filter(item => !item.hidden);
          const index = tabs.indexOf(tab);
          let next;
          if (event.key === 'ArrowRight') next = tabs[(index + 1) % tabs.length];
          if (event.key === 'ArrowLeft') next = tabs[(index + tabs.length - 1) % tabs.length];
          if (event.key === 'Home') next = tabs[0];
          if (event.key === 'End') next = tabs[tabs.length - 1];
          if (next) { event.preventDefault(); next.click(); next.focus(); }
          if (event.key === 'Escape') this.collapse();
        };
      }
      document.querySelector('#keepRibbon').onchange = (event) => {
        this.keepOpen = event.target.checked;
        this.expanded = this.keepOpen;
        this.apply();
        this.saveRibbon();
      };
      document.addEventListener('click', (event) => {
        if (!this.keepOpen && this.expanded && !event.target.closest('#toolbars, .ribbon-tabs, #hideTools, #toolbarDialog, #configureTools')) this.collapse();
      });
      root.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
          this.collapse();
          this.tabs.find(tab => tab.dataset.ribbonTab === this.selected)?.focus();
        }
      });
      document.querySelectorAll('[data-group-choice]').forEach(
        (input) =>
          (input.onchange = () =>
            this.change((config) => {
              config.groups[input.dataset.groupChoice].visible = input.checked;
            })),
      );
      document.querySelector('#toolbarScope').onchange = (event) => {
        this.scope = event.target.value;
        this.apply();
      };
      document.querySelector('#toolPreset').onchange = (event) =>
        this.setPreset(event.target.value);
      document.querySelector('#resetTools').onclick = () => {
        if (this.scope === 'document' && this.context.documentId)
          delete this.preferences.documents[this.context.documentId];
        else if (this.scope === 'format' && this.context.format)
          delete this.preferences.formats[this.context.format];
        else this.preferences.library = structuredClone(this.defaults);
        this.persist();
        this.apply();
      };
      document.querySelector('#hideTools').onclick = () => {
        this.expanded = !this.expanded;
        this.apply();
        this.saveRibbon();
      };
      this.apply();
    }
    static validate(value) {
      if (value?.version !== 1) throw Error('Invalid toolbar preferences.');
      function config(input) {
        if (
          !input ||
          !['primary', 'intermediate', 'advanced'].includes(input.preset) ||
          !input.groups
        )
          throw Error('Invalid toolbar preset.');
        const groups = {};
        for (const id of ['read', 'view', 'panes', 'save']) {
          const g = input.groups[id];
          if (!g || ['visible', 'open', 'pinned'].some((k) => typeof g[k] !== 'boolean'))
            throw Error('Invalid toolbar group.');
          groups[id] = { visible: g.visible, open: g.open, pinned: g.pinned };
        }
        return { preset: input.preset, groups };
      }
      const result = { version: 1, library: config(value.library), formats: {}, documents: {} };
      for (const [key, item] of Object.entries(value.formats || {})) {
        if (!['pdf', 'epub', 'text', 'markdown', 'html', 'image'].includes(key)) throw Error('Invalid file-type preferences.');
        result.formats[key] = config(item);
      }
      for (const [key, item] of Object.entries(value.documents || {})) {
        if (!/^sha256-[a-f0-9]{64}$/.test(key)) throw Error('Invalid book preferences.');
        result.documents[key] = config(item);
      }
      return result;
    }
    effective() {
      return (
        this.preferences.documents[this.context.documentId] ||
        this.preferences.formats[this.context.format] ||
        this.preferences.library ||
        this.defaults
      );
    }
    currentScope() {
      if (this.preferences.documents[this.context.documentId]) return 'document';
      if (this.preferences.formats[this.context.format]) return 'format';
      return 'library';
    }
    scoped(scope = this.scope) {
      if (scope === 'document' && this.context.documentId)
        return this.preferences.documents[this.context.documentId] || this.effective();
      if (scope === 'format' && this.context.format)
        return this.preferences.formats[this.context.format] || this.preferences.library;
      return this.preferences.library;
    }
    change(edit, scope = this.scope) {
      const config = structuredClone(this.scoped(scope));
      config.groups = { ...structuredClone(this.defaults.groups), ...config.groups };
      edit(config);
      if (scope === 'document' && this.context.documentId)
        this.preferences.documents[this.context.documentId] = config;
      else if (scope === 'format' && this.context.format)
        this.preferences.formats[this.context.format] = config;
      else this.preferences.library = config;
      this.persist();
      this.apply();
    }
    setPreset(preset) {
      this.change((config) => {
        config.preset = preset;
        for (const [id, group] of Object.entries(config.groups)) {
          group.visible = preset === 'advanced' || id === 'read' || id === 'view' || (preset === 'intermediate' && id === 'panes');
          // Retain legacy fields so existing preferences and backups stay valid.
          group.open = id === 'read';
          group.pinned = id === 'read';
        }
      });
    }
    persist() {
      try {
        localStorage.setItem(this.key, JSON.stringify(this.preferences));
      } catch {
        this.onError('Toolbar settings could not be saved in this browser.');
      }
    }
    setContext(format, documentId) {
      this.context = { format, documentId };
      const scope = document.querySelector('#toolbarScope');
      scope.querySelector('[value=format]').disabled = !format;
      scope.querySelector('[value=document]').disabled = !documentId;
      if ((this.scope === 'document' && !documentId) || (this.scope === 'format' && !format)) {
        this.scope = 'library';
        scope.value = 'library';
      }
      this.apply();
    }
    apply() {
      this.applying = true;
      const config = this.effective();
      const visible = this.tabs.filter(tab => config.groups[tab.dataset.ribbonTab].visible);
      if (!visible.some(tab => tab.dataset.ribbonTab === this.selected)) this.selected = visible[0]?.dataset.ribbonTab || null;
      for (const tab of this.tabs) {
        const id = tab.dataset.ribbonTab;
        tab.hidden = !config.groups[id].visible;
        tab.setAttribute('aria-selected', String(id === this.selected));
        tab.tabIndex = id === this.selected ? 0 : -1;
      }
      this.root.hidden = !this.expanded || !visible.length;
      this.root.querySelectorAll('[data-toolgroup]').forEach(group => {
        group.hidden = group.dataset.toolgroup !== this.selected;
      });
      document.querySelector('#keepRibbon').checked = this.keepOpen;
      const toggle = document.querySelector('#hideTools');
      toggle.textContent = this.root.hidden ? 'Show ribbon' : 'Collapse ribbon';
      toggle.setAttribute('aria-expanded', String(!this.root.hidden));
      const scoped = this.scoped();
      document
        .querySelectorAll('[data-group-choice]')
        .forEach(
          (input) =>
            (input.checked = scoped.groups?.[input.dataset.groupChoice]?.visible !== false),
        );
      document.querySelector('#toolPreset').value = scoped.preset || 'primary';
      this.applying = false;
    }
    saveRibbon() {
      try { localStorage.setItem(this.ribbonKey, JSON.stringify({selected: this.selected, keepOpen: this.keepOpen, expanded: this.expanded})); }
      catch { this.onError('Ribbon settings could not be saved in this browser.'); }
    }
    collapse() {
      this.expanded = false;
      this.apply();
      this.saveRibbon();
    }
    closeUnpinned() {
      if (!this.keepOpen) this.collapse();
    }
  }
  window.OpenBooksToolbar = OpenBooksToolbar;
})();
