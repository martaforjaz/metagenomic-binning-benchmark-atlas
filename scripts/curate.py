"""Deterministic conservative curation. No missingness is evidence of paper omission."""
import csv,json,re
from pathlib import Path
from import_workbook import dump
R=Path(__file__).resolve().parents[1]
STATES={'historical_unverified','verified','not_extracted','not_found_after_check','not_applicable','contradictory','access_unconfirmed'}
FIELDS={'samples':('C','count'),'platform':('D','text'),'simulator':('E','text'),'assembler':('F','text'),'origin':('G','text'),'size':('H','Gbp'),'read_length':('I','bp'),'environment':('J','text'),'ncbi':('K','accession'),'ena':('L','accession'),'link_ref':('M','reference'),'original_ref':('N','reference'),'year':('O','year'),'reuse_refs':('P','reference'),'n50':('Q','bp'),'assembly_size':('R','bp')}
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def family(label):
    n=label.lower().replace(' ','')
    for prefix,f in [('cami1','cami-i'),('cami2','cami-ii'),('camimouse','cami-mouse-gut'),('synth_','strong-synthetic'),('fl20','autometa-mix51'),('mix-51','autometa-mix51'),('zymo_d','zymo-d6331'),('simhc','metasim'),('simlc','metasim'),('simmc','metasim')]:
        if n.startswith(prefix):return f
    if label in ['Hjor','Viby','DamH','Mari','AaIE','Hade']:return 'danish-wwtp'
    if label in ['454','S1','S2','S3','S4']:return 'lake-lanier'
    return slug(label)
def normalize_number(raw,unit):
    t=raw.replace('\u00a0','').replace(' ','')
    m=re.fullmatch(r'(\d+(?:\.\d+)?)(Gbp|Mbp|bp)?',t,re.I)
    if not m:return None
    v=float(m[1]);u=(m[2] or unit).lower()
    if unit=='bp': v*= {'gbp':1e9,'mbp':1e6,'bp':1}[u]
    if unit=='Gbp':v*= {'gbp':1,'mbp':.001,'bp':1e-9}[u]
    return v

