import * as pdfjsLib from '../../vendor/pdfjs/pdf.min.mjs';
globalThis.pdfjsLib = pdfjsLib;
pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  '../../vendor/pdfjs/pdf.worker.min.mjs',
  import.meta.url,
).href;
const base = new URL('../../vendor/pdfjs/', import.meta.url).href;
const container = document.querySelector('#viewerContainer'),
  message = document.querySelector('#message');
let viewer,
  task,
  initialView = {},
  restoring = false,
  timer,
  lastWidth = 0,
  session = null;
function notify(data) {
  parent.postMessage({ ...data, session }, location.origin);
}
function locationChanged() {
  if (!viewer?.pagesCount || restoring) return;
  const page = viewer.currentPageNumber,
    div = viewer.getPageView(page - 1)?.div;
  notify({
    type: 'PDF_LOCATION',
    page,
    total: viewer.pagesCount,
    view: {
      page,
      scale: Number.isFinite(Number(viewer.currentScaleValue))
        ? Number(viewer.currentScaleValue)
        : viewer.currentScaleValue,
      rotation: viewer.pagesRotation,
      offset: div ? (container.scrollTop - div.offsetTop) / Math.max(1, div.clientHeight) : 0,
    },
  });
}
function applyView(view) {
  if (!viewer?.pagesCount) return;
  if ([0, 90, 180, 270].includes(view.rotation)) viewer.pagesRotation = view.rotation;
  if (view.scale !== undefined) viewer.currentScaleValue = view.scale;
  if (view.page)
    viewer.currentPageNumber = Math.max(1, Math.min(viewer.pagesCount, Number(view.page) || 1));
}
window.addEventListener('message', (event) => {
  if (event.origin !== location.origin || event.source !== parent) return;
  const data = event.data;
  if (data?.type === 'OPEN_PDF') {
    session = data.session;
    initialView = data.view || {};
    open(data.file);
  }
  if (data?.type === 'PDF_READ_TEXT' && data.session === session && viewer?.pdfDocument) {
    const requestSession = session;
    viewer.pdfDocument.getPage(viewer.currentPageNumber).then(page => page.getTextContent()).then(content => {
      if (session === requestSession) notify({type: 'PDF_READ_TEXT', requestId: data.requestId, text: content.items.map(item => item.str + (item.hasEOL ? '\n' : ' ')).join('')});
    }).catch(() => { if (session === requestSession) notify({type: 'PDF_READ_TEXT', requestId: data.requestId, error: 'Could not extract text from this PDF page.'}); });
  }
  if (data?.type === 'PDF_PAGE') {
    initialView.page = data.page;
    applyView({ page: data.page });
    locationChanged();
  }
  if (data?.type === 'PDF_VIEW') {
    Object.assign(initialView, data.view || {});
    applyView(data.view || {});
    locationChanged();
  }
});
container.addEventListener('pointerdown', () => notify({ type: 'PDF_FOCUS', intent: 'pointer' }));
container.addEventListener('focusin', () => notify({ type: 'PDF_FOCUS', intent: 'focus' }));
container.addEventListener('keydown', () => notify({ type: 'PDF_FOCUS', intent: 'keyboard' }));
container.addEventListener(
  'scroll',
  () => {
    clearTimeout(timer);
    timer = setTimeout(locationChanged, 150);
  },
  { passive: true },
);
notify({ type: 'PDF_READY' });
async function open(file) {
  try {
    if (task) return;
    const { PDFViewer, EventBus, PDFLinkService } = await import(
      '../../vendor/pdfjs/pdf_viewer.mjs'
    );
    const eventBus = new EventBus(),
      linkService = new PDFLinkService({ eventBus });
    viewer = new PDFViewer({
      container,
      viewer: document.querySelector('#viewer'),
      eventBus,
      linkService,
      removePageBorders: true,
      isEvalSupported: false,
    });
    linkService.setViewer(viewer);
    eventBus.on('pagesinit', () => {
      restoring = true;
      applyView({ scale: 'page-width', ...initialView });
      const div = viewer.getPageView(viewer.currentPageNumber - 1)?.div;
      if (div && Number.isFinite(initialView.offset))
        container.scrollTop = div.offsetTop + initialView.offset * div.clientHeight;
      message.hidden = true;
      restoring = false;
      locationChanged();
    });
    eventBus.on('pagechanging', () => {
      clearTimeout(timer);
      timer = setTimeout(locationChanged, 150);
    });
    task = pdfjsLib.getDocument({
      data: await file.arrayBuffer(),
      cMapUrl: base + 'cmaps/',
      cMapPacked: true,
      standardFontDataUrl: base + 'standard_fonts/',
      wasmUrl: base + 'wasm/',
      isEvalSupported: false,
      enableXfa: false,
    });
    const pdfDocument = await task.promise;
    viewer.setDocument(pdfDocument);
    linkService.setDocument(pdfDocument);
  } catch (error) {
    message.hidden = false;
    message.textContent = 'Could not display this PDF. Try another file.';
    notify({ type: 'PDF_ERROR', message: message.textContent });
    console.warn(error);
  }
}
new ResizeObserver(() => {
  const width = container.clientWidth;
  if (viewer?.pagesCount && width > 0 && width !== lastWidth) {
    lastWidth = width;
    if (['page-width', 'page-fit', 'auto'].includes(viewer.currentScaleValue))
      viewer.currentScaleValue = viewer.currentScaleValue;
  }
}).observe(container);
