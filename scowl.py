import os


parent = os.path.dirname(__file__)
DIR = os.path.join(parent, "./scowl-2020.12.07/final")
LEVELS = [10, 20, 35, 40, 50, 55, 60, 70, 80, 95]

ALLOWED_LETTERS = set('abcdefghijklmnopqrstuvwxyz')


def read_scowl(file):
    """ Read data from a SCOWL file if it exists """
    if os.path.isfile(file):
        with open(file, encoding="latin-1") as file:
            return file.read().splitlines()
    else:
        return []


def get_words(level=None):
    """
    Get all english words with level less than or equal to the given level.
    Level can also be a list of levels to take from.
    If level not given, get them all.
    """
    if level is None:
        levels = LEVELS
    elif type(level) == list:
        levels = level
    else:
        levels = [lvl for lvl in LEVELS if lvl <= level]

    words = []
    for level in levels:
        words += read_scowl(f"{DIR}/english-words.{level}")
        words += read_scowl(f"{DIR}/american-words.{level}")
    return words


def filter(words, allowed=ALLOWED_LETTERS, min_length=None, max_length=None):
    """
    Filter the given word by minimum and maximum length.
    allowed: SET of letters allowed, if not None
    """
    filtered = []
    for word in words:
        word = word.lower().strip()
        if min_length and len(word) < min_length:
            continue
        if max_length and len(word) > max_length:
            continue

        # if word is not a subset of allowed letters
        if allowed and not set(word).issubset(allowed):
            continue
        filtered.append(word)
    return filtered


if __name__ == "__main__":
    for level in LEVELS:
        words = get_words([level])
        print(f"{level}: {len(words)}")

