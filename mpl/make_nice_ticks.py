
import numpy as np

# Nice-looking human-interpretable tick intervals which will be allowed:
nice_intervals = [0.1, 0.2, 0.25, 0.5]


def make_ticks_nicer(ax, axis="y", min_buffer=0.025, max_buffer=0.025,
                     n_ticks=5, buffer_below_zero=False):
    """Brute force approach to making Matplotlib plots have `nice` looking,
    human-readable axis ticks.

    Args:
        ax (matplotlib.axes): axes object to apply changes to.
        axis (str): axis to apply changes to - either `x` or `y`.
        min_buffer (float): fraction of the total range of datapoints on the
            axis to add as a whitespace buffer before the minimum datapoint.
        max_buffer (float): fraction of the total range of datapoints on the
            axis to add as a whitespace buffer after the maximum datapoint.
        n_ticks (int): the absolute maximum number of generated ticks to
            return, including the axis minimum and maximum.
        buffer_below_zero (bool): if False and minimum plotted datapoint is >= 0
            then the new axis minimum will not be set below zero.
    """
    assert axis in ["x", "y"], f"Invalid `axis` arg: {axis}"
    datamin, datamax = eval(f"ax.dataLim.{axis}min"), eval(f"ax.dataLim.{axis}max"),

    # Just return plot if no data:
    if np.isnan(datamin) or np.isnan(datamax):
        return ax

    # Apply the buffer zones around the data:
    data_range = datamax - datamin
    if min_buffer:
        new_datamin = datamin - (data_range * min_buffer)
        if new_datamin < 0 <= datamin and not buffer_below_zero:
            new_datamin = datamin
        datamin = new_datamin
    if max_buffer:
        datamax += data_range * max_buffer

    # Use the real gap between the min/max datapoints to determine the range of
    # 'nice' tick gaps that we should start generating ticks for:
    abs_gap = abs(datamax - datamin) / n_ticks

    closest_ticks = {i: abs(abs_gap - i) for i in nice_intervals}
    closest_two = sorted(closest_ticks.values())[:2]
    closest_ticks = {k: v for k, v in closest_ticks.items() if v in closest_two}

    intervals = nice_intervals
    while True:  # Try bigger/smaller tick intervals to see if can get closer to abs_gap:
        bigger = [i * 10 for i in intervals]
        b_closest_ticks = {i: abs(abs_gap - i) for i in bigger}
        b_closest_ticks = {**b_closest_ticks, **closest_ticks}
        b_closest_two = sorted(b_closest_ticks.values())[:2]

        smaller = [i / 10 for i in intervals]
        s_closest_ticks = {i: abs(abs_gap - i) for i in smaller}
        s_closest_ticks = {**s_closest_ticks, **closest_ticks}
        s_closest_two = sorted(s_closest_ticks.values())[:2]

        if min(b_closest_two) < min(closest_two):
            closest_two = b_closest_two
            closest_ticks = {k: v for k, v in b_closest_ticks.items() if v in closest_two}
            intervals = bigger
        elif min(s_closest_two) < min(closest_two):
            closest_two = s_closest_two
            closest_ticks = {k: v for k, v in s_closest_ticks.items() if v in closest_two}
            intervals = smaller
        else:
            break

    # Iterate through each matching tick gap, create a set of ticks that spans the min
    # and max data points, and save to the dictionary:
    generated_ticks = dict()
    for gap in closest_ticks.keys():
        first_tick = (datamin // gap) * gap
        new_ticks = [first_tick]
        # Keep adding ticks until the tick max is greater than the data max:
        while new_ticks[-1] < datamax:
            new_ticks.append(new_ticks[-1] + gap)
        # Remove the first tick if the second is less than the data min:
        while new_ticks[1] < datamin:
            new_ticks = new_ticks[1:]
        # Save to the dictionary:
        generated_ticks[gap] = new_ticks

    # Calculate the length of each generated set of ticks, and find the set(s)
    # which are closest to the `n_ticks` arg:
    closeness_dict = {k: abs(len(v) - n_ticks) for k, v in generated_ticks.items()}
    closest = min(closeness_dict.values())
    closest = max([k for k, v in closeness_dict.items() if v == closest])
    ticks = generated_ticks[closest]

    # Add the ticks to the plot axis:
    eval(f"ax.set_{axis}ticks(ticks)")
    eval(f"ax.set_{axis}lim(ticks[0], ticks[-1])")
