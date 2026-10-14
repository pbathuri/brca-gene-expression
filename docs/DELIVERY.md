# Scientific handoff

Before using real mode:
```bash
Rscript scripts/install_bio.R
Rscript scripts/deseq2.R data/raw outputs/real
```
Run the first command once in a supported R/Bioconductor environment, not in a compute job. Record R and Bioconductor versions and create an renv lock after verification. Installations can differ between laptop and cluster; sessionInfo belongs with every final run.

Required figures: cohort flow (patients/samples before and after exclusions), library-size distribution, VST PCA, sample-distance clustering, volcano plot, top-gene heatmap and pathway summary. Captions state sample size, normalization, comparison direction, thresholds and limitations. Gene heatmaps selected on significance are descriptive; they are not independent validation of class separation.

Required tables: source manifest, sample exclusions, full gene-level DE results, mapping-loss counts and up/down enrichment results including nonsignificant pathways. Keep patient-level outputs in approved storage.

Notebook 04 expects data/raw/pathways.gmt for real enrichment. If it is not available, the notebook tells you what to acquire instead of inventing pathways. Final release is incomplete until a legitimate gene-set library is supplied and interpreted.

Final talk: question/cohort; counts and design; QC; gene-level results; pathway interpretation; limits and next experiment. Include three literature-supported interpretations and one result that changed your initial expectation. A null result is acceptable. A screenshot of a volcano plot without a reproducible count-to-results path is not.

Acceptance: another student rebuilds the cohort matrix from the frozen manifest, reruns the R model, checks the contrast direction, and reproduces selected numerical results within appropriate tolerance. Compare the design matrix and tested-gene universe, not only file hashes. No clinical claims.
