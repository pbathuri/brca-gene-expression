# Five-week roadmap

Week 1 begins at kickoff; enter actual dates on the issue board. Every gate needs a peer review and mentor sign-off.

## Week 1 — Build a defensible cohort

**Build:** Query GDC; download count files; record file UUIDs, checksums and paired sample metadata.

**Learn:** Read a STAR count file and distinguish a patient, sample and aliquot.

**Evidence:** Frozen manifest, counts matrix, sample table and cohort flow.

**Done when:** At least ten complete pairs or lead-approved scope change; no duplicate aliquots.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## Week 2 — Inspect and normalize

**Build:** Audit library sizes and low counts; fit size factors; inspect VST PCA and clustering.

**Learn:** Explain why counts, TPM and transformed counts serve different purposes.

**Evidence:** QC notebook, exclusion log, sample-distance heatmap and PCA.

**Done when:** Metadata aligns exactly with columns; outliers are investigated before outcomes are selected.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## Week 3 — Estimate differential expression

**Build:** Fit DESeq2 with patient + condition; use tumor-versus-normal contrast and BH adjustment.

**Learn:** Interpret log2 fold change, p-value, FDR and independent filtering.

**Evidence:** Full DE table, volcano plot, coefficient/design audit and HPC record.

**Done when:** Full-rank paired design; one sample per patient/condition; all tested genes retained in export.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## Week 4 — Interpret pathways and check sensitivity

**Build:** Map stable IDs to unique symbols; perform enrichment separately for up/down genes.

**Learn:** Explain the tested-gene background and why enrichment is not proof of mechanism.

**Evidence:** Pathway tables, top-gene heatmap and sensitivity comparison.

**Done when:** Gene-set version and mapping losses recorded; BH across tested pathways; limitations explicit.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## Week 5 — Write and reproduce the scientific story

**Build:** Review selected genes against primary literature; repeat from frozen inputs.

**Learn:** Separate discovery, replication and clinical claims.

**Evidence:** Reproducible notebooks, scientific figures, 6-slide talk and methods note.

**Done when:** Independent rerun; three gene/pathway interpretations cited; no diagnostic claims.

**Work split:** S1 audits inputs; S2 implements or verifies transformations; S3 owns the analysis decision; S4 communicates it; S5 reruns and records failures. See BACKLOG.csv for concrete assignments.

## If time gets tight

Keep acquisition, one defensible baseline, validation and the final explanation. Defer extra seasons/assets, advanced models and visual polish. Do not replace missing real data with unlabeled demo outputs.
