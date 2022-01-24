from utils import plot

with open('wordle_solutions.txt', 'r') as file:
    words = file.readlines()

plot(words, "Letter Frequency of 5-Letter Words")
