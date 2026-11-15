# DSS LLM Research

Shared code repository for the **UW Data Science Society, Research & Analytics team** (Autumn 2026 to Winter 2027).

Each project team works in its own folder under `teams/`. Code that more than one team needs (seeding, bootstrap confidence intervals, run logging) lives in `shared/`.

## Projects

| Team | Project | Folder |
| --- | --- | --- |
| Neural Nexus (Niru, Yunseo, Ishan) | From Facts to Function Calls: Do Hallucination Neurons Govern Tool Hallucination in LLM Agents? | [`teams/neural-nexus`](teams/neural-nexus) |
| Research Navigator (Utkarsh, Shaurya) | Self-Improving LLM Literature Screening, Checked for Citation Accuracy | [`teams/research-navigator`](teams/research-navigator) |
| Reasoning Efficiency (Jai) | Same Model, Three Trainings: How Training Method Shapes Efficient Math Reasoning | [`teams/reasoning-efficiency`](teams/reasoning-efficiency) |

## Repository layout

```
dss-llm-research/
├── shared/                  # small utilities any team can import
│   └── dss_common/
├── teams/
│   └── <team>/
│       ├── README.md        # question, datasets, how to run
│       ├── requirements.txt # team-specific dependencies
│       ├── src/             # reusable code (importable)
│       ├── notebooks/       # exploration and analysis
│       ├── configs/         # experiment settings (YAML)
│       ├── data/            # local only, never committed
│       └── results/         # small summary tables and figures only
├── docs/                    # team-wide guides
└── .github/                 # PR and issue templates
```

## Getting started

Requires Python 3.11+ and Git.

```bash
git clone https://github.com/kim-gu06/dss-llm-research.git
cd dss-llm-research

# one virtual environment per team keeps dependencies from clashing
cd teams/<your-team>
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e ../../shared        # makes `import dss_common` work
```

Running on UW Hyak or Colab? See [`docs/compute.md`](docs/compute.md).

## How we work

- Branch from `main`, open a pull request, and get one review from a teammate before merging. Details in [`CONTRIBUTING.md`](CONTRIBUTING.md).
- **Never commit** datasets, model weights, API keys or large outputs. The `.gitignore` blocks the common cases; check `git status` before you commit anyway.
- After each meeting, spend about 10 minutes updating the **26AU R&A Tracker** with progress, next steps and blockers.
- Long-term goal: work strong enough to present at the UW Undergraduate Research Symposium.

## Contacts

Research & Analytics Lead: Kimberly Gu xieng@uw.edu
