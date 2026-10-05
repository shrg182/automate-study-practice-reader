(() => {
  const STORAGE_KEY = "study-studio-read-later-v1";
  const DEFAULT_ITEMS = [
    {id:"deepseek-lenin-quotes",url:"https://chat.deepseek.com/share/o7nxp5pxe30i2kphkj",title:"网传列宁语录",category:"Philosophy",notes:"Repeated reading in Russian.",status:"unread",createdAt:"2026-10-05T08:32:48.482Z",updatedAt:"2026-10-05T08:32:48.482Z"},
    {id:"deepseek-lenin-philosophical-notebooks",url:"https://chat.deepseek.com/share/vhv5c4aklvzc9cebga",title:"列宁《哲学笔记》",category:"Philosophy",notes:"Repeated reading in Russian.",status:"unread",createdAt:"2026-10-05T08:06:38.022Z",updatedAt:"2026-10-05T08:06:38.022Z"},
    {id:"example-chatgpt-share",url:"https://chatgpt.com/share/6ac34d9a-3f00-83e9-94aa-879c15fc214c",title:"Shared ChatGPT conversation",category:"AI",notes:"Public ChatGPT link saved as an example for later reading.",status:"unread",createdAt:"2026-10-05T00:00:00.000Z",updatedAt:"2026-10-05T00:00:00.000Z"}
  ];
  const $ = selector => document.querySelector(selector);
  let items = load();

  function load() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
      if (Array.isArray(saved)) {
        const merged = new Map(DEFAULT_ITEMS.map(item => [item.url, item]));
        saved.forEach(item => merged.set(item.url, {...item,category:normalizeCategory(item.category)}));
        const result = [...merged.values()];
        localStorage.setItem(STORAGE_KEY, JSON.stringify(result));
        return result;
      }
    } catch {}
    localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_ITEMS));
    return [...DEFAULT_ITEMS];
  }
  function normalizeCategory(value) {
    const category = String(value || "").trim();
    return category.toLocaleLowerCase() === "phylosophy" ? "Philosophy" : category;
  }
  function save(message = "Saved in this browser") {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    $("#saveStatus").textContent = message;
    render();
  }
  function normalizeUrl(value) {
    const url = new URL(value.trim());
    if (!["http:", "https:"].includes(url.protocol)) throw new Error("Use a public http or https link.");
    return url.href;
  }
  function titleFor(url) {
    try { return new URL(url).hostname.replace(/^www\./, ""); } catch { return "Saved link"; }
  }
  function formValues() {
    const url = normalizeUrl($("#url").value);
    return {url,title:$("#title").value.trim() || titleFor(url),category:normalizeCategory($("#category").value),notes:$("#notes").value.trim()};
  }
  $("#linkForm").addEventListener("submit", event => {
    event.preventDefault();
    try {
      const data = formValues();
      if (items.some(item => item.url === data.url)) return alert("This link is already in Read Later.");
      const now = new Date().toISOString();
      items.unshift({...data,id:crypto.randomUUID?.() || `${Date.now()}-${Math.random()}`,status:"unread",createdAt:now,updatedAt:now});
      event.currentTarget.reset(); setComposer(false); save("Link added");
    } catch (error) { alert(error.message); }
  });
  function edit(item) {
    const title = prompt("Title", item.title); if (title === null) return;
    const category = prompt("Category", item.category || ""); if (category === null) return;
    const notes = prompt("Notes", item.notes || ""); if (notes === null) return;
    Object.assign(item,{title:title.trim() || titleFor(item.url),category:normalizeCategory(category),notes:notes.trim(),updatedAt:new Date().toISOString()}); save("Changes saved");
  }
  function remove(item) {
    if (!confirm(`Delete “${item.title}” from Read Later?`)) return;
    items = items.filter(candidate => candidate.id !== item.id); save("Link deleted");
  }
  function filtered() {
    const query = $("#search").value.trim().toLocaleLowerCase();
    const status = $("#statusFilter").value;
    const result = items.filter(item => (status === "all" || item.status === status) && (!query || [item.title,item.url,item.category,item.notes].join(" ").toLocaleLowerCase().includes(query)));
    const order = $("#sortOrder").value;
    return result.sort((a,b) => order === "oldest" ? a.createdAt.localeCompare(b.createdAt) : order === "title" ? a.title.localeCompare(b.title) : b.createdAt.localeCompare(a.createdAt));
  }
  function render() {
    const list = $("#linkList"), template = $("#linkTemplate"); list.innerHTML = "";
    const visible = filtered();
    visible.forEach(item => {
      const card = template.content.firstElementChild.cloneNode(true); card.dataset.status = item.status;
      const title = card.querySelector(".title-link"); title.href = item.url; title.textContent = item.title;
      const url = card.querySelector(".url"); url.href = item.url; url.textContent = item.url;
      const open = card.querySelector(".open"); open.href = item.url;
      card.querySelector(".notes").textContent = item.notes || "";
      card.querySelector(".category").textContent = item.category || "";
      const date = card.querySelector("time"); date.dateTime = item.createdAt; date.textContent = `Saved ${new Date(item.createdAt).toLocaleDateString()}`;
      const status = card.querySelector(".item-status"); status.value = item.status; status.onchange = () => {item.status=status.value;item.updatedAt=new Date().toISOString();save("Reading status saved")};
      card.querySelector(".edit").onclick = () => edit(item); card.querySelector(".delete").onclick = () => remove(item);
      list.append(card);
    });
    const counts = Object.fromEntries(["unread","reading","read"].map(status => [status,items.filter(item => item.status === status).length]));
    $("#resultCount").textContent = `${visible.length} ${visible.length === 1 ? "link" : "links"}`;
    $("#statusCounts").textContent = `${counts.unread} unread · ${counts.reading} reading · ${counts.read} read`;
    $("#emptyState").hidden = visible.length > 0;
    const categories = [...new Set(items.map(item => item.category).filter(Boolean))].sort();
    const suggestions = $("#categorySuggestions"); suggestions.innerHTML = "";
    categories.forEach(category => { const option = document.createElement("option"); option.value = category; suggestions.append(option); });
  }
  ["#search","#statusFilter","#sortOrder"].forEach(selector => $(selector).addEventListener(selector === "#search" ? "input" : "change", render));
  function setComposer(open) {
    $("#linkForm").hidden = !open;
    $("#showAddForm").setAttribute("aria-expanded", String(open));
    $("#showAddForm").textContent = open ? "− Close" : "＋ Add link";
    if (open) $("#url").focus();
  }
  $("#showAddForm").onclick = () => setComposer($("#linkForm").hidden);
  $("#cancelAdd").onclick = () => { $("#linkForm").reset(); setComposer(false); };
  $("#exportBtn").onclick = () => {
    const blob = new Blob([JSON.stringify({schema:"study-studio-read-later-v1",exportedAt:new Date().toISOString(),items},null,2)+"\n"],{type:"application/json"});
    const link = document.createElement("a"); link.href = URL.createObjectURL(blob); link.download = `read-later-${new Date().toISOString().slice(0,10)}.json`; link.click(); URL.revokeObjectURL(link.href);
  };
  $("#importInput").onchange = async event => {
    const file = event.target.files[0]; if (!file) return;
    try {
      const data = JSON.parse(await file.text()), incoming = Array.isArray(data) ? data : data.items;
      if (!Array.isArray(incoming)) throw new Error("This is not a Read Later backup.");
      const valid = incoming.map(item => ({...item,url:normalizeUrl(String(item.url || "")),title:String(item.title || titleFor(item.url)),category:normalizeCategory(item.category),notes:String(item.notes || ""),status:["unread","reading","read"].includes(item.status)?item.status:"unread",id:String(item.id || crypto.randomUUID?.() || Date.now()),createdAt:String(item.createdAt || new Date().toISOString()),updatedAt:String(item.updatedAt || new Date().toISOString())}));
      const byUrl = new Map(items.map(item => [item.url,item])); valid.forEach(item => byUrl.set(item.url,item)); items = [...byUrl.values()]; save(`${valid.length} links imported`);
    } catch (error) { alert(`Import failed: ${error.message}`); }
    event.target.value = "";
  };
  render();
})();
