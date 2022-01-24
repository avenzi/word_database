import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from time import time
import os.path

ALLOWED_LETTERS = set('abcdefghijklmnopqrstuvwxyz')
REPLACE_LETTERS = {'ê': 'e', 'é': "e"}


def read_scowl(file):
    """ Read data from a SCOWL file if it exists """
    if os.path.isfile(file):
        with open(file, encoding="latin-1") as file:
            return file.readlines()
    else:
        return []


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


def plot(freq, title):
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

################
################

# From Stanford 5-letter dataset
stanford_link = "https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt"
stanford = requests.get(stanford_link).content.decode('utf-8').split('\n')
print("From stanford five letter dataset: ", len(stanford))

# From SCOWL datasets
sizes = [10, 20, 35, 40, 50, 55, 60, 70, 80]
scowl = []
for size in sizes:
    scowl += read_scowl(f"./scowl-2020.12.07/final/english-words.{size}")
    scowl += read_scowl(f"./scowl-2020.12.07/final/american-words.{size}")
    scowl += read_scowl(f"./scowl-2020.12.07/final/british-words.{size}")
    scowl += read_scowl(f"./scowl-2020.12.07/final/british-abbreviations.{size}")
    scowl += read_scowl(f"./scowl-2020.12.07/final/variant_1-words.{size}")
    scowl += read_scowl(f"./scowl-2020.12.07/final/variant_1-abbreviations.{size}")
    scowl += read_scowl(f"./scowl-2020.12.07/final/variant_2-words.{size}")
    scowl += read_scowl(f"./scowl-2020.12.07/final/variant_2-abbreviations.{size}")
    scowl += read_scowl(f"./scowl-2020.12.07/final/variant_3-words.{size}")
    scowl += read_scowl(f"./scowl-2020.12.07/final/variant_3-abbreviations.{size}")


#
start = time()
n = 1
total = len(scowl)
scowl_5 = []
for word in scowl:
    word = word.strip().lower()  # strip whitespace and convert to lower case
    if len(word) != 5:
        continue

    for letter, replacement in REPLACE_LETTERS.items():
        word = word.replace(letter, replacement)
    if set(word).issubset(ALLOWED_LETTERS):  # all letters are allowed
        scowl_5.append(word)


print("From SCOWL:", len(scowl_5))

words = list(set(stanford + scowl_5))
print("Total: ", len(words))

not_in_scowl = []
for word in stanford:
    if word not in scowl_5:
        not_in_scowl.append(word)
#print("Not in scowl:", len(not_in_scowl), not_in_scowl)

freq = frequency(words)
plot(freq, "Letter Frequency of 5-Letter Words")
