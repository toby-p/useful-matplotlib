
from bokeh.palettes import viridis


neon_5 = ["#4deeea", "#74ee15", "#ffe700", "#f000ff", "#001eff"]
itfc_blue = "#1919A3"
spine_color = "#b3b3b3"
tick_color = "#737373"


def make_colormap(labels, color_func=viridis, shuffle=False):
    """Make a color map of artist labels to HexColor.

    Args:
        labels (list of str): labels of plot artists (often DataFrame column
            names which are plotted).
        color_func (func): a function which will generate an arbitrary number of
            HexColors. The default is the `bokeh.palettes.viridis` function.
        shuffle (bool): if True then the colors will be chosen alternately from
            either end of the generated colors, which is useful if trying to
            separate the `labels` sequentially.
    """
    colors = color_func(len(labels))
    if shuffle:
        d = dict()
        for i, v in enumerate(labels):
            if i % 2 == 0:
                d[v] = colors.pop(len(colors)-1)
            else:
                d[v] = colors.pop(0)
    else:
        d = dict(zip(labels, colors))
    return d


