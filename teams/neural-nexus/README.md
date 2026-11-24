# Neural Nexus: From Facts to Function Calls

**Team:** Niru A, Yunseo Ju, Ishan Sharma

**Research question:** Do hallucination-associated neurons (H-Neurons) identified from factual QA also drive hallucinated tool calls in multi-turn LLM agents, and can suppressing them reduce hallucinations without hurting task completion?

## Datasets

| Dataset | Use | Source |
| --- | --- | --- |
| TriviaQA | Identify factual H-Neurons | [HF: mandarjoshi/trivia_qa](https://huggingface.co/datasets/mandarjoshi/trivia_qa) |
| BFCL v3 Multi-Turn (Base, Missing Function, Missing Parameter) | Agent evaluation and probe training | [HF: gorilla-llm/Berkeley-Function-Calling-Leaderboard](https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard) |
| ToolBeHonest | Extra eval on unsolvable tool tasks | [GitHub](https://github.com/ToolBeHonest/ToolBeHonest) |

**Models:** start with Gemma-3-4B-IT; add Mistral-7B-Instruct-v0.3 and Llama-3.1-8B-Instruct if compute allows (Gemma and Llama are gated on Hugging Face).

**Reference code:** [thunlp/H-Neurons](https://github.com/thunlp/H-Neurons). Do not copy it into this repo; clone it alongside and check its license before reusing code.

## Planned layout

```
src/
  hneurons.py      # TriviaQA sampling + L1 logistic regression on neuron features
  agent_runs.py    # BFCL multi-turn runs, logging calls, args and activations
  probes.py        # factual vs agent-trained L1, MLP, SAE, random-neuron baseline
  suppression.py   # scale selected neurons by alpha in {1.0, 0.75, 0.5, 0.25, 0}
  gating.py        # risk classifier that suppresses only when risk is high
configs/
  gemma3_4b.yaml
notebooks/
  01_reproduce_hneurons.ipynb
  02_bfcl_baseline.ipynb
```

## Metrics

Hallucinated-call rate, task success rate, clarification/refusal rate, steps and latency per task, probe AUROC/F1, gated vs always-on. Use held-out tasks, random-neuron controls, multiple seeds, and `dss_common.bootstrap_ci`.

## Next steps (from the proposal)

| Task | Owner | Target |
| --- | --- | --- |
| Get H-neuron pipeline pilot to work | Ishan Sharma | Nov 25 |
| Get H-Neuron pipline to run fully, identify H-Neurons | TBD | Nov 28 |
| Run different the model w/ different suppression amounts on multi turn benchmarks | TBD | Dec 2|


## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e ../../shared
```
