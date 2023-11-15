import string

from checker import SpellChecker
from matplotlib import pyplot as plt
import tkinter as tk

c = SpellChecker(sorting_key=lambda item: item.distance)
class Application(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.resizable(False, False)
        self.title("Spell Checker")
        self.geometry("500x200")

    def run(self):
        self.mainloop()

    def create_widgets(self):
        self.text_box = tk.Text(self, width=60, height=10, wrap=tk.WORD)
        self.text_box.tag_config("green", background="green")
        self.check_button = tk.Button(self, text="Check", command=self.get_corrections)
        self.text_box.pack(side=tk.TOP)
        self.check_button.pack(side=tk.BOTTOM)

        self.window = tk.Toplevel(self)
        self.window.withdraw()
        self.window.overrideredirect(True)
        self.text_label = tk.Label(self.window, text="")
        self.text_label.pack()


    def get_corrections(self):
        text = self.text_box.get("1.0", tk.END).split()
        start_index = '1.0'

        for original_word in text:
            self.update()
            # Используйте опцию nocase для поиска без учета регистра
            start_index = self.text_box.search(original_word, start_index, stopindex=tk.END, nocase=True)

            # Проверка, что start_index не пуст
            if not start_index:
                continue

            # Исправление: Преобразование start_index в формат line.column
            line, column = map(int, start_index.split('.'))
            start_index = f"{line}.{column}"

            # Удаление знаков препинания с конца слова
            word_without_punctuation = original_word.rstrip(string.punctuation)

            # Преобразование слова к нижнему регистру
            word_lower = word_without_punctuation.lower()

            # Проверка, что токен не пустой после удаления знаков препинания
            if not word_lower:
                continue

            # Дополнительная логика для слов после приставки "пол-"
            if word_lower.startswith("пол-"):
                prefix_length = len("пол-")
                word_after_prefix = original_word[prefix_length:].rstrip(string.punctuation)
                word_after_prefix_lower = word_after_prefix.lower()

                # Проверка, что токен не пустой после удаления знаков препинания
                if not word_after_prefix_lower:
                    continue

                end_index = f"{start_index}+{prefix_length + len(word_after_prefix)}c"
            else:
                end_index = f"{start_index}+{len(original_word)}c"

            tags = self.text_box.tag_names(start_index)
            if tags:
                continue

            # Проверка орфографии
            correction = self.check_word(word_after_prefix_lower) if word_lower.startswith("пол-") else self.check_word(
                word_lower)

            if correction.distance == 1.0:
                self.text_box.tag_add("green", start_index, end_index)
            else:
                tag = f"tag_{start_index}_{end_index}"
                self.text_box.tag_config(tag, background='yellow')
                self.text_box.tag_add(tag, start_index, end_index)
                self.text_box.tag_bind(tag, "<Enter>", lambda event, correction=correction: self.show_window(event,
                                                                                                             f'{correction.word}({correction.distance * 100:.2f}%)'))
                self.text_box.tag_bind(tag, "<Leave>", self.hide_window)

    def show_window(self, event, text):
        x, y, _, _ = self.text_box.bbox(tk.CURRENT)
        self.window.geometry(f"+{self.winfo_rootx() + x}+{self.winfo_rooty() + y - 20}")
        self.text_label.config(text=text)
        self.window.deiconify()

    def hide_window(self, event):
        self.window.withdraw()

    def check_word(self, word):
        correction = c.get_correction(word)
        print(correction)
        return correction


if __name__ == "__main__":
    app = Application()
    app.create_widgets()
    app.run()