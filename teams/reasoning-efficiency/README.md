# Reasoning Efficiency: Same Model, Three Trainings

**Team:** Jai Bhambhani

**Research question:** When the same 7B math model (Qwen2.5-Math-7B) is post-trained three ways, which method produces the most efficient reasoning once accuracy is weighted by problem difficulty and divided by tokens used?

## Models (all on Hugging Face)

| Role | Model |
| --- | --- |
| Control (base) | Qwen2.5-Math-7B |
| Distillation | DeepSeek-R1-Distill-Qwen-7B |
| RL only | SimpleRL-Zoo Qwen2.5-Math-7B (checkpoint TBD) |
| Fine-tuning + RL | Qwen2.5-Math-7B-Instruct |

## Data

- **MATH-500** ([HF: HuggingFaceH4/MATH-500](https://huggingface.co/datasets/HuggingFaceH4/MATH-500)): 500 problems, 7 subjects, difficulty levels 1 to 5.
- **Generated responses:** 4 models x 500 problems x 4 attempts = 8,000 graded responses (to be released publicly in Winter).

## Metric: Reasoning Efficiency Gain (REG)

Difficulty-weighted gain over the base model per 1,000 tokens. With level L_i, per-problem accuracy c_{m,i} over 4 attempts, and mean tokens T_m:

```
REG_m = [ sum_i L_i * (c_{m,i} - c_{0,i}) / sum_i L_i ] / (T_m / 1000)
```

(Confirm this matches the definition in the proposal before implementing; the PDF export dropped the formula.)

## Planned layout

```
src/
  generate.py   # vLLM generation: same prompt, 4 attempts, temp 0.6, 4,096-token cap
  grade.py      # extract final answers, auto-check, flag truncated responses
  reg.py        # REG and its two parts, overall and by subject
  models.py     # mixed-effects models (statsmodels)
configs/
  pilot.yaml
```

## Evaluation plan

Bootstrap 95% CIs (2,000 resamples over problems), split-half reliability (attempts 1 to 2 vs 3 to 4), sensitivity to IRT and equal weights, auto vs hand grading on 100 responses, Holm correction.

## Next steps (from the proposal)

| Task | Owner | Target |
| --- | --- | --- |
| Confirm GPU; pilot one model on 50 problems | Jai | Nov 14 |
| Build grading pipeline; hand-check pilot grades | Jai | Nov 21 |
| Generate all 8,000 responses; first REG | Jai | Dec 5 |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # vLLM needs a Linux GPU machine (Hyak/Colab)
pip install -e ../../shared
```
