/* Dedicated pointer handles keep document selection and annotation gestures independent. */
(() => {
  'use strict';
  function install(handle, options) {
    let cancel = () => {};
    const down = (event) => {
      if (event.button !== 0 || !options.allowed()) return;
      event.preventDefault();
      options.activate();
      const start = { x: event.clientX, y: event.clientY };
      let last = start,
        dragging = false,
        target = null,
        frame;
      const cover = document.createElement('div'),
        preview = document.createElement('div'),
        status = document.createElement('div');
      cover.className = 'drag-cover pane-drag-cover';
      preview.className = 'pane-drop-preview';
      status.className = 'pane-drag-status';
      status.setAttribute('role', 'status');
      // A temporary surface bridges iframe boundaries without retaining native pointer capture.
      document.body.append(cover);
      function paint() {
        target = null;
        preview.hidden = true;
        const viewport = options.root.getBoundingClientRect();
        if (
          last.x < viewport.left ||
          last.x > viewport.right ||
          last.y < viewport.top ||
          last.y > viewport.bottom
        )
          return;
        for (const pane of options.targets()) {
          const rect = pane.getBoundingClientRect();
          if (
            last.x < rect.left ||
            last.x > rect.right ||
            last.y < rect.top ||
            last.y > rect.bottom
          )
            continue;
          const distances = [
            ['left', (last.x - rect.left) / rect.width],
            ['right', (rect.right - last.x) / rect.width],
            ['top', (last.y - rect.top) / rect.height],
            ['bottom', (rect.bottom - last.y) / rect.height],
          ];
          distances.sort((a, b) => a[1] - b[1]);
          const edge = distances[0][0];
          target = { id: pane.id, edge };
          let x = rect.left,
            y = rect.top,
            width = rect.width,
            height = rect.height;
          if (edge === 'left' || edge === 'right') {
            width /= 2;
            if (edge === 'right') x += width;
          } else {
            height /= 2;
            if (edge === 'bottom') y += height;
          }
          const bottom = Math.min(y + height, viewport.bottom);
          y = Math.max(y, viewport.top);
          height = Math.max(0, bottom - y);
          Object.assign(preview.style, {
            left: x + 'px',
            top: y + 'px',
            width: width + 'px',
            height: height + 'px',
          });
          preview.hidden = false;
          status.textContent = `Place ${edge === 'top' ? 'above' : edge === 'bottom' ? 'below' : edge + ' of'} ${pane.querySelector('.activate').textContent}. Escape cancels.`;
          return;
        }
        status.textContent = 'Drag over another pane to choose a position. Escape cancels.';
      }
      function tick() {
        if (!dragging) return;
        const rect = options.root.getBoundingClientRect();
        if (last.x >= rect.left && last.x <= rect.right) {
          const delta = last.y < rect.top + 60 ? -18 : last.y > rect.bottom - 60 ? 18 : 0;
          if (delta) options.root.scrollTop += delta;
        }
        paint();
        frame = requestAnimationFrame(tick);
      }
      function move(e) {
        last = { x: e.clientX, y: e.clientY };
        if (!dragging && Math.hypot(last.x - start.x, last.y - start.y) > 8) {
          dragging = true;
          window.OpenBooksDrag.isDragging = true;
          document.body.classList.add('dragging-pane');
          document.body.append(preview, status);
          paint();
          frame = requestAnimationFrame(tick);
        }
        if (dragging) paint();
      }
      function finish(commit = false) {
        const drop = target;
        cancelAnimationFrame(frame);
        dragging = false;
        window.OpenBooksDrag.isDragging = false;
        document.body.classList.remove('dragging-pane');
        cover.remove();
        preview.remove();
        status.remove();
        window.removeEventListener('pointermove', move, true);
        window.removeEventListener('pointerup', up, true);
        window.removeEventListener('pointercancel', abort, true);
        window.removeEventListener('keydown', key, true);
        window.removeEventListener('blur', abort);
        cancel = () => {};
        if (commit && drop) options.drop(drop);
        else options.finished();
      }
      function up(e) {
        last = { x: e.clientX, y: e.clientY };
        if (dragging) paint();
        finish(dragging);
      }
      function abort() {
        finish();
      }
      function key(e) {
        if (e.key === 'Escape' || e.key === 'Tab') {
          if (e.key === 'Escape') {
            e.preventDefault();
            e.stopPropagation();
          }
          abort();
        }
      }
      cancel = abort;
      window.addEventListener('pointermove', move, true);
      window.addEventListener('pointerup', up, true);
      window.addEventListener('pointercancel', abort, true);
      window.addEventListener('keydown', key, true);
      window.addEventListener('blur', abort);
    };
    handle.draggable = false;
    handle.ondragstart = (event) => event.preventDefault();
    handle.addEventListener('pointerdown', down);
    handle.onclick = (event) => {
      event.preventDefault();
      if (event.detail === 0) options.help();
    };
    return () => {
      cancel();
      handle.removeEventListener('pointerdown', down);
    };
  }
  window.OpenBooksDrag = { install, isDragging: false };
})();
