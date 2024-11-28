import difflib
import pandas as pd
import json
import re

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

def spell_check(misspelled_df, column_name):
    for index, row in misspelled_df.iterrows():
        text = row[column_name]
        for word in text.split(" "):
            word = re.sub(r"[^\w]", "", replace_french_chars(word.lower()))
            if word not in maindp['Word'].str.lower().values:
                matches = difflib.get_close_matches(word, maindp['Word'].str.lower().values, n=5, cutoff=0.65)
                if matches:
                    corrected_text = text.replace(word, matches[0])
                    suggestion = ", suggested correction(s): " + ", ".join(matches)
                    print(f"Word: {text}\nCorrected: {corrected_text}\nSuggestion: {suggestion}\n")

#main program
with open('datasets/cleaned_tagalog_dictionary.json', ) as f:
    diksiyonaryoph = json.load(f)

#dataframe for the dictionary dataset
maindp = pd.DataFrame(diksiyonaryoph)

#dataframe for the testing dataset
misspelled_dataset = 'datasets/misspelled words.xlsx'
column_name = 'row1'

misspelled_df = pd.read_excel(misspelled_dataset)
spell_check(misspelled_df, column_name)