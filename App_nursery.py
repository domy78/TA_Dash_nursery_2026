"""
Tableau de Bord — Pépinières
Flask + HTML/CSS/JavaScript (Chart.js + Plotly.js)
Lancer : py App_nursery.py
Ouvrir  : http://127.0.0.1:8051
"""

import json
import pandas as pd
import numpy as np
from flask import Flask, jsonify

app = Flask(__name__)

# ── Chargement & nettoyage ────────────────────────────────────────────────────
df = pd.read_excel("Tableau_de_bord_pepinieres (version 1).xlsx")
df["Semés"]            = pd.to_numeric(df["Semés"], errors="coerce").fillna(0).astype(int)
df["Taux_Germination"] = pd.to_numeric(df["Taux_Germination"], errors="coerce")
df["Cause_mortalité"]  = df["Cause_mortalité"].fillna("")
df["Problèmes"]        = df["Problèmes"].fillna("")

RECORDS = []
for _, r in df.iterrows():
    RECORDS.append({
        "Pays":            str(r["Pays"]),
        "Région":          str(r["Région"]),
        "Organisation":    str(r["Organisation"]),
        "Projet":          str(r["Projet"]),
        "Espèce":          str(r["Espèce"]),
        "Trimestre":       str(r["Trimestre"]),
        "Semés":           int(r["Semés"]),
        "Germés":          int(r["Germés"]),
        "Distribués":      int(r["Distribués"]),
        "Morts":           int(r["Morts"]),
        "Taux_Germination":float(r["Taux_Germination"]) if pd.notna(r["Taux_Germination"]) else None,
        "Capacité":        int(r["Capacité"]),
        "Pots_préparés":   int(r["Pots_préparés"]),
        "Cause_mortalité": str(r["Cause_mortalité"]) if r["Cause_mortalité"] else "",
        "Problèmes":       str(r["Problèmes"]) if r["Problèmes"] else "",
    })

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/api/data")
def api_data():
    return jsonify(RECORDS)

@app.route("/")
def index():
    return HTML

