import string
from checker import SpellChecker
import re


class SpellCheckerConsole:
    def __init__(self):
        self.checker = SpellChecker(sorting_key=lambda item: item.distance)

    def run(self):
        while True:
            text_input = input("Enter text (type 'exit' to quit): ")
            if text_input.lower() == 'exit':
                break
            self.check_text(text_input)

    def word_probability(self, word): return self.checker.counter[word] / self.checker.total

    def viterbi_segment(self, text):
        probs, lasts = [1.0], [0]
        for i in range(1, len(text) + 1):
            prob_k, k = max((probs[j] * self.word_probability(text[j:i]), j) for j in range(max(0, i - self.checker.max_len), i))
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

            viterby_correction, viterby_probability = self.viterbi_segment(word_lower)
            print(viterby_correction, viterby_probability)
            if viterby_probability:
                self.print_correction(original_word, viterby_correction, viterby_probability * 100)

            elif word_lower.startswith("пол-"):
                prefix_length = len("пол-")
                word_after_prefix = word_lower[prefix_length:].rstrip(string.punctuation)

                if not word_after_prefix:
                    continue

                correction = self.check_word(word_after_prefix)
                self.print_correction(original_word, f'пол-{correction.word}', correction.distance * 100)
            else:
                correction = self.check_word(word_lower)
                self.print_correction(original_word, correction.word, correction.distance * 100)


    def check_word(self, word):
        correction = self.checker.get_correction(word)
        return correction

    def print_correction(self, original_word, correction, probability):
        print(f"Original Text: {original_word}".ljust(50), end="")
        if original_word == correction:
            print("Corrected text: (No corrections needed)")
        else:
            if int(probability) != 0:
                print(f"Corrected text: {correction} ({probability:.2f}%)")
            else:
                print(f"Corrected text: {' '.join(correction)}")


if __name__ == "__main__":
    console = SpellCheckerConsole()
    console.run()