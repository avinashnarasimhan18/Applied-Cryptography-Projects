"""
This is a helper function to generate random plaintexts from EFF's wordlist
"""

import os
import random
import requests


def fetch_words_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            words = response.text.split()  # Split the text into words
            return words
        else:
            print("Failed to fetch words from URL:", response.status_code)
            return []
    except requests.RequestException as e:
        print("Error fetching words from URL:", e)
        return []


def remove_numeric_strings(word_list):
    return [word for word in word_list if not word.isdigit()]


def generate_random_string(word_list, length):
    random_string = ""
    while len(random_string) < length:
        random_word = random.choice(word_list)
        if len(random_string) + len(random_word) < length:
            random_string += random_word + " "
        else:
            remaining_length = length - len(random_string)
            random_string += random_word[:remaining_length]
    return random_string.strip()


# Example usage:
if os.path.exists("random_plaintexts.txt"):
    os.remove("random_plaintexts.txt")
words_url = "https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt"
words_list = fetch_words_from_url(words_url)
filtered_words_list = remove_numeric_strings(words_list)

output_file_path = "random_plaintexts.txt"
print("Enter number of plaintexts to generate:")
number_of_plaintexts = int(input())
print("Enter length of each plaintext (600):")
length_of_plaintext = int(input())
if filtered_words_list:
    with open(output_file_path, 'w') as output_file:
        for i in range(number_of_plaintexts + 1):
            random_plaintext = generate_random_string(filtered_words_list, length_of_plaintext)
            output_file.write(random_plaintext + '\n\n')
