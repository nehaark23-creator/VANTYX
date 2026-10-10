src = open("build_dashboard.py", encoding="utf-8").read()

if "uploadCSV" in src:
    print("Already patched. Nothing to do.")
    raise SystemExit

edits = []

# Edit 1: upload bar
edits.append(('''<section id="overview">''',
'''<div class="upbar"><label class="upl">Upload CSV<input type="file" accept=".csv" hidden onchange="uploadCSV(this)"></label><span class="small" id="upStatus">Showing the default dataset. Upload a search-terms CSV to run the triage on it.</span></div>
<section id="overview">'''))

# Edit 2: css
edits.append(('''.hidden{display:none}''',
'''.hidden{display:none}
.upbar{display:flex;align-items:center;gap:14px;margin-bottom:18px}
.upl{background:var(--blue);color:#fff;border-radius:8px;padding:10px 16px;font-size:13px;font-weight:600;cursor:pointer}'''))

# Edit 3: data loading becomes a function
edits.append(('''const D = __DATA__;
const R = D.rows.map(a => ({q:a[0], m:a[1], c:a[2], g:a[3], clicks:a[4], conv:a[5],
  cost:a[6], dec:a[7], conf:a[8], reason:a[9], word:a[10], key:a[0]+"|"+a[2]+"|"+a[3]}));
R.sort((a,b) => b.cost - a.cost);

let corr = {};
try { corr = JSON.parse(localStorage.getItem("corr_" + D.id) || "{}"); } catch(e) {}''',
'''let D, R, corr = {};
function setData(data){
  D = data;
  R = D.rows.map(a => ({q:a[0], m:a[1], c:a[2], g:a[3], clicks:a[4], conv:a[5],
    cost:a[6], dec:a[7], conf:a[8], reason:a[9], word:a[10], key:a[0]+"|"+a[2]+"|"+a[3]}));
  R.sort((a,b) => b.cost - a.cost);
  corr = {};
  try { corr = JSON.parse(localStorage.getItem("corr_" + D.id) || "{}"); } catch(e) {}
  selWord = null; page = 0;
}'''))

# Edit 5 (before edit 4, so the anchors do not clash): first call
edits.append(('''
renderRules(); renderAll();
</script>''',
'''
setData(__DATA__); renderRules(); renderAll();
</script>'''))

# Edit 4: upload function
edits.append(('''function renderAll(){ renderOverview(); renderTerms(); renderReview(); }''',
'''function renderAll(){ renderOverview(); renderTerms(); renderReview(); }

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
}'''))

for i, (old, new) in enumerate(edits, 1):
    n = src.count(old)
    if n != 1:
        print(f"Edit {i} failed: found {n} matches (expected 1). Nothing was changed.")
        raise SystemExit
    src = src.replace(old, new)

open("build_dashboard.py", "w", encoding="utf-8").write(src)
print("All 5 edits applied.")