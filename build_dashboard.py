import json

import pandas as pd

from pipeline import make_payload

df = pd.read_csv("output.csv")
data = make_payload(df)
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Search Term Triage Engine</title>
<style>
:root{--bg:#f5f7fb;--card:#fff;--text:#172033;--muted:#667085;--line:#e6eaf0;
--blue:#2563eb;--green:#16a34a;--red:#dc2626;--amber:#d97706}
*{box-sizing:border-box}
body{margin:0;font-family:Inter,"Segoe UI",Arial,sans-serif;background:var(--bg);color:var(--text)}
.sidebar{width:235px;background:#111827;color:#fff;padding:22px 16px;position:fixed;top:0;bottom:0}
.logo{font-size:18px;font-weight:800;padding:8px 10px 24px}.logo span{color:#60a5fa}
.nav{display:grid;gap:7px}
.nav button{border:0;background:transparent;color:#cbd5e1;text-align:left;padding:11px 12px;border-radius:9px;cursor:pointer;font-size:14px}
.nav button.active,.nav button:hover{background:#1f2937;color:#fff}
.side-note{position:absolute;left:16px;right:16px;bottom:20px;padding:12px;background:#1f2937;border-radius:10px;color:#9ca3af;font-size:11px;line-height:1.5}
.main{margin-left:235px;padding:22px 28px}
.title h1{font-size:24px;margin:0 0 5px}.title p{margin:0 0 20px;color:var(--muted);font-size:13px}
.cards{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:18px}
.card,.panel{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
.label{font-size:12px;color:var(--muted)}.value{font-size:25px;font-weight:800;margin-top:7px}
.sub{font-size:11px;color:var(--muted);margin-top:5px}
.green{color:var(--green)}.red{color:var(--red)}.amber{color:var(--amber)}
.grid2{display:grid;grid-template-columns:1.35fr 1fr;gap:16px;margin-bottom:16px}
.panel h3{margin:0;font-size:15px}
.panel-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.small{font-size:11px;color:var(--muted)}
.bk{display:grid;grid-template-columns:90px 1fr 60px;gap:10px;align-items:center;margin:11px 0;font-size:12px}
.seg{display:flex;height:20px;border-radius:5px;overflow:hidden;background:#eef2f7}
.seg div{height:100%}
.c-promote{background:#60a5fa}.c-block{background:#f87171}.c-ignore{background:#cbd5e1}.c-review{background:#fbbf24}
.donutbox{display:flex;align-items:center;gap:25px;min-height:200px}
.donut{width:150px;height:150px;border-radius:50%;position:relative;flex:none}
.donut:after{content:"";position:absolute;inset:35px;background:white;border-radius:50%}
.legend{display:grid;gap:12px;font-size:12px}
.legend i{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:7px}
.toolbar{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:12px}
.toolbar input,.toolbar select,button.b{border:1px solid var(--line);background:#fff;border-radius:8px;padding:9px 11px;font-size:12px}
.toolbar input{min-width:230px}button.b{cursor:pointer}
.primary{background:var(--blue)!important;color:#fff;border-color:var(--blue)!important}
.table-wrap{overflow:auto}
.table{width:100%;border-collapse:collapse;font-size:12px}
.table th{background:#f8fafc;color:#667085;text-align:left;font-weight:700}
.table th,.table td{padding:11px 10px;border-bottom:1px solid var(--line);vertical-align:middle}
.term{font-weight:650}.reason{color:#475467;max-width:330px}
.pill{padding:4px 8px;border-radius:999px;font-size:10px;font-weight:700;display:inline-block;white-space:nowrap}
.p-promote{background:#dcfce7;color:#166534}.p-block{background:#fee2e2;color:#991b1b}
.p-ignore{background:#eef2f7;color:#475467}.p-review{background:#fef3c7;color:#92400e}
.cf{font-size:11px;font-weight:700}.cf-high{color:#166534}.cf-medium{color:#92400e}.cf-low{color:#991b1b}
.tag{font-size:10px;color:#7c3aed;font-weight:700;margin-left:6px}
.pager{display:flex;gap:10px;align-items:center;margin-top:12px;font-size:12px;color:var(--muted)}
.hidden{display:none}
.upbar{display:flex;align-items:center;gap:14px;margin-bottom:18px}
.upl{background:var(--blue);color:#fff;border-radius:8px;padding:10px 16px;font-size:13px;font-weight:600;cursor:pointer}
.hintbox{background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;padding:12px;font-size:13px;margin:12px 0}
.actions{display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.actions button{padding:10px 16px;font-size:13px;font-weight:600}
.rule{font-size:13px;line-height:1.6;margin-bottom:12px}
@media(max-width:1000px){.sidebar{display:none}.main{margin-left:0}.cards{grid-template-columns:repeat(2,1fr)}.grid2{grid-template-columns:1fr}}
</style>
</head>
<body>
<aside class="sidebar">
  <div class="logo">Triage<span>Engine</span></div>
  <div class="nav">
    <button data-s="overview" class="active" onclick="showSection('overview')">Overview</button>
    <button data-s="terms" onclick="showSection('terms')">Search Terms</button>
    <button data-s="review" onclick="showSection('review')">Human Review</button>
    <button data-s="rules" onclick="showSection('rules')">How it decides</button>
  </div>
  <div class="side-note"><b>Human-in-the-loop</b><br>Terms with too little data are not guessed. They go to review.</div>
</aside>

<main class="main">
  <div class="title"><h1>Search Term Triage Engine</h1>
  <p>Promote / block / ignore for every term, with a confidence level and a one-line reason</p></div>

  <div class="upbar"><label class="upl">Upload CSV<input type="file" accept=".csv" hidden onchange="uploadCSV(this)"></label><span class="small" id="upStatus">Showing the default dataset. Upload a search-terms CSV to run the triage on it.</span></div>
<section id="overview">
    <div class="cards" id="cards"></div>
    <div class="grid2">
      <div class="panel">
        <div class="panel-head"><h3>Decisions by click volume</h3><span class="small">Model decisions, before review</span></div>
        <div id="buckets"></div>
        <div class="small" id="bucketNote"></div>
      </div>
      <div class="panel">
        <div class="panel-head"><h3>Current decisions</h3><span class="small">Including reviewer calls</span></div>
        <div class="donutbox"><div class="donut" id="donut"></div><div class="legend" id="legend"></div></div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-head"><h3>Biggest review groups</h3><span class="small">Similar terms, decided together</span></div>
      <div class="table-wrap"><table class="table">
        <thead><tr><th>Shared word</th><th>Terms</th><th>Total cost</th><th>Evidence leans</th><th></th></tr></thead>
        <tbody id="topGroups"></tbody></table></div>
    </div>
  </section>

  <section id="terms" class="hidden">
    <div class="panel">
      <div class="panel-head"><h3>All search terms</h3><span class="small" id="countNote"></span></div>
      <div class="toolbar">
        <input id="search" placeholder="Search terms..." oninput="page=0;renderTerms()">
        <select id="filter" onchange="page=0;renderTerms()">
          <option value="all">All decisions</option><option value="promote">Promote</option>
          <option value="block">Block</option><option value="ignore">Ignore</option>
          <option value="review">Needs review</option></select>
        <button class="b" onclick="exportAll()">Export all decisions</button>
        <button class="b" onclick="exportNeg()">Negatives (block)</button>
        <button class="b" onclick="exportKw()">New keywords (promote)</button>
      </div>
      <div class="table-wrap"><table class="table">
        <thead><tr><th>Search term</th><th>Campaign</th><th>Clicks</th><th>Conv.</th><th>Cost</th><th>Decision</th><th>Confidence</th><th>Reason</th></tr></thead>
        <tbody id="termTable"></tbody></table></div>
      <div class="pager">
        <button class="b" onclick="prevPage()">Previous</button>
        <span id="pageInfo"></span>
        <button class="b" onclick="nextPage()">Next</button>
        <span style="margin-left:auto">Sorted by cost, highest first</span>
      </div>
    </div>
  </section>

  <section id="review" class="hidden">
    <div class="panel">
      <div class="panel-head"><h3>Human review</h3><span class="small" id="reviewNote"></span></div>
      <div id="reviewBody"></div>
    </div>
  </section>

  <section id="rules" class="hidden">
    <div class="panel">
      <div class="panel-head"><h3>How each term is decided</h3><span class="small">Computed in Python, shown here</span></div>
      <div id="rulesBody"></div>
    </div>
  </section>
</main>

<script>
let D, R, corr = {};
function setData(data){
  D = data;
  R = D.rows.map(a => ({q:a[0], m:a[1], c:a[2], g:a[3], clicks:a[4], conv:a[5],
    cost:a[6], dec:a[7], conf:a[8], reason:a[9], word:a[10], key:a[0]+"|"+a[2]+"|"+a[3]}));
  R.sort((a,b) => b.cost - a.cost);
  corr = {};
  try { corr = JSON.parse(localStorage.getItem("corr_" + D.id) || "{}"); } catch(e) {}
  selWord = null; page = 0;
}
function save(){ try { localStorage.setItem("corr_" + D.id, JSON.stringify(corr)); } catch(e) {} }

const final = r => corr[r.key] || r.dec;
const fmt = n => Number(n).toLocaleString();
const money = n => Number(n).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2});
const pct = x => (x*100).toFixed(2) + "%";
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const label = d => d === "review" ? "NEEDS REVIEW" : d.toUpperCase();
const pill = d => `<span class="pill p-${d}">${label(d)}</span>`;
const cf = c => `<span class="cf cf-${c.toLowerCase()}">${c}</span>`;

function showSection(id){
  document.querySelectorAll("main section").forEach(s => s.classList.add("hidden"));
  document.getElementById(id).classList.remove("hidden");
  document.querySelectorAll(".nav button").forEach(b => b.classList.toggle("active", b.dataset.s === id));
}

function pending(){ return R.filter(r => r.dec === "review" && !corr[r.key]); }
function groups(){
  const m = {};
  for (const r of pending()) { if (!r.word) continue; (m[r.word] = m[r.word] || []).push(r); }
  return Object.entries(m).map(([w, items]) => ({
    w, items, n: items.length,
    cost: items.reduce((s, r) => s + r.cost, 0),
    lean: D.hints[w].lean
  })).sort((a, b) => b.n - a.n);
}

/* ---------- Overview ---------- */
function renderOverview(){
  const cnt = {promote:0, block:0, ignore:0, review:0};
  R.forEach(r => cnt[final(r)]++);
  const total = R.length;
  const cards = [
    ["Terms processed", fmt(total), "", "Rows in output.csv"],
    ["Promote", fmt(cnt.promote), "green", "Clear evidence of value"],
    ["Block", fmt(cnt.block), "red", "Clear evidence of waste"],
    ["Ignore", fmt(cnt.ignore), "", "Enough data, no clear signal"],
    ["Needs review", fmt(cnt.review), "amber", "Too little data to call"]
  ];
  document.getElementById("cards").innerHTML = cards.map(c =>
    `<div class="card"><div class="label">${c[0]}</div><div class="value ${c[2]}">${c[1]}</div><div class="sub">${c[3]}</div></div>`).join("");

  let acc = 0; const stops = [];
  const colors = {promote:"#60a5fa", block:"#f87171", ignore:"#cbd5e1", review:"#fbbf24"};
  for (const k of ["promote","block","ignore","review"]) {
    const p = cnt[k] / total * 100;
    stops.push(`${colors[k]} ${acc}% ${acc + p}%`); acc += p;
  }
  document.getElementById("donut").style.background = `conic-gradient(${stops.join(",")})`;
  document.getElementById("legend").innerHTML = ["promote","block","ignore","review"].map(k =>
    `<div><i style="background:${colors[k]}"></i>${k === "review" ? "Needs review" : k[0].toUpperCase() + k.slice(1)} <b>${(cnt[k]/total*100).toFixed(1)}%</b></div>`).join("");

  const B = [["1-4 clicks",1,4],["5-9 clicks",5,9],["10-29",10,29],["30-99",30,99],["100+",100,1e12]];
  document.getElementById("buckets").innerHTML = B.map(([name, lo, hi]) => {
    const sub = R.filter(r => r.clicks >= lo && r.clicks <= hi);
    const n = sub.length || 1;
    const c = {promote:0, block:0, ignore:0, review:0};
    sub.forEach(r => c[r.dec]++);
    const segs = ["promote","block","ignore","review"].map(k =>
      `<div class="c-${k}" style="width:${c[k]/n*100}%" title="${k}: ${fmt(c[k])}"></div>`).join("");
    return `<div class="bk"><span>${name}</span><div class="seg">${segs}</div><span class="small">${fmt(sub.length)}</span></div>`;
  }).join("");
  const low = R.filter(r => r.clicks < D.cfg.min_clicks).length;
  document.getElementById("bucketNote").innerHTML =
    `${fmt(low)} of ${fmt(total)} terms (${(low/total*100).toFixed(0)}%) have fewer than ${D.cfg.min_clicks} clicks. The system does not guess on these.
     <br><span style="color:#60a5fa">&#9632;</span> promote &nbsp;<span style="color:#f87171">&#9632;</span> block &nbsp;<span style="color:#94a3b8">&#9632;</span> ignore &nbsp;<span style="color:#fbbf24">&#9632;</span> review`;

  const g = groups().slice(0, 6);
  document.getElementById("topGroups").innerHTML = g.length ? g.map(x =>
    `<tr><td class="term">${esc(x.w)}</td><td>${fmt(x.n)}</td><td>${money(x.cost)}</td>
     <td>${pill(x.lean)}</td><td><button class="b" onclick="openGroup('${x.w}')">Review</button></td></tr>`).join("")
    : `<tr><td colspan="5" class="small">No pending groups.</td></tr>`;
}

/* ---------- Terms ---------- */
let page = 0; const PS = 50;
function filtered(){
  const q = document.getElementById("search").value.toLowerCase();
  const f = document.getElementById("filter").value;
  return R.filter(r => (f === "all" || final(r) === f) && (!q || r.q.toLowerCase().includes(q)));
}
function renderTerms(){
  const list = filtered();
  const pages = Math.max(1, Math.ceil(list.length / PS));
  if (page >= pages) page = pages - 1;
  const rows = list.slice(page * PS, page * PS + PS);
  document.getElementById("termTable").innerHTML = rows.map(r => {
    const f = final(r), rev = !!corr[r.key];
    return `<tr><td class="term">${esc(r.q)}</td><td>${esc(r.c)}</td><td>${fmt(r.clicks)}</td><td>${fmt(r.conv)}</td>
      <td>${money(r.cost)}</td><td>${pill(f)}${rev ? '<span class="tag">REVIEWER</span>' : ''}</td>
      <td>${rev ? "-" : cf(r.conf)}</td><td class="reason">${rev ? "Decided by reviewer" : esc(r.reason)}</td></tr>`;
  }).join("");
  document.getElementById("pageInfo").textContent = `Page ${page + 1} of ${pages}`;
  document.getElementById("countNote").textContent = `${fmt(list.length)} terms`;
}
function prevPage(){ if (page > 0) { page--; renderTerms(); } }
function nextPage(){ page++; renderTerms(); }

/* ---------- Review ---------- */
let selWord = null;
function openGroup(w){ selWord = w; renderReview(); showSection("review"); }
function applyGroup(decision){
  const g = groups().find(x => x.w === selWord);
  if (!g) return;
  g.items.forEach(r => corr[r.key] = decision);
  save(); renderAll();
}
function resetReview(){
  if (!confirm("Remove all reviewer decisions?")) return;
  corr = {}; save(); renderAll();
}
function renderReview(){
  const g = groups();
  const noHint = pending().filter(r => !r.word).length;
  const done = Object.keys(corr).length;
  document.getElementById("reviewNote").textContent = `${fmt(done)} terms decided by reviewer`;
  let html = "";
  if (!g.length) {
    html += `<div class="hintbox">All groups with evidence are reviewed.</div>`;
  } else {
    if (!selWord || !g.find(x => x.w === selWord)) selWord = g[0].w;
    const cur = g.find(x => x.w === selWord);
    const opts = g.map(x => `<option value="${x.w}" ${x.w === selWord ? "selected" : ""}>${esc(x.w)}  -  ${fmt(x.n)} terms  -  leans ${x.lean}</option>`).join("");
    html += `<div class="toolbar"><select style="min-width:320px;padding:9px" onchange="selWord=this.value;renderReview()">${opts}</select></div>
      <div class="hintbox">${esc(D.hints[selWord].text)}</div>
      <div class="actions">
        ${["promote","block","ignore"].map(d =>
          `<button class="b ${d === cur.lean ? "primary" : ""}" onclick="applyGroup('${d}')">${d[0].toUpperCase() + d.slice(1)} all ${fmt(cur.n)}</button>`).join("")}
      </div>
      <div class="small" style="margin-bottom:8px">Highest-cost terms in this group</div>
      <div class="table-wrap"><table class="table">
        <thead><tr><th>Search term</th><th>Clicks</th><th>Conv.</th><th>Cost</th><th>Why review</th></tr></thead>
        <tbody>${cur.items.slice(0, 10).map(r =>
          `<tr><td class="term">${esc(r.q)}</td><td>${fmt(r.clicks)}</td><td>${fmt(r.conv)}</td><td>${money(r.cost)}</td><td class="reason">${esc(r.reason)}</td></tr>`).join("")}</tbody></table></div>`;
  }
  html += `<div class="small" style="margin-top:16px">${fmt(noHint)} more terms have too little data and no word-level evidence. They stay in review; a bulk decision would be a guess.</div>
    <div style="margin-top:12px"><button class="b" onclick="resetReview()">Reset reviewer decisions</button></div>`;
  document.getElementById("reviewBody").innerHTML = html;
}

/* ---------- Rules ---------- */
function renderRules(){
  const c = D.cfg;
  const items = [
    ["1. Baseline", `Account conversion rate is ${pct(D.base)} (total conversions / total clicks). Each term is compared with the rate of its own campaign (campaigns differ a lot), not with zero.`],
    ["2. Too little data", `Terms with fewer than ${c.min_clicks} clicks go to <b>human review</b>. Two clicks and one conversion is noise, not a winner.`],
    ["3. Block", `Rate below the baseline, and a binomial test says the chance of this being bad luck is under ${c.alpha_block*100}%. Example: 60 clicks and 0 conversions when about 2 were expected.`],
    ["4. Promote", `At least ${c.min_promote_conv} conversions, rate at least ${c.min_lift}x the baseline, and under ${c.alpha_promote*100}% chance it is luck. Stricter than block because a wrong promote costs money.`],
    ["5. Ignore", `Enough data, but no clear difference from the baseline.`],
    ["6. Word-level hints", `For review terms, the system checks whether the words in the query are strong across many other terms. This is shown as evidence only. A person makes the call, and similar terms are decided together.`],
    ["7. Reason and confidence", `Every row has a one-line reason with the numbers behind it, and a High / Medium / Low confidence based on how strong the evidence is.`]
  ];
  document.getElementById("rulesBody").innerHTML = items.map(i => `<div class="rule"><b>${i[0]}</b><br>${i[1]}</div>`).join("");
}

/* ---------- Export ---------- */
function csvCell(x){ return '"' + String(x).replace(/"/g, '""') + '"'; }
function download(name, header, rows){
  const text = [header, ...rows].map(r => r.map(csvCell).join(",")).join("\n");
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([text], {type:"text/csv"}));
  a.download = name; a.click();
}
function exportAll(){
  download("triage_decisions.csv",
    ["query","match_type","campaign","ad_group","decision","confidence","reason","source"],
    R.map(r => { const rev = !!corr[r.key];
      return [r.q, r.m, r.c, r.g, final(r), rev ? "" : r.conf, rev ? "Decided by reviewer" : r.reason, rev ? "reviewer" : "model"]; }));
}
function exportNeg(){
  download("negatives.csv", ["query","match_type","campaign","ad_group"],
    R.filter(r => final(r) === "block").map(r => [r.q, r.m, r.c, r.g]));
}
function exportKw(){
  download("keywords.csv", ["query","match_type","campaign","ad_group"],
    R.filter(r => final(r) === "promote").map(r => [r.q, r.m, r.c, r.g]));
}

function renderAll(){ renderOverview(); renderTerms(); renderReview(); }

async function uploadCSV(inp){
  const f = inp.files[0]; if (!f) return;
  const st = document.getElementById("upStatus");
  st.textContent = "Running triage on " + f.name + " ...";
  try {
    const res = await fetch("/triage", {method:"POST", body:f});
    const j = await res.json();
    if (!res.ok) throw new Error(j.error || "Server error");
    setData(j); renderRules(); renderAll(); showSection("overview");
    st.textContent = "Loaded " + f.name + ": " + fmt(j.rows.length) + " terms";
  } catch(e) {
    st.textContent = "Upload failed: " + e.message +
      (location.protocol === "file:" ? " (open the page via python server.py, not by double-clicking the file)" : "");
  }
  inp.value = "";
}
setData(__DATA__); renderRules(); renderAll();
</script>
</body>
</html>
"""

html = TEMPLATE.replace("__DATA__", payload)
with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)
print("dashboard.html created with", len(data["rows"]), "rows")


