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
        text = [word.lower().strip() for word in self.text_box.get("1.0", tk.END).split()]
        start_index = '1.0'
        
        for word in text:
            self.update()
            start_index = self.text_box.search(word, start_index, stopindex=tk.END)
            end_index = f"{start_index}+{len(word)}c"
            tags = self.text_box.tag_names(start_index)
            if tags:
                continue
            correction = self.check_word(word)
            if correction.distance == 1.0:
                self.text_box.tag_add("green", start_index, end_index)
            else:
                tag = f"tag_{start_index}_{end_index}"
                self.text_box.tag_config(tag, background='yellow')
                self.text_box.tag_add(tag, start_index, end_index)
                self.text_box.tag_bind(tag, "<Enter>", lambda event, correction=correction: self.show_window(event, f'{correction.word}({correction.distance*100:.2f}%)'))
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