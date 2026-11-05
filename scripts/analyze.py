"""Generate denominators, chart inputs and figures from published CSVs."""
import csv,json,collections,shutil
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from import_workbook import dump
from validate import read
R=Path(__file__).resolve().parents[1]
BLUE='#0072B2';ORANGE='#D55E00';GREEN='#009E73';GREY='#B3B8BE'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','svg.hashsalt':'atlas','pdf.fonttype':42})
def save(fig,name):
 fig.tight_layout()
 for ext in ['svg','pdf','png']:fig.savefig(R/f'figures/{name}.{ext}',dpi=320,bbox_inches='tight',metadata={'Creator':'Metagenomic Binning Benchmark Atlas'} if ext=='pdf' else None)
 for f in (R/'figures').glob(name+'.svg'):
  f.write_text('\n'.join(line.rstrip() for line in f.read_text().splitlines())+'\n')
 plt.close(fig)
def analyze():
 ds=read('data/curated/datasets.csv');cs=read('data/curated/claims.csv');es=read('data/curated/reported_reuse.csv');issues=read('data/derived/issues.csv');n=len(ds)
 stats=[]
 for f in dict.fromkeys(c['field'] for c in cs):
  found=[c for c in cs if c['field']==f];present=sum(c['raw_value'] not in ['','/'] for c in found)
  stats.append(dict(field=f,nonempty_historical=present,denominator=n,percent_nonempty=round(present/n*100,2),meaning='Presence in historical workbook; NOT publication reporting quality'))
 dump(Path('data/derived/field_presence.csv'),stats)
 origins=collections.Counter(x['origin'] for x in ds);tech=collections.Counter('mixed short/long (claimed)' if 'Illumina' in x['technology'] and any(y in x['technology'] for y in ['Nanopore','PacBio','Long']) else 'long-read (claimed)' if any(y in x['technology'] for y in ['Nanopore','PacBio']) else 'not extracted' if not x['technology'] else 'other/short-read (claimed)' for x in ds)
 dump(Path('data/derived/origin_counts.csv'),[dict(origin=k,count=v,denominator=n) for k,v in origins.items()]);dump(Path('data/derived/technology_counts.csv'),[dict(technology=k,count=v,denominator=n) for k,v in tech.items()])
 summary=dict(date='2026-11-05',records=n,families=len({d['family_id'] for d in ds}),claims=len(cs),audit_flags=len(issues),reported_reuse_edges=len(es),article_citations=len(read('data/curated/studies.csv')),primary_repository_sources=len(read('data/curated/sources.csv')),ground_truth_not_extracted=sum(d['ground_truth_status']=='not_extracted' for d in ds),origin_counts=dict(origins))
 (R/'data/derived/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 # Opening figure: transparent components rather than a composite score.
 chosen=[x for x in stats if x['field'] in ['platform','samples','assembler','size','read_length','n50','assembly_size','original_ref']]
 fig,ax=plt.subplots(figsize=(8.2,4.2));ys=np.arange(len(chosen));ax.barh(ys,[x['nonempty_historical'] for x in chosen],color=BLUE,height=.65)
 ax.set(yticks=ys,yticklabels=[{'size':'Read data size','samples':'Sample count','original_ref':'Original reference','read_length':'Read length','assembly_size':'Assembly size','n50':'N50 (ambiguous)','platform':'Platform','assembler':'Assembler'}[x['field']] for x in chosen],xlim=(0,n+7),xlabel='Non-empty historical cells / 63 records',title='What the original workbook records')
 for y,x in zip(ys,chosen):ax.text(x['nonempty_historical']+.6,y,f"{x['nonempty_historical']}/63",va='center',fontsize=9)
 ax.invert_yaxis();ax.grid(axis='x',alpha=.12);save(fig,'metadata')
 fig,axs=plt.subplots(1,2,figsize=(9.5,3.8))
 for ax,c,title in [(axs[0],origins,'Origin labels after audit'),(axs[1],tech,'Technology claims')]:
  ax.barh(list(c),list(c.values()),color=[BLUE,GREEN,ORANGE,GREY][:len(c)]);ax.set_title(title);ax.set_xlabel('Records (denominator = 63)');ax.invert_yaxis()
 save(fig,'coverage')
 # Historical matrix contains only manuscript-reported relationships, not newly verified reuse.
 methods={}
 for row in read('data/historical/workbook_cells.csv'):
  if row['sheet']=='Table4' and row['cell'].startswith('J') and int(row['cell'][1:])>=76:methods[row['cell'][1:]]=row['value']
 labels={'01':'GraphBin','02':'MetaCoAG','05':'Avamb','08':'SemiBin preprint','15':'MetaBAT 2','16':'CCVAE','17':'MetaBinner preprint','29':'GraphMB','37':'STRONG','41':'Vamb','43':'SolidBin','49':'BMC3C'}
 families=sorted({d['family_id'] for d in ds if any(e['dataset_id']==d['dataset_id'] for e in es)});cols=list(labels);index={d['dataset_id']:d['family_id'] for d in ds};m=np.zeros((len(families),len(cols)),dtype=int)
 for e in es:
  k=e['reference_id'].split('-')[-1]
  if k in cols:m[families.index(index[e['dataset_id']]),cols.index(k)]+=1
 dump(Path('data/derived/reuse_matrix.csv'),[dict(family_id=f,**{labels[k]:int(m[i,j]) for j,k in enumerate(cols)}) for i,f in enumerate(families)])
 fig,ax=plt.subplots(figsize=(10,7.5));im=ax.imshow(m,cmap='Blues',aspect='auto',vmin=0);ax.set(xticks=range(len(cols)),xticklabels=list(labels.values()),yticks=range(len(families)),yticklabels=[x[4:] for x in families],title='Reported dataset reuse in the historical workbook')
 plt.setp(ax.get_xticklabels(),rotation=50,ha='right',fontsize=8);plt.setp(ax.get_yticklabels(),fontsize=8);fig.colorbar(im,ax=ax,label='Subset–reference edges (unverified)');save(fig,'reuse')
 metrics=read('results/metrics.csv');fig,ax=plt.subplots(figsize=(8.3,3.5));keys=['Average purity (bp)','Average completeness (bp)','Percentage of binned bp'];x=np.arange(3)
 for i,row in enumerate(metrics):ax.bar(x+(i-.5)*.35,[float(row[k]) for k in keys],width=.35,label=row['Tool'],color=[BLUE,ORANGE][i])
 ax.set(xticks=x,xticklabels=['Mean bin purity','Mean mapped-genome\ncompleteness','Fraction of bp binned'],ylim=(0,1.12),ylabel='Fraction',title='Re-evaluating official AMBER outputs · CAMI_low');ax.legend(loc='upper center',ncol=2,frameon=False,fontsize=9);save(fig,'evaluation')
 for f in (R/'figures').glob('*.svg'):shutil.copy(f,R/'site/assets'/f.name)
 shutil.copy(R/'data/curated/catalog.json',R/'site/catalog.json')
 print(json.dumps(summary))
if __name__=='__main__':analyze()
