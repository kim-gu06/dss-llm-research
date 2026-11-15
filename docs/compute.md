# Compute

Every project here runs 4B to 8B models, so most real runs need a GPU.

## Options

- **UW Hyak (Klone)**: the main option for full runs. Access goes through a UW group allocation, and DSS is confirming which allocation the team can use. Keep large files in scratch, not in your home directory.
- **Google Colab**: fine for pilots and small subsets. Sessions reset, so save outputs to Drive.
- **Local laptop**: data loading, analysis notebooks and CPU-only code.

## Habits that save GPU time

- Pilot on a small subset first (for example 50 problems or about 5 records per review) to measure runtime and token use before a full run.
- Use `vllm` for batched generation when you only need outputs, and Transformers plus `nnsight`/TransformerLens when you need activations.
- Cache model outputs to disk and grade or analyze from the cache instead of regenerating.
- Set `HF_HOME` to a scratch directory so model downloads do not fill your quota.

## Hugging Face access

Gemma and Llama checkpoints are gated. Accept the license on each model page, create a read token, and put it in `.env` as `HF_TOKEN`.
