import string
from checker import SpellChecker
import re
from entry import Entry
from time import perf_counter


class SpellCheckerConsole:
    def __init__(self):
        self.checker = SpellChecker(sorting_key=lambda item: item.distance)
        print("Welcome to the Spell Checker Console!")
        print("This program can help you identify and correct spelling errors in your text.\n")

    def run(self):
        while True:
            text_input = input("Enter text (type 'exit' to quit): ")
            if text_input.lower() == 'exit':
                break
            self.check_text(text_input)

    def word_probability(self, word):
        return self.checker.counter[word] / self.checker.total

    def viterbi_segment(self, text):
        probs, lasts = [1.0], [0]
        for i in range(1, len(text) + 1):
            max_probability = 0
            max_probability_index = 0

            for j in range(max(0, i - self.checker.max_len), i):
                current_probability = probs[j] * self.word_probability(text[j:i])

                if current_probability > max_probability:
                    max_probability = current_probability
                    max_probability_index = j

            prob_k, k = max_probability, max_probability_index

            probs.append(prob_k)
            lasts.append(k)
        words = []
        i = len(text)
        while 0 < i:
            words.append(text[lasts[i]:i])
            i = lasts[i]
        words.reverse()
        return words, probs[-1]

    def check_text(self, text):
        words = re.split(r'[ ,.!?]', text)
        for original_word in words:
            word_without_punctuation = original_word.rstrip(string.punctuation)
            word_lower = word_without_punctuation.lower()

            if not word_lower:
                continue

            if not self.is_russian(word_lower):
                print(f"Error: Please write in Russian. Word '{original_word}' is not in Russian or contains digits.")
                continue

            t1 = perf_counter()
            if word_lower.startswith("пол-"):
                second_part = word_lower.split("-")[1]
                viterby_correction, viterby_probability = self.viterbi_segment(second_part)
                corrections = self.check_word(second_part)
            else:
                viterby_correction, viterby_probability = self.viterbi_segment(word_lower)
                corrections = self.check_word(word_lower)

            self.print_correction(original_word, [correction for correction in corrections]
                                  + [' '.join(viterby_correction)], perf_counter() - t1)

    @staticmethod
    def is_russian(word):
        return all(1072 <= ord(char) <= 1103 or char in ['ё', '-'] for char in word)

    def check_word(self, word):
        corrections = self.checker.get_corrections(word)
        return corrections

    def print_correction(self, original_word, corrections, time):
        print(f"Original Text: {original_word}".ljust(50), "Corrected text: ", end="")

        corrected_words = []
        for correction in corrections:
            if isinstance(correction, Entry):
                corrected_words.append(f"{correction.word} ({correction.distance * 100:.2f}%)")
            elif correction != original_word.lower():
                corrected_words.append(f"{correction}")

        print(f"{' / '.join(corrected_words)}\nFound correction in {time}s\n")


if __name__ == "__main__":
    console = SpellCheckerConsole()
    console.run()
