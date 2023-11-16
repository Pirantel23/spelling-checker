from levenshtein import levenshtein_distance_normalized
from entry import Entry
from collections import Counter

class SpellChecker:
    def __init__(self, sorting_key) -> None:
        self.sorting_key = sorting_key
        #Data from https://bokrcorpora.narod.ru/frqlist/frqlist.html
        with open('data.txt', 'r', encoding='utf-8') as data_file:
            self.data = [Entry(word) for word in data_file.read().split('\n')]
            self.max_len = max(len(entry.word) for entry in self.data)
            self.counter = Counter(words.word for words in self.data)
            self.total = float(sum(self.counter.values()))
    
    def calculate_distances(self, word) -> list[Entry]:
        for entry in self.data:
            entry.distance = levenshtein_distance_normalized(entry.word, word)
        return self.data
    
    def get_correction(self, word) -> Entry: 
        distance_data = self.calculate_distances(word)
        correction = max(distance_data, key=self.sorting_key)
        correction.other = word
        return correction