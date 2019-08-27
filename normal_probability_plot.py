
import matplotlib.pyplot as plt
import numpy as np


def normal_probability_plot(x, n_bins=20, random_seed=None, **kwargs):
    """Normal probability plot showing standardized values of `x` against a
    normally distributed dataset of the same length. Also plots histograms of
    the standardized and real values of `x`."""
    d = dict(label_size=11, dpi=150, figsize=(12, 4))
    kw = {**d, **kwargs}

    fig, ax = plt.subplots(1, 3, figsize=kw["figsize"], dpi=kw["dpi"])

    # Plot the real value histogram:
    ax[2].hist(x, n_bins, alpha=1)

    # Standardize x to the normal distribution:
    x = sorted((x - x.mean()) / np.std(x))

    # Create a random truly norma distribution of the same length:
    if random_seed:
        np.random.seed(random_seed)
    normal = sorted(np.random.normal(0, 1, len(x)))

    ax[1].hist(x, n_bins, alpha=1)
    min_xy = min(normal + x)
    max_xy = max(normal + x)
    ax[0].plot([min_xy, max_xy], [min_xy, max_xy], color="r", linewidth=3, zorder=0)
    ax[0].scatter(x, normal, zorder=1, s=20)

    # Customize axes & labels:
    [ax[0].spines[s].set_visible(False) for s in ["right", "top"]]
    [ax[1].spines[s].set_visible(False) for s in ["right", "top"]]
    [ax[2].spines[s].set_visible(False) for s in ["right", "top"]]
    ax[0].set_xlabel("Standardized Observed Value", weight="bold", size=kw["label_size"])
    ax[0].set_ylabel("Expected Normal Value", weight="bold", size=kw["label_size"])
    ax[1].set_xlabel("Standardized Observed Value", weight="bold", size=kw["label_size"])
    ax[1].set_ylabel("Datapoint Count", weight="bold", size=kw["label_size"])
    ax[2].set_xlabel("Real Observed Value", weight="bold", size=kw["label_size"])
    ax[2].set_ylabel("Datapoint Count", weight="bold", size=kw["label_size"])

    return fig
