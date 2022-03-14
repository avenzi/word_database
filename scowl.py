from scipy.stats import truncnorm
from random import choices
from time import time

from json import load, dump
import os


# Directory containing this file.
# This is so relative file paths work no matter where it's imported from
PARENT = os.path.dirname(__file__)


class Words:
    """
    Class used to pick words n stuff.
    "Level" refers to an index in self.scowl_levels.
    Assumes a SCOWL database download exists in the same directory.
    """
    def __init__(self):
        # directory where the SCOWL database is
        self.scowl_dir = os.path.join(PARENT, "./scowl-2020.12.07")
        assert os.path.isdir(self.scowl_dir), f"SCOWL Database directory not found: {self.scowl_dir}"

        # list of scowl file categories to pull from
        self.scowl_categories = ["final/english-words", "final/american-words"]
        self.offensive = ["misc/offensive.1"]  # offensive words to EXCLUDE

        # Each entry MUST correspond with a SCOWL level, and it must be in order
        self.scowl_levels = [10, 20, 35, 40, 50, 55, 60, 70, 80, 95]
        self.min = 0  # min level index
        self.max = len(self.scowl_levels)-1  # max level index

        self.allowed_letters = set('abcdefghijklmnopqrstuvwxyz')
        self.vowels = set('aeiouyw')

        # load letter frequencies
        self.freqs_file = os.path.join(PARENT, "freqs.json")
        with open(self.freqs_file) as file:
            self.freqs = load(file)

    def read_scowl(self, file):
        """ Read data from a SCOWL file if it exists """
        words = []
        filepath = f"{self.scowl_dir}/{file}"
        if os.path.isfile(filepath):
            with open(filepath, encoding="latin-1") as f:
                words += f.read().splitlines()
        return words

    def generate_letter_frequencies(self, max_level=None):
        """ Generate the Letter Frequency file from the SCOWL database """
        if max_level is None: max_level = self.max
        # output total letter frequency list to JSON
        words = self.get_words(max_level=max_level)
        freqs = {}
        for word in words:
            for letter in word:  # count occurrences of each letter
                freqs[letter] = freqs.get(letter, 0) + 1

        # normalize distribution
        total = sum(freqs.values())  # sum of all letter counts
        freqs = {let: freq/total for let, freq in freqs.items()}  # divide all freqs by total

        self.freqs = freqs
        with open(self.freqs_file, 'w') as file:
            dump(freqs, file)

        print(f"Exporting Frequency Data to: {self.freqs_file}")

    def letter_frequency(self, word, avg=True, count_repeats=False):
        """
        Return the sum of letter frequencies in the word.
        Uses the Letter Frequency file output by generate_letter_frequency().
        """
        if not word:
            return 0
        tot = 0
        unique = set()
        for letter in word:
            if count_repeats or letter not in unique:
                tot += self.freqs[letter]
                unique.add(letter)

        if avg:
            if count_repeats:
                tot = tot / len(word)
            else:
                tot = tot / len(set(word))
        return tot

    def get_weights(self, levels, mean, std):
        """ Return a list of normally distributed index weights for the given levels with the given mean and std """
        size = len(levels)

        # only 1 option
        if size == 1:
            return [1]

        # uniform distribution
        if mean is None:
            return [1]*size

        # create truncated normal distribution
        assert 0 <= mean <= size-1, f"Mean must be within the range of possible levels (0-{size-1})"
        assert std > 0, "Standard deviation must be positive and nonzero"
        lower = (0 - mean) / std  # (low - mean) / std
        upper = ((size-1) - mean) / std  # (high - mean) / std

        weights = []
        for i in range(size):
            p = truncnorm.pdf(i, lower, upper, loc=mean, scale=std)
            weights.append(p)
        return weights

    def get_words(self,
                  min_level=None, max_level=None,
                  min_length=None, max_length=None,
                  allowed=None, vowel_required=False
                  ):
        """
        Get all english words within the level range and length range.
        <allowed> is an optional string/list/set of allowed letters.
        <vowel_required> only return words with at least one vowel.
        """
        if min_level is None: min_level = self.min
        if max_level is None: max_level = self.max
        if allowed is None: allowed = self.allowed_letters
        else: allowed = set(let.lower() for let in allowed)  # ensure lowercase
        assert self.min <= min_level <= max_level <= self.max, f"Got: {min_level}, {max_level}"

        words = []
        for file in self.scowl_categories:
            for level in range(min_level, max_level+1):  # indexes
                scowl_level = self.scowl_levels[level]
                words += self.read_scowl(f"{file}.{scowl_level}")

        # filter
        offensive = self.read_scowl(self.offensive)
        filtered = []
        for word in words:
            word = word.lower().strip()
            if min_length and len(word) < min_length:
                continue
            if max_length and len(word) > max_length:
                continue
            if word in offensive:  # remove offensive
                continue

            # if word is not a subset of allowed letters
            if allowed and not set(word).issubset(allowed):
                continue
            # filter words without vowels, if specified
            if vowel_required and set(word).isdisjoint(self.vowels):
                continue
            filtered.append(word)

        return filtered

    def get_random_word(self, min_level=None, max_level=None, mean_level=None, std=1, **kwargs):
        """
        Get a random word from a random level
        min/max _level are the min and max levels
        <mean> is around what level to set the mean choice. Uniform if None.
        <std> is the standard deviation around the given mean, default is 1.
        <kwargs> any additional kwargs are passed to self.get_words()
        """
        if min_level is None: min_level = self.min
        if max_level is None: max_level = self.max
        assert self.min <= min_level <= max_level <= self.max, f"Values must be: {self.min} <= min <= max <= {self.max}"
        if mean_level is not None:
            assert min_level <= mean_level <= max_level, f"Mean must be between min and max, not {mean_level}"

        levels = list(range(min_level, max_level+1))  # levels to choose from
        weights = self.get_weights(levels, mean=mean_level, std=std)  # create weights for those levels
        #print([f"{100.0*w/sum(weights):.3}%" for w in weights])

        # try to get words from randomly chosen levels
        for _ in range(len(levels)):  # only iterate for as many levels
            level = choices(levels, weights=weights)[0]  # choose level

            # get words from that level
            words = self.get_words(level, level, **kwargs)

            if len(words) > 0:  # if at least one word found
                return choices(words)[0], level/self.max  # return a random word and its level over the max
            else:  # no words found
                weights[level-min_level] = 0  # remove this level from the weights so it won't get chosen next loop

        # Found no words with the given constraints in any levels
        raise Exception("No words could be chosen from the database with the given constraints.")



