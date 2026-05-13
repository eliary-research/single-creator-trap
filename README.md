# The Single-Creator Trap — Data + Preliminary Findings

This repository accompanies the preliminary report:

> Kim, C. (2026). *The Single-Creator Trap: Preliminary Findings from a Prospective Cold-Start Case Study*. Working paper, Eliary Inc.

**Status:** Preliminary report — manuscript in preparation.
**Target venue:** ICWSM 2027 (full paper, January 2027 submission).
**Author:** Chan Min Park (Eliary Inc.).
**License:** Data — CC BY 4.0. Code — MIT.

## What this is

A prospective case study of cold-start dynamics on a Q&A social platform launched March 29, 2026, with full anonymized telemetry across the first 21 days. The repository contains:

- `preliminary_findings_20260504.md` — 800-word preliminary report
- `data/` — 10 anonymized CSV/JSON files (Phase 1 baseline)
- `figures/` — figure rendering specifications and (forthcoming) generated PNGs
- `CITATION.cff` — citation metadata

## Why prospective failure documentation matters

The cold-start literature is dominated by retrospective studies of *successful* platforms — survivor bias systematically excludes the failure mode. We document a launch in real time that did not produce strong network effects, and define the Single-Creator Trap and the Creator Concentration Index (CCI) so that future researchers can apply the framework to their own platforms.

## Data manifest

All identifiers are hashed; no personally identifying information is present. Dates are preserved at day-level granularity.

| File | Rows | Purpose |
|------|------|---------|
| `baseline_phase1.csv` | 16 | Daily aggregate metrics (DAU, signups, content, CCI, network) Apr 1 – Apr 16 |
| `baseline_phase1.json` | 16 | JSON mirror of baseline CSV |
| `daily_metrics_phase1.csv` | 29 | Extended daily metrics Mar 18 – Apr 15 (k-factor, retention, network, ask-answer rates) |
| `daily_metrics_phase1.json` | 29 | JSON mirror |
| `creators_phase1.csv` | 50 | Per-creator cumulative content (raw username column dropped in `_anon` version) |
| `creators_phase1_anon.csv` | 50 | Per-creator cumulative content with `creator_001 … creator_050` anonymized IDs |
| `creators_phase1.json` | 50 | JSON mirror |
| `creators_phase1_anon.json` | 50 | JSON mirror, anonymized |
| `retention_phase1.csv` | ~60 | Cohort × day-offset × channel retention table |
| `activation_phase1.csv` | 2 | Channel-level activation funnel summary |

**Use `*_anon` files for any public analysis.** Non-anonymized files are retained internally for cross-validation only.

## Reproducing the analyses

The CSV files alone are sufficient to reproduce every numeric claim in the preliminary report. The full SQL extraction queries (against the production Spanner database) are documented in the forthcoming manuscript appendix.

```python
# Example: compute D-7 retention for the largest invite cohort
import pandas as pd

ret = pd.read_csv("data/retention_phase1.csv")
cohort = ret[(ret.cohort_date == "2026-04-02") &
             (ret.channel == "invite") &
             (ret.day_offset == 7)]
print(cohort.rate.values[0])  # 0.0732 → 7.3%
```

## Preliminary key findings (Phase 1)

- DAU peaked at 114 (April 2 launch spike) and collapsed to 7 by April 16 — a 94% drop in 14 days.
- The Creator Concentration Index (CCI) was ≥ 0.5 on most observation days; CCI = 1.0 on April 9 and April 13.
- Largest invite cohort (April 2, N = 123): D-1 = 50.4%, D-3 = 21.1%, **D-7 = 7.3%**.
- **Friendship-formation count: zero** across all 291 signups in 21 days. We interpret this as the structural shadow of single-creator dependency.

Phase 2 (intervention) and Phase 3 (creator silence test) data are under active analysis; results will appear in the full manuscript.

## Citing this work

Please cite as:

```bibtex
@misc{kim2026singlecreatortrap,
  author       = {Kim, Chanmin},
  title        = {The Single-Creator Trap: Preliminary Findings from a Prospective Cold-Start Case Study},
  year         = {2026},
  howpublished = {Eliary Inc. working paper, May 2026},
  url          = {https://github.com/eliary-research/single-creator-trap}
}
```

A `CITATION.cff` file is provided for automated citation parsers.

## Contact

Chan Min Park — chanmin@eliary.com

## License

- **Data** (`data/` directory): [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- **Documents and code**: MIT License

You are free to use, redistribute, and build upon the data and analyses with attribution.
