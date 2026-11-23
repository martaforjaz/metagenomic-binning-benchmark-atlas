# Metagenomic Binning Benchmark Atlas

**Which metagenomic binning benchmarks can we fairly compare?** A provenance-aware catalog, bounded scoping review and executable common-protocol evaluation.

![Four phases from published records to catalog, validation and comparison.](figures/paper-workflow.svg)

The workflow distinguishes historical catalog provenance from standardized evaluation.

![Percent of historical workbook records with an entry for each catalog field.](figures/paper-results.svg)

Coverage describes the 63 historical workbook records. It does not measure reporting completeness in the original publications.
The vector figures are available as PDF in [figures/](figures/). With Python, NumPy and Matplotlib installed, run `python paper_figures.py` to regenerate them. The visual conventions follow [figures4papers](https://github.com/ChenLiu-1996/figures4papers).

## What is here

- **63 historical subset records**, 33 provisional families and 1008 cell-traceable fields, imported from the most complete workbook revision.
- **82 audit flags** for ambiguous quantities, tool roles, identifiers and related inconsistencies; these are observations, not confirmed-error counts.
- **13 article citations** checked against 11 primary repositories, with an explicit extraction boundary and a 2026 resource discovery.
- **Two official public outputs re-evaluated** with AMBER 2.0.8 on the same CAMI_low sample/truth: CONCOCT mean purity 0.837, mapped-genome completeness 0.933; MaxBin 0.948 and 0.826.

[Explore the static site](https://martaforjaz.github.io/metagenomic-binning-benchmark-atlas/) · [Technical report (PDF)](docs/technical_report.pdf) · [Report (Markdown)](docs/technical_report.md) · [Catalog CSV](data/curated/datasets.csv) · [Scoping review](docs/review.md) · [Publication status](docs/publication.md)

## Follow a catalog field to its evidence

**Example: the AMBER publication DOI, `10.1093/gigascience/giy069`.**

1. **Publication.** Open the [AMBER paper via its DOI](https://doi.org/10.1093/gigascience/giy069).
2. **Catalog.** Find the `amber` row in [studies.csv](data/curated/studies.csv). Its `doi` points to the paper, and its `source_id`, `src-amber`, joins to [sources.csv](data/curated/sources.csv), which records the authors' repository documentation at a specific commit.
3. **Check.** Run `python -m pytest tests/test_atlas.py -k citations_have_traceable_primary_evidence -q` in the project environment. The [test](tests/test_atlas.py) checks that the DOI is in the [bibliography](bibliography.bib), that the evidence URL includes its pinned commit, and that the retrieval status is recorded as successful.

This check validates the citation and its evidence trail. Historical dataset values in [claims.csv](data/curated/claims.csv) have separate, workbook-cell provenance and retain their historical verification status.

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
