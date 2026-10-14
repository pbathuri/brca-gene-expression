# Learning goals and evidence

Each reading is a 20–30 minute start, followed by a concrete exercise. Links are in SOURCES.md. The mentor asks each student to demonstrate the learning goal, not just show a completed file.

| Week | Read | Practice | Learning goal | Evidence |
|---|---|---|---|---|
| 1 | GDC STAR counts and API retrieval in SOURCES.md | Inspect one count file and draw patient/sample/file relationships. | Acquire high-dimensional biological data | Paired cohort manifest and schema checks |
| 2 | DESeq2 vignette: count matrix input, normalization and transformations | Explain where size factors, VST and raw counts are used. | Clean, normalize and explore | QC notebook with library sizes, PCA and clustering |
| 3 | DESeq2 vignette: paired samples, contrasts and multiple testing | Interpret a tumor-normal coefficient and distinguish p from FDR. | Perform differential expression | Reviewed paired model, full DE table and volcano plot |
| 4 | MSigDB collection documentation; METHODS.md: pathways | Count an overlap by hand and explain the gene universe. | Interpret biological pathways | Versioned gene sets, background and sensitivity comparison |
| 5 | Three primary papers chosen from the real results | State one mechanism hypothesis and one competing explanation. | Communicate genomic results reproducibly | Scientific figures, cited interpretation and clean rerun |

Across all five weeks: each student authors one small reviewed PR weekly, reviews the preceding seat’s work, records meaningful assistant use, and can rerun another student’s notebook. In Week 4, each team executes one real cluster job if access is available and explains its CPU/memory choice. An unavailable allocation must be reported, never disguised.
