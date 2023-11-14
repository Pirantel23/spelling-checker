class Entry:
    def __init__(self, word, probability) -> None:
        self.word = word
        self.probability = probability
    
    def __repr__(self) -> str:
        return f'Entry({self.__dict__})'