import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from time import time
import os.path

ALLOWED_LETTERS = set('abcdefghijklmnopqrstuvwxyz')
REPLACE_LETTERS = {'ê': 'e', 'é': "e"}


def validate_words(words):
    """ Ensure only accepted letters are in the words """
    result = []
    for word in words:
        word = word.strip().lower()  # strip whitespace and convert to lower case
        if len(word) != 5:
            continue

        for letter, replacement in REPLACE_LETTERS.items():
            word = word.replace(letter, replacement)
        if set(word).issubset(ALLOWED_LETTERS):  # all letters are allowed
            result.append(word)
    return result


def frequency(words):
    freq = {}  # total: {}, 1:{}, 2:{}, 3:{} ...
    freq["total"] = {}
    for word in words:
        for i in range(len(word)):
            letter = word[i]
            freq["total"][letter] = freq["total"].get(letter, 0) + 1
            freq[i+1] = freq.get(i+1, {})
            freq[i+1][letter] = freq[i+1].get(letter, 0) + 1

    return freq


def plot(words, title):
    words = validate_words(words)
    freq = frequency(words)

    fig, ax = plt.subplots(2, len(freq.keys()), figsize=(4*len(freq.keys()), 7), sharey=True)
    fig.suptitle(title)

    i = 0
    for plot in freq.keys():  # what are we plotting
        letter_freqs = freq[plot]
        total_sum = sum(letter_freqs.values())

        # sorted alphabetically
        alpha_letters = sorted(letter_freqs.keys())  # sorted alphabetically
        alpha_nums = [letter_freqs[key]/total_sum for key in alpha_letters]  # sorted alphabetically

        ax[0][i].bar([let.upper() for let in alpha_letters], alpha_nums, align='center')

        # sorted numerically by frequency
        freq_letters = sorted(letter_freqs.keys(), key=letter_freqs.get, reverse=True)
        freq_nums = [letter_freqs[key]/total_sum for key in freq_letters]

        ax[1][i].bar([let.upper() for let in freq_letters], freq_nums, align='center')

        # plot column title
        if type(plot) == str:
            plot_title = plot.capitalize()
        else:
            plot_title = f"Letter #{plot}"
        ax[0][i].set_title(plot_title)  # plot column title

        # increment plot index
        i += 1

    # y axis labels
    ax[0][0].set_ylabel('Frequency (Alphabetical)')
    ax[1][0].set_ylabel('Frequency (Sorted)')
    ax[0][0].yaxis.set_major_formatter(PercentFormatter(1))  # percents
    ax[1][0].yaxis.set_major_formatter(PercentFormatter(1))  # percents

    plt.tight_layout()

    plt.show()