'use strict';
const search=document.querySelector('#search'), origin=document.querySelector('#origin'), body=document.querySelector('#catalog-body'), count=document.querySelector('#count');
let catalog=[];
function cell(row,text){const td=document.createElement('td');td.textContent=text||'Not extracted';row.appendChild(td);return td;}
function render(){const q=search.value.trim().toLowerCase();const selected=catalog.filter(d=>(!origin.value||d.origin===origin.value)&&[d.subset,d.family_id,d.accessions,d.environment,d.technology].join(' ').toLowerCase().includes(q));body.replaceChildren();for(const d of selected){const tr=document.createElement('tr');const td=cell(tr,d.subset);const sub=document.createElement('small');sub.textContent=d.dataset_id+' · '+d.family_id;td.appendChild(sub);cell(tr,d.origin);cell(tr,d.technology);cell(tr,d.environment);cell(tr,d.accessions);cell(tr,d.source.replace('workbook:',''));body.appendChild(tr);}count.textContent=`${selected.length} of ${catalog.length} historical subset records shown`;}
fetch('catalog.json').then(r=>{if(!r.ok)throw Error('Catalog response '+r.status);return r.json();}).then(rows=>{catalog=rows;render();}).catch(()=>{count.textContent='Catalog could not load. Serve this directory over HTTP, or download the CSV below.';});
search.addEventListener('input',render);origin.addEventListener('change',render);
