import string
from checker import SpellChecker
import re

c = SpellChecker(sorting_key=lambda item: item.distance)

class SpellCheckerConsole:
    def __init__(self):
        pass

    def run(self):
        while True:
            text_input = input("Enter text (type 'exit' to quit): ")
            if text_input.lower() == 'exit':
                break
            self.check_text(text_input)

    def check_text(self, text):
        words = re.split(r'[ ,.!?]', text)
        for original_word in words:
            # Remove punctuation from the end of the word
            word_without_punctuation = original_word.rstrip(string.punctuation)
            word_lower = word_without_punctuation.lower()

            # Check if the word is not empty after removing punctuation
            if not word_lower:
                continue

            # Additional logic for words after the prefix "пол-"
            if word_lower.startswith("пол-"):
                prefix_length = len("пол-")
                word_after_prefix = word_lower[prefix_length:].rstrip(string.punctuation)

                # Check if the token is not empty after removing punctuation
                if not word_after_prefix:
                    continue

                # Display the correction
                correction = self.check_word(word_after_prefix)
                self.print_correction(original_word, correction)
            else:
                # Display the correction
                correction = self.check_word(word_lower)
                self.print_correction(original_word, correction)

    def check_word(self, word):
        correction = c.get_correction(word)
        return correction

    def print_correction(self, original_word, correction):
        print(f"Original Word: {re.sub(r'[^\w\s]', '', original_word)}".ljust(50), end="")
        if original_word.lower() == correction.word.lower():
            print("Corrected word: (No corrections needed)")
        else:
            print(f"Corrected word: {correction.word} ({correction.distance * 100:.2f}%)")


if __name__ == "__main__":
    console = SpellCheckerConsole()
    console.run()
