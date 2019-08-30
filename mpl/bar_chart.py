
import itertools
import matplotlib.pyplot as plt
import pandas as pd

from .colors import itfc_blue, neon_5, tick_color, spine_color


spines = ["top", "bottom", "right", "left"]


def bar_chart(df: pd.DataFrame, category_col: str, data_col: str,
              sort: str = "alpha", figsize: tuple = (6, 6), ax=None,
              drop_spines: list = None, x_labels: bool = True,
              x_rotation: int = 90, colors=neon_5):
    assert sort in ["alpha", "asc", "desc"], f"Invalid sort arg: {sort}"
    assert all([s in spines for s in drop_spines])

    # Get & sort data:
    s = df.groupby(category_col)[data_col].mean()
    if sort == "alpha":
        s = s.sort_index()
    elif sort == "asc":
        s = s.sort_values(ascending=True)
    elif sort == "desc":
        s = s.sort_values(ascending=False)

    # Define colors for the plot:
    if isinstance(colors, list):
        colour = dict(zip(list(range(len(s))), itertools.cycle(colors)))
        colour = list(colour.values())
    elif isinstance(colors, str):
        colour = colors
    else:
        colour = itfc_blue

    # Create the plot:
    if not ax:
        fig, ax = plt.subplots(figsize=figsize)
    ax.bar(x=range(len(s)), height=s.values, color=colour, width=0.8, bottom=[0 for _ in range(len(s))], align="center")

    # X-axis labels:
    if x_labels:
        ax.set_xticks(range(len(s)))
        ax.set_xticklabels(list(s.index), rotation=x_rotation)
    else:
        ax.set_xticks([])

    # Customise border spines:
    ax.tick_params(axis="x", colors=tick_color)
    ax.tick_params(axis="y", colors=tick_color)
    for loc in drop_spines:
        ax.spines[loc].set_visible(False)
    for loc in set(spines) - set(drop_spines):
        ax.spines[loc].set_color(spine_color)

    return fig
