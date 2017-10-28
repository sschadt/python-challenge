# -*- coding: utf-8 -*-
""" Main.py

Paragraph text analyzer

This module takes a text file path as the argument, and analyzes the file for word count,
sentence count, average letter count per word, and average sentence length.  

Example:

        $ python pyparagraph.py "[relative file path]"

        Paragraph Analysis
        -----------------
        Approximate Word Count: 122
        Average Letter Count: 4.56557377049
        Approximate Sentence Count: 5
        Average Sentence Length: 24.4
"""
import sys
import string
import statistics as s

# ------------------------------------
# ------- FUNCTION DEFINITION  -------
# ------------------------------------
def word_statistics(txt):
    """ Given a text string, break into words list to determine word/letter counts.
        * Determine number of words from list of words from text string
        * Create list of letter lengths from words list
        * Returns dictionary containing word count and average letter count
    """

    # 1. First, return all words cleaned up from any punctuation
    exclude = set(string.punctuation)
    all_text_clean = ''.join(ch for ch in txt if ch not in exclude)

    # 2. Next, split the cleaned words into a list
    all_words_clean = all_text_clean.split(" ")

    # Define helper lists for summary statistics
    cleaned_words = []
    cleaned_word_lengths = []

    # *** Create list of cleaned words (without trailing punctuation), and list of word lengths ***
    for word in all_words_clean:
        # Append current word to our list
        cleaned_words.append(word)

        # Append word length to our word length list (skip over empty strings - these are punctuation words that got erased)
        word_length = len(word)
        if (word_length > 0):
            cleaned_word_lengths.append(len(word))

    # Build our summary table values, and store in a dictionary to return:
    # Total word count, Average letter count
    dict_summary =  {
                    "Approximate Word Count": str(len(cleaned_words)), 
                    "Average Letter Count": str(s.mean(cleaned_word_lengths))
                    }
    return dict_summary

def sentence_statistics(txt):
    """ Given a text string, break up words into sentences to determine statistics
        * Determine number of sentences, by breaking up text string into sentence list items
        * Returns dictionary containing sentence count, and average sentence length (in words)
    """
    sentence_list = []
    sentence_lengths = []
    dict_sentences = {}

    # Break up the sentences into a list
    sentence_list = txt.split(". ")

    # Loop through all sentences, create dictionary to store their words in list
    for sentence in sentence_list:
        # Add list of current sentence's words to sentence dictionary
        dict_sentences[sentence] = sentence.split(" ")

    # Loop through dictionary and store each sentence's word count in list (if it has more than one word)
    for key, value in dict_sentences.items():
        number_of_words = len(value)
        sentence_lengths.append(number_of_words)

    # Build our summary table values, and store in a dictionary to return:
    # Total sentence count, average sentence length
    dict_summary =  {
                    "Approximate Sentence Count": str(len(sentence_list)), 
                    "Average Sentence Length": str(s.mean(sentence_lengths))
                    }
    return dict_summary

# ------------------------------------
# -------- MAIN PROGRAM BODY  --------
# ------------------------------------
# Parse file from command-line argument
args = sys.argv
filepath = args[1]

# Initialize list to hold text from file
all_text = []

# Initialize text file object
with open(filepath, 'r') as text:
    # Read all of the text file into a single list, and store text in a separate variable
    all_text = text.readlines()
    all_text_string = all_text[0]

# Call function to return word/letter summary statistics
dict_word_summary = word_statistics(all_text_string)

# Call function to return sentence statistics
dict_sentence_summary = sentence_statistics(all_text_string)

# ***** Print summary table *****
print("Paragraph Analysis")
print("------------------")
for key, value in dict_word_summary.items():
    print (f"{key}: {value}")
for key, value in dict_sentence_summary.items():
    print (f"{key}: {value}")
