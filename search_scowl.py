import os

search = ["eBook"]
for subdir, dirs, files in os.walk("scowl-2020.12.07/final"):
    for file in files:
        filepath = subdir + os.sep + file
        with open(filepath, encoding="latin-1") as file:
            words = file.readlines()
        for word in words:
            word = word.strip()
            if word in search:
                print(f"Found '{word}' in {filepath}")