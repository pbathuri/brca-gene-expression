# Working as a team

| Seat | Primary responsibility | Name |
|---|---|---|
| S1 | Cohort steward | Fill at kickoff |
| S2 | QC engineer | Fill at kickoff |
| S3 | Statistics lead | Fill at kickoff |
| S4 | Pathway analyst | Fill at kickoff |
| S5 | Reproducibility lead | Fill at kickoff |

| Executive mentor | Scope, methods review, blocker escalation and acceptance | Fill at kickoff |

Each week everyone spends roughly 1 hour reading/practice, 2–3 hours building, 1 hour testing/review, and 1 hour meeting/documentation. Pair students with different strengths. Roles describe ownership, not permission to avoid learning another part of the workflow.

Review ring: S1 reviews S2, S2 reviews S3, S3 reviews S4, S4 reviews S5, S5 reviews S1. Rotate the meeting facilitator weekly. In Week 4, swap the analysis and data roles for the reproduction exercise. No one approves their own PR. The mentor reviews changes to the scientific question, cohort/universe, statistical design or publication policy.

Weekly meeting: 5 minutes blockers, 15 minutes two demos, 15 minutes evidence review, 15 minutes pair planning, 10 minutes issue assignment. Show a table, figure or failing test rather than a verbal percentage-complete update.

Use `week-N/short-topic` branches. One notebook owner per branch avoids JSON merge conflicts. Move reusable code into `src/`; clear sensitive notebook outputs before committing. A PR needs a question, a change summary, a reproduction command, a test result and one limitation. Small PRs should take under 15 minutes to review.

Blocked for 30 minutes? Record what you tried and ask your pair. Blocked for a day? Ask the mentor to choose a fallback. No access to HPC by Week 2 means run locally and retain the job scripts; do not claim a cluster run happened.
