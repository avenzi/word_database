import os
from frequency import positional_frequency_plot


def wordle_filter(words):
    """ Ensure only accepted letters are in the words """
    result = []
    for word in words:
        word = word.strip().lower()  # strip whitespace and convert to lower case
        if len(word) != 5:
            continue
        result.append(word)
    return result


parent = os.path.dirname(__file__)
SOLUTIONS = os.path.join(parent, "wordle_solutions.txt")
print(SOLUTIONS)

with open(SOLUTIONS, 'r') as file:
    words = file.readlines()

words = wordle_filter(words)
positional_frequency_plot(words, "Wordle Letter Frequency")