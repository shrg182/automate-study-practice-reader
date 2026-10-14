/* Geometry only: moving views must not detach live PDF/EPUB iframes. */
(() => {
  'use strict';
  function measure(node, settings) {
    const own = node.height || 0;
    if (node.pane) return { width: settings.minWidth, height: Math.max(settings.minHeight, own) };
    const a = measure(node.first, settings),
      b = measure(node.second, settings);
    return {
      width: node.axis === 'cols' ? a.width + b.width + 9 : Math.max(a.width, b.width),
      height: Math.max(
        own,
        node.axis === 'rows' ? a.height + b.height + 9 : Math.max(a.height, b.height),
      ),
    };
  }
  function responsive(node, width, settings) {
    if (node.pane) return { ...node, source: node };
    const a = measure(node.first, settings),
      b = measure(node.second, settings),
      axis = node.axis === 'cols' && width < a.width + b.width + 9 ? 'rows' : node.axis;
    const firstWidth =
      axis === 'rows'
        ? width
        : Math.max(a.width, Math.min(width - b.width - 9, (width - 9) * node.ratio));
    return {
      ...node,
      source: node,
      axis,
      first: responsive(node.first, firstWidth, settings),
      second: responsive(node.second, axis === 'rows' ? width : width - firstWidth - 9, settings),
    };
  }
  function frames(node, rect, settings, panes = [], dividers = [], path = 'root') {
    if (node.pane) {
      panes.push({ id: node.pane, ...rect });
      return { panes, dividers };
    }
    const a = measure(node.first, settings),
      b = measure(node.second, settings),
      cols = node.axis === 'cols',
      span = (cols ? rect.width : rect.height) - 9,
      key = cols ? 'width' : 'height';
    const first = Math.max(a[key], Math.min(span - b[key], span * node.ratio)),
      second = span - first;
    const firstRect = { ...rect, [key]: first },
      secondRect = {
        ...rect,
        [cols ? 'x' : 'y']: rect[cols ? 'x' : 'y'] + first + 9,
        [key]: second,
      };
    dividers.push({
      path,
      node,
      rect,
      first,
      second,
      box: cols
        ? { x: rect.x + first, y: rect.y, width: 9, height: rect.height }
        : { x: rect.x, y: rect.y + first, width: rect.width, height: 9 },
    });
    frames(node.first, firstRect, settings, panes, dividers, path + 'a');
    frames(node.second, secondRect, settings, panes, dividers, path + 'b');
    return { panes, dividers };
  }
  window.OpenBooksLayout = { measure, responsive, frames };
})();
