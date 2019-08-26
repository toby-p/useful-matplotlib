
import matplotlib.pyplot as plt
import numpy as np


def normal_probability_plot(x, n_bins=20, random_seed=None):
    """Normal probability plot showing standardized values of `x` against a
    normally distributed dataset of the same length. Also plots a histogram of
    the standardized values of `x`.

    Args:
        x (list, array: float): datapoints.
        n_bins (int): number of bins in the histogram.
        random_seed (int): numpy random seed to produce reproducible plots.
    """
    # Standardize x to the normal distribution:
    x = sorted((x - x.mean()) / np.std(x))

    # Create a random truly norma distribution of the same length:
    if random_seed:
        np.random.seed(random_seed)
    normal = sorted(np.random.normal(0, 1, len(x)))

    # Make the plots:
    fig, ax = plt.subplots(1, 2, figsize=(12, 5), dpi=200)
    ax[1].hist(x, n_bins, alpha=1)
    min_xy = min(normal+x)
    max_xy = max(normal+x)
    ax[0].plot([min_xy, max_xy], [min_xy, max_xy], color="r", linewidth=3, zorder=0)
    ax[0].scatter(x, normal, zorder=1, s=20)

    # Customize axes & labels:
    [ax[0].spines[s].set_visible(False) for s in ["right", "top"]]
    [ax[1].spines[s].set_visible(False) for s in ["right", "top"]]
    ax[0].set_xlabel("Standardized Observed Value", weight="bold", size=12)
    ax[0].set_ylabel("Expected Normal Value", weight="bold", size=12)
    ax[1].set_xlabel("Standardized Observed Value", weight="bold", size=12)
    ax[1].set_ylabel("Datapoint Count", weight="bold", size=12)

    return fig
