/* Showcase controls: provenance, shareable views, and a portable evidence brief. */
const surveyBreak = 'Survey break: the redesign began in January 2025. FY2025 combines Oct–Dec 2024 under the old survey with Jan–Sep 2025 under the new survey. Collection, sampling and weighting changed; differences cannot be attributed entirely to behavior.';
const metroLimit = 'MSA is metropolitan-area classification, not a rural/urban label. In January 2025, Large MSA expanded from the 30 largest metros to metros of at least 1 million people; about 11% of households moved from Other MSA to Large MSA. FY2025 mixes both definitions.';
const forecastLimit = 'Forecast caveat: exploratory aggregate projections use a 2023 cutoff and revised historical estimates. Sensitivity bands are not confidence intervals; the selected model may not beat a last-observation baseline.';
const pdfLink = (file, page) => new URL(`reports/${encodeURIComponent(file)}#page=${page}`, location.href).href;
const methodFile = '2025+HOUSEHOLD+MAIL+SURVEY.pdf';

const breakNote = document.createElement('p');
breakNote.className = 'notice warn';
breakNote.id = 'surveyBreak';
$('#trend').before(breakNote);
const originalChart = chart;
chart = function (selector, rows, projection = []) {
  const valid = rows.filter(r => Number.isFinite(r.value) && Number.isFinite(r.year));
  if (!valid.length) {
    $(selector).innerHTML = '<text x="70" y="130">No published observations for this selection.</text>';
    return;
  }
  originalChart(selector, valid, projection);
  const all = [...valid, ...projection];
  const minYear = Math.min(...all.map(r => r.year));
  const maxYear = Math.max(...all.map(r => r.year));
  const maxValue = Math.max(...all.map(r => r.high ?? r.value)) * 1.15;
  const x = year => 70 + (year - minYear) / Math.max(1, maxYear - minYear) * 860;
  const y = value => 265 - value / Math.max(1, maxValue) * 220;
  let marks = '';
  // A diamond records an edition change; it does not imply a behavior change.
  valid.forEach((r, i) => {
    if (i && r.edition !== valid[i - 1].edition) {
      marks += `<path d="M ${x(r.year)} ${y(r.value)-7} l 7 7 -7 7 -7 -7 Z" fill="white" stroke="#26384b" stroke-width="2"><title>Report edition ${r.edition}; ${r.file}, PDF p. ${r.page}</title></path>`;
    }
  });
  if (valid.some(r => r.year === 2025)) {
    const sx = x(2025);
    marks += `<line x1="${sx}" y1="28" x2="${sx}" y2="265" stroke="#526476" stroke-width="2" stroke-dasharray="4 4"/><text x="${sx-8}" y="20" text-anchor="end">2025 survey break †</text>`;
  }
  const last = all.at(-1);
  marks += `<text x="${x(last.year)-8}" y="${Math.max(40,y(last.value)-14)}" text-anchor="end" font-weight="700">${projection.length?'Projection':'Published'}: ${fmt(last.value)}</text>`;
  $(selector).insertAdjacentHTML('beforeend', marks);
  $(selector).setAttribute('aria-label', `${projection.length?'History and exploratory projection':'Published history'}: ${valid[0].year} to ${last.year}. Latest value ${fmt(last.value)}.`);
};
const originalTrend = renderTrend;
renderTrend = function () {
  const ds = selection();
  if (!ds.length) {
    $('#latest').textContent = '—'; $('#change').textContent = '—'; $('#count').textContent = '0';
    $('#numericSummary').textContent = 'No published observations match these filters. Choose another report or year range.';
    $('#trendRows').replaceChildren(); chart('#trend', []); return;
  }
  originalTrend();
  const a = ds[0], b = ds.at(-1);
  const pct = a.value ? 100*(b.value/a.value-1) : null;
  $('#chartTitle').textContent = ds.length===1 ? `${b.market}: ${fmt(b.value)} in ${b.year}` : `${b.market} ${b.value<a.value?'fell':b.value>a.value?'rose':'was unchanged'}${pct===null?'':` ${Math.abs(pct).toFixed(1)}%`}, ${a.year}–${b.year}`;
  $('#numericSummary').textContent += ' Published estimates may reflect revisions and classification changes, not only behavior.';
  if(a.value===0) { $('#change').textContent='Not defined'; $('#numericSummary').textContent=`${b.market}: ${fmt(a.value)} in ${a.year} and ${fmt(b.value)} in ${b.year}. Percentage change is undefined for a zero baseline. Unit: ${b.unit}.`; }
  legend.textContent=`${b.unit} · ${$('#view').value==='edition'?'Report edition '+b.edition:'Latest available estimates'} · ● Published observation · ◇ Different source edition · † Survey redesign`;
  breakNote.hidden = !ds.some(r=>r.year===2025);
  breakNote.innerHTML = `${esc(surveyBreak)} <a href="${pdfLink(methodFile,75)}" target="_blank" rel="noopener">Appendix B, PDF pp. 75–77</a>`;
};
const legend = document.createElement('p'); legend.className='chart-key';
legend.textContent='● Published observation   ◇ A different report edition supplies this estimate   † Survey redesign';
$('#trend').after(legend);

