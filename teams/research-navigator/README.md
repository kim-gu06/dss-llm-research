# Research Navigator: Self-Improving Literature Screening, Checked for Citation Accuracy

**Team:** Utkarsh, Shaurya

**Research question:** Can eval-driven prompt optimization raise the recall of an LLM literature-screening pipeline without lowering the accuracy of the claims it extracts and cites?

## Datasets

| Dataset | Measures | Source |
| --- | --- | --- |
| SYNERGY (26 systematic reviews, 169,288 records, CC0) | Screening recall and precision | [asreview/synergy-dataset](https://github.com/asreview/synergy-dataset) (`pip install synergy-dataset`) |
| SciFact (1,409 claims) | Whether a cited abstract supports a claim | [allenai/scifact](https://github.com/allenai/scifact) |
| Hand-labeled claim/citation pairs (~100) | Claim extraction and citation accuracy on full text | Built by the team; labels live in `labels/` |

## Planned layout

```
src/
  screener.py      # include/exclude from each review's eligibility criteria
  extractor.py     # claims with a quoted supporting span and a citation
  optimize.py      # DSPy prompt optimization on the dev split only
  evaluate.py      # recall/precision, SciFact support accuracy, hand-label accuracy
eval/              # READ-ONLY to the optimizer (see below)
  split.json       # fixed dev / held-out split of the 26 reviews
labels/
  guide.md         # labeling guide
configs/
  pilot.yaml
```

## Run controls

These come from the proposal and should be enforced in code, not just by habit:

- Every optimization run starts as a **dry run** (about 5 records per review, 1 iteration).
- Hard caps on records, iterations and API spend; the run stops at a cap.
- A full run needs an explicit `--full` flag and ends as a **draft PR** showing dev and held-out scores side by side. Both teammates review before merging.
- `eval/` and `labels/` are read-only to the optimizer. A `CODEOWNERS` rule on those paths can require both of you to approve changes.
- Report results only on held-out reviews, with bootstrap 95% CIs, 3+ seeds, and Cohen's kappa for the hand labels.

## Next steps (from the proposal)

| Task | Owner | Target |
| --- | --- | --- |
| Load SYNERGY and SciFact; fix the dev / held-out split | Utkarsh | Nov 17 |
| Build baseline screener and extractor; run on 3 dev reviews | Shaurya | Nov 20 |
| Write labeling guide; label first 30 pairs (two annotators) | Shaurya and Utkarsh | Nov 24 |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e ../../shared
cp ../../.env.example ../../.env   # add your API key
```
