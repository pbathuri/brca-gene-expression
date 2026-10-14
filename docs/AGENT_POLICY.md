# Controlled coding-assistant use

The student is the author of the decision and the reviewer of every line merged.

Allowed: ask for an explanation, propose a small function, draft a unit test, or diagnose an error using a minimal non-sensitive example. Before asking, write the expected input/output and one failure case yourself.

Do not delegate a whole analysis, invent results/citations, let an agent alter the cohort or metric definitions, or grant it production credentials. Do not send WRDS extracts, access tokens or patient-level data to an external assistant without explicit institutional permission. Public access does not automatically authorize uploading a dataset to another service.

For each meaningful assisted change:
1. Open an issue with the question and acceptance criterion.
2. Limit the agent to named files and a small task. Keep execution and network access under human control.
3. Inspect the diff. Run a hand-worked example and a relevant test.
4. Log tool/model, date, files changed, assistance summary, validation and reviewer in `docs/AI_LOG.csv`. Do not log secrets or copy private prompts.
5. Explain the code to your reviewer. If you cannot explain it, do not merge it.

An agent cannot approve its own patch, change access rights, publish data, create cluster allocations or decide statistical exclusions. The executive mentor signs off on method changes. A second student checks conclusions against computed results.

Prompt example: “Implement only the weighted eFG calculation from this public toy table. Do not alter metric definitions. Return a small diff and one zero-attempt test.”
