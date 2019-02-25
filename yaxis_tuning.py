"""Functions to help with formatting Matplotlib charts. The main function here
is `tune_mpl_yaxis`, which can be imported by modules which create Matplotlib
charts to fine-tune the y-axis format.
"""
import math
import numpy as np

def magnitude(x):
    """Get the order 10 magnitude of a float."""
    return int(math.log10(x))

def strip_trailing_zeroes(s):
    """Remove trailing zeroes from a string formatted float."""
    if "." in s:
        if s[-1:]=="0" or s[-1:]==".":
            s = s[:-1]
            return strip_trailing_zeroes(s)
        else:
            return s
    else:
        return s

def calc_y_lims(source_data, minmax_buffer=True, ylim0=False):
    """Determine y-axis limits for a Matplotlib figure axis.

    Args:
        source_data (pandas DataFrame): source data of the chart.
        minmax_buffer (bool): whether or not to include a whitespace buffer in
            the chart area around the top and bottom of the line plot.
        ylim0 (bool): if True force the minimum of the y-axis to zero regardless
            of the actual `datamin` value.
    """
    datamin, datamax = source_data.min().min(), source_data.max().max(),
    diff = datamax-datamin
    mag = magnitude(diff)
    interval = 10**mag
    while diff-interval<interval:
        interval/=10
    ymin = datamin-(datamin%interval)
    if minmax_buffer and math.isclose(ymin, datamin):
        ymin-=interval
    if ylim0:
        ymin = 0
    ymax = datamax - (datamax%interval)+interval
    if minmax_buffer and math.isclose(ymax, datamax):
        ymax+=interval
    return ymin, ymax

def list_decimal_precision(l):
    """Calculate the number of decimal places to display when printing numbers
    in a list, based on the range between the min and max values in the list.

    Args:
        l (list of floats/ints)
    """
    data_range = max(l)-min(l)
    if data_range==0 or np.isnan(data_range):
        return 1
    m = magnitude(data_range)
    if m>1: n = 0
    elif m==1: n = 1
    else: n = np.abs(m)+2
    return n

def str_format_float(f, precision, currency=False, trailing_zeroes=True):
    """String format a float to the desired precision.
    """
    s = "{:,.{}f}".format(f, precision)
    if not trailing_zeroes:
        s = strip_trailing_zeroes(s)
    s = s.replace("nan", "")
    if currency:
        s = "$"+s
    return s

def str_format_integer(i, currency=False, trailing_zeroes=False):
    """Prettily format an integer for printing."""
    if i==0: return "0"
    mag = magnitude(i)
    if mag >= 9: unit = "bn"
    elif mag >= 6: unit = "m"
    elif mag >= 4: unit = "k"
    else: unit = ""
    divisors = {"bn":1000000000, "m":1000000, "k":1000, "":1}
    detail = {"bn":2, "m":2, "k":1, "":0}
    f = "{:,.{}f}".format(i/divisors[unit], detail[unit])
    if not trailing_zeroes:
        f = strip_trailing_zeroes(f)
    f += unit
    if currency:
        f = "$" + f
    return f

def str_format_int_list(l, trailing_zeroes=False, currency=False):
    return [str_format_integer(i, currency, trailing_zeroes) for i in l]

def str_format_float_list(l, trailing_zeroes=False, currency=False):
    precision = list_decimal_precision(l)
    return [str_format_float(f, precision, currency, trailing_zeroes) for f in l]

def str_format_percent_list(l, trailing_zeroes=False):
    l = [pc*100 for pc in l]
    precision = list_decimal_precision(l)
    l = ["{:,.{}f}".format(pc, precision) for pc in l]
    if not trailing_zeroes:
        l = [strip_trailing_zeroes(s) for s in l]
    return ["{}%".format(s) for s in l]

def reduce_mpl_visible_yticks(ax, max_n_ticks=5):
    """Reduce the number of y-ticks visible on a Matplotlib axis.
    """
    ticks = [t for t in ax.get_yticks() if t>=ax.get_ylim()[0] and t<=ax.get_ylim()[1]]
    while len(ticks)>max_n_ticks:
        ticks = [t for i, t in enumerate(ticks) if i%2>0]
    return ticks

def tune_mpl_yaxis(ax, source_data, percent_format=False, currency_format=False,
                   max_n_ticks=None, trailing_zeroes=False, minmax_buffer=True,
                   ylim0=False, fontsize=12):
    """Fine-tune the display format of a Matplotlib y-axis.

    Args:
        ax (Matplotlib axis): plot area on which changes will be made.
        source_data (pandas DataFrame): source used to construct the chart.
        percent_format, currency_format (bool): whether or not to format the
            axis as a percent or currency. If both are supplied, percent takes
            precedence over currency.
        max_n_ticks (int): if supplied then the number of ticks on the axes will
            be reduced until it is less than or equal to the `max_n_ticks` arg
            (usually it ends up being less than this number).
        trailing_zeroes (bool): if True remove trailing zeroes on string
            formatted numbers (e.g. `1.0` becomes `1`).
        minmax_buffer (bool): if True make sure there is a buffer of whitespace
            around the top and bottom of the chart.
        ylim0 (bool): if True force the minimum of the y-axis to zero regardless
            of the minimum datapoint in the source.
        fontsize (float): size of the y-axis label font.
    """
    new_lims = calc_y_lims(source_data, minmax_buffer, ylim0)
    ax.set_ylim(new_lims)
    if max_n_ticks:
        ticks = reduce_mpl_visible_yticks(ax, max_n_ticks)
    else:
        ticks = [t for t in ax.get_yticks()]
    ax.set_yticks(ticks)
    data_min, data_max = source_data.min().min(), source_data.max().max()
    diff = data_max-data_min
    if diff>=10 and not percent_format:
        tick_labels = str_format_int_list(ticks, trailing_zeroes, currency_format)
    elif percent_format: # Percent format takes precedence over currency.
        tick_labels = str_format_percent_list(ticks, trailing_zeroes)
    else:
        tick_labels = str_format_float_list(ticks, trailing_zeroes, currency_format)
    ax.set_yticklabels(tick_labels, fontdict=dict(weight="bold", fontsize=fontsize))
