'''
spelling checker using filwordnet made by
Joseph Imperial
Doctoral Researcher at University of Bath studying Responsible AI.
Instructor and NLP Researcher at National University.

source: https://github.com/imperialite/FilWordNetExtractor/tree/master/FilWordNet%20files
'''

import pandas as pd
from functools import reduce
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import re
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

words_df = pd.read_excel(r'C:\Users\einge\Downloads\words.xlsx')

senses_df = pd.read_excel(r'C:\Users\einge\Downloads\senses.xlsx')

synsets_df = pd.read_excel(r'C:\Users\einge\Downloads\synsets.xlsx')

combined_df = pd.merge(words_df, senses_df, on=['wordid'])

filwordnet = pd.merge(combined_df, synsets_df, on=['synsetid'])


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

                filwordnet_find = []
                queried = filwordnet[filwordnet['lemma'] == word]

                for index, row in queried.iterrows():
                    filwordnet_find.append(row.lemma)

                if re.sub(r"[^\w]", "", word.lower()) not in filwordnet_find:
                    position = content.find(word)
                    self.text.tag_add(word, f"1.{position}", f"1.{position + len(word)}")
                    self.text.tag_config(word, foreground="red")


SpellingChecker()
