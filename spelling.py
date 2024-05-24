import difflib
import pandas as pd
from functools import reduce
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import unicodedata
import json
import re
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


def replace_french_chars(text):
    french_chars = {
        'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a', 'æ': 'ae',
        'ç': 'c', 'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'ì': 'i', 'í': 'i',
        'î': 'i', 'ï': 'i', 'ñ': 'n', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ö': 'o', 'ø': 'o', 'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u', 'ý': 'y',
        'ÿ': 'y', 'ß': 'ss'
    }
    for char, replacement in french_chars.items():
        text = text.replace(char, replacement)
    return text

def normalize_unicode(obj):
    if isinstance(obj, dict):
        return {normalize_unicode(key): normalize_unicode(value) for key, value in obj.items()}
    elif isinstance(obj, str):
        return replace_french_chars(obj)
    else:
        return obj

with open('datasets/tagalog-words.json') as f:
    dataset = json.load(f)

normalized_data = normalize_unicode(dataset)

# Save the normalized data to a new JSON file
with open('datasets/normalized_tagalog-words.json', 'w') as f:
    json.dump(normalized_data, f, indent=4)

with open('datasets/normalized_tagalog-words.json', ) as f:
    diksiyonaryoph = json.load(f)

df = pd.DataFrame(diksiyonaryoph)
transpose_dp = df.transpose()
maindp = transpose_dp.reset_index()


class SpellingChecker:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x500")

        self.text = ScrolledText(self.root, font=("Arial", 14))
        self.text.bind("<KeyRelease>", self.check)
        self.text.pack()

        self.old_spaces = 0

        self.root.mainloop()

    def check(self, event):
        content = self.text.get("1.0", tk.END)
        space_count = content.count(" ")

        for tag in self.text.tag_names():
            self.text.tag_delete(tag)

        if space_count != self.old_spaces:
            self.old_spaces = space_count
            for word in content.split(" "):
                word = re.sub(r"[^\w]", "", replace_french_chars(word.lower()))
                if word not in maindp['index'].str.lower().values:
                    matches = difflib.get_close_matches(word, maindp['index'].str.lower().values, n=3, cutoff=0.5)
                    if matches:
                        position = content.find(word)
                        self.text.tag_add(word, f"1.{position}", f"1.{position + len(word)}")
                        self.text.tag_config(word, foreground="red")
                        suggestion = ", suggested correction(s): " + ", ".join(matches)
                        self.text.insert(tk.END, suggestion)


SpellingChecker()