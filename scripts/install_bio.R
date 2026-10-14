# Run once in your approved R environment. Resolve/install packages before batch jobs.
if (!requireNamespace("BiocManager", quietly=TRUE)) install.packages("BiocManager", repos="https://cloud.r-project.org")
BiocManager::install("DESeq2", ask=FALSE, update=FALSE)
if (!requireNamespace("renv", quietly=TRUE)) install.packages("renv", repos="https://cloud.r-project.org")
print(sessionInfo())
# After the team confirms compatibility: renv::init(); renv::snapshot()
