"""Fail on broken schemas, identifiers, units or provenance relationships."""
import csv,json,re
from pathlib import Path
from curate import STATES
R=Path(__file__).resolve().parents[1]
def read(p):return list(csv.DictReader((R/p).open()))
def validate():
 ds=read('data/curated/datasets.csv');claims=read('data/curated/claims.csv');ids={x['dataset_id'] for x in ds}
 assert len(ids)==len(ds)==63
 fam={x['family_id'] for x in read('data/curated/families.csv')}
 assert all(x['family_id'] in fam for x in ds)
 assert len({x['claim_id'] for x in claims})==len(claims)==16*len(ds)
 for c in claims:
  assert c['dataset_id'] in ids and c['status'] in STATES
  assert re.fullmatch(r'workbook:Table4:[C-R]\d+',c['source'])
  assert c['status']!='not_found_after_check' or c['verification_date']
 for d in ds:
  for k in ['read_length_bp','data_size_gbp','sample_count']:
   assert not d[k] or float(d[k])>0
  if d['read_layout']=='paired_end':assert d['read_length_bp']
 assert json.loads((R/'data/curated/catalog.json').read_text())==[dict(x,**{k:(float(x[k]) if k in ['data_size_gbp','read_length_bp'] else int(x[k])) for k in ['sample_count','read_length_bp','data_size_gbp'] if x[k]}) for x in ds]
 refs={x['reference_id'] for x in read('data/historical/references.csv')}
 assert all(e['dataset_id'] in ids and e['reference_id'] in refs for e in read('data/curated/reported_reuse.csv'))
 sources={x['source_id'] for x in read('data/curated/sources.csv')}
 for s in read('data/curated/studies.csv'):assert s['source_id'] in sources and s['doi'] and s['source_url']
 from collections import Counter
 assert len(read('data/derived/issues.csv'))>0
 metrics=read('results/metrics.csv');assert len(metrics)==2
 for m in metrics:
  for k,v in m.items():
   if k not in ['Tool','Sample']: assert 0<=float(v)<=1
 print('PASS: schemas, 63 identifiers, 1008 claims, units, references, source links and metric bounds')
if __name__=='__main__':validate()
