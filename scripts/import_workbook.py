"""Extract scientific table cells only; never copy personal/activity documents."""
import argparse, csv, hashlib, json, re
from pathlib import Path
import openpyxl
ROOT=Path(__file__).resolve().parents[1]
def dump(path, rows):
    path=ROOT/path;path.parent.mkdir(parents=True,exist_ok=True)
    if rows:
        with path.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
def extract(path):
    w=openpyxl.load_workbook(path,data_only=True)
    sha=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    records=[];cells=[];versions=[]
    for name,start,end in [('Table1',7,62),('Table2',6,53),('Table3',6,68),('Table4',6,68)]:
        s=w[name]
        for row in s.iter_rows(min_row=start,max_row=end):
            for c in row[:{'Table1':13,'Table2':17,'Table3':16,'Table4':18}[name]]:
                if c.value is not None:
                    cells.append(dict(sheet=name,cell=c.coordinate,value=str(c.value).strip(),source_sha256=sha))
        versions.append(dict(sheet=name,role='canonical' if name=='Table4' else 'historical_revision',rows=s.max_row,columns=s.max_column))
    for i in range(6,69):
        s=w['Table4']; vals=[s.cell(i,j).value for j in range(2,19)]
        if vals[0] is None:continue
        keys=['label','samples','platform','simulator','assembler','origin','size','read_length','environment','ncbi','ena','link_ref','original_ref','year','reuse_refs','n50','assembly_size']
        records.append(dict(row=i,**{k:'' if v is None else str(v).strip() for k,v in zip(keys,vals)}))
    refs=[];current=None
    for row in w['References3&4']:
        for c in row:
            if c.value is None:continue
            t=str(c.value).strip();m=re.fullmatch(r'\[(\d+)\]',t)
            if m:current='legacy-ref-'+m[1].zfill(2)
            elif current:
                refs.append(dict(reference_id=current,source_cell=c.coordinate,text=t,url=c.hyperlink.target if c.hyperlink else (t if t.startswith('http') else '')))
    dump(Path('data/historical/table4.csv'),records)
    dump(Path('data/historical/workbook_cells.csv'),cells)
    dump(Path('data/historical/references.csv'),refs)
    (ROOT/'data/historical/workbook_manifest.json').write_text(json.dumps(dict(sha256=sha,sheets=versions,canonical='Table4',policy='Earlier revisions are not independent datasets; earlier values are recovery candidates, not verified corrections.'),indent=2)+'\n')
    print('Extracted',len(records),'Table4 records;',len(cells),'scientific cells')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('workbook');extract(p.parse_args().workbook)