// Add comparisons without silently substituting age shares for received volume.
const historyCard = document.createElement('div'); historyCard.className='card';
historyCard.innerHTML = `<h2>Households over time</h2><p>Published comparison columns in the 2025 report. These comparisons span the survey redesign.</p><div class="controls"><label for="historyDimension">Comparison<select id="historyDimension"><option value="Packages by metro classification">Packages received by metro classification</option><option value="Age shares">Age: share of mail and households</option></select></label><label for="historyYear">Survey year<select id="historyYear"><option>2015</option><option>2020</option><option selected>2025</option></select></label><label for="historyMetric">Measure<select id="historyMetric"></select></label><button id="historyCsv">Export comparison CSV</button></div><div id="historyBars"></div><p id="historyMeaning"></p><p id="historyNotes" class="notice warn"></p><div id="historySource"></div><details><summary>All published comparison values</summary><table><thead><tr><th>Group</th><th>2015</th><th>2020</th><th>2025 †</th></tr></thead><tbody id="historyTable"></tbody></table></details>`;
$('#demographics').append(historyCard);
function historyRows() { return (DATA.demographicHistory||[]).filter(r=>r.dimension===$('#historyDimension').value && String(r.year)===$('#historyYear').value && r.metric===$('#historyMetric').value); }
function renderHistory(reset=false) {
  const available=(DATA.demographicHistory||[]).filter(r=>r.dimension===$('#historyDimension').value);
  if(reset) options($('#historyMetric'), [...new Set(available.map(r=>r.metric))]);
  const rows=historyRows();
  if(!rows.length) { $('#historyBars').textContent='No published values are available for this selection.'; $('#historyTable').replaceChildren(); $('#historySource').replaceChildren(); return; }
  const max=Math.max(...rows.map(r=>r.value),1);
  $('#historyBars').innerHTML=rows.map(r=>`<div class="barrow"><span>${esc(r.group)}</span><div class="bar" style="width:${r.value/max*100}%"></div><b>${fmt(r.value)}${r.unit==='Percent'?'%':''}</b></div>`).join('');
  $('#historyMeaning').textContent=`${rows[0].metric} · ${rows[0].unit} · ${rows[0].year}. These are the report's estimates, not a harmonized constant-method series.`;
  $('#historyNotes').textContent=surveyBreak+($('#historyDimension').value.startsWith('Packages')?' '+metroLimit:' Shares of households and shares of mail are percentages, not pieces received.');
  $('#historySource').innerHTML=source(rows[0]);
  $('#historyTable').innerHTML=rows.map(r=>`<tr><td>${esc(r.group)}</td>${[2015,2020,2025].map(year=>{const v=available.find(x=>x.group===r.group&&x.metric===r.metric&&x.year===year);return `<td>${v?fmt(v.value):'Not reported'}</td>`;}).join('')}</tr>`).join('');
}
$('#historyDimension').onchange=()=>renderHistory(true);
$('#historyYear').onchange=()=>renderHistory(); $('#historyMetric').onchange=()=>renderHistory();
$('#historyCsv').onclick=()=>download('mailers-demographic-comparison.csv',historyRows());
renderHistory(true);
const sourceNote=document.createElement('div'); sourceNote.className='notice warn';
sourceNote.innerHTML=`<strong>January 2025 is a survey break.</strong> ${esc(surveyBreak)} The new design uses an address-based frame and targeted strata for lower-income and renter areas, with web or telephone-assisted participation. The earlier survey offered paper and online diaries—not paper alone. The reports do not establish a simple claim that the sampling frame became “wider.” ${esc(metroLimit)} <a href="${pdfLink(methodFile,75)}">Methodology, PDF p. 75</a> · <a href="${pdfLink(methodFile,76)}">Collection, p. 76</a> · <a href="${pdfLink(methodFile,80)}">MSA definitions, p. 80</a>`;
$('#sources .card').prepend(sourceNote);

