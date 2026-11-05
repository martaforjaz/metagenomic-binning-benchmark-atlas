"""Build numbers once from CSV, render English reports and the static site."""
import csv,json,re,shutil,html
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from validate import read
R=Path(__file__).resolve().parents[1]
def build():
 s=json.loads((R/'data/derived/summary.json').read_text());metrics=read('results/metrics.csv');run=json.loads((R/'results/run.json').read_text());stats=read('data/derived/field_presence.csv')
 a,b=metrics
 m={**s,'concoct_purity':f"{float(a['Average purity (bp)']):.3f}",'concoct_completeness':f"{float(a['Average completeness (bp)']):.3f}",'maxbin_purity':f"{float(b['Average purity (bp)']):.3f}",'maxbin_completeness':f"{float(b['Average completeness (bp)']):.3f}"}
 report=f'''# Metagenomic Binning Benchmark Atlas

Technical report · 5 November 2026 · Independent extension by Marta Forjaz

## Abstract

This resource converts a historical undergraduate dataset workbook into a reproducible, provenance-aware research artifact. It contains {s['records']} historical subset records in {s['families']} provisional families, {s['claims']} cell-traceable field assertions, {s['reported_reuse_edges']} workbook-reported reuse relationships and {s['audit_flags']} audit flags. A bounded repository-assisted scoping review verifies {s['article_citations']} article citations against {s['primary_repository_sources']} primary repositories. A common AMBER 2.0.8 protocol successfully re-evaluates two public official example outputs for CAMI_low. No binners were run. The contribution is integration, validation and reproducible evaluation, not a claim of new binning methodology or exhaustive literature coverage.

## 1. Background and research questions

Metagenomic sequencing mixes DNA from multiple organisms. Assembly reconstructs longer fragments (contigs); binning groups fragments into candidate genomes, often using composition, abundance and assembly connectivity. A bin is a hypothesis about genome membership, not automatically a complete, uncontaminated genome. Known simulated/mock truth supports direct assignment evaluation; marker-based estimates on real communities answer a related but different question.

RQ1: Which datasets and protocols are used? RQ2: What documentation supports reproduction? RQ3: Which conditions support fair cross-study comparison? RQ4: Can a small common-protocol evaluation be reproduced?

## 2. Historical work versus the independent extension

The original January-February 2024 NOVA undergraduate placement, supervised by Andre Lamurias, documented literature reading, weekly meetings and successive dataset tables. Its report describes an intended baseline evaluation but supplies no executed baseline artifacts. This extension does not attribute new work or endorsement to the former supervisor. The original PDF/activity sheet remain private because they contain administrative personal information; the video and third-party illustration are not redistributed.

The extension performs scientific-cell extraction, conservative normalization, explicit provenance and uncertainty modelling, a scoped current repository review, executable validation, descriptive analysis and public-output re-evaluation. Derived literature observations, historical claims and newly calculated experimental results remain separate.

## 3. Data and provenance methods

Table4 is the most complete workbook revision. Rows 6-68 define the canonical record population. Earlier tables are recovery candidates, not independent datasets. The private original's SHA-256 is recorded in workbook_manifest.json. Public scientific extracts support reproduction without requiring the private attachments. No original administrative document is included.

The unit of catalog analysis is a historical dataset subset row, not an individual sequence, sample, family or paper. The {s['families']} families are provisional label/context groups; shared accession does not establish identical sequence contents. Separate CSVs model assemblies, field claims, reported reuse, reviewed studies and source verification. Numeric conversions use explicit units or the column heading, never infer ambiguous products. All converted historical values remain historically unverified.

Each of 16 fields per subset has a raw value, source cell and status. Missing or slash cells mean not extracted; they do not prove absence from a publication. Not-found-after-check requires a specific source inspection. Not-applicable and access-unconfirmed are separate states. See data_dictionary.md and audit.md for schema and exact examples.

The audit found ambiguous Gbp products, suspect N50 units, missing assembly-size units, mock/simulation conflicts, possible species-versus-sample counts and shared accessions. {s['audit_flags']} flags include shared-accession pairs and multiple observations on the same record; they are not a count of confirmed independent errors. Earlier revisions are preserved as candidates; complete manual reconciliation remains unfinished.

## 4. Bounded current review

A new primary-source search was attempted on 5 November 2026. Europe PMC and publisher access were denied by the outbound proxy. No search-result counts are claimed. A documented repository-assisted thematic selection then inspected CAMI/AMBER, Vamb, SemiBin and linked graph, strain, simulation and contrastive-learning resources. Exact immutable source URLs, checksums and evidence excerpts are public. Thirteen article citations were checked against author/community documentation, not all full texts. Search strategy, inclusion criteria, thematic stop rule, synthesis and limits are in review.md.

CAMI I/II and CAMISIM establish why release, sample and simulation configuration matter [cami1; cami2; camisim]. GraphBin refines prior labels; MetaCoAG and GraphMB require graph-related inputs with different assumptions [graphbin; metacoag; graphmb]. Vamb/Avamb, SemiBin/SemiBin2 and COMEBin use different learned representations and training information [vamb; avamb; semibin; semibin2; comebin]. MetaBinner adds ensemble construction [metabinner]. The Vamb README also links a 2026 TaxVamb DOI, retained as an incompletely extracted current resource rather than a fully reviewed article. A complete publication-level reporting assessment is outside this release's verified evidence.

## 5. Computed catalog results

All metadata-presence percentages use the same denominator: {s['records']} canonical subset rows. They measure whether the historical workbook contains a nonempty assertion, never whether authors documented the field. No reporting-quality percentage or weighted reproducibility score is inferred.

'''
 report+='| Field | Nonempty historical cells | Denominator | Percentage |\n|---|---:|---:|---:|\n'
 for x in stats:report+=f"| {x['field']} | {x['nonempty_historical']} | {x['denominator']} | {x['percent_nonempty']}% |\n"
 report+='''
![Historical metadata presence](../figures/metadata.png)

Figure 1. Historical metadata presence, denominator 63 subset records. Nonempty cells can still be wrong or ambiguous; missing cells are not paper omissions. Data: field_presence.csv.

The reuse analysis counts workbook-reported subset-reference relationships. It is not a newly confirmed study-dataset bipartite graph. Family aggregation sums relationships and can count several subsets from one family/study; no independent-study rate is calculated. The selected matrix columns are disclosed in the analysis script. Origin and technology plots describe the historical selection; contradictory origin labels remain a visible category. All 63 historical ground-truth statuses are not extracted, not “no truth available”. The official AMBER truth artifact is verified separately.

![Reported reuse](../figures/reuse.png)

Figure 2. Workbook-reported reuse, aggregated by provisional family for selected references. Cells count subset-reference edges, not independent experiments. Unverified and incomplete.

## 6. Predeclared small evaluation

The protocol was saved before successful execution in experiments/protocol.json. Dataset: official CAMI I low-complexity gold-standard assembly example, SampleID CAMI_low; exact input identity comes from checksums, not label alone. Upstream AMBER commit f8b3a601043d13fc4227d5691c13561eb4490e50, evaluator version 2.0.8. Two prediction files are labelled CONCOCT (exact binary version not established) and MaxBin 2.0.2 (upstream label).

Three assignments and the genome-removal table total less than 3 MB. No raw reads or assemblies were reconstructed. Inputs remain upstream and are fetched with an immutable commit and validated hashes. The AMBER repository is GPL-3.0; upstream fixtures are not redistributed. The task verifies equal SampleID, unique sequence IDs and that prediction IDs belong to the gold standard.

Settings follow the official tested example: remove genomes marked “circular element”, discard 1% smallest predicted bins, minimum sequence length 0, completeness thresholds 50/70/90% and contamination thresholds 10/5%. Compute limits: 2 numeric-library threads, 180-second subprocess timeout, 3 MB input cap. Wall time is measured for the AMBER subprocess including its report generation, not binner training or a performance benchmark. Peak memory was not measured. Definitions follow AMBER's source/documentation [amber].

Mean purity (precision_avg_bp) is the unweighted mean of within-bin dominant-genome bp fractions. Mean completeness (recall_avg_bp) is AMBER 2 mapped-genome completeness; genomes without a mapped prediction are treated differently by the CAMI 1 metric. Binned bp fraction uses the evaluator's sample universe. Accuracy counts correctly assigned dominant-genome bp over the complete sample. The adjusted Rand index uses the evaluator's bp partition definition. Raw evaluator output preserves all metrics, including alternative CAMI 1 averages. Do not mix these definitions.

'''
 report+='| Official output | Mean purity | Mean mapped-genome completeness | Binned bp fraction | Accuracy | Adjusted Rand index |\n|---|---:|---:|---:|---:|---:|\n'
 for x in metrics:report+='| '+x['Tool']+' | '+' | '.join(f'{float(x[k]):.6f}' for k in ['Average purity (bp)','Average completeness (bp)','Percentage of binned bp','Accuracy (bp)','Adjusted Rand index (bp)'])+' |\n'
 report+=f'''
Measured AMBER subprocess wall time for the recorded run: {run['wall_seconds']:.2f} seconds; Python {run['python']}; exit code {run['exit_code']}. Gold-standard input: {run['gold_sequences']} sequence identifiers and {run['gold_genomes']} genome identifiers before requested removals. Full command and timestamp are in results/run.json. The upstream expected-output fixture independently agrees with the selected numeric results within 1e-6.

![Common-protocol re-evaluation](../figures/evaluation.png)

Figure 3. Recomputed official example metrics. Same sample/truth and evaluator settings, archived predicted outputs. CONCOCT shows higher mapped-genome completeness and MaxBin higher purity in this specific example. No binners were run. These results are not a benchmark of current tools or evidence of biological novelty.

## 7. Answers, limitations and next work

RQ1: The historical collection covers CAMI releases, environmental/human communities, simulations, mixtures and long-read examples, but many variant identities and quantities require primary confirmation. RQ2: The workbook's field presence can be measured reproducibly; publication-level data/code/instruction availability cannot be inferred from it and has not been exhaustively assessed. RQ3: Fair comparison needs matching sample/assembly, truth universe, original training/features, filters, binning task and metric semantics. RQ4: Yes: two official archived outputs were successfully re-evaluated with one common AMBER protocol, bounded to an illustrative public example.

Coverage is selective, inherited labels may be wrong, and families are provisional. The current source review is repository-documentation based with incomplete full texts, supplements and external archive checks. The 2026 resource discovery is not evidence of exhaustive 2026 literature coverage. No dataset archive is declared complete or usable from a URL or HTTP response alone. No global method ranking is supported. Provenance of some historical citations remains contradictory.

Next priorities: full-text/supplement extraction; resolve flagged quantity, accession and sample-count claims; verify exact biological archive manifests and redistribution terms; expand beyond the official example using matched archived outputs; add strain-aware evaluation only with appropriate truth and denominators. These would strengthen scientific scope without treating interface work as research evidence.

## 8. Reproduction and publication

Run make setup, make reproduce, make test, make experiment, then make reproduce. The lockfile includes package hashes; the original administrative attachments are unnecessary. Scientific figures are exported as PDF, SVG and 320-dpi PNG. The static site uses no external assets or backend. See docs/reproduce.md for full instructions. GitHub publication state and any remaining Pages activation are reported separately in docs/publication.md; local generation does not establish public deployment.

## References

'''
 for x in read('data/curated/studies.csv'):report+=f"[{x['study_id']}] {x['title']} ({x['year']}). https://doi.org/{x['doi']} . Citation checked against {x['source_id']}; article full text not independently retrieved.\n\n"
 (R/'docs/technical_report.md').write_text(report)
 readme=f'''# Metagenomic Binning Benchmark Atlas

**Which metagenomic binning benchmarks can we fairly compare?** A provenance-aware catalog, bounded scoping review and executable common-protocol evaluation.

![Historical metadata availability](figures/metadata.png)

## What is here

- **{s['records']} historical subset records**, {s['families']} provisional families and {s['claims']} cell-traceable fields, imported from the most complete workbook revision.
- **{s['audit_flags']} audit flags** for ambiguous quantities, tool roles, identifiers and related inconsistencies; these are observations, not confirmed-error counts.
- **{s['article_citations']} article citations** checked against {s['primary_repository_sources']} primary repositories, with an explicit extraction boundary and a 2026 resource discovery.
- **Two official public outputs re-evaluated** with AMBER 2.0.8 on the same CAMI_low sample/truth: CONCOCT mean purity {m['concoct_purity']}, mapped-genome completeness {m['concoct_completeness']}; MaxBin {m['maxbin_purity']} and {m['maxbin_completeness']}.

[Explore the static site](https://martaforjaz.github.io/metagenomic-binning-benchmark-atlas/) · [Technical report (PDF)](docs/technical_report.pdf) · [Report (Markdown)](docs/technical_report.md) · [Catalog CSV](data/curated/datasets.csv) · [Scoping review](docs/review.md) · [Publication status](docs/publication.md)

## Read the evidence correctly

Metadata plots measure presence in the historical workbook, **not missing reporting in papers**. Catalog claims remain historically unverified with field-level provenance. All historical ground-truth statuses are not extracted; they do not mean truth is absent. Reported reuse edges are not newly verified study relationships. The literature review is bounded and repository-assisted: full-text/supplement review and external archive access are incomplete. No global ranking is produced.

The experiment recalculates archived official examples on simulated CAMI data; it does **not** execute binners or assess current method performance. AMBER 2 mapped-genome completeness differs from CAMI 1 completeness. See the [fixed protocol](experiments/protocol.json), [metrics](results/metrics.csv) and [execution record](results/run.json).

## Reproduce

Linux, Python 3.12, Git, uv and make. No GPU or large sequencing downloads.

```sh
make setup
make reproduce
make test
make experiment
make reproduce
```

[Complete instructions](docs/reproduce.md) · [Data dictionary](docs/data_dictionary.md) · [Audit](docs/audit.md) · [Provenance and access](docs/provenance.md) · [References](bibliography.bib)

## Research context

The 2024 NOVA undergraduate project, supervised by Andre Lamurias, involved literature research and dataset tables. This **2026 independent extension** adds the software, provenance model, audit, current scoped review and re-evaluation. It does not imply the former supervisor's participation or approval. Original administrative documents, video and third-party illustrations are not redistributed. All displayed figures are newly generated.

Metagenomic binning groups assembled DNA fragments into candidate genomes. Composition, abundance and assembly graphs provide complementary evidence, but a bin is not automatically a complete or uncontaminated genome. Fair evaluation requires a matching sequence universe, ground truth, task, filters and metrics.

Code: MIT. Original curation/text/figures: CC BY 4.0. External articles, metadata, tools and example data retain their own terms; [licenses and attribution](LICENSES.md). Maintained by Marta Forjaz. Review date: 5 November 2026.
'''
 (R/'README.md').write_text(readme)
 site=(R/'site/template.html').read_text()
 for k,v in m.items():site=site.replace('@@'+k+'@@',str(v))
 assert '@@' not in site
 (R/'site/index.html').write_text(site)
 pdf(report)
 dest=R/'site/downloads';dest.mkdir(exist_ok=True)
 for file in ['docs/technical_report.pdf','docs/technical_report.md','docs/review.md','docs/audit.md','docs/data_dictionary.md','docs/provenance.md','data/curated/datasets.csv','data/curated/claims.csv','data/derived/issues.csv','data/derived/field_presence.csv','results/metrics.csv','results/run.json','experiments/protocol.json','bibliography.bib']:
  if (R/file).exists():shutil.copy(R/file,dest/Path(file).name)
 print('Built README, technical report PDF/Markdown and static site')
