# CLAUDE.md: Neural Nexus (H-Neurons in tool-calling agents)

Put this file at `teams/<team>/CLAUDE.md`. Read it fully before doing anything.

## Project

Question: do hallucination-associated neurons (H-Neurons) found on factual QA also drive hallucinated tool calls in multi-turn agents, and can suppressing them reduce hallucinations without hurting task completion?

Plan: (1) replicate H-Neurons (Gao et al. 2025, arXiv 2512.01797) on **Gemma-3-4B-IT** with TriviaQA; (2) test transfer to **BFCL v3 multi-turn** (Base, Missing Function, Missing Parameter); (3) scale the neurons by alpha in {1.0, 0.75, 0.5, 0.25, 0}; (4) extra eval on ToolBeHonest. Later models if compute allows: Mistral-7B-Instruct-v0.3, Llama-3.1-8B-Instruct.

## Deadlines (time-box everything)

- Nov 25: H-neuron pipeline pilot works
- Nov 28: full pipeline runs, H-Neurons identified
- Dec 2: suppression sweeps on multi-turn benchmarks

A working reference run beats a polished port. Do the simplest thing that meets each date.

## Environment

- Windows + WSL2 (Ubuntu), VS Code. Local GPU is NVIDIA. Heavy jobs (10x sampling at scale, big extraction, BFCL sweeps) go to Hyak, see `docs/compute.md`.
- Python 3.11+. Two separate venvs, never mixed:
  - team venv `teams/<team>/.venv`: our code (torch, transformers, sklearn, ...), plus `pip install -e ../../shared`
  - reference venv `~/venvs/href`: the official repo's `requirements.txt` (pulls vLLM, which pins its own torch)
- Gemma weights are gated; HF access is granted (`huggingface-cli login`). Judge key goes in `OPENAI_API_KEY`. **Never commit tokens, keys, weights, datasets or large outputs.**
- Always bf16 for anything that touches activations. Never fp16 (Gemma-3 is fragile) and never quantized (changes the activations we measure).

## Reference code

Official implementation: github.com/thunlp/H-Neurons (MIT). Team rule: **do not copy it into this repo.** Clone it outside, at `~/refs/H-Neurons` (override with env var `HNEURONS_REF`), and record the commit hash in `docs/`. Only reuse its code after checking the license; if we port a function, keep an attribution comment and the license notice, and tell the team lead.

## What the official README says (scripts not read yet)

1. `collect_responses.py`: sample TriviaQA, 10x per question for training, judge `rule` or `llm` (`gpt-4o`). Keep only questions that are consistently correct or consistently wrong.
2. `extract_answer_tokens.py`: LLM picks answer tokens in the tokenized response.
3. `sample_balanced_ids.py`: balanced faithful/hallucinated question IDs (1000).
4. `extract_activations.py`: CETT per neuron, `--method mean --use_mag --use_abs`, locations `answer_tokens`, `all_except_answer_tokens`, `input`, `output`.
5. `classifier.py`: sparse logistic regression, `--train_mode 3-vs-1` (paper setting), `--penalty l1`.
6. Intervention: scale the **input to `down_proj`** at neurons with positive L1 weights (`scripts/intervene_model.py` has examples).
- No script for the grid search over C. The paper picks C to maximize held-out accuracy plus TriviaQA performance under suppression. We write that.
- Each response gives **two rows**: answer-token cluster and other-token cluster (each a per-neuron mean CETT). y=1 only for the answer cluster of a **hallucinated** response; everything else is 0. (The paper's printed formula has faithful=1, which contradicts its prose. Use hallucinated=1.)

## Layout

Follow the team README's planned `src/`: `hneurons.py`, `agent_runs.py`, `probes.py`, `suppression.py`, `gating.py`. Add only `model.py` (loading, chat template, neuron index map) at first. Split other helpers out of `hneurons.py` only when they hurt.

Contracts between TriviaQA and BFCL sides (`hneurons.py` and `agent_runs.py` never import each other):
- **Neuron index map** (flat index <-> layer, neuron) from `model.py`; every artifact stores its ID and loading asserts it matches.
- **`answer_mask`**: bool over response tokens. TriviaQA: from the judge. BFCL: from the parsed call (function name + argument values).
- **`h_neurons.json`**: written by `hneurons.py` (indices, weights, C, map ID, model revision); read by `agent_runs.py`, `suppression.py`, `probes.py`.
- **Decision-point JSONL** per assistant turn: ids, turn, `prompt_ids`, `response_ids`, `prompt_len`, `answer_mask`, labels, alpha. Log exact generated token IDs, never re-tokenized text.

## Open checks (resolve first)

- Run `--help` on all five scripts, save output to `results/official_help.txt`.
- README step 1 writes `train_samples.jsonl` but step 2 reads `consistency_samples.jsonl`: find what produces it.
- Does `extract_activations.py` hook the input of `down_proj` or recompute the MLP with SiLU? Gemma uses GELU-tanh. Which layer path does it assume for Gemma-3's multimodal wrapper?
- Exact CETT formula behind `--use_mag --use_abs` (down_proj column norm?).
- TriviaQA parquet (`rc.nocontext`) present in the clone, or download from HF `mandarjoshi/trivia_qa`.
- vLLM on Gemma-3-4B with <12 GB VRAM may OOM; fall back to Hyak.
- BFCL: confirm Gemma-3-4B-IT is a supported model (prompt mode). Local BFCL models run through vLLM/sglang, so no hooks. Plan: OpenAI-compatible server wrapping the HF model with alpha hooks, pointed at by BFCL (`--skip-server-setup`), or a custom handler. Verify the flag in current docs.

## Status

Nothing done yet. No reference clone, no venvs, Gemma not loaded.

Goal 1 (done when all hold): Gemma-3-4B-IT loads in bf16 and answers chat-templated prompts greedily; the neuron index map is saved (expect 34 layers x 10,240 per layer, verify from config); alpha=1 scaling hook gives bit-identical outputs to the unhooked model; peak VRAM and tokens/sec noted. Then run the official scripts as a pilot (200 questions, 40 train IDs) before any porting.

## Conventions

- Use `dss_common` for seeding, `bootstrap_ci`, run logging. Do not reimplement them.
- Experiment settings in `configs/*.yaml` (judge model string, seeds, sample counts, C). `data/` is local only; `results/` is small tables and figures only.
- Metrics: hallucinated-call rate, task success, clarification/refusal rate, steps and latency, probe AUROC/F1, gated vs always-on. Held-out tasks, layer-matched random-neuron controls, multiple seeds, bootstrap CIs.
- Branch from `main`, open a PR, one teammate review. Update the 26AU R&A Tracker after meetings.

## How to work here

- Read files before editing. Small, reviewable changes. Never edit the reference clone.
- Run pilot-sized first. Ask before any run that spends meaningful API money (judge calls) or Hyak hours.
- Quote error messages verbatim when reporting problems. Don't guess about the official scripts; read them.
- Keep a short `docs/DEVIATIONS.md` of every place we depart from the paper or the official code.
