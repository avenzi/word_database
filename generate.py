import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import argparse

from scowl import Words


def frequency_plot(freqs, title):
    """
    Plot the letter frequency of the given <words>.
    The plot has the given <title>.
    """
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("level", nargs='?', help="Choose words from this SCOWL level or lower")
    args = parser.parse_args()

    words = Words()

    if args.level:
        words.generate_letter_frequencies(max_level=int(args.level))
    else:
        words.generate_letter_frequencies()

    freqs = words.freqs
    frequency_plot(freqs, "Word Letter Frequency")