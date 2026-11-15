from typing import Callable, Sequence

import numpy as np


def bootstrap_ci(
    values: Sequence[float],
    stat: Callable[[np.ndarray], float] = np.mean,
    n_resamples: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> tuple[float, float, float]:
    """Percentile bootstrap confidence interval.

    Resamples the *units* in `values` (e.g. one score per problem or per review)
    with replacement. Returns (point_estimate, lower, upper).
    """
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        raise ValueError("values is empty")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, arr.size, size=(n_resamples, arr.size))
    boot = np.array([stat(arr[i]) for i in idx])
    lower, upper = np.quantile(boot, [alpha / 2, 1 - alpha / 2])
    return float(stat(arr)), float(lower), float(upper)
