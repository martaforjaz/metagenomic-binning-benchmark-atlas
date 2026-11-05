# Data dictionary and schema

UTF-8 CSV with header; JSON catalog mirrors dataset rows. Stable IDs are allocated from the canonical workbook row (ds-001 = row 6) and must not be recycled when labels change. Blank scalar values mean unavailable in this extraction, never zero. Machine checks: `python scripts/validate.py`.

| File | Unit / key | Meaning |
|---|---|---|
| historical/table4.csv | one historical subset row; row | Scientific source assertions, before normalization |
| historical/workbook_cells.csv | sheet + cell | Scientific cell values and workbook SHA-256; excludes administrative attachments |
| historical/references.csv | reference_id + source_cell | Historical bibliography text; duplicate/colliding entries retained |
| curated/families.csv | family_id | Inferred grouping; not a sequencing identity assertion |
| curated/datasets.csv, catalog.json | dataset_id | Release/subset records, not individual samples or independent experiments |
| curated/claims.csv | claim_id | One of 16 fields per record, raw/normalized value, unit, source and epistemic status |
| curated/assemblies.csv | assembly_id → dataset_id | Assembly assertions separate from sequencing; values unverified |
| curated/reported_reuse.csv | dataset_id + reference_id | Workbook-reported reuse, not reverified study evidence |
| curated/studies.csv | study_id | Bounded current citation selection, source and extraction scope |
| curated/sources.csv | source_id | Immutable primary repository URL, commit, content hash, check date and excerpt |
| curated/current_resources.csv | resource_id | New resources/citations not fully reviewed as articles |
| derived/issues.csv | dataset_id + field + code + note | Audit flags; multiple flags/record, no error-rate denominator |
| derived/recovery_candidates.csv | dataset_id + field + source | Earlier values that fill a historical blank or differ from canonical assertions; not verified corrections |
| derived/revision_matches.csv | sheet + row | Earlier-version recovery candidates; no independent datasets |
| derived/field_presence.csv | field | Counts/percentages of nonempty historical cells over 63 records |
| derived/reuse_matrix.csv | family_id | Sum of subset/reference edges per selected study column |
| results/metrics.csv | Tool + Sample | Recomputed AMBER output fractions, separate from literature claims |
| experiments/protocol.json | one protocol | Fixed sample, evaluator commit/version, inputs, settings, metrics and resource limits |
| experiments/inputs.sha256.json | input path | Exact fetched third-party artifact identity and bytes |

## Dataset fields

`release` is only filled for explicit CAMI I/II labels, otherwise not extracted. `subset` preserves a cleaned historical name. `sample_count` is a syntactically parsed integer **claim**, with possible organism-count ambiguity flagged. `origin` is real/simulated/semi/contradictory; the historical terminology is not promoted to a verified ontology. `technology` corrects only the obvious Illumina spelling and retains uncertain claims. `environment` is original descriptive prose, not a validated environmental ontology.

`read_length_bp` describes each end for explicit `2xN` values and `read_layout=paired_end`; a bare number does not establish paired/single layout. `data_size_gbp` is sequencing-size metadata: explicit Mbp is divided by 1,000; bare scalar values inherit the Gbp heading. Products are withheld. Numeric normalization never establishes scientific validity. `accessions` retains identifiers regardless of which workbook archive column held them; no claim that an ENA-style accession is an NCBI-only identifier. `assembly_id` links assembly metadata, never a raw-read accession. `ground_truth_status=not_extracted` across the historical catalog is not evidence that ground truth does not exist. The official AMBER gold standard is verified separately by artifact checksums and sample/sequence validation.

## Claim status vocabulary

- `historical_unverified`: present in source workbook, not newly primary-source verified.
- `verified`: checked against an identified source/artifact; record scope/date.
- `not_extracted`: not extracted into this resource, including original blank/slash.
- `not_found_after_check`: a specific source was examined and the information was not found; requires check date and scope. Not used to reinterpret workbook blanks.
- `not_applicable`: explicitly inapplicable with justification; never inferred from slash.
- `contradictory`: inconsistent representation or conflicting evidence; raw value retained.
- `access_unconfirmed`: resource not successfully retrieved/validated for the stated operation.

Publication metadata availability, code availability, instructions, dataset access and gold-standard availability are separate concepts. No weighted reproducibility score is calculated. A 200 response is not a completeness or usability check.
