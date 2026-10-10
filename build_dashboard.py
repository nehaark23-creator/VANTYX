import json, sys
import pandas as pd
import config as C

HTML = r"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>query / sense - PS-01 Triage Engine</title><style>
:root{--navy:#14233a;--bg:#f7f5f0;--line:#e9e5dc;--text:#1c2733;--mut:#697586;--amber:#e0a73a;--green:#2f7d5b;--red:#c0584a}
*{box-sizing:border-box}html{font-size:15px}
body{margin:0;font-family:"Plus Jakarta Sans",Inter,"Segoe UI",system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.45}
button,input,select{font:inherit;color:inherit}
.side{position:fixed;top:0;bottom:0;left:0;width:250px;background:var(--navy);color:#cbd5e1;padding:22px 14px;display:flex;flex-direction:column;gap:6px}
.brand{display:flex;gap:12px;align-items:center;padding:4px 8px 22px}.lg{width:40px;height:40px;border-radius:10px;background:var(--amber);display:grid;place-items:center;color:#fff;font-size:18px}.brand b{display:block;color:#fff;font-size:17px}.brand small{font-size:10px;letter-spacing:.14em;color:#8ea0b8}
.sec{font-size:10px;letter-spacing:.16em;color:#8ea0b8;padding:6px 10px}
.side>button{display:flex;gap:12px;align-items:center;border:0;border-left:3px solid transparent;background:none;color:#cbd5e1;padding:12px;border-radius:8px;text-align:left;cursor:pointer;font-weight:600;font-size:15px}.side>button:hover{background:#1b3150}.side>button.on{background:#223a5a;color:#fff;border-left-color:var(--amber)}
.bd{margin-left:auto;background:#3b4f6b;color:#f5c26b;border-radius:99px;padding:1px 9px;font-size:11px}
.guide{margin-top:auto;border:1px solid #2c4263;border-radius:10px;padding:14px;font-size:12px;line-height:1.55;color:#9fb0c6}.guide b{color:var(--amber);display:block;margin-bottom:6px;font-size:13px}
.main{margin-left:250px}.crumb{background:#fff;border-bottom:1px solid var(--line);padding:20px 40px;color:var(--mut);display:flex;justify-content:space-between;font-size:14px}.crumb b{color:var(--text)}
.pg{padding:34px 40px 70px}.wrap{max-width:1240px;margin:0 auto}.hid{display:none!important}
.eb{font-size:11px;letter-spacing:.16em;color:var(--mut);font-weight:700}h1{font-size:36px;margin:8px 0;letter-spacing:-.02em;line-height:1.15}h3{margin:0 0 4px;font-size:17px}.sub{color:var(--mut);margin:0 0 26px;max-width:700px;line-height:1.55;font-size:15px}small{color:var(--mut);font-size:12px}
.head{display:flex;justify-content:space-between;align-items:flex-start;gap:20px}
.btn{background:var(--navy);color:#fff;border:0;border-radius:9px;padding:12px 20px;font-weight:700;cursor:pointer;font-size:14px;white-space:nowrap}.btn.am{background:var(--amber);color:#1c2733}.btn.ln{background:#fff;color:var(--text);border:1px solid var(--line)}.btn:disabled{opacity:.45;cursor:default}
.card,.kpi,.rc{background:#fff;border:1px solid var(--line);border-radius:12px}.card{padding:24px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:22px}.kpi{padding:20px 22px}.kt{display:flex;justify-content:space-between;font-weight:600;font-size:14px}
.ic{width:34px;height:34px;border-radius:9px;background:#eef2f6;color:#41566f;display:grid;place-items:center;font-size:15px}.ic.g{background:#e3f1ea;color:var(--green)}.ic.r{background:#f8e4e0;color:var(--red)}.ic.a{background:#fbefd6;color:#a8700f}
.kv{font-size:34px;font-weight:800;margin:16px 0 6px;letter-spacing:-.02em}.kv.sm{font-size:28px}.ks{font-size:12px;color:var(--mut)}
.pill{display:inline-block;padding:5px 11px;border-radius:99px;font-size:12px;font-weight:700;white-space:nowrap}.pill.promote{background:#e3f1ea;color:var(--green)}.pill.block{background:#f8e4e0;color:#a63f31}.pill.ignore{background:#e9edf2;color:#51606f}.pill.review{background:#fbefd6;color:#9a6508}
.ct{font-size:12px;font-weight:700;padding:3px 10px;border-radius:7px}.ct.High{background:#e3f1ea;color:var(--green)}.ct.Medium{background:#fbefd6;color:#9a6508}.ct.Low{background:#f8e4e0;color:#a63f31}
.tool{display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap}.tool input,.tool select{border:1px solid var(--line);background:#fff;border-radius:9px;padding:12px 14px;font-size:14px}.tool input{flex:1;min-width:260px}.cnt{align-self:center;color:var(--mut);font-size:13px;white-space:nowrap}
.tw{overflow-x:auto;background:#fff;border:1px solid var(--line);border-radius:12px}table{width:100%;border-collapse:collapse;font-size:14px}th{text-align:left;font-size:11px;letter-spacing:.07em;color:var(--mut);padding:14px 12px;border-bottom:1px solid var(--line);white-space:nowrap}th.s{cursor:pointer}th.s:hover{color:var(--text)}td{padding:14px 12px;border-bottom:1px solid #f1eee7;vertical-align:top}tr:last-child td{border-bottom:0}
.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}td small{display:block;margin-top:3px}.qq{min-width:220px}.why{min-width:270px;color:#4a5766;font-size:13px}.hn{color:#7a6530;margin-top:4px;font-size:12px}
.pgr{display:flex;gap:14px;align-items:center;justify-content:space-between;margin-top:16px;color:var(--mut);font-size:13px}.pgr div{display:flex;gap:10px;align-items:center}.pgr button,.more button{border:1px solid var(--line);background:#fff;border-radius:8px;padding:9px 16px;cursor:pointer;font-weight:600}.more{text-align:center;margin-top:16px}
.tabs{display:inline-flex;background:#fff;border:1px solid var(--line);border-radius:10px;padding:4px;margin-bottom:18px}.tabs button{border:0;background:none;padding:10px 18px;border-radius:7px;cursor:pointer;font-weight:600;color:var(--mut)}.tabs button.on{background:#f1eee7;color:var(--text)}
.rc{padding:22px 24px;margin-bottom:16px}.rtop{display:flex;justify-content:space-between;gap:20px}.rt{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-size:17px}.rm{color:var(--mut);font-size:13px;margin-top:8px}
.od{border:1px solid var(--line);border-radius:9px;padding:10px 16px;text-align:center;align-self:flex-start}.od small{display:block;letter-spacing:.1em;margin-bottom:6px;font-size:10px}
.wf{background:#f7f5f0;border-radius:8px;padding:12px 16px;margin:14px 0;font-size:14px}.hint{margin-top:6px;color:#6b5a2a;font-size:13px}
.rbot{display:flex;gap:20px;align-items:flex-end;border-top:1px solid var(--line);padding-top:16px;flex-wrap:wrap}.ch{display:flex;gap:8px;margin-top:8px}.ch button{border:1px solid var(--line);background:#fff;border-radius:8px;padding:10px 18px;cursor:pointer;font-weight:700;font-size:13px}.ch button:hover{background:#f4f6f9}.ch button.on{background:#e8eef6;border-color:#7d97bb;color:#14233a}
.nt{flex:1;min-width:240px}.nt input{width:100%;border:1px solid var(--line);border-radius:8px;padding:11px 12px;margin-top:8px;font-size:14px}.save{background:var(--navy);color:#fff;border:0;border-radius:8px;padding:12px 18px;font-weight:700;cursor:pointer}
.empty{padding:50px;text-align:center;color:var(--mut)}.g2{display:grid;grid-template-columns:1.45fr 1fr;gap:20px;margin-bottom:20px}.g3{display:grid;grid-template-columns:1.45fr 1fr;gap:20px;margin-bottom:20px}.g4{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px}
.br{display:grid;grid-template-columns:130px 1fr 80px;gap:14px;align-items:center;margin-top:16px}.br b{text-align:right}.bt{height:8px;background:#f1eee7;border-radius:9px;overflow:hidden}.bt i{display:block;height:100%;border-radius:9px}
.bt i.promote,.bt i.cfHigh{background:var(--green)}.bt i.block,.bt i.cfLow{background:var(--red)}.bt i.ignore{background:#94a3b8}.bt i.review,.bt i.cfMedium{background:var(--amber)}
.cp{display:grid;grid-template-columns:130px 1fr 130px;gap:14px;align-items:center;margin-top:18px}.cpl{display:flex;justify-content:space-between;font-size:12px;color:var(--mut);margin-bottom:6px}.bv{text-align:right}.bv small{display:block}
.donut{width:150px;height:150px;border-radius:50%;margin:14px auto 20px;display:grid;place-items:center}.donut>div{width:106px;height:106px;border-radius:50%;background:#fff;display:grid;place-content:center;text-align:center;font-weight:800;font-size:22px;line-height:1.1}.donut small{font-size:9px;letter-spacing:.12em;font-weight:600}
.nba{background:var(--navy);color:#fff;border-radius:12px;padding:30px;display:flex;flex-direction:column;justify-content:center}.nba h2{margin:8px 0 12px;font-size:25px;line-height:1.25}.nba p{color:#b8c5d6;margin:0 0 22px;line-height:1.55}.nba .eb{color:#8ea0b8}
.vl{color:var(--mut);font-size:13px;cursor:pointer;float:right;font-weight:600}
.xp{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}.xh{background:#223a5a;color:#fff;padding:30px}.xh h2{font-size:28px;margin:10px 0}.xh p{color:#b8c5d6;max-width:520px;margin:0;line-height:1.55}.xb{padding:22px}.tiles{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px}.tile{background:#f7f5f0;border-radius:9px;padding:14px 16px;display:flex;gap:12px}.tile i{color:var(--green);font-style:normal;font-weight:800}.tile b{display:block;font-size:14px}.dl{display:flex;gap:12px;flex-wrap:wrap}
.ol{padding-left:0;list-style:none;line-height:1.7;margin:16px 0 0}.ol li{margin-bottom:10px}
.drop{display:grid;place-items:center;gap:6px;border:1.5px dashed #d9d3c5;border-radius:12px;padding:70px 20px;background:#fbfaf7;cursor:pointer;text-align:center;margin:18px 0}.up{font-size:30px}
.note{background:#f3eee2;border:1px solid #ebe3cf;border-radius:10px;padding:16px 18px;font-size:13px;line-height:1.55;color:#5b5236;margin-top:16px}
.rule{margin-top:12px;line-height:1.55;font-size:14px}
@media(max-width:1100px){.side{display:none}.main{margin:0}.kpis{grid-template-columns:repeat(2,1fr)}.g2,.g3,.g4{grid-template-columns:1fr}.pg{padding:20px}}
</style></head><body>
<aside class="side"><div class="brand"><div class="lg">&#10148;</div><div><b>query / sense</b><small>PS-01 &middot; TRIAGE ENGINE</small></div></div><div class="sec">WORKSPACE</div>
<button id="n-overview" onclick="go('overview')"><span>&#9638;</span>Overview</button>
<button id="n-upload" onclick="go('upload')"><span>&#8679;</span>Upload report</button>
<button id="n-terms" onclick="go('terms')"><span>&#9776;</span>Search terms</button>
<button id="n-review" onclick="go('review')"><span>&#9873;</span>Human review<span class="bd" id="rbadge">0</span></button>
<button id="n-analytics" onclick="go('analytics')"><span>&#9636;</span>Analytics</button>
<button id="n-export" onclick="go('export')"><span>&#8681;</span>Export results</button>
<div class="guide"><b>Decision guide</b>Low-data queries stay in Human Review. Original triage decisions are always preserved.</div></aside>
<div class="main"><div class="crumb"><span>Workspace / <b id="crumb">Overview</b></span><span>Google Ads search terms</span></div>

<section id="p-overview" class="pg"><div class="wrap"><div class="head"><div><div class="eb">PERFORMANCE AT A GLANCE</div><h1>Search term overview</h1><p class="sub">A clear read on what your query report is telling you, and where a human should take a closer look.</p></div><button class="btn" onclick="go('upload')">&#8679; Upload report</button></div>
<div class="kpis" id="kpis"></div>
<div class="g3"><div class="card"><h3>Conversion performance</h3><small>Conversions and attributed value by triage decision</small><div id="ov1"></div></div>
<div class="card"><h3>Confidence mix</h3><small>Signal strength across triaged terms</small><div class="donut" id="dc1"><div><span id="dv1"></span><small>TERMS</small></div></div><div id="cf1"></div></div></div>
<div class="g3"><div class="card"><h3>Decision breakdown <span class="vl" onclick="go('terms')">View terms &rarr;</span></h3><small>How the triage engine sorted this report</small><div id="ov3"></div></div>
<div class="nba"><div class="eb">NEXT BEST ACTION</div><h2>Keep uncertain queries in human hands.</h2><p id="nbat"></p><div><button class="btn am" onclick="go('review')">Open review queue &rarr;</button></div></div></div></div></section>

<section id="p-upload" class="pg hid"><div class="wrap"><div class="eb">BRING IN A REPORT</div><h1>Upload search terms</h1><p class="sub">Start with a Google Ads search terms CSV. The Python engine runs on the server and makes every decision.</p>
<div class="g2"><div class="card"><h3>Choose your CSV file</h3><small>Google Ads search terms report &middot; CSV format</small>
<label class="drop" ondragover="event.preventDefault()" ondrop="event.preventDefault();pf(event.dataTransfer.files[0])"><input type="file" accept=".csv" hidden onchange="pf(this.files[0])"><div class="up">&#8679;</div><b id="fname">Drop your report here</b><small>or click to browse &middot; CSV only</small></label>
<div class="head" style="align-items:center"><small>Required fields: search term, impressions, clicks, cost</small><button class="btn" id="goBtn" disabled onclick="run()">Run triage</button></div></div>
<div><div class="card"><h3>What happens next</h3><small>Careful by design, easy to audit.</small><ol class="ol"><li><b>01 &nbsp;Pool the rows</b><br><small>Same query in different match types is added together.</small></li><li><b>02 &nbsp;Apply triage</b><br><small>Promote, Block or Ignore, only with enough evidence.</small></li><li><b>03 &nbsp;Review uncertain terms</b><br><small>Low-data queries are held for a person, not guessed.</small></li></ol></div><div class="note"><b>Source decisions stay intact.</b> Reviewer corrections are recorded separately. Export includes both decisions so the audit trail remains clear.</div></div></div></div></section>

<section id="p-terms" class="pg hid"><div class="wrap"><div class="eb">EXPLORE THE REPORT</div><h1>Search terms</h1><p class="sub">Search, sort, and filter every query. Click a column heading to sort. A reviewer correction shows next to the original decision.</p>
<div class="tool"><input id="q" placeholder="Search query, campaign or ad group..." oninput="rTerms()"><select id="fd" onchange="rTerms()"><option value="all">All decisions</option><option value="promote">Promote</option><option value="block">Block</option><option value="ignore">Ignore</option><option value="review">Human Review</option></select><select id="fc" onchange="rTerms()"><option value="all">All confidence</option><option>High</option><option>Medium</option><option>Low</option></select><select id="fk" onchange="rTerms()"></select><select id="fp" onchange="rTerms()"><option value="25">25 / page</option><option value="50" selected>50 / page</option><option value="100">100 / page</option></select><button class="btn ln" onclick="clr()">Reset</button></div>
<div class="tw"><table><thead><tr><th class="s" onclick="srt('q')">QUERY &#8645;</th><th class="s" onclick="srt('camp')">CAMPAIGN &#8645;</th><th class="s" onclick="srt('ag')">AD GROUP &#8645;</th><th class="s" onclick="srt('c')" style="text-align:right">CLICKS &#8645;</th><th class="s" onclick="srt('k')" style="text-align:right">COST &#8645;</th><th class="s" onclick="srt('v')" style="text-align:right">CONV. &#8645;</th><th>DECISION</th><th>CONFIDENCE</th><th>REASON</th></tr></thead><tbody id="tb"></tbody></table></div><div class="pgr"><span id="cnt"></span><div id="pg"></div></div></div></section>

<section id="p-review" class="pg hid"><div class="wrap"><div class="head"><div><div class="eb">HUMAN-IN-THE-LOOP</div><h1>Review queue</h1><p class="sub">Give uncertain queries a considered decision. Corrections are saved without replacing the original recommendation.</p></div><span class="pill review" id="rcount"></span></div>
<div class="tabs"><button id="t-need" onclick="tab='need';revN=50;rRev()"></button><button id="t-done" onclick="tab='done';revN=50;rRev()"></button></div>
<div class="tool"><input id="rq" placeholder="Search queries in this list..." oninput="revN=50;rRev()"><select id="rs" onchange="rRev()"><option value="k">Highest spend first</option><option value="c">Most clicks first</option></select></div>
<div id="rl"></div><div class="more" id="rmore"></div></div></section>

<section id="p-analytics" class="pg hid"><div class="wrap"><div class="eb">UNDERSTAND OUTCOMES</div><h1>Analytics</h1><p class="sub">Compare decisions against real account outcomes. Use conversion value, click volume, and confidence as context, not a black box.</p>
<div class="g3"><div class="card"><h3>Conversion performance</h3><small>Conversions and value by triage outcome</small><div id="a1"></div></div><div class="card"><h3>Confidence distribution</h3><small>How certain the engine is about its decisions</small><div class="donut" id="dc2"><div><span id="dv2"></span><small>TERMS</small></div></div><div id="cf2"></div></div></div>
<div class="g4"><div class="card"><h3>Clicks by decision</h3><small>Where search traffic is coming from</small><div id="a2"></div></div><div class="card"><h3>Cost by decision</h3><small>Spend associated with each recommendation</small><div id="a3"></div></div></div>
<div class="card"><h3>How the engine decides</h3><small>Statistical test, thresholds live in config.py</small>__RULES__</div>
<div class="note"><b>Read with care.</b> A decision label is not a performance guarantee. Conversion metrics reflect the uploaded report and its attribution settings.</div></div></section>

<section id="p-export" class="pg hid"><div class="wrap"><div class="eb">TAKE DECISIONS WITH YOU</div><h1>Export results</h1><p class="sub">Download the final report as CSV, with the original recommendation and any saved reviewer decision kept as separate fields.</p>
<div class="g2"><div class="xp"><div class="xh"><div class="eb" style="color:#e0a73a">FINAL RESULTS</div><h2>One report. A clear audit trail.</h2><p>The export combines triage recommendations, confidence signals, reasons and completed reviewer corrections.</p></div>
<div class="xb"><div class="tiles"><div class="tile"><i>&#10003;</i><div><b>Triage decision</b><small>Engine recommendation</small></div></div><div class="tile"><i>&#10003;</i><div><b>Reviewer decision</b><small>Human correction, if saved</small></div></div><div class="tile"><i>&#10003;</i><div><b>Confidence</b><small>High / medium / low</small></div></div><div class="tile"><i>&#10003;</i><div><b>Reason</b><small>Why a decision was suggested</small></div></div></div>
<div class="dl"><button class="btn am" onclick="exAll()">&#8681; Download CSV</button><button class="btn ln" onclick="exNeg()">negatives.csv</button><button class="btn ln" onclick="exKw()">keywords.csv</button></div><p><small id="xinfo"></small></p></div></div>
<div><div class="card"><h3>Before you export</h3><small>A quick check for a useful handoff.</small><ol class="ol"><li>01 &nbsp;Review pending uncertain terms where practical.</li><li>02 &nbsp;Keep original and reviewer decisions distinct downstream.</li><li>03 &nbsp;Use the confidence and reason columns to prioritize follow-up.</li></ol></div>
<div class="note"><b>Export reflects the latest saved review decisions.</b><br>negatives.csv = terms finally decided Block. keywords.csv = terms finally decided Promote.</div>
<p><button class="btn ln" onclick="exClear()">Clear saved reviewer decisions</button></p></div></div></div></section>
</div>
<script>
let rows=__DATA__,ovr={},draft={},cur=[],page=0,revN=50,tab='need',sort={k:'k',dir:-1},file=null;
try{ovr=JSON.parse(localStorage.getItem('ovr2')||'{}')}catch(e){}
const $=id=>document.getElementById(id);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const N=x=>Number(x||0).toLocaleString(undefined,{maximumFractionDigits:0});
const M=x=>'$'+Number(x||0).toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2});
const LBL={promote:'Promote',block:'Block',ignore:'Ignore',review:'Human Review'};
const D4=['promote','block','ignore','review'];
const pill=d=>`<span class="pill ${d}">&#9679; ${LBL[d]||d}</span>`;
const ctag=c=>`<span class="ct ${c}">${c}</span>`;
const key=r=>r.q+'|'+r.camp+'|'+r.ag;
const persist=()=>{try{localStorage.setItem('ovr2',JSON.stringify(ovr))}catch(e){}};
const fin=r=>{const o=ovr[key(r)];return o?o.d:r.d};
const revAll=()=>rows.filter(r=>r.d==='review');
const revNeed=()=>revAll().filter(r=>!ovr[key(r)]);
const PAGES=['overview','upload','terms','review','analytics','export'];
const TITLE={overview:'Overview',upload:'Upload report',terms:'Search terms',review:'Human review',analytics:'Analytics',export:'Export results'};
function badge(){$('rbadge').textContent=N(revNeed().length)}
function go(p){PAGES.forEach(x=>{$('p-'+x).classList.toggle('hid',x!==p);$('n-'+x).classList.toggle('on',x===p)});$('crumb').textContent=TITLE[p];({overview:rOver,terms:rTerms,review:rRev,analytics:rAna,upload:()=>{},export:rExp})[p]();badge();scrollTo(0,0)}
function agg(){const a={},cf={High:0,Medium:0,Low:0};D4.forEach(d=>a[d]={n:0,c:0,v:0,k:0,cv:0});rows.forEach(r=>{const o=a[r.d]||(a[r.d]={n:0,c:0,v:0,k:0,cv:0});o.n++;o.c+=r.c;o.v+=r.v;o.k+=r.k;o.cv+=r.cv;cf[r.cf]=(cf[r.cf]||0)+1});return{a,cf}}
const kpi=(t,v,s,i,c,sm)=>`<div class="kpi"><div class="kt">${t}<span class="ic ${c||''}">${i}</span></div><div class="kv ${sm?'sm':''}">${v}</div><div class="ks">${s}</div></div>`;
function setDonut(d,v,l){const{cf}=agg(),T=rows.length||1,h=cf.High/T*100,m=h+cf.Medium/T*100;$(d).style.background=`conic-gradient(#2f7d5b 0 ${h}%,#e0a73a ${h}% ${m}%,#c0584a ${m}% 100%)`;$(v).textContent=N(rows.length);$(l).innerHTML=['High','Medium','Low'].map(x=>`<div class="br" style="grid-template-columns:80px 1fr 70px;margin-top:12px"><span>${x}</span><div class="bt"><i class="cf${x}" style="width:${Math.max(.5,(cf[x]||0)/T*100)}%"></i></div><b>${N(cf[x]||0)}</b></div>`).join('')}
function rOver(){const{a,cf}=agg(),sum=f=>D4.reduce((s,d)=>s+a[d][f],0);
$('kpis').innerHTML=kpi('Total terms',N(rows.length),'Unique terms after pooling','&#8981;')+kpi('Promote',N(a.promote.n),'Worth adding as keywords','&#8599;','g')+kpi('Block',N(a.block.n),'Potential negative keywords','&#10005;','r')+kpi('Ignore',N(a.ignore.n),'No action recommended','&#9719;')+kpi('Human review',N(a.review.n),'Too little data to decide','&#9873;','a')+kpi('High confidence',N(cf.High),'Strong supporting evidence','&#10003;','g')+kpi('Low confidence',N(cf.Low),'Limited sample or signal','?','r')+kpi('Total clicks',N(sum('c')),'Across all search terms','&#10148;')+kpi('Total conversions',N(sum('v')),'Reported conversion actions','&#10003;','g')+kpi('Total cost',M(sum('k')),'Spend in the imported report','~','a',1)+kpi('Conversion value',M(sum('cv')),'Value attributed to conversions','&#9638;','g',1);
const mv=Math.max(1,...D4.map(d=>a[d].v)),mn=Math.max(1,...D4.map(d=>a[d].n));
$('ov1').innerHTML=D4.map(d=>`<div class="cp">${pill(d)}<div><div class="cpl"><span>${N(a[d].v)} conversions</span><span>${N(a[d].c)} clicks</span></div><div class="bt"><i class="${d}" style="width:${Math.max(1,a[d].v/mv*100)}%"></i></div></div><div class="bv"><small>Value</small><b>${M(a[d].cv)}</b></div></div>`).join('');
$('ov3').innerHTML=D4.map(d=>`<div class="br">${pill(d)}<div class="bt"><i class="${d}" style="width:${Math.max(1,a[d].n/mn*100)}%"></i></div><b>${N(a[d].n)}</b></div>`).join('');
$('nbat').textContent=N(revNeed().length)+' terms are waiting for a decision. Your corrections are saved separately from the original triage.';
setDonut('dc1','dv1','cf1')}
function srt(k){sort=sort.k===k?{k,dir:-sort.dir}:{k,dir:-1};rTerms()}
function pgo(d){page=Math.max(0,page+d);rTerms(true)}
function clr(){$('q').value='';$('fd').value='all';$('fc').value='all';$('fk').value='all';rTerms()}
function fillCamps(){const s=$('fk'),v=s.value||'all',c=[...new Set(rows.map(r=>r.camp))].sort();s.innerHTML='<option value="all">All campaigns</option>'+c.map(x=>`<option value="${esc(x)}">${esc(x)}</option>`).join('');s.value=c.includes(v)?v:'all'}
function rTerms(keep){if(keep!==true)page=0;if($('fk').options.length<2)fillCamps();
const q=$('q').value.toLowerCase(),f=$('fd').value,c=$('fc').value,k=$('fk').value,PS=+$('fp').value;
const a=rows.filter(r=>(!q||(r.q+' '+r.camp+' '+r.ag).toLowerCase().includes(q))&&(f==='all'||fin(r)===f)&&(c==='all'||r.cf===c)&&(k==='all'||r.camp===k));
a.sort((x,y)=>(typeof x[sort.k]==='string'?x[sort.k].localeCompare(y[sort.k]):x[sort.k]-y[sort.k])*sort.dir);
const n=Math.max(1,Math.ceil(a.length/PS));if(page>=n)page=n-1;const s=page*PS;
$('tb').innerHTML=a.slice(s,s+PS).map(r=>{const f2=fin(r);return `<tr><td class="qq"><b>${esc(r.q)}</b><small>${esc(r.mt)} match &middot; ${N(r.i)} impr${r.n>1?' &middot; pooled '+r.n+' rows':''}</small></td><td>${esc(r.camp)}</td><td>${esc(r.ag)}</td><td class="num">${N(r.c)}</td><td class="num">${M(r.k)}</td><td class="num">${N(r.v)}<small>${M(r.cv)}</small></td><td>${pill(f2)}${f2!==r.d?`<small>reviewed, was ${LBL[r.d]}</small>`:''}</td><td>${ctag(r.cf)}</td><td class="why">${esc(r.why)}${r.h?`<div class="hn">${esc(r.h)}</div>`:''}</td></tr>`}).join('')||'<tr><td colspan="9" class="empty">No terms match these filters.</td></tr>';
$('cnt').textContent=a.length?`Showing ${N(s+1)}-${N(Math.min(s+PS,a.length))} of ${N(a.length)}`:'Showing 0';
$('pg').innerHTML=`<button onclick="pgo(-1)">&larr; Prev</button><span>Page ${page+1} / ${N(n)}</span><button onclick="pgo(1)">Next &rarr;</button>`}
const dv=r=>draft[key(r)]||ovr[key(r)]||{};
function rRev(){const need=revNeed(),done=revAll().filter(r=>ovr[key(r)]),q=($('rq').value||'').toLowerCase(),sk=$('rs').value;
$('t-need').textContent='Needs Review ('+N(need.length)+')';$('t-done').textContent='Completed ('+N(done.length)+')';
$('t-need').classList.toggle('on',tab==='need');$('t-done').classList.toggle('on',tab==='done');$('rcount').innerHTML='&#9719; '+N(need.length)+' to review';
cur=(tab==='need'?need:done).filter(r=>!q||(r.q+' '+r.camp+' '+r.ag).toLowerCase().includes(q)).sort((a,b)=>b[sk]-a[sk]);
$('rl').innerHTML=cur.slice(0,revN).map((r,i)=>{const x=dv(r);
return `<div class="rc"><div class="rtop"><div><div class="rt"><b>${esc(r.q)}</b>${pill(r.d)}${ctag(r.cf)}</div><div class="rm">${esc(r.camp)} / ${esc(r.ag)} &middot; ${N(r.i)} impressions &middot; ${N(r.c)} clicks &middot; ${M(r.k)} cost &middot; ${N(r.v)} conversions</div></div><div class="od"><small>ORIGINAL DECISION</small>${pill(r.d)}</div></div><div class="wf"><b>Why flagged:</b> ${esc(r.why)}${r.h?`<div class="hint">${esc(r.h)}</div>`:''}</div><div class="rbot"><div><small>Choose a decision</small><div class="ch">${['promote','block','ignore'].map(z=>`<button class="${x.d===z?'on':''}" onclick="pick(${i},'${z}')">${LBL[z]}</button>`).join('')}</div></div><div class="nt"><small>Note</small><input placeholder="Optional context for this correction" value="${esc(x.note||'')}" oninput="nt(${i},this.value)"></div><button class="save" onclick="sv(${i})">&#10003; Save decision</button></div></div>`}).join('')||'<div class="empty">Nothing here.</div>';
$('rmore').innerHTML=cur.length>revN?`<button onclick="revN+=50;rRev()">Show 50 more (${N(cur.length-revN)} left)</button>`:'';badge()}
function pick(i,d){const k=key(cur[i]);draft[k]={...dv(cur[i]),d};rRev()}
function nt(i,v){const k=key(cur[i]);draft[k]={...dv(cur[i]),note:v}}
function sv(i){const r=cur[i],k=key(r),x=dv(r);if(!x.d){alert('Choose Promote, Block or Ignore first.');return}ovr[k]={d:x.d,note:x.note||''};delete draft[k];persist();rRev()}
function rAna(){const{a}=agg(),w=(d,f)=>{const m=Math.max(1,...D4.map(z=>a[z][f]));return Math.max(1,a[d][f]/m*100)};
$('a1').innerHTML=D4.map(d=>`<div class="cp">${pill(d)}<div><div class="cpl"><span>${N(a[d].v)} conversions</span><span>${N(a[d].c)} clicks</span></div><div class="bt"><i class="${d}" style="width:${w(d,'v')}%"></i></div></div><div class="bv"><small>Value</small><b>${M(a[d].cv)}</b></div></div>`).join('');
$('a2').innerHTML=D4.map(d=>`<div class="br">${pill(d)}<div class="bt"><i class="${d}" style="width:${w(d,'c')}%"></i></div><b>${N(a[d].c)}</b></div>`).join('');
$('a3').innerHTML=D4.map(d=>`<div class="br" style="grid-template-columns:130px 1fr 110px">${pill(d)}<div class="bt"><i class="${d}" style="width:${w(d,'k')}%"></i></div><b>${M(a[d].k)}</b></div>`).join('');
setDonut('dc2','dv2','cf2')}
function rExp(){$('xinfo').textContent=N(Object.keys(ovr).length)+' reviewer corrections saved in this browser. negatives.csv has '+N(rows.filter(r=>fin(r)==='block').length)+' terms, keywords.csv has '+N(rows.filter(r=>fin(r)==='promote').length)+' terms.'}
function dl(name,H,A){const b=new Blob([[H,...A].map(r=>r.map(x=>`"${String(x==null?'':x).replace(/"/g,'""')}"`).join(',')).join('\n')],{type:'text/csv'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;a.click()}
function exAll(){dl('triage_results.csv',['query','campaign','ad_group','match_type','impressions','clicks','cost','conversions','conversion_value','triage_decision','confidence','reason','hint','reviewer_decision','reviewer_note','final_decision'],rows.map(r=>{const o=ovr[key(r)]||{};return[r.q,r.camp,r.ag,r.mt,r.i,r.c,r.k,r.v,r.cv,r.d,r.cf,r.why,r.h,o.d||'',o.note||'',fin(r)]}))}
function exNeg(){dl('negatives.csv',['campaign','ad_group','negative_keyword','match_type','reason'],rows.filter(r=>fin(r)==='block').map(r=>[r.camp,r.ag,r.q,'exact',r.why]))}
function exKw(){dl('keywords.csv',['campaign','ad_group','keyword','match_type','reason'],rows.filter(r=>fin(r)==='promote').map(r=>[r.camp,r.ag,r.q,'exact',r.why]))}
function exClear(){if(confirm('Remove all saved reviewer decisions from this browser?')){ovr={};persist();rExp();badge()}}
function pf(f){file=f||null;$('fname').textContent=f?f.name:'Drop your report here';$('goBtn').disabled=!f}
async function run(){if(!file)return;const b=$('goBtn');b.textContent='Processing...';b.disabled=true;try{const r=await fetch('/triage',{method:'POST',body:file});if(!r.ok)throw new Error(await r.text());rows=await r.json();$('fk').innerHTML='';go('overview')}catch(e){alert('Upload failed. Open the app through python server.py (http://localhost:8000). '+e.message)}b.textContent='Run triage';b.disabled=false}
go('overview');
</script></body></html>"""


def to_rows(out):
    out = out.copy()
    for c in ["query", "campaign", "ad_group", "match_type", "reason", "hint", "confidence", "decision"]:
        if c not in out.columns:
            out[c] = ""
    for c in ["impressions", "clicks", "conversions", "cost", "conversion_value", "n_rows"]:
        if c not in out.columns:
            out[c] = 0
    out = out.fillna("")
    rows = []
    for r in out.to_dict("records"):
        rows.append({"q": str(r["query"]), "camp": str(r["campaign"]), "ag": str(r["ad_group"]),
                     "mt": str(r["match_type"]), "i": float(r["impressions"] or 0),
                     "c": float(r["clicks"] or 0), "v": float(r["conversions"] or 0),
                     "k": round(float(r["cost"] or 0), 2), "cv": round(float(r["conversion_value"] or 0), 2),
                     "d": r["decision"], "cf": r["confidence"], "why": str(r["reason"]),
                     "h": str(r["hint"]), "n": int(r["n_rows"] or 1)})
    return rows


def rules_html():
    g = lambda k, d: getattr(C, k, d)
    items = [
        "<b>1. Pool the evidence.</b> Rows with the same query, campaign and ad group (different match types) are added together first.",
        "<b>2. Compare with the campaign's own rate.</b> Each campaign has its own normal conversion rate, so a term is judged against its campaign.",
        f"<b>3. Abstain on thin data.</b> Fewer than {g('MIN_CLICKS',10)} clicks means human review. 2 clicks and 1 conversion is noise.",
        f"<b>4. Block.</b> Rate below the campaign rate and a binomial test says the chance of bad luck is under {g('ALPHA_BLOCK',0.05)*100:g}%.",
        f"<b>5. Promote.</b> At least {g('MIN_PROMOTE_CONV',2)} conversions, rate at least {g('MIN_LIFT',1.5)}x the campaign rate, and chance of luck under {g('ALPHA_PROMOTE',0.01)*100:g}%.",
        "<b>6. Hints.</b> Word-level evidence for review terms only (each term capped at 50 clicks). A human makes the call.",
        "<b>7. Reason on every row</b> with the numbers, so it can be checked before action.",
    ]
    return "".join(f'<div class="rule">{x}</div>' for x in items)


def render(rows, dest="dashboard.html"):
    data = json.dumps(rows, separators=(",", ":")).replace("</", "<\\/")
    h = HTML.replace("__DATA__", data).replace("__RULES__", rules_html())
    open(dest, "w", encoding="utf-8").write(h)
    print("Wrote", dest, "with", len(rows), "terms")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "output.csv"
    render(to_rows(pd.read_csv(src)))