# ── Template HTML ─────────────────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tableau de Bord — Pépinières</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:#0e1a14;font-family:'Outfit',sans-serif;color:#e2f0e6;min-height:100vh}
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:#0e1a14}
::-webkit-scrollbar-thumb{background:#2a3d28;border-radius:3px}

/* Header */
.header{background:linear-gradient(135deg,#162310,#0e1a14);border-bottom:1px solid #2a3d28;
  padding:16px 32px;display:flex;align-items:center;justify-content:space-between}
.header-title{display:flex;align-items:center;gap:12px}
.header-title h1{font-size:1.1rem;font-weight:700;color:#e2f0e6}
.header-title span{font-size:.78rem;color:#7aab82;margin-left:8px}
.header-meta{font-size:.75rem;color:#7aab82;font-family:monospace}

/* Main container */
.main{padding:24px 32px;max-width:1500px;margin:0 auto}

/* Card */
.card{background:#162310;border:1px solid #2a3d28;border-radius:14px;padding:20px 22px;margin-bottom:16px}

/* Filters */
.filters-row{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end}
.filter-group{display:flex;flex-direction:column;gap:6px;flex:1;min-width:150px}
.filter-group label{font-size:.7rem;color:#7aab82;text-transform:uppercase;letter-spacing:.07em}
.filter-group select{
  background:#1a2e18;border:1px solid #2a3d28;color:#e2f0e6;
  padding:8px 12px;border-radius:8px;font-family:'Outfit',sans-serif;
  font-size:13px;cursor:pointer;appearance:none;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%237aab82' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 10px center;padding-right:30px;
}
.filter-group select:focus{outline:none;border-color:#4ade80}
.filter-group select option{background:#1a2e18;color:#e2f0e6}
.btn-reset{background:none;border:1px solid #2a3d28;color:#7aab82;
  padding:8px 18px;border-radius:8px;cursor:pointer;font-family:'Outfit',sans-serif;
  font-size:.75rem;letter-spacing:.06em;text-transform:uppercase;
  transition:all .2s;align-self:flex-end;height:38px}
.btn-reset:hover{border-color:#4ade80;color:#4ade80}

/* KPI grid */
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px}
.kpi-card{background:#162310;border:1px solid #2a3d28;border-radius:14px;
  padding:18px 20px;border-top-width:3px}
.kpi-icon{font-size:1.5rem;margin-bottom:8px}
.kpi-label{font-size:.7rem;color:#7aab82;text-transform:uppercase;letter-spacing:.08em}
.kpi-value{font-size:1.6rem;font-weight:700;color:#e2f0e6;margin:4px 0}
.kpi-sub{font-size:.72rem}

/* Chart grids */
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}
.grid-2-left{display:grid;grid-template-columns:1.4fr 1fr;gap:16px;margin-bottom:16px}
.grid-2-right{display:grid;grid-template-columns:1.2fr 1fr;gap:16px;margin-bottom:16px}
.chart-title{font-size:.85rem;font-weight:600;color:#e2f0e6;margin-bottom:12px}
canvas{width:100%!important}

/* Table */
.table-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:12.5px}
thead th{background:#0e1a14;color:#7aab82;font-weight:600;font-size:11px;
  text-transform:uppercase;letter-spacing:.06em;padding:10px 14px;
  border-bottom:1px solid #2a3d28;text-align:left;cursor:pointer;white-space:nowrap}
thead th:hover{color:#4ade80}
tbody tr{border-bottom:1px solid #1f2f1e}
tbody tr:nth-child(even){background:#131f10}
tbody td{padding:9px 14px;color:#e2f0e6;white-space:nowrap}
.pager{display:flex;gap:8px;align-items:center;margin-top:14px;font-size:.8rem;color:#7aab82}
.pager button{background:none;border:1px solid #2a3d28;color:#7aab82;
  padding:4px 10px;border-radius:6px;cursor:pointer;font-family:'Outfit',sans-serif}
.pager button:hover{border-color:#4ade80;color:#4ade80}
.pager button:disabled{opacity:.35;cursor:default}
.pager span{color:#e2f0e6}

@media(max-width:900px){
  .kpi-grid{grid-template-columns:repeat(2,1fr)}
  .grid-2,.grid-2-left,.grid-2-right{grid-template-columns:1fr}
  .main{padding:16px}
  .header{padding:12px 16px}
}
</style>
</head>
<body>

<!-- Header -->
<div class="header">
  <div class="header-title">
    <span style="font-size:1.6rem">🌱</span>
    <div>
      <h1>Tableau de Bord — Pépinières
        <span>Suivi de la production &amp; mortalité 2025</span>
      </h1>
    </div>
  </div>
  <div class="header-meta">2025 | 5 pays | <span id="total-count">—</span> enregistrements</div>
</div>

<div class="main">

  <!-- Filtres -->
  <div class="card">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px">
      <span>🔍</span>
      <span style="font-weight:600;font-size:.9rem">Filtres</span>
    </div>
    <div class="filters-row">
      <div class="filter-group">
        <label>Pays</label>
        <select id="f-pays" onchange="updateAll()">
          <option value="">Tous les pays</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Région</label>
        <select id="f-region" onchange="updateAll()">
          <option value="">Toutes les régions</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Projet</label>
        <select id="f-type" onchange="updateAll()">
          <option value="">Tous les projets</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Trimestre</label>
        <select id="f-trim" onchange="updateAll()">
          <option value="">Tous les trimestres</option>
        </select>
      </div>
      <button class="btn-reset" onclick="resetFilters()">Réinitialiser</button>
    </div>
  </div>

  <!-- KPIs -->
  <div class="kpi-grid">
    <div class="kpi-card" style="border-top-color:#4ade80">
      <div class="kpi-icon">🌱</div>
      <div class="kpi-label">Total Semés</div>
      <div class="kpi-value" id="kpi-semes-val">—</div>
      <div class="kpi-sub" style="color:#4ade80" id="kpi-semes-sub"></div>
    </div>
    <div class="kpi-card" style="border-top-color:#86efac">
      <div class="kpi-icon">🌿</div>
      <div class="kpi-label">Total Germés</div>
      <div class="kpi-value" id="kpi-germes-val">—</div>
      <div class="kpi-sub" style="color:#86efac" id="kpi-germes-sub"></div>
    </div>
    <div class="kpi-card" style="border-top-color:#60a5fa">
      <div class="kpi-icon">🚚</div>
      <div class="kpi-label">Total Distribués</div>
      <div class="kpi-value" id="kpi-distrib-val">—</div>
      <div class="kpi-sub" style="color:#60a5fa" id="kpi-distrib-sub"></div>
    </div>
    <div class="kpi-card" style="border-top-color:#f87171">
      <div class="kpi-icon">💀</div>
      <div class="kpi-label">Total Morts</div>
      <div class="kpi-value" id="kpi-morts-val">—</div>
      <div class="kpi-sub" style="color:#f87171" id="kpi-morts-sub"></div>
    </div>
    <div class="kpi-card" style="border-top-color:#fbbf24">
      <div class="kpi-icon">📈</div>
      <div class="kpi-label">Taux Germination</div>
      <div class="kpi-value" id="kpi-txgerm-val">—</div>
      <div class="kpi-sub" style="color:#fbbf24" id="kpi-txgerm-sub"></div>
    </div>
    <div class="kpi-card" style="border-top-color:#f87171">
      <div class="kpi-icon">📉</div>
      <div class="kpi-label">Taux Mortalité</div>
      <div class="kpi-value" id="kpi-txmort-val">—</div>
      <div class="kpi-sub" style="color:#f87171" id="kpi-txmort-sub"></div>
    </div>
    <div class="kpi-card" style="border-top-color:#c084fc">
      <div class="kpi-icon">🏭</div>
      <div class="kpi-label">Capacité Totale</div>
      <div class="kpi-value" id="kpi-capa-val">—</div>
      <div class="kpi-sub" style="color:#c084fc" id="kpi-capa-sub"></div>
    </div>
    <div class="kpi-card" style="border-top-color:#fbbf24">
      <div class="kpi-icon">🪴</div>
      <div class="kpi-label">Pots Préparés</div>
      <div class="kpi-value" id="kpi-pots-val">—</div>
      <div class="kpi-sub" style="color:#fbbf24" id="kpi-pots-sub"></div>
    </div>
  </div>

  <!-- Ligne 1: Histogramme pays + Carte -->
  <div class="grid-2-left">
    <div class="card">
      <div class="chart-title">📊 Production par pays</div>
      <canvas id="chart-pays" height="300"></canvas>
    </div>
    <div class="card">
      <div class="chart-title">🗺️ Carte géographique</div>
      <div id="chart-carte" style="height:300px"></div>
    </div>
  </div>

  <!-- Ligne 2: Camemberts -->
  <div class="grid-2">
    <div class="card">
      <div class="chart-title">🥧 Germés par projet</div>
      <canvas id="chart-pie-org" height="260"></canvas>
    </div>
    <div class="card">
      <div class="chart-title">🌿 Semés par espèce</div>
      <canvas id="chart-pie-esp" height="260"></canvas>
    </div>
  </div>

  <!-- Ligne 3: Courbe trimestre + Causes -->
  <div class="grid-2-right">
    <div class="card">
      <div class="chart-title">📈 Évolution par trimestre</div>
      <canvas id="chart-trim" height="260"></canvas>
    </div>
    <div class="card">
      <div class="chart-title">💀 Causes de mortalité</div>
      <canvas id="chart-causes" height="260"></canvas>
    </div>
  </div>

  <!-- Ligne 4: Région + Problèmes -->
  <div class="grid-2">
    <div class="card">
      <div class="chart-title">📊 Production par région</div>
      <canvas id="chart-region" height="250"></canvas>
    </div>
    <div class="card">
      <div class="chart-title">⚠️ Problèmes signalés</div>
      <canvas id="chart-prob" height="250"></canvas>
    </div>
  </div>

  <!-- Tableau -->
  <div class="card">
    <div class="chart-title">📋 Données détaillées</div>
    <div class="table-wrap">
      <table id="data-table">
        <thead>
          <tr>
            <th onclick="sortTable(0)">Pays</th>
            <th onclick="sortTable(1)">Région</th>
            <th onclick="sortTable(2)">Organisation</th>
            <th onclick="sortTable(3)">Type</th>
            <th onclick="sortTable(4)">Espèce</th>
            <th onclick="sortTable(5)">Trimestre</th>
            <th onclick="sortTable(6)">Semés</th>
            <th onclick="sortTable(7)">Germés</th>
            <th onclick="sortTable(8)">Distribués</th>
            <th onclick="sortTable(9)">Morts</th>
            <th onclick="sortTable(10)">Taux Germ.</th>
            <th onclick="sortTable(11)">Cause mortalité</th>
          </tr>
        </thead>
        <tbody id="table-body"></tbody>
      </table>
    </div>
    <div class="pager">
      <button id="btn-prev" onclick="prevPage()">&#8592; Préc.</button>
      <span>Page <span id="page-num">1</span> / <span id="page-total">1</span></span>
      <button id="btn-next" onclick="nextPage()">Suiv. &#8594;</button>
      <span style="margin-left:auto" id="row-count"></span>
    </div>
  </div>

</div><!-- /main -->

<script>
// ── Constantes ────────────────────────────────────────────────────────────────
const C = {
  a1:'#4ade80', a2:'#86efac', a3:'#fbbf24', a4:'#f87171',
  a5:'#60a5fa', a6:'#c084fc', text:'#e2f0e6', sub:'#7aab82',
  grid:'#1f2f1e', bg:'rgba(0,0,0,0)', card:'#162310'
};
const PIECOLORS = [C.a1,C.a2,C.a3,C.a4,C.a5,C.a6,'#34d399','#fb923c'];
const TRIM_ORDER = ['T1 2025','T2 2025','T3 2025','T4 2025'];
const GPS = {
  'Burkina Faso':[12.36,-1.53],
  'Mali':[17.57,-3.99],
  'Niger':[17.60,8.08],
  'Ghana':[7.95,-1.02],
  'Sénégal':[14.50,-14.45]
};

// ── État ──────────────────────────────────────────────────────────────────────
let allData = [];
let filteredData = [];
let charts = {};
let tablePage = 0;
const PAGE_SIZE = 12;
let tableData = [];
let sortCol = -1, sortAsc = true;

// ── Utilitaires ───────────────────────────────────────────────────────────────
function fmtK(n){
  if(n==null||isNaN(n)) return '0';
  if(n>=1e6) return (n/1e6).toFixed(1)+'M';
  if(n>=1e3) return (n/1e3).toFixed(1)+'k';
  return Math.round(n).toString();
}
function sum(arr,key){ return arr.reduce((s,r)=>s+(r[key]||0),0); }
function mean(arr,key){
  const vals = arr.filter(r=>r[key]!=null).map(r=>r[key]);
  return vals.length ? vals.reduce((a,b)=>a+b,0)/vals.length : 0;
}
function groupSum(arr, groupKey, sumKeys){
  const map={};
  arr.forEach(r=>{
    const k=r[groupKey];
    if(!map[k]){map[k]={label:k};sumKeys.forEach(s=>map[k][s]=0);}
    sumKeys.forEach(s=>map[k][s]+=(r[s]||0));
  });
  return Object.values(map);
}

// ── Chart.js defaults ─────────────────────────────────────────────────────────
Chart.defaults.color = C.text;
Chart.defaults.borderColor = C.grid;
Chart.defaults.font.family = 'Outfit, sans-serif';

function baseScales(){
  return {
    x:{grid:{color:C.grid},ticks:{color:C.sub}},
    y:{grid:{color:C.grid},ticks:{color:C.sub}}
  };
}
function baseLegend(){
  return {labels:{color:C.text,boxWidth:12,padding:14}};
}

// ── Initialisation des graphiques ─────────────────────────────────────────────
function initCharts(){
  // 1. Bar pays
  charts.pays = new Chart(document.getElementById('chart-pays'),{
    type:'bar',
    data:{labels:[],datasets:[
      {label:'Semés',     backgroundColor:C.a1,data:[]},
      {label:'Germés',    backgroundColor:C.a2,data:[]},
      {label:'Distribués',backgroundColor:C.a5,data:[]},
      {label:'Morts',     backgroundColor:C.a4,data:[]},
    ]},
    options:{
      responsive:true,
      plugins:{legend:baseLegend()},
      scales:baseScales(),
      backgroundColor:C.bg,
    }
  });

  // 2. Pie org
  charts.pieOrg = new Chart(document.getElementById('chart-pie-org'),{
    type:'doughnut',
    data:{labels:[],datasets:[{data:[],backgroundColor:PIECOLORS,borderColor:'#0e1a14',borderWidth:2}]},
    options:{
      responsive:true,
      cutout:'52%',
      plugins:{legend:baseLegend()}
    }
  });

  // 3. Pie espèce
  charts.pieEsp = new Chart(document.getElementById('chart-pie-esp'),{
    type:'doughnut',
    data:{labels:[],datasets:[{data:[],backgroundColor:[...PIECOLORS].reverse(),borderColor:'#0e1a14',borderWidth:2}]},
    options:{
      responsive:true,
      cutout:'52%',
      plugins:{legend:baseLegend()}
    }
  });

  // 4. Line trimestre
  charts.trim = new Chart(document.getElementById('chart-trim'),{
    type:'line',
    data:{labels:TRIM_ORDER,datasets:[
      {label:'Semés',     borderColor:C.a1,backgroundColor:'rgba(74,222,128,0.08)',fill:true, data:[],tension:.3,pointRadius:5},
      {label:'Germés',    borderColor:C.a2,backgroundColor:'transparent',          fill:false,data:[],tension:.3,pointRadius:5},
      {label:'Distribués',borderColor:C.a5,backgroundColor:'transparent',          fill:false,data:[],tension:.3,pointRadius:5},
      {label:'Morts',     borderColor:C.a4,backgroundColor:'transparent',          fill:false,data:[],tension:.3,pointRadius:5},
    ]},
    options:{
      responsive:true,
      plugins:{legend:baseLegend()},
      scales:baseScales()
    }
  });

  // 5. Horizontal bar causes
  charts.causes = new Chart(document.getElementById('chart-causes'),{
    type:'bar',
    data:{labels:[],datasets:[{data:[],backgroundColor:PIECOLORS,borderWidth:0}]},
    options:{
      indexAxis:'y',
      responsive:true,
      plugins:{legend:{display:false}},
      scales:{
        x:{grid:{color:C.grid},ticks:{color:C.sub}},
        y:{grid:{color:C.grid},ticks:{color:C.sub}}
      }
    }
  });

  // 6. Bar région
  charts.region = new Chart(document.getElementById('chart-region'),{
    type:'bar',
    data:{labels:[],datasets:[
      {label:'Semés',     backgroundColor:C.a1,data:[]},
      {label:'Germés',    backgroundColor:C.a2,data:[]},
      {label:'Distribués',backgroundColor:C.a5,data:[]},
    ]},
    options:{
      responsive:true,
      plugins:{legend:baseLegend()},
      scales:baseScales()
    }
  });

  // 7. Horizontal bar problèmes
  charts.prob = new Chart(document.getElementById('chart-prob'),{
    type:'bar',
    data:{labels:[],datasets:[{data:[],backgroundColor:C.a3,borderWidth:0}]},
    options:{
      indexAxis:'y',
      responsive:true,
      plugins:{legend:{display:false}},
      scales:{
        x:{grid:{color:C.grid},ticks:{color:C.sub}},
        y:{grid:{color:C.grid},ticks:{color:C.sub}}
      }
    }
  });

  // 8. Carte géo (Plotly)
  Plotly.newPlot('chart-carte',[{
    type:'scattergeo',lat:[],lon:[],mode:'markers',
    marker:{size:[],color:[],colorscale:'Greens',showscale:false}
  }],{
    paper_bgcolor:'rgba(0,0,0,0)',
    geo:{
      scope:'africa',bgcolor:'rgba(0,0,0,0)',
      landcolor:'#1a2e18',oceancolor:'#0e1a14',
      coastlinecolor:'#2a3d28',countrycolor:'#2a3d28',
      showland:true,showocean:true,showcountries:true,showcoastlines:true,
      center:{lat:14,lon:-2},projection:{scale:3.5}
    },
    margin:{l:0,r:0,t:0,b:0},
    font:{color:C.text}
  },{displayModeBar:false,responsive:true});
}

// ── Mise à jour de tous les composants ────────────────────────────────────────
function updateAll(){
  const d = getFiltered();
  filteredData = d;
  document.getElementById('total-count').textContent = d.length;

  updateKPIs(d);
  updateChartPays(d);
  updateChartCarte(d);
  updateChartPieOrg(d);
  updateChartPieEsp(d);
  updateChartTrim(d);
  updateChartCauses(d);
  updateChartRegion(d);
  updateChartProb(d);
  tablePage = 0;
  renderTable(d);
}

// ── Filtrage ──────────────────────────────────────────────────────────────────
function getFiltered(){
  const pays   = document.getElementById('f-pays').value;
  const region = document.getElementById('f-region').value;
  const type   = document.getElementById('f-type').value;
  const trim   = document.getElementById('f-trim').value;
  return allData.filter(r=>
    (!pays   || r['Pays']===pays) &&
    (!region || r['Région']===region) &&
    (!type   || r['Projet']===type) &&
    (!trim   || r['Trimestre']===trim)
  );
}

function resetFilters(){
  ['f-pays','f-region','f-type','f-trim'].forEach(id=>{
    document.getElementById(id).value='';
  });
  updateAll();
}

// ── KPIs ──────────────────────────────────────────────────────────────────────
function updateKPIs(d){
  const semes   = sum(d,'Semés');
  const germes  = sum(d,'Germés');
  const distrib = sum(d,'Distribués');
  const morts   = sum(d,'Morts');
  const capa    = sum(d,'Capacité');
  const pots    = sum(d,'Pots_préparés');
  const txGerm  = mean(d,'Taux_Germination');
  const txMortArr = d.filter(r=>r.Germés>0).map(r=>r.Morts/r.Germés);
  const txMort  = txMortArr.length ? txMortArr.reduce((a,b)=>a+b,0)/txMortArr.length : 0;

  set('kpi-semes-val',  fmtK(semes));
  set('kpi-semes-sub',  d.length+' enregistrements');
  set('kpi-germes-val', fmtK(germes));
  set('kpi-germes-sub', (txGerm*100).toFixed(1)+'% taux germ. moyen');
  set('kpi-distrib-val',fmtK(distrib));
  set('kpi-distrib-sub',(germes?(distrib/germes*100).toFixed(1):0)+'% des germés');
  set('kpi-morts-val',  fmtK(morts));
  set('kpi-morts-sub',  (germes?(morts/germes*100).toFixed(1):0)+'% des germés');
  set('kpi-txgerm-val', (txGerm*100).toFixed(1)+'%');
  set('kpi-txgerm-sub', 'taux moyen sur la sélection');
  set('kpi-txmort-val', (txMort*100).toFixed(1)+'%');
  set('kpi-txmort-sub', 'mortalité / germés');
  set('kpi-capa-val',   fmtK(capa));
  set('kpi-capa-sub',   d.length+' pépinières');
  set('kpi-pots-val',   fmtK(pots));
  set('kpi-pots-sub',   (capa?(pots/capa*100).toFixed(0):0)+'% de la capacité');
}
function set(id,v){document.getElementById(id).textContent=v;}

// ── Graphique 1 : Pays ────────────────────────────────────────────────────────
function updateChartPays(d){
  const g = groupSum(d,'Pays',['Semés','Germés','Distribués','Morts']);
  const labels = g.map(r=>r.label);
  charts.pays.data.labels = labels;
  charts.pays.data.datasets[0].data = g.map(r=>r.Semés);
  charts.pays.data.datasets[1].data = g.map(r=>r.Germés);
  charts.pays.data.datasets[2].data = g.map(r=>r.Distribués);
  charts.pays.data.datasets[3].data = g.map(r=>r.Morts);
  charts.pays.update();
}

// ── Graphique 2 : Carte géo ────────────────────────────────────────────────────
function updateChartCarte(d){
  const map={};
  d.forEach(r=>{
    const p=r['Pays'];
    if(!map[p]) map[p]={semes:0,germes:0,morts:0};
    map[p].semes+=r.Semés; map[p].germes+=r.Germés; map[p].morts+=r.Morts;
  });
  const pays=Object.keys(map);
  const lats=pays.map(p=>GPS[p]?GPS[p][0]:0);
  const lons=pays.map(p=>GPS[p]?GPS[p][1]:0);
  const sizes=pays.map(p=>Math.min(50,Math.max(8,Math.sqrt(map[p].semes)*0.8)));
  const colors=pays.map(p=>map[p].germes);
  const texts=pays.map(p=>`<b>${p}</b><br>Semés: ${fmtK(map[p].semes)}<br>Germés: ${fmtK(map[p].germes)}<br>Morts: ${fmtK(map[p].morts)}`);
  Plotly.restyle('chart-carte',{
    lat:[lats],lon:[lons],
    'marker.size':[sizes],'marker.color':[colors],
    text:[texts],hoverinfo:'text',
    mode:'markers+text',textposition:'top center',
    textfont:{color:C.text,size:11},
    'marker.showscale':true,
    'marker.colorscale':'Greens',
    'marker.colorbar':{thickness:10,tickfont:{color:C.sub,size:9},title:{text:'Germés',font:{color:C.sub}}}
  });
}

// ── Graphique 3 : Pie org ────────────────────────────────────────────────────
function updateChartPieOrg(d){
  const g=groupSum(d,'Projet',['Germés']);
  charts.pieOrg.data.labels=g.map(r=>r.label);
  charts.pieOrg.data.datasets[0].data=g.map(r=>r.Germés);
  charts.pieOrg.update();
}

// ── Graphique 4 : Pie espèce ─────────────────────────────────────────────────
function updateChartPieEsp(d){
  const g=groupSum(d,'Espèce',['Semés']);
  charts.pieEsp.data.labels=g.map(r=>r.label);
  charts.pieEsp.data.datasets[0].data=g.map(r=>r.Semés);
  charts.pieEsp.update();
}

// ── Graphique 5 : Courbe trimestre ────────────────────────────────────────────
function updateChartTrim(d){
  const map={};
  TRIM_ORDER.forEach(t=>map[t]={Semés:0,Germés:0,Distribués:0,Morts:0});
  d.forEach(r=>{
    const t=r.Trimestre;
    if(map[t]){map[t].Semés+=r.Semés;map[t].Germés+=r.Germés;
               map[t].Distribués+=r.Distribués;map[t].Morts+=r.Morts;}
  });
  charts.trim.data.datasets[0].data = TRIM_ORDER.map(t=>map[t].Semés);
  charts.trim.data.datasets[1].data = TRIM_ORDER.map(t=>map[t].Germés);
  charts.trim.data.datasets[2].data = TRIM_ORDER.map(t=>map[t].Distribués);
  charts.trim.data.datasets[3].data = TRIM_ORDER.map(t=>map[t].Morts);
  charts.trim.update();
}

// ── Graphique 6 : Causes mortalité ────────────────────────────────────────────
function updateChartCauses(d){
  const cnt={};
  d.forEach(r=>{ if(r['Cause_mortalité']) cnt[r['Cause_mortalité']]=(cnt[r['Cause_mortalité']]||0)+1; });
  const entries=Object.entries(cnt).sort((a,b)=>b[1]-a[1]);
  charts.causes.data.labels=entries.map(e=>e[0]);
  charts.causes.data.datasets[0].data=entries.map(e=>e[1]);
  charts.causes.data.datasets[0].backgroundColor=PIECOLORS.slice(0,entries.length);
  charts.causes.update();
}

// ── Graphique 7 : Région ─────────────────────────────────────────────────────
function updateChartRegion(d){
  const g=groupSum(d,'Région',['Semés','Germés','Distribués']);
  charts.region.data.labels=g.map(r=>r.label);
  charts.region.data.datasets[0].data=g.map(r=>r.Semés);
  charts.region.data.datasets[1].data=g.map(r=>r.Germés);
  charts.region.data.datasets[2].data=g.map(r=>r.Distribués);
  charts.region.update();
}

// ── Graphique 8 : Problèmes ───────────────────────────────────────────────────
function updateChartProb(d){
  const cnt={};
  d.forEach(r=>{
    if(!r['Problèmes']) return;
    r['Problèmes'].split(',').forEach(p=>{
      const t=p.trim();
      if(t) cnt[t]=(cnt[t]||0)+1;
    });
  });
  const entries=Object.entries(cnt).sort((a,b)=>b[1]-a[1]);
  charts.prob.data.labels=entries.map(e=>e[0]);
  charts.prob.data.datasets[0].data=entries.map(e=>e[1]);
  charts.prob.update();
}

// ── Tableau ───────────────────────────────────────────────────────────────────
function renderTable(d){
  tableData = d;
  const total = Math.ceil(d.length/PAGE_SIZE)||1;
  if(tablePage>=total) tablePage=total-1;
  document.getElementById('page-num').textContent   = tablePage+1;
  document.getElementById('page-total').textContent = total;
  document.getElementById('row-count').textContent  = d.length+' lignes';
  document.getElementById('btn-prev').disabled = tablePage===0;
  document.getElementById('btn-next').disabled = tablePage>=total-1;

  const slice = d.slice(tablePage*PAGE_SIZE,(tablePage+1)*PAGE_SIZE);
  const tbody = document.getElementById('table-body');
  tbody.innerHTML = slice.map(r=>`
    <tr>
      <td>${r['Pays']}</td>
      <td>${r['Région']}</td>
      <td>${r['Organisation']}</td>
      <td>${r['Projet']}</td>
      <td>${r['Espèce']}</td>
      <td>${r['Trimestre']}</td>
      <td>${r['Semés'].toLocaleString()}</td>
      <td>${r['Germés'].toLocaleString()}</td>
      <td>${r['Distribués'].toLocaleString()}</td>
      <td style="color:${r['Morts']>500?'#f87171':'inherit'}">${r['Morts'].toLocaleString()}</td>
      <td style="color:${r['Taux_Germination']&&r['Taux_Germination']>0.85?'#4ade80':'inherit'}">
        ${r['Taux_Germination']!=null?(r['Taux_Germination']*100).toFixed(1)+'%':'—'}
      </td>
      <td>${r['Cause_mortalité']||'—'}</td>
    </tr>`).join('');
}

function prevPage(){ if(tablePage>0){tablePage--;renderTable(tableData);} }
function nextPage(){
  const total=Math.ceil(tableData.length/PAGE_SIZE);
  if(tablePage<total-1){tablePage++;renderTable(tableData);}
}

let sortDir = {};
function sortTable(col){
  const keys=['Pays','Région','Organisation','Projet','Espèce','Trimestre',
               'Semés','Germés','Distribués','Morts','Taux_Germination','Cause_mortalité'];
  const k=keys[col];
  sortDir[col] = !sortDir[col];
  tableData.sort((a,b)=>{
    const av=a[k]??'', bv=b[k]??'';
    return typeof av==='number'
      ? (sortDir[col]?av-bv:bv-av)
      : (sortDir[col]?String(av).localeCompare(String(bv)):String(bv).localeCompare(String(av)));
  });
  tablePage=0;
  renderTable(tableData);
}

// ── Remplissage des filtres ────────────────────────────────────────────────────
function populateFilters(data){
  const unique=(key)=>[...new Set(data.map(r=>r[key]))].filter(Boolean).sort();
  fillSelect('f-pays',   unique('Pays'));
  fillSelect('f-region', unique('Région'));
  fillSelect('f-type',   unique('Projet'));
  const trims = TRIM_ORDER.filter(t=>data.some(r=>r.Trimestre===t));
  fillSelect('f-trim', trims);
}
function fillSelect(id, values){
  const sel=document.getElementById(id);
  values.forEach(v=>{ const o=document.createElement('option'); o.value=o.textContent=v; sel.appendChild(o); });
}

// ── Point d'entrée ────────────────────────────────────────────────────────────
fetch('/api/data')
  .then(r=>r.json())
  .then(data=>{
    allData = data;
    populateFilters(data);
    initCharts();
    updateAll();
  })
  .catch(err=>console.error('Erreur chargement données:', err));
</script>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n✅  Dashboard Pépinières → http://127.0.0.1:8062\n")
    app.run(port=8062, debug=False)
