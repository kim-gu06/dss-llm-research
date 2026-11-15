# Contributing

## Branches

- `main` is always runnable. Do not push to it directly.
- Name branches `<team>/<short-description>`, for example `neural-nexus/triviaqa-probe` or `research-navigator/baseline-screener`.

## Commits

Small and descriptive: `Add BFCL multi-turn loader`, not `stuff` or `fix`.

## Pull requests

1. Open a PR into `main` when a piece of work runs end to end, even if results are preliminary.
2. Fill in the PR template (what changed, how to run it, what you checked).
3. At least **one teammate reviews** before merging. Cross-team reviews are welcome for anything in `shared/`.
4. Prefer *Squash and merge* so `main` history stays readable.

## Experiments

- Put settings in `configs/*.yaml`, not hard-coded in notebooks, so runs can be repeated.
- Set and record random seeds (`dss_common.seed_everything`).
- Log each run with `dss_common.log_run` so results, configs and the Git commit stay linked.
- Do a small dry run (a handful of examples, one iteration) before any full or paid run.
- Commit only small summaries to `results/` (CSV tables, PNG figures). Large outputs stay local or on Hyak.

## Notebooks

Clear large outputs before committing, and move code you reuse into `src/`. Name notebooks with a number prefix: `01_load_data.ipynb`, `02_baseline.ipynb`.

## Secrets

Keep API keys in a local `.env` file (copy `.env.example`). `.env` is gitignored. If a key is ever committed, tell Kim right away and rotate it; deleting the commit is not enough.
