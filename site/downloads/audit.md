# Audit of the 2024 material

Audited 5 November 2026. The original PDF and activity spreadsheet establish a January–February 2024 undergraduate research placement at NOVA, supervised by André Lamúrias. They describe reading papers, weekly discussions and successive Excel tables. They express an ambition to supply baseline results; they do **not** document commands, output files or an executed baseline. No historical experimental result is claimed here. The 2026 extension is independent and does not imply the supervisor's participation or approval.

## Version choice and privacy

The dataset workbook has Table1 (62 × 38 cells), Table2 (53 × 17), Table3 (68 × 16), Table4 (97 × 19) and References3&4 (227 × 15). These are successive revisions, not five independent collections. Table4 rows 6–68 contain 63 records and add simulator/assembler separation, read length, year and reuse references. Its tool legend and data dictionary start below the dataset block and must not become dataset rows.

The importer preserves scientific cells from earlier versions as recovery evidence. `revision_matches.csv` records exact normalized-label candidates. It does not auto-fill fields: the earlier columns have different meanings and ambiguous sample subsets. Unmatched historical labels remain candidates, outside the 63-record denominator. The field-level recovery ledger contains 132 differing historical assertions, distinguishing recoverable missing values from conflicting revisions. These are candidates, not verified replacements. A full manual reconciliation remains future work.

Originals remain outside the Git checkout in the task's private attachment area. They are not uploaded to GitHub. The activity sheet and PDF contain an unnecessary student identifier and institutional administrative content. Only this paraphrased scientific audit is public. The video was not downloaded: no scientific calculation requires it and redistribution rights have not been established. The supplied Merenlab illustration is not used; all atlas figures are generated anew. No signatures, contacts or original cover pages are published.

## Specific inconsistencies and their treatment

| Example | Problem | Public treatment |
|---|---|---|
| CAMI2 HiSeq (Toy) | `2x245` in Size (Gbp) could encode a product, paired reads or a different unit | Quantity withheld; raw cell retained |
| CAMI2 Marine / Strain Madness / Rhizosphere | `3x105` is not an unambiguous scalar quantity | No assumed 315 Gbp or 300,000 bp conversion |
| Strong100 and WWTP N50 | 13.3, 8.7, etc. under a bp heading; likely unit/semantics ambiguity | Flag; do not silently multiply by 1,000 |
| WWTP assembly sizes | 0.86, 1.32, etc. without units | Preserve raw values; no inferred bp size |
| NWC2 / HSM / Strainberry | Mbp values in a Gbp-headed column | Explicit suffix is mechanically converted; still historically unverified |
| Mix-51 and sponge spike-ins | “Simulated” label versus physical DNA mixture description | Origin marked contradictory; variants remain separate |
| Mock sample counts | 10 or 17 may be community organism counts rather than number of samples | Flag, retain historical assertions |
| S3 / S4 | Same SRA accession | Possible duplicate; no automatic merge |
| Six WWTP subsets | Same project accession but different plant names | Shared-accession flags; retain distinct subsets |
| Sharon | 2012 table year versus 2013 citation | Online/issue date unresolved |
| HPM2 | 16S label, spelling and references 50/55 conflict with other provenance | Explicit reference/assay uncertainty |
| SimHC / simLC+ / simMC | MetaSim in assembler column; complexity labels suspect | Flag role and label ambiguity |
| Soil | Broad biodiversity paper cited as sequencing provenance | Accession-to-paper relationship not confirmed |
| References 2/54, 29/56 | Duplicate bibliography entries | Preserve historical numbering; canonical new study IDs independent |
| SemiBin / MetaBinner | Historical preprint dates | Current repository citations identify 2022 and 2023 journal papers |

The 82 flags are **audit observations**, including every detected shared-accession pair. They are not 82 proven scientific errors or independent failures. Family grouping is a curator inference from labels and project context, not demonstrated sequence identity.

## Data layers

A raw sequencing accession is not an assembly, a contig-to-genome mapping is not a sequencing dataset, and a binner output is not ground truth. The catalog therefore separates family, release/subset, assembly record, claim provenance, reported reuse relationship and experiment artifacts. An accession does not establish access, completeness, license or compatibility. Historical N50 values are never used as read length.
