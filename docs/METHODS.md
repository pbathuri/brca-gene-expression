# Analysis plan

The inferential unit is the patient. The default cohort uses complete tumor/normal pairs. Do not treat technical aliquots as independent people. If pairing cannot be established, stop and ask the mentor to approve a new design and cohort; do not quietly switch to unpaired testing.

## Model
For gene g and sample j, DESeq2 models K_gj with a negative-binomial distribution: mean μ_gj = s_j q_gj and variance μ_gj + α_g μ_gj². s_j accounts for library size/composition. The design is `~ patient + condition`, with normal as the reference. The condition coefficient estimates tumor-versus-normal log2 expression change conditional on patient. A paired design cannot independently estimate covariates constant within patient, such as sex; avoid collinear additions. A batch term requires variation and a full-rank design, not a blind formula change.

Filter genes with counts ≥10 in at least the number of paired patients. Freeze the rule before examining significance. Fit DESeq2 on raw integer counts. Use normalized counts or VST for visualization; never run DESeq2 on TPM, FPKM, log-CPM or VST values. Save design matrix, filter mask and sessionInfo.

Primary reporting: BH-adjusted p-value <0.05 and |log2 fold change|≥1 as a descriptive reporting threshold. This is not a formal test that the effect exceeds 1; such a claim needs an explicit effect-size threshold test. Report the full table, including NA adjusted p-values from filtering/outlier handling. Interpret unshrunken fold changes cautiously for low counts. LFC shrinkage is a useful extension with an explicitly supported method; do not claim the starter has performed it.

The Python demo uses a paired t-test on synthetic log-CPM to test file flow and plotting. It is **not** the real method, a biological benchmark or a shortcut to final results. Real mode invokes scripts/deseq2.R and fails if R/DESeq2 is unavailable.

## QC
Check raw library sizes and sample labels, then log-CPM PCA for an initial look. The R workflow supplies VST PCA and sample-distance clustering. Look for swapped labels, duplicates, gross library-size differences and unexplained outliers. Document exclusions based on data quality, not whether they strengthen a finding. Re-run the paired model after removing a sample only by removing or explicitly redesigning its pair.

## Pathways
Download a human gene-symbol GMT collection (for example MSigDB Hallmark) through its official site under its terms. Record version, retrieval date and hash; save as data/raw/pathways.gmt. Keep a stable Ensembl-to-symbol table from the same GDC annotation. The starter removes duplicate symbols entirely rather than selecting the most significant mapping. Report how many genes this loses.

Run over-representation analysis separately for upregulated and downregulated genes. Background is uniquely mapped genes eligible for the adjusted-p-value decision (nonmissing pvalue and padj), not every gene in the genome. Restrict each set to that universe and test sets of size 15–500. A hypergeometric upper-tail test measures overlap; the script adjusts all up/down pathway tests together using BH. Report tested set count, background count and overlaps even when no pathway is significant. Selection and independence assumptions limit interpretation. Ranked GSEA is an optional second approach, not interchangeable with this overlap test.

## Sensitivity and interpretation
Week 4: compare min-count thresholds 5, 10 and 20 with the same paired design, and compare top-gene overlap/effect directions rather than only discovery counts. The HPC script supports these real DESeq2 refits. Also inspect whether a small number of patients drives an effect; a leave-one-pair-out extension requires fresh fits.

Read primary literature for three selected genes/pathways, and distinguish known biology from a new hypothesis. Cell-type mixture, adjacent-normal field effects, subtype and batch can explain associations. These findings cannot establish causation or diagnose/treat a patient. External validation is outside the minimum five-week scope.
