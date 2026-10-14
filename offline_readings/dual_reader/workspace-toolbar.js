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
        preset: 'primary',
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
      root.querySelectorAll('[data-toolgroup]').forEach((group) => {
        const id = group.dataset.toolgroup;
        // Save the user's intent synchronously: delayed native toggle events can race
        // with page-position messages that refresh the active toolbar context.
        group.querySelector('summary').onclick = (event) => {
          event.preventDefault();
          const open = !group.open;
          this.change((config) => {
            config.groups[id].open = open;
          }, this.currentScope());
        };
        group.querySelector('[data-pin]').onclick = () =>
          this.change((config) => {
            config.groups[id].pinned = !config.groups[id].pinned;
            config.groups[id].open = true;
          }, this.currentScope());
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
        const hidden = !root.hidden;
        root.hidden = hidden;
        document.querySelector('#hideTools').textContent = hidden ? 'Show tools' : 'Reading mode';
        document.querySelector('#hideTools').setAttribute('aria-expanded', String(!hidden));
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
        if (!['pdf', 'epub'].includes(key)) throw Error('Invalid file-type preferences.');
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
          group.visible = true;
          group.open =
            preset === 'advanced' ||
            id === 'read' ||
            (preset === 'intermediate' && ['view', 'panes'].includes(id));
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
      this.root.querySelectorAll('[data-toolgroup]').forEach((group) => {
        const setting =
          config.groups?.[group.dataset.toolgroup] || this.defaults.groups[group.dataset.toolgroup];
        group.hidden = !setting.visible;
        group.open = setting.open;
        const pin = group.querySelector('[data-pin]');
        pin.setAttribute('aria-pressed', String(setting.pinned));
        pin.textContent = setting.pinned ? 'Unpin' : 'Pin';
      });
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
    closeUnpinned() {
      this.change((config) => {
        for (const group of Object.values(config.groups)) if (!group.pinned) group.open = false;
      }, this.currentScope());
    }
  }
  window.OpenBooksToolbar = OpenBooksToolbar;
})();
