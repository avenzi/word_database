import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import argparse
import json

if __name__ == "__main__":
    from scowl import get_words, filter, LEVELS
else:
    from .scowl import get_words, filter, LEVELS

ALLOWED_LETTERS = set('abcdefghijklmnopqrstuvwxyz')
OUTPUT_JSON = "freqs.json"


def total_frequency(words):
    """ Get the total frequencies of letters in a word list """
    if len(words) == 0:
        raise Exception("No words given")

    freq = {}
    for word in words:
        for i in range(len(word)):
            letter = word[i]
            freq[letter] = freq.get(letter, 0) + 1

    return freq


def frequency_plot(words, title):
    """
    Plot the letter frequency of the given <words>.
    The plot has the given <title>.
    """
    freqs = total_frequency(words)

    fig, ax = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
    fig.suptitle(title)

    total_sum = sum(freqs.values())

    # sorted alphabetically
    alpha_letters = sorted(freqs.keys())  # sorted alphabetically
    alpha_nums = [freqs[key]/total_sum for key in alpha_letters]  # sorted alphabetically

    ax[0].bar([let.upper() for let in alpha_letters], alpha_nums, align='center')

    # sorted numerically by frequency
    freq_letters = sorted(freqs.keys(), key=freqs.get, reverse=True)
    freq_nums = [freqs[key]/total_sum for key in freq_letters]

    ax[1].bar([let.upper() for let in freq_letters], freq_nums, align='center')

    # y axis labels
    ax[0].set_ylabel('Frequency (Alphabetical)')
    ax[1].set_ylabel('Frequency (Sorted)')
    ax[0].yaxis.set_major_formatter(PercentFormatter(1))  # percents
    ax[1].yaxis.set_major_formatter(PercentFormatter(1))  # percents

    plt.tight_layout()

    plt.show()
    plt.savefig(title)


def positional_frequency(words):
    """ Get the total and positional frequencies of letters in a word list """
    if len(words) == 0:
        raise Exception("No words given")

    freq = {}  # total: {}, 1:{}, 2:{}, 3:{} ...
    freq["total"] = {}
    for word in words:
        for i in range(len(word)):
            letter = word[i]
            freq["total"][letter] = freq["total"].get(letter, 0) + 1
            freq[i+1] = freq.get(i+1, {})
            freq[i+1][letter] = freq[i+1].get(letter, 0) + 1

    return freq


def positional_frequency_plot(words, title):
    """
    Plot the letter frequency of the given <words>.
    The plot has the given <title>.
    """
    freq = positional_frequency(words)

    fig, ax = plt.subplots(2, len(freq.keys()), figsize=(4*len(freq.keys()), 5), sharey=True)
    fig.suptitle(title)

    i = 0
    for plot in freq.keys():  # what are we plotting
        letter_freqs = freq[plot]
        total_sum = sum(letter_freqs.values())

        # sorted alphabetically
        alpha_letters = sorted(letter_freqs.keys())  # sorted alphabetically
        alpha_nums = [letter_freqs[key]/total_sum for key in alpha_letters]  # sorted alphabetically

        ax[0,i].bar([let.upper() for let in alpha_letters], alpha_nums, align='center')

        # sorted numerically by frequency
        freq_letters = sorted(letter_freqs.keys(), key=letter_freqs.get, reverse=True)
        freq_nums = [letter_freqs[key]/total_sum for key in freq_letters]

        ax[1,i].bar([let.upper() for let in freq_letters], freq_nums, align='center')

        # plot column title
        if type(plot) == str:
            plot_title = plot.capitalize()
        else:
            plot_title = f"Letter #{plot}"
        ax[0,i].set_title(plot_title)  # plot column title

        # increment plot index
        i += 1

    # y axis labels
    ax[0,0].set_ylabel('Frequency (Alphabetical)')
    ax[1,0].set_ylabel('Frequency (Sorted)')
    ax[0,0].yaxis.set_major_formatter(PercentFormatter(1))  # percents
    ax[1,0].yaxis.set_major_formatter(PercentFormatter(1))  # percents

    plt.tight_layout()

    plt.show()
    plt.savefig(title)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("level", nargs='?', help="Choose words from this SCOWL level or lower")
    args = parser.parse_args()

    if args.level:
        words = get_words(int(args.level))
    else:
        words = get_words()
    words = filter(words)
    print("Words pulled:", len(words))

    # output total letter frequency list to JSON
    freqs = total_frequency(words)
    maximum = max(freqs.values())
    freqs = {let: freq/maximum for let, freq in freqs.items()}
    with open('freqs.json', 'w') as file:
        json.dump(freqs, file)

    # plot it too
    frequency_plot(words, "Word Letter Frequency")


