from levenshtein import levenshtein_distance_normalized
from entry import Entry
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

class SpellChecker:
    def __init__(self, sorting_key) -> None:
        self.sorting_key = sorting_key
        #Data from https://bokrcorpora.narod.ru/frqlist/frqlist.html
        with open('data.txt', 'r', encoding='utf-8') as data_file:
            self.data = [Entry(word) for word in data_file.read().split('\n')]
            self.max_len = max(len(entry.word) for entry in self.data)
            self.counter = Counter(words.word for words in self.data)
            self.total = float(sum(self.counter.values()))
    
    def calculate_distance(self, entry, target_word):
        entry.distance = levenshtein_distance_normalized(entry.word, target_word)
        return entry

    def calculate_distances(self, word) -> list[Entry]:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.calculate_distance, entry, word) for entry in self.data]

        self.data = [future.result() for future in futures]

        return self.data
    
    def get_corrections(self, word) -> Entry: 
        distance_data = self.calculate_distances(word)
        corrections = sorted(distance_data, key=self.sorting_key, reverse = True)[:5]
        for correction in corrections:
            correction.other = word
            
        return corrections