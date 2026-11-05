"""Fetch immutable official inputs, validate identity, run the predeclared protocol."""
import csv, hashlib, json, os, platform, subprocess, sys, time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run():
    p=json.loads((R/'experiments/protocol.json').read_text()); v=R/'experiments/vendor/AMBER'
    if not (v/'.git').exists():
        v.parent.mkdir(parents=True,exist_ok=True)
        subprocess.run(['git','clone',p['upstream']+'.git',str(v)],check=True)
    subprocess.run(['git','-C',str(v),'checkout','--detach',p['commit']],check=True,capture_output=True)
    assert subprocess.check_output(['git','-C',str(v),'rev-parse','HEAD'],text=True).strip()==p['commit']
    files=[v/f for f in p['files']]; assert sum(f.stat().st_size for f in files)<p['limits']['maximum_input_bytes']
    manifest=[dict(path=f.relative_to(v).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size) for f in files]
    saved=R/'experiments/inputs.sha256.json'
    if saved.exists(): assert json.loads(saved.read_text())==manifest,'Input integrity mismatch'
    else:saved.write_text(json.dumps(manifest,indent=2)+'\n')
    def assignments(f):
        result={};sample=None
        for line in f.read_text().splitlines():
            if line.startswith('@SampleID:'):sample=line.split(':',1)[1]
            if line and not line.startswith(('@','#')):
                parts=line.split('\t');assert parts[0] not in result,'Duplicate sequence';result[parts[0]]=parts[1:]
        return sample,result
    sample,gold=assignments(files[0]);counts={}
    for f in files[1:3]:
        s,a=assignments(f);assert s==sample;assert set(a)<=set(gold),'Predicted sequence absent from gold standard'
        counts[f.name]=len(a)
    out=R/'results/amber';out.mkdir(parents=True,exist_ok=True)
    command=[sys.executable,str(v/'amber.py'),'-g',str(files[0]),str(files[1]),str(files[2]),'-r',str(files[3]),'-k','circular element','-p','1','-n','0','-x','50,70,90','-y','10,5','-l','CONCOCT (CAMI),MaxBin 2.0.2 (CAMI)','-o',str(out),'--stdout','--silent']
    env=dict(os.environ,MPLBACKEND='Agg',OMP_NUM_THREADS='2',OPENBLAS_NUM_THREADS='2')
    started=time.time()
    with (R/'results/experiment.log').open('w') as log:
        proc=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,env=env,timeout=180)
    elapsed=time.time()-started
    if proc.returncode: raise RuntimeError((R/'results/experiment.log').read_text()[-3000:])
    import pandas as pd
    df=pd.read_csv(out/'results.tsv',sep='\t')
    df.to_csv(R/'results/amber_results.tsv',sep='\t',index=False)
    df=df.rename(columns={'precision_avg_bp':'Average purity (bp)','recall_avg_bp':'Average completeness (bp)','percentage_of_assigned_bps':'Percentage of binned bp','accuracy_bp':'Accuracy (bp)','adjusted_rand_index_bp':'Adjusted Rand index (bp)'})
    df=df[df['Tool']!='Gold standard']
    cols=['Tool','Sample']+p['metrics']
    df[cols].to_csv(R/'results/metrics.csv',index=False)
    (R/'results/run.json').write_text(json.dumps(dict(exit_code=proc.returncode,wall_seconds=elapsed,python=platform.python_version(),evaluator=p['evaluator_version'],commit=p['commit'],gold_sequences=len(gold),gold_genomes=len(set(x[0] for x in gold.values())),predicted_sequences=counts,command=['python','experiments/vendor/AMBER/amber.py']+['<repo>/'+x.split(str(R)+'/')[-1] if str(R) in x else x for x in command[2:]],run_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),interpretation=p['interpretation']),indent=2)+'\n')
    print(df[cols].to_string(index=False));print('Wall seconds:',round(elapsed,2))
if __name__=='__main__':run()