function saveText(name, text) {
  const blob = new Blob([text], {type:'text/markdown;charset=utf-8'});
  const url=URL.createObjectURL(blob), a=document.createElement('a'); a.href=url; a.download=name; a.click(); setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function brief() {
  const ds=selection(), quotes=DATA.summaries[$('#topic').value]||[];
  const lines=['# Mailers evidence brief','',`View: ${new URL(location.href).href}`,'','## Published trend figures',''];
  if(ds.length) {
    const a=ds[0],b=ds.at(-1),pct=a.value?100*(b.value/a.value-1):null;
    lines.push(`${b.market}: ${fmt(a.value)} (${a.year}) → ${fmt(b.value)} (${b.year}), ${pct===null?'percentage change undefined for zero baseline':pct.toFixed(1)+'% change'}. Unit: ${b.unit}. Calculated from published values; not a causal estimate.`, '');
    ds.forEach(r=>lines.push(`- ${r.year}: ${r.value} ${r.unit}; report edition ${r.edition}, Table ${r.table}, PDF page ${r.page}. [Source](${pdfLink(r.file,r.page)})`));
  } else lines.push('No published trend observations match the selection.');
  lines.push('','## Interpretation limits','',surveyBreak,metroLimit,'Historical estimates retain revisions and may use different classifications. Markets overlap; do not sum them.', '', '## Forecast caveat','',forecastLimit,'','## Selected source passages',`Topic: ${$('#topic').value}`,'');
  quotes.forEach(q=>lines.push(`> ${q.text}`,`[2025 report, PDF page ${q.page}](${pdfLink(q.file,q.page)})`,''));
  lines.push('Arithmetic and extractive source text only. No generative model was used.');
  saveText('mailers-evidence-brief.md',lines.join('\n'));
}
for(const target of ['#csv','#copy']) {const b=document.createElement('button');b.textContent='Export brief';b.className='export-brief';b.onclick=brief;$(target).after(b);}

// Hash state is allow-listed and validated against the actual select options.
const stateIds=['view','edition','market','start','end','dimension','measure','forecastMarket','horizon','topic','historyDimension','historyYear','historyMetric'];
let restoring=false;
function setTab(id,focus=false) {
  const buttons=[...document.querySelectorAll('nav button')];
  if(!buttons.some(b=>b.dataset.tab===id)) id='overview';
  buttons.forEach(b=>{const active=b.dataset.tab===id;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1;if(active&&focus)b.focus();});
  document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('active',p.id===id));
}
function saveView() {
  if(restoring)return;
  const params=new URLSearchParams();params.set('tab',document.querySelector('nav button[aria-selected=true]').dataset.tab);
  stateIds.forEach(id=>params.set(id,$('#'+id).value));
  try {history.replaceState(null,'','#'+params.toString());} catch { /* Reading and exporting still work when a file browser restricts history. */ }
}
function assign(id,value) {if(value!==null && [...$('#'+id).options].some(o=>o.value===value))$('#'+id).value=value;}
function restoreView() {
  restoring=true;
  try {
    const p=new URLSearchParams(location.hash.slice(1));
    assign('view',p.get('view'));assign('edition',p.get('edition'));refreshControls();
    ['market','start','end','dimension','measure','forecastMarket','horizon','topic','historyDimension','historyYear'].forEach(id=>assign(id,p.get(id)));
    renderHistory(true);assign('historyMetric',p.get('historyMetric'));renderHistory();
    renderTrend();demos();forecast();insights();setTab(p.get('tab'));
  } finally {restoring=false;}
}
const nav=document.querySelector('nav');nav.setAttribute('role','tablist');nav.setAttribute('aria-label','Dashboard sections');nav.setAttribute('aria-orientation','vertical');
const tabs=[...nav.querySelectorAll('button')];
tabs.forEach((b,i)=>{
  b.id='tab-'+b.dataset.tab;b.setAttribute('role','tab');b.setAttribute('aria-controls',b.dataset.tab);
  const panel=$('#'+b.dataset.tab);panel.setAttribute('role','tabpanel');panel.setAttribute('aria-labelledby',b.id);
  b.onclick=()=>{setTab(b.dataset.tab);saveView();window.scrollTo(0,0);};
  b.onkeydown=e=>{let next;if(e.key==='ArrowRight'||e.key==='ArrowDown')next=(i+1)%tabs.length;else if(e.key==='ArrowLeft'||e.key==='ArrowUp')next=(i+tabs.length-1)%tabs.length;else if(e.key==='Home')next=0;else if(e.key==='End')next=tabs.length-1;if(next!==undefined){e.preventDefault();setTab(tabs[next].dataset.tab,true);saveView();}};
});
stateIds.forEach(id=>{const old=$('#'+id).onchange;$('#'+id).onchange=e=>{if(old)old(e);if(id==='view'||id==='edition')renderTrend();saveView();};});
window.addEventListener('hashchange',restoreView);
restoreView();
