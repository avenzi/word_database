import matplotlib.pyplot as plt
from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.palettes import viridis
from bokeh.models import RadioButtonGroup, CustomJS, Select, TextInput
from bokeh.layouts import gridplot, widgetbox
from random import random

from scowl import Words


def difficulty(word, level):
    R = level / words.max
    F = words.letter_frequency(word)
    L = len(set(word))
    diff = ((1/(10*F))-(2/3)) * (abs((L-6)/3)+1) * (3*R**3 + 1)
    return diff, F


def make_search(source, name):
    """ Add a search widget to a bokeh plot """
    # Setting initial values
    select = Select(options=source.data[name])
    text = TextInput(placeholder='Search',
        callback=CustomJS(
            args=dict(source=source, name=name, select=select),
            code="""
                select.options = source.data[name].filter(i => i.includes(this.value));
                """
        )
    )
    return widgetbox(text, select)


def frequency_hist_total():
    all = words.get_words()

    avg_freqs_no_repeat = []
    avg_freqs_repeat = []
    for word in all:
        avg_freqs_no_repeat.append(words.letter_frequency(word, count_repeats=False))
        avg_freqs_repeat.append(words.letter_frequency(word, count_repeats=True))

    fig, ax = plt.subplots(2, 1, figsize=(10, 5), sharex=True, sharey=True)
    _, bins, _ = ax[0].hist(avg_freqs_no_repeat, bins=50, align='mid', label="No repeats")
    ax[0].set_title("Ignore Repeats")
    ax[1].hist(avg_freqs_repeat, bins=bins, align='mid', label="Repeats")
    ax[1].set_title("Count Repeats")
    ax[0].set_ylabel('Number of words')
    ax[1].set_xlabel('Total Letter Frequency')
    ax[1].set_xlim(0, 1)
    plt.tight_layout()
    plt.show()


def frequency_hist_by_level():
    """
    Displays the letter frequency of each word, separated by SCOWL level.
    """
    fig, ax = plt.subplots(words.max+1, 1, figsize=(5, 7), sharex=True)
    fig.suptitle("Word letter frequency by SCOWL Level")
    ax[words.max].set_xlabel('Word Letter Frequency')

    for level in range(words.max+1):
        all = words.get_words(min_level=level, max_level=level)
        freqs = []
        for word in all:
            freqs.append(words.letter_frequency(word))

        ax[level].set_ylabel(f"{level}")
        ax[level].hist(freqs, bins=50, align='mid', label="No repeats")
    plt.tight_layout()
    plt.show()


def frequency_by_length():
    """ Plots word frequency metric as a function of word length """
    TOOLTIPS = [
        ("WLF", "$y"),
        ("Length", "$x"),
        ("word", "@word"),
    ]
    p1 = figure(width=600, height=300, tooltips=TOOLTIPS)
    p1.xaxis.axis_label = f"Word Length"
    p1.yaxis.axis_label = "Word Letter Frequency"

    p2 = figure(width=600, height=300, tooltips=TOOLTIPS, x_range=p1.x_range, y_range=p1.y_range)
    p2.xaxis.axis_label = f"Number of Unique Letters"
    p2.yaxis.axis_label = "Word Letter Frequency"

    p3 = figure(width=600, height=300, tooltips=TOOLTIPS)
    p3.xaxis.axis_label = f"Word Length"
    p3.yaxis.axis_label = "Avg Letter Frequency"

    p4 = figure(width=600, height=300, tooltips=TOOLTIPS, x_range=p3.x_range, y_range=p3.y_range)
    p4.xaxis.axis_label = f"Number of Unique Letters"
    p4.yaxis.axis_label = "Avg Unique Letter Frequency"

    colors = viridis(words.max+1)
    labels = [f"L{lvl}" for lvl in range(words.max+1)]

    for level in range(0, words.max+1):
        all = words.get_words(min_level=level, max_level=level)
        _words = []
        lengths = []
        ulengths = []
        freqs = []
        avgfreqs = []

        for word in all:
            if random() < 1/(level+1):
                lengths.append(len(word))
                ulengths.append(len(set(word)))
                freqs.append(words.letter_frequency(word, avg=False))
                avgfreqs.append(words.letter_frequency(word, avg=True))
                _words.append(word)

        source = ColumnDataSource(data=dict(
            len=lengths,
            ulen=ulengths,
            freq=freqs,
            avgfreq=avgfreqs,
            word=_words,
        ))

        p1.circle('len', 'freq', size=4, source=source, name=labels[level], color=colors[level])
        p2.circle('ulen', 'freq', size=4, source=source, name=labels[level], color=colors[level])
        p3.circle('len', 'avgfreq', size=4, source=source, name=labels[level], color=colors[level])
        p4.circle('ulen', 'avgfreq', size=4, source=source, name=labels[level], color=colors[level])

    # Radio buttons
    b = RadioButtonGroup(labels=labels, active=0)
    b.js_on_click(CustomJS(
        args=dict(
            figs=[p1, p2, p3, p4],
            labels=labels
        ),
        code="""
        for (let fig of figs) {
            fig.select_one(this.labels[this.active]).visible = true
        }
        for (var label of labels) {
            if (label != this.labels[this.active]){
                for (let fig of figs) {
                    fig.select_one(label).visible = false
                }
            }
        }
        """
    ))

    p = gridplot([[p1, p2],[p3, p4],[b]])
    show(p)


