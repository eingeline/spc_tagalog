import pandas as pd
import json
import re
import Levenshtein as lev
from fuzzywuzzy import fuzz


def replace_french_chars(text):
    """Replace French-specific characters."""
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
    """Normalize strings in the dictionary."""
    if isinstance(obj, dict):
        return {normalize_unicode(key): normalize_unicode(value) for key, value in obj.items()}
    elif isinstance(obj, str):
        return replace_french_chars(obj)
    else:
        return obj


def check_spacing_correction(word):
    """Check if splitting the word produces valid dictionary entries."""
    for i in range(1, len(word)):
        first_part = word[:i]
        second_part = word[i:]
        if (first_part in maindp['Word'].str.lower().values and
                second_part in maindp['Word'].str.lower().values):
            return f"{first_part} {second_part}"
    return None


def check_merge_correction(first_word, second_word):
    """Check if merging two words creates a valid dictionary entry."""
    combined_word = first_word + second_word
    if combined_word in maindp['Word'].str.lower().values:
        return combined_word
    return None


shortcut_dict = {
    "bat": "bakpt",
    "ba't": "bakpt",
    "lng": "ling",
    "mgl": "magaoling",
    "ok": "okry",
    "kc": "kas1",
    "d2": "dit0",
    "Knp": "Kanin1",
    "wla": "wola",
    "cge": "s1gi",
    "pnta": "pvnta",
    "cguro": "s1guro"
}


def replace_shortcuts(word):
    """Replace shortcut words with their full form."""
    return shortcut_dict.get(word.lower(), word)


def spell_check(misspelled_df, column_name):
    """Process misspelled words for corrections."""
    n = 0  # Track corrections made
    for index, row in misspelled_df.iterrows():
        text = row[column_name]
        words = text.split(" ")
        corrected_words = words[:]

        i = 0
        while i < len(corrected_words):

            normalized_word = re.sub(r"[^\w]", "", replace_french_chars(corrected_words[i].lower()))
            cleaned_word = replace_shortcuts(normalized_word.lower())

            threshold = 2 if len(cleaned_word) < 5 else len(cleaned_word) // 2


            # Prioritize merge correction
            if i < len(corrected_words) - 1:
                merge_correction = check_merge_correction(corrected_words[i], corrected_words[i + 1])
                if merge_correction:
                    corrected_words[i] = merge_correction
                    corrected_words.pop(i + 1)  # Remove the second word after merging
                    print(f"\nSpacing correction (merge): '{text}' corrected to '{merge_correction}'")
                    continue  # Skip to the next word after merging

            # Check if the word is misspelled
            if cleaned_word not in maindp['Word'].str.lower().values:
                # Calculate similarity scores
                distances_lev = {dict_word: lev.distance(cleaned_word, dict_word) for dict_word in
                                 maindp['Word'].str.lower().values}
                distances_fuzz = {dict_word: fuzz.ratio(cleaned_word, dict_word) for dict_word in
                                  maindp['Word'].str.lower().values}

                combined_matches = {word: (distances_lev[word] + (100 - distances_fuzz[word]) / 50)
                                    for word in maindp['Word'].str.lower().values}

                closest_matches = sorted(combined_matches.items(), key=lambda x: x[1])[:5]
                matches = [match[0] for match in closest_matches if match[1] <= threshold]

                # Check for spacing correction (split)
                spacing_correction = check_spacing_correction(cleaned_word)
                if spacing_correction:
                    corrected_words[i] = spacing_correction
                    print(f"\nSpacing correction (split): '{text}' split to '{spacing_correction}'")

                # Suggest spelling corrections
                if matches:
                    print(f"Word: {text} - Suggested corrections: {', '.join(matches)}\n")
                else:
                    print(f"Word: {text} - No suggestions found.\n")
            else:
                print("The word is correct. Word: " + cleaned_word + "\n")

            i += 1  # Increment index
        n += 1  # Increment correction count

    print(f"Total corrections made: {n}")


# Main program
with open('datasets/final_tagalog-dictionary.json', encoding='utf-8') as f:
    diksiyonaryoph = json.load(f)

# DataFrame for the dictionary dataset
maindp = pd.DataFrame(diksiyonaryoph)

# DataFrame for the testing dataset
misspelled_dataset = 'datasets/misspelled words.xlsx'
column_name = 'row1'

misspelled_df = pd.read_excel(misspelled_dataset)
spell_check(misspelled_df, column_name)
