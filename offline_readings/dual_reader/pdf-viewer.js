import * as pdfjsLib from '../../vendor/pdfjs/pdf.min.mjs';
globalThis.pdfjsLib=pdfjsLib;
pdfjsLib.GlobalWorkerOptions.workerSrc=new URL('../../vendor/pdfjs/pdf.worker.min.mjs',import.meta.url).href;
const base=new URL('../../vendor/pdfjs/',import.meta.url).href;
const container=document.querySelector('#viewerContainer'),message=document.querySelector('#message');
let viewer,task,requestedPage=1;
function notify(data){parent.postMessage(data,location.origin)}
window.addEventListener('message',event=>{if(event.origin!==location.origin||event.source!==parent)return;const data=event.data;if(data?.type==='OPEN_PDF')open(data.file);if(data?.type==='PDF_PAGE'){requestedPage=data.page;if(viewer?.pagesCount)viewer.currentPageNumber=Math.max(1,Math.min(viewer.pagesCount,requestedPage))}});
notify({type:'PDF_READY'});
async function open(file){
 try{
  if(task)return;
  const {PDFViewer,EventBus,PDFLinkService}=await import('../../vendor/pdfjs/pdf_viewer.mjs');
  const eventBus=new EventBus(),linkService=new PDFLinkService({eventBus});
  viewer=new PDFViewer({container,viewer:document.querySelector('#viewer'),eventBus,linkService,removePageBorders:true,isEvalSupported:false});linkService.setViewer(viewer);
  eventBus.on('pagesinit',()=>{viewer.currentScaleValue='page-width';viewer.currentPageNumber=Math.max(1,Math.min(viewer.pagesCount,requestedPage));message.hidden=true;notify({type:'PDF_LOCATION',page:viewer.currentPageNumber,total:viewer.pagesCount})});
  eventBus.on('pagechanging',event=>notify({type:'PDF_LOCATION',page:event.pageNumber,total:viewer.pagesCount}));
  task=pdfjsLib.getDocument({data:await file.arrayBuffer(),cMapUrl:base+'cmaps/',cMapPacked:true,standardFontDataUrl:base+'standard_fonts/',wasmUrl:base+'wasm/',isEvalSupported:false,enableXfa:false});
  const pdfDocument=await task.promise;viewer.setDocument(pdfDocument);linkService.setDocument(pdfDocument);
 }catch(error){message.hidden=false;message.textContent='Could not display this PDF. Try another file.';notify({type:'PDF_ERROR',message:message.textContent});console.warn(error)}
}
let lastWidth=0;
new ResizeObserver(()=>{const width=container.clientWidth;if(viewer?.pagesCount&&width>0&&width!==lastWidth){lastWidth=width;viewer.currentScaleValue='page-width'}}).observe(container);