def curate():
    rows=list(csv.DictReader((R/'data/historical/table4.csv').open()));catalog=[];claims=[];issues=[];edges=[];assemblies=[]
    def issue(d,f,c,n):issues.append(dict(dataset_id=d,field=f,code=c,note=n))
    for x in rows:
        label=' '.join(x['label'].split());d='ds-'+str(int(x['row'])-5).zfill(3);f=family(label)
        cat=dict(dataset_id=d,family_id='fam-'+f,release='CAMI I' if f=='cami-i' else 'CAMI II' if f=='cami-ii' else '',subset=label,origin=x['origin'].lower(),technology=x['platform'].replace('Ilumina','Illumina'),environment=x['environment'],sample_count='',read_length_bp='',read_layout='',data_size_gbp='',assembly_id='asm-'+d[3:] if x['assembler'] not in ('','/') or x['assembly_size'] else '',ground_truth_status='not_extracted',access_status='access_unconfirmed',source='workbook:Table4:B'+x['row'],evidence_status='historical_unverified')
        for k,(col,unit) in FIELDS.items():
            raw=x[k];status='not_extracted' if raw in ('','/') else 'historical_unverified';val=raw if status!='not_extracted' else ''
            if k=='size' and val:
                value=normalize_number(raw,unit)
                if value is None:status='contradictory';issue(d,k,'ambiguous_quantity','Product or non-scalar value in Gbp column; no conversion.')
                else:cat['data_size_gbp']=value;val=str(value)
            if k=='samples' and val:
                value=normalize_number(raw,'count')
                if value is not None and value.is_integer():cat['sample_count']=int(value);val=str(int(value))
                else:status='contradictory';issue(d,k,'ambiguous_count','Non-integer count; preserve raw value.')
            if k=='read_length' and val:
                m=re.fullmatch(r'2x(\d+)',raw.replace(' ',''))
                value=int(m[1]) if m else normalize_number(raw,'bp')
                if value is not None:cat['read_length_bp']=value;val=str(value);cat['read_layout']='paired_end' if m else 'not_extracted'
            if k=='n50' and val:
                issue(d,k,'n50_semantics_unconfirmed','Workbook legend calls N50 read length; assembly/read N50 and unit require primary confirmation.')
                if normalize_number(raw,'bp') is not None and normalize_number(raw,'bp')<100:status='contradictory';issue(d,k,'suspected_kbp','Small decimal under bp heading; do not rescale without source.')
            if k=='assembly_size' and val and not re.search(r'[a-zA-Z]',raw):status='contradictory';issue(d,k,'missing_unit','Assembly size lacks unit; no numeric conversion.')
            if k=='origin' and (label.startswith('Mix-51') or label.startswith('FL20')):status='contradictory'
            claims.append(dict(claim_id=d+'-'+k,dataset_id=d,field=k,value=val,raw_value=raw,unit=unit,status=status,source='workbook:Table4:'+col+x['row'],verification_date='',note='Blank or slash means not extracted; slash is not inferred as not applicable.' if status=='not_extracted' else 'Historical workbook assertion; not a verified primary-source fact.'))
        if label.startswith('Mix-51') or label.startswith('FL20'):issue(d,'origin','mock_vs_simulated','Workbook says simulated but describes physical DNA mixtures/spike-ins; origin unresolved.');cat['origin']='contradictory'
        if label in ['MSA-1003','Zymo_D6331_STD','Zymo_D6331_LOW','Zymo_D6331_ULI','ZymoEVEN']:issue(d,'samples','samples_vs_organisms','Mock composition may be confused with sample count; retain unverified count.')
        if label=='HPM2':issue(d,'original_ref','reference_collision','Refs 50 and 55 point to HMP consortium and Almeida; HPM2 spelling, assay and cohort unresolved.')
        if label in ['SimHC','simLC+','simMC']:issue(d,'assembler','tool_role','MetaSim is a simulator; placement in assembler field is suspect.');issue(d,'environment','complexity_label','Name and prose complexity labels need confirmation.')
        if label=='Sharon':issue(d,'year','publication_year','Workbook 2012 vs reference text 2013; online/issue date unresolved.')
        if label=='Soil':issue(d,'original_ref','source_relevance','Regional biodiversity paper may not describe sequencing dataset; accession-to-publication unresolved.')
        if cat['assembly_id']:assemblies.append(dict(assembly_id=cat['assembly_id'],dataset_id=d,assembler=x['assembler'],assembly_size_raw=x['assembly_size'],n50_raw=x['n50'],status='historical_unverified',source='workbook:Table4:F'+x['row']))
        for ref in sorted(set(re.findall(r'\[(\d+)\]',x['reuse_refs']))):edges.append(dict(dataset_id=d,reference_id='legacy-ref-'+ref.zfill(2),relationship='reported_reuse',status='historical_unverified',source='workbook:Table4:P'+x['row']))
        cat['accessions']='; '.join(v for v in [x['ncbi'],x['ena']] if v not in ('','/'))
        catalog.append(cat)
    # Detect shared accession without merging: project-level identifiers are not equivalent variants.
    for i,x in enumerate(catalog):
        if not x['accessions']:continue
        for y in catalog[i+1:]:
            if x['accessions']==y['accessions']:issue(x['dataset_id'],'accessions','shared_accession','Also '+y['dataset_id']+'; shared project/run does not prove identical subset.')
    dump(Path('data/curated/datasets.csv'),catalog);dump(Path('data/curated/claims.csv'),claims);dump(Path('data/curated/assemblies.csv'),assemblies);dump(Path('data/derived/issues.csv'),issues);dump(Path('data/curated/reported_reuse.csv'),edges)
    fams=[dict(family_id=f,membership_rule='Conservative label/project grouping; not sequence identity',status='curator_inferred') for f in sorted(set(x['family_id'] for x in catalog))]
    dump(Path('data/curated/families.csv'),fams)
    (R/'data/curated/catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n')
    # Earlier tables: exact label overlaps only; preserve candidates outside canonical facts.
    cells=list(csv.DictReader((R/'data/historical/workbook_cells.csv').open()));candidates=[]
    for c in cells:
        if c['sheet']=='Table4' or not re.fullmatch(r'B\d+',c['cell']):continue
        matches=[x['dataset_id'] for x in catalog if slug(x['subset'])==slug(c['value'])]
        candidates.append(dict(sheet=c['sheet'],row=re.sub(r'\D','',c['cell']),label=c['value'],possible_dataset_ids=';'.join(matches),decision='recovery_candidate_only' if matches else 'historical_label_unresolved'))
    dump(Path('data/derived/revision_matches.csv'),candidates)
    recovered=[]
    lookup={(c['sheet'],c['cell']):c['value'] for c in cells}
    maps={'Table1':{'samples':'C','platform':'D','origin':'F','size':'G','environment':'H','read_length':'K','n50':'L','assembly_size':'M'},'Table2':{'samples':'C','platform':'D','origin':'F','size':'G','environment':'H','ncbi':'I','ena':'J','read_length':'O','n50':'P','assembly_size':'Q'},'Table3':{'samples':'C','platform':'D','origin':'F','size':'G','environment':'H','ncbi':'I','ena':'J','read_length':'N','n50':'O','assembly_size':'P'}}
    by_id={c['dataset_id']:x for c,x in zip(catalog,rows)}
    for c in candidates:
        if not c['possible_dataset_ids']:continue
        for did in c['possible_dataset_ids'].split(';'):
            for field,col in maps[c['sheet']].items():
                old=lookup.get((c['sheet'],col+c['row']),'')
                new=by_id[did][field]
                if old not in ('','/') and old!=new:
                    recovered.append(dict(dataset_id=did,field=field,earlier_value=old,canonical_value=new,source='workbook:'+c['sheet']+':'+col+c['row'],decision='recoverable_missing_assertion' if new in ('','/') else 'conflicting_revision_assertion',status='historical_unverified'))
    dump(Path('data/derived/recovery_candidates.csv'),recovered)

    print(len(catalog),'records;',len(fams),'families;',len(claims),'claims;',len(issues),'flags;',len(edges),'reported reuse edges')
if __name__=='__main__':curate()
