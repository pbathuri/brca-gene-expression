# TCGA-BRCA cohort

Use GDC open-access **Gene Expression Quantification / STAR - Counts**, primary tumor and solid tissue normal only. Use the unstranded raw count column, not TPM or FPKM. No FASTQ/BAM processing is needed for this five-week project.

## Acquisition
```bash
python scripts/fetch_gdc.py --max-pairs 10
```
The default builds a paired pilot cohort, writes candidates and the selected manifest, downloads the files, checks MD5 against GDC metadata, and builds counts.csv / samples.csv / genes.csv. For a full paired cohort after the pilot passes QA: `python scripts/fetch_gdc.py --max-pairs 0`. The script refuses to replace existing canonical inputs; move the previous cohort to an approved versioned location first. Download before a compute job; do not depend on outbound internet on compute nodes.

Selection is deterministic: complete patients sorted by ID, then one file per patient/condition sorted by UUID. This is an administrative duplicate rule, **not** a quality-based choice. Review candidates.csv to ensure it does not retain an inappropriate aliquot; record any revised rule before fitting. The script skips ambiguous multi-sample file associations rather than guessing. Compare selected IDs with the portal; archive the complete response and manifest.

## Canonical files
- `counts.csv`: gene_id rows, sample_id columns, raw nonnegative integers, no STAR summary rows.
- `samples.csv`: index sample_id, columns patient, condition (normal/tumor), file_id, sample_type. Row order must match counts columns exactly.
- `genes.csv`: gene_id, gene_name (and gene_type when available). Stable Ensembl IDs retain the original annotation in downloaded files; strip the version suffix only for matching. Fail on duplicates after stripping.
- `gdc_manifest.csv`: UUID, filename, checksum, patient/sample linkage and condition.

Validate complete pairs and one sample per patient/condition. Start with ten pairs. The full paired cohort is preferable to a hand-picked set. Record reasons for exclusions, counts before/after every filter, source access date and GDC release. Do not mix GDC releases or quantification workflows without resolving annotation differences.

Adjacent normal samples come from patients with cancer; this comparison is not cancer patients versus healthy volunteers. Tumor purity, cell composition, clinical subtype and collection/batch effects may contribute to differences. Pairing adjusts patient-level baseline differences, not all confounding.

Raw data are open-access but source terms and institutional rules still apply. Keep patient identifiers and sample-level tables out of public presentations where unnecessary. Publish code, permitted aggregate results and a reproducible acquisition specification rather than casually mirroring the entire cohort.

Optional Hugging Face mirrors are not the default. Before using one, verify original GDC UUIDs, annotation release, count units, transformations, license and patient pairing. If these cannot be recovered, do not substitute it for the defined cohort.
