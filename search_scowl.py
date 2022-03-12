import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("words", nargs='+', help="word to search")
args = parser.parse_args()
search = args.words

parent = os.path.dirname(__file__)
DIR = os.path.join(parent, "./scowl-2020.12.07/final")

for subdir, dirs, files in os.walk(DIR):
    for file in files:
        filepath = subdir + os.sep + file
        with open(filepath, encoding="latin-1") as file:
            words = file.readlines()
        for word in words:
            word = word.strip()
            if word in search:
                print(f"Found '{word}' in {filepath}")