def difficulty_by_variable():
    tooltips = [
        ("Difficulty", "$y"),
        ("word", "@words"),
    ]
    tools="pan,wheel_zoom,box_zoom,reset,ywheel_zoom"

    p1 = figure(width=400, height=400, tooltips=tooltips, tools=tools)
    p1.xaxis.axis_label = "Word Length"
    p1.yaxis.axis_label = "Difficulty"

    p2 = figure(width=400, height=400, tooltips=tooltips, tools=tools)
    p2.xaxis.axis_label = "Number of Unique Letters"
    p2.yaxis.axis_label = "Difficulty"

    p3 = figure(width=400, height=400, tooltips=tooltips, tools=tools)
    p3.xaxis.axis_label = "Average Letter Frequency"
    p3.yaxis.axis_label = "Difficulty"

    p4 = figure(width=400, height=400, tooltips=tooltips, tools=tools)
    p4.xaxis.axis_label = "SCOWL Level"
    p4.yaxis.axis_label = "Difficulty"

    colors = viridis(4)

    diffs = []
    levels = []
    freqs = []
    lengths = []
    ulengths = []
    total_words = []
    for level in range(0, words.max+1):
        all = words.get_words(min_level=level, max_level=level, min_length=4, vowel_required=True)
        for word in all:
            diff, freq = difficulty(word, level)
            diffs.append(diff)
            levels.append(level)
            freqs.append(freq)
            lengths.append(len(word))
            ulengths.append(len(set(word)))
        total_words += all

    source = ColumnDataSource(data=dict(
        diffs=diffs,
        freqs=freqs,
        levels=levels,
        lengths=lengths,
        ulengths=ulengths,
        words=total_words,
    ))

    p1.circle('lengths', 'diffs', size=5, source=source, color=colors[0])
    p2.circle('ulengths', 'diffs', size=5, source=source, color=colors[1])
    p3.circle('freqs', 'diffs', size=5, source=source, color=colors[2])
    p4.circle('levels', 'diffs', size=5, source=source, color=colors[3])

    g = gridplot([[p1, p2], [p3, p4]])
    show(g)

def full_difficulty():
    TOOLTIPS = [
        ("WLF", "$x"),
        ("Difficulty", "$y"),
        ("word", "@word"),
    ]
    p = figure(width=1000, height=600, tooltips=TOOLTIPS, title="Difficulty according to svg. frequency", tools="pan,wheel_zoom,box_zoom,reset,ywheel_zoom")
    p.xaxis.axis_label = "Word Letter Frequency"
    p.yaxis.axis_label = "Difficulty Score"

    colors = viridis(words.max+1)
    labels = [f"L{lvl}" for lvl in range(words.max+1)]

    for level in range(0, words.max+1):
        all = words.get_words(min_level=level, max_level=level, min_length=4, vowel_required=True)
        diffs = []
        freqs = []
        for word in all:
            diff, freq = difficulty(word, level)
            diffs.append(diff)
            freqs.append(freq)

        source = ColumnDataSource(data=dict(
            x=freqs,
            y=diffs,
            word=all,
        ))

        p.circle('x', 'y', size=5, source=source, name=labels[level], color=colors[level])

    b = RadioButtonGroup(labels=labels, active=0)
    b.js_on_click(CustomJS(
        args=dict(
            figs=[p],
            labels=labels
        ),
        code="""
        for (let fig of figs) {
            fig.select_one(this.labels[this.active]).visible = true
        }
        for (var label of labels) {
            if (label != this.labels[this.active]){
                for (let fig of figs) {
                    fig.select_one(label).visible = false
                }
            }
        }
        """
    ))
    g = gridplot([[p],[b]])
    show(g)


if __name__ == "__main__":
    words = Words()

    #frequency_hist_total()
    #frequency_hist_by_level()

    #frequency_by_length()
    difficulty_by_variable()
    full_difficulty()