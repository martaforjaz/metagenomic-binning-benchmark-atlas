# Reproduce the atlas

Tested on Linux x86-64 with Python 3.12.14. Requires Git, Python 3.12, uv, make and network access to GitHub and PyPI for first installation. Python package versions and artifact hashes are in `requirements.lock`. No GPU, aligner, raw reads or binner installation is needed. Scientific analysis runs offline after dependency installation; the official example is fetched separately.

```sh
make setup
make reproduce   # curate the published scientific extraction, validate, figures, reports/site
make test
make experiment  # fetch immutable AMBER commit and verify small official input hashes; reevaluate
make reproduce  # incorporate recalculated metrics into figures/reports
```

`make experiment` runs AMBER 2.0.8 directly from a fixed upstream commit using the locked environment. Its own requirement versions match requirements.in. It checks SampleID, unique sequence identifiers, prediction subsets of gold and total input size before evaluating. No input files are redistributed. The predeclared settings remove entries marked circular element and apply 1% smallest-bin filtering. Do not compare these metrics with runs using other filters. `results/amber_results.tsv` preserves full evaluator output; the ignored `results/amber/` directory contains the full local interactive report.

The original workbook is unnecessary to reproduce the **published** extraction and analysis. To reimport it if privately available:

```sh
.venv/bin/python scripts/import_workbook.py /private/path/Table_datasets_MetagenomicBinning.xlsx
make reproduce
```

The importer only reads scientific table cells; do not put attachments in the checkout. Source workbook SHA-256 is checked against the published manifest when auditing a reimport. To update the current literature curation, edit study/source records after reading identified sources, retain extraction scope and dates, then rerun tests. Repository citation verification is not a full-text paper audit.

Serve the static site with `python3 -m http.server 8000 --directory site` and open it locally. No backend, telemetry or third-party JavaScript is used. The search filters subset, family, accession, origin, platform and environment. Download the CSV for the full evidence fields and raw claims.

`make pdf` uses ReportLab through the report builder, without LaTeX. All figures are generated in vector PDF/SVG and 320 dpi PNG. The PDF is a readable technical-report rendering; machine-readable tables and full citations live alongside it.
