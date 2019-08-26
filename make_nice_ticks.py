
import numpy as np

# Nice-looking human-interpretable tick intervals which will be allowed on the plot:
nice_intervals = np.array([1, 2, 5, 10, 25, 50, 100])


def make_ticks_nicer(ax, axis="y", min_buffer=0.025, max_buffer=0.025,
                     max_n_ticks=5, buffer_below_zero=False):
    """Brute force approach to making Matplotlib plots have `nice` looking,
    human-readable axis ticks.

    Args:
        ax (matplotlib.axes): axes object to apply changes to.
        axis (str): axis to apply changes to - either `x` or `y`.
        min_buffer (float): fraction of the total range of datapoints on the
            axis to add as a whitespace buffer before the minimum datapoint.
        max_buffer (float): fraction of the total range of datapoints on the
            axis to add as a whitespace buffer after the maximum datapoint.
        max_n_ticks (int): the absolute maximum number of generated ticks to
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
    old_min, old_max = datamin, datamax
    if min_buffer:
        new_datamin = datamin - (data_range * min_buffer)
        if new_datamin < 0 <= datamin and not buffer_below_zero:
            new_datamin = datamin
        datamin = new_datamin
    if max_buffer:
        datamax += data_range * max_buffer

    # Use the real gap between the min/max datapoints to determine the range of
    # 'nice' tick gaps that we should start generating ticks for:
    abs_gap = (datamax - datamin) / max_n_ticks
    test_gaps = list()
    intervals = nice_intervals
    last_checked = None
    while True:
        tick_gaps = [i for i in intervals if abs_gap/2 < i < abs_gap*2]
        if len(tick_gaps) == len(intervals):
            if last_checked == intervals:
                break
            intervals *= 10
        elif not len(tick_gaps):
            intervals /= 10
        else:
            break
        last_checked = intervals

    # Iterate through each matching tick gap, create a set of ticks that spans the min
    # and max data points, and save to the dictionary:
    generated_ticks = dict()
    for gap in tick_gaps:
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
    # which are closest to the `max_n_ticks` arg:
    closeness_dict = {k: abs(len(v) - max_n_ticks) for k, v in generated_ticks.items()}
    closest = min(closeness_dict.values())
    closest = max([k for k, v in closeness_dict.items() if v == closest])
    ticks = generated_ticks[closest]

    # Add the ticks to the axes and use the min/max to set axis limits:
    eval(f"ax.set_{axis}ticks(ticks)")
    eval(f"ax.set_{axis}lim(ticks[0], ticks[-1])")
