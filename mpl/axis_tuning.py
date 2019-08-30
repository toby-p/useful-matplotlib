def axis_lim_by_ticks(ax, axis="y", arbitrary_max=None):
    """Take a Matplotlib axes object and use the generated ticks to set the axis
    limit, by adding the tick/subtracting the tick value to get the tick
    multiple closest to the data max.

    Args:
        ax (Matplotlib axes): object to make changes to.
        axis (str): axis to tune either `x` or `y`.
        arbitrary_max (float): arbitrary maximum value to include in the axis
            range, otherwise determined by the plotted datapoints.
    """
    ticks = eval(f"ax.get_{axis}ticks()")
    tick_gap = truncate_float([ticks[i+1]-ticks[i] for i in range(len(ticks)-1)])
    tick_gap = list(set(tick_gap))
    if len(tick_gap)>1:
        _print("Unable to determine tick gap.")
        return
    else:
        tick_gap = tick_gap[0]
    _min, _max = eval(f"ax.get_{axis}lim()[0]"), eval(f"ax.get_{axis}lim()[1]")
    if axis=="x":
        data_max = ax.dataLim.max[0]
    elif axis=="y":
        data_max = ax.dataLim.max[1]
    if arbitrary_max:
        data_max = max(arbitrary_max, data_max)
    visible_ticks = [t for t in ticks if t<=_max and t>=_min]
    while True:
        if visible_ticks[-1]<data_max:
            visible_ticks.append(visible_ticks[-1]+tick_gap)
        elif visible_ticks[-1]-tick_gap>data_max:
            visible_ticks = visible_ticks[:-1]
        else:
            break

    eval(f"ax.set_{axis}lim(_min, visible_ticks[-1])")
    eval(f"ax.set_{axis}ticks(visible_ticks)")
