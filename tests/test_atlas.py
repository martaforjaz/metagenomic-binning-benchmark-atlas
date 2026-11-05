import csv,json,sys,hashlib,re
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from curate import normalize_number,family,STATES
from validate import validate,read
from check_links import check

def test_full_relational_validation():validate()
def test_explicit_unit_conversions_and_ambiguous_products():
 assert normalize_number('164Mbp','Gbp')==.164
 assert normalize_number('0.17 Gbp','bp')==170000000
 assert normalize_number('133\u00a0668','bp')==133668
 assert normalize_number('2x245','Gbp') is None
 assert normalize_number('3x105','Gbp') is None
 assert normalize_number('/','bp') is None

def test_no_false_not_found_or_not_applicable():
 for c in read('data/curated/claims.csv'):
  if c['raw_value'] in ('','/'):assert c['status']=='not_extracted'
  assert c['status'] not in ['not_applicable','not_found_after_check']

def test_variants_not_collapsed_by_shared_accession():
 ds=read('data/curated/datasets.csv');s3=next(x for x in ds if x['subset']=='S3');s4=next(x for x in ds if x['subset']=='S4')
 assert s3['accessions']==s4['accessions'] and s3['dataset_id']!=s4['dataset_id']
 assert family('CAMI1 Low')==family('CAMI1 High')
 assert family('CAMI1 Low')!=family('CAMI2 Airways')

def test_ambiguous_values_withheld_and_truth_not_inferred():
 ds=read('data/curated/datasets.csv')
 assert not next(x for x in ds if 'HiSeq' in x['subset'])['data_size_gbp']
 assert all(x['ground_truth_status']=='not_extracted' for x in ds)
 assert next(x for x in ds if x['subset']=='Mix-51')['origin']=='contradictory'

def test_official_upstream_expected_metric_values():
 # Expected numbers from upstream features/amber_stdout.feature, NOT copied from generated metrics.
 expected={'CONCOCT (CAMI)':(.837135,.933410,.966790,.663234,.643557),'MaxBin 2.0.2 (CAMI)':(.947763,.825796,.863569,.809257,.917149)}
 keys=['Average purity (bp)','Average completeness (bp)','Percentage of binned bp','Accuracy (bp)','Adjusted Rand index (bp)']
 rows=read('results/metrics.csv');assert {r['Tool'] for r in rows}==set(expected)
 for row in rows:
  assert row['Sample']=='CAMI_low'
  assert [float(row[k]) for k in keys]==pytest.approx(expected[row['Tool']],abs=1e-6)
 full=list(csv.DictReader((R/'results/amber_results.tsv').open(),delimiter='\t'))
 gold=next(x for x in full if x['Tool']=='Gold standard')
 assert float(gold['accuracy_bp'])==1
 assert float(gold['precision_avg_bp'])==1

def test_report_numbers_and_data_consistency():
 s=json.loads((R/'data/derived/summary.json').read_text());text=(R/'README.md').read_text()
 for key in ['records','claims','audit_flags','article_citations']:assert str(s[key]) in text
 stats=read('data/derived/field_presence.csv')
 for x in stats:
  assert int(x['denominator'])==s['records']
  assert float(x['percent_nonempty'])==pytest.approx(int(x['nonempty_historical'])/s['records']*100,abs=.0051)
 assert 'not missing reporting in papers' in text

def test_document_and_site_links():check()
def test_no_originals_or_personal_administrative_identifiers():
 public=[R/'README.md',*list((R/'docs').glob('*.md')),*list((R/'data').rglob('*.csv')),R/'site/index.html']
 pattern=re.compile(r'\b63195\b|martaforjazpereira@gmail\.com')
 for p in public:assert not pattern.search(p.read_text()),p
 assert not list(R.glob('*.xlsx')) and not list(R.glob('*.MOV'))

def test_recomputed_input_hash_manifest_if_present():
 for x in json.loads((R/'experiments/inputs.sha256.json').read_text()):
  f=R/'experiments/vendor/AMBER'/x['path']
  if f.exists():assert hashlib.sha256(f.read_bytes()).hexdigest()==x['sha256']

def test_citations_have_traceable_primary_evidence():
 sources={x['source_id']:x for x in read('data/curated/sources.csv')}
 for s in read('data/curated/studies.csv'):
  assert s['doi'] in (R/'bibliography.bib').read_text()
  source=sources[s['source_id']];assert source['commit'] in source['url']
  assert source['result']=='content_retrieved'

def test_declared_catalog_schema():
 schema=json.loads((R/'data/curated/catalog.schema.json').read_text())['items']
 for row in json.loads((R/'data/curated/catalog.json').read_text()):
  assert set(row)==set(schema['required'])
  for k,v in row.items():
   types=schema['properties'][k]['type']
   assert isinstance(v,(int,float,str)) if isinstance(types,list) else isinstance(v,str)

def test_earlier_revision_recovery_candidates_are_not_silent_corrections():
 recovered=read('data/derived/recovery_candidates.csv')
 assert len(recovered)==132
 assert all(r['status']=='historical_unverified' for r in recovered)
 assert {r['decision'] for r in recovered}=={'recoverable_missing_assertion','conflicting_revision_assertion'}