def pdf(text):
 from reportlab.pdfbase import pdfmetrics
 from reportlab.pdfbase.ttfonts import TTFont
 import matplotlib
 fonts=Path(matplotlib.get_data_path())/'fonts/ttf'
 pdfmetrics.registerFont(TTFont('AtlasSans',str(fonts/'DejaVuSans.ttf')))
 pdfmetrics.registerFont(TTFont('AtlasBold',str(fonts/'DejaVuSans-Bold.ttf')))
 styles=getSampleStyleSheet()
 for style in styles.byName.values():style.fontName='AtlasSans'
 for name in ['Title','Heading1','Heading2']:styles[name].fontName='AtlasBold'
 styles['Normal'].fontSize=9;styles['Normal'].leading=13;styles['Normal'].spaceAfter=7
 styles['Title'].fontSize=27;styles['Title'].leading=31;styles['Heading1'].fontSize=16;styles['Heading1'].leading=20;styles['Heading2'].fontSize=13
 for n in ['Title','Heading1','Heading2']:styles[n].textColor=colors.HexColor('#142a38')
 story=[];lines=text.splitlines();i=0
 def para(t,style='Normal'):return Paragraph(html.escape(t).replace('**',''),styles[style])
 while i<len(lines):
  line=lines[i].strip();i+=1
  if not line:continue
  if line.startswith('|'):
   tablelines=[line]
   while i<len(lines) and lines[i].startswith('|'):tablelines.append(lines[i]);i+=1
   rows=[[para(x.strip()) for x in l.strip('|').split('|')] for l in tablelines if not re.match(r'^\|[- :|]+\|$',l)]
   width=475/len(rows[0]);t=Table(rows,colWidths=[width]*len(rows[0]),repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eef4f7')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#dce5e9')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5)]));story.extend([t,Spacer(1,12)]);continue
  if line.startswith('!['):
   path=re.search(r'\]\((.+)\)',line)[1];f=(R/'docs'/path).resolve();im=Image(str(f));scale=min(475/im.imageWidth,330/im.imageHeight);im.drawWidth=im.imageWidth*scale;im.drawHeight=im.imageHeight*scale;story.extend([Spacer(1,8),im]);continue
  if line.startswith('# '):story.append(para(line[2:],'Title'))
  elif line.startswith('## '):story.append(para(line[3:],'Heading1'))
  else:story.append(para(line))
 def footer(c,d):
  c.saveState();c.setFont('AtlasSans',8);c.setFillColor(colors.HexColor('#526673'));c.drawString(60,32,'Metagenomic Binning Benchmark Atlas | Independent extension | 2026-11-05');c.drawRightString(535,32,str(d.page));c.restoreState()
 SimpleDocTemplate(str(R/'docs/technical_report.pdf'),pagesize=(595.28,841.89),rightMargin=60,leftMargin=60,topMargin=48,bottomMargin=48,title='Metagenomic Binning Benchmark Atlas',author='Marta Forjaz').build(story,onFirstPage=footer,onLaterPages=footer)
if __name__=='__main__':build()
