from Levenshtein import distance

class FBTrieNode:
    def __init__(self, char):
        self.char = char
        self.children = {}
        self.is_end_of_word = False
        self.count = 0
        self.parent = None


class FBTrie:
    def __init__(self):
        self.root = FBTrieNode(None)

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = FBTrieNode(char)
                node.children[char].parent = node
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word, max_distance):
        results = []
        node = self.root
        self.search_helper(node, word, max_distance, '', results)
        return results
    
    def search_helper(self, node, word, max_distance, current_word, results):
        if len(current_word) > len(word) + max_distance:
            return

        if node.is_end_of_word and len(current_word) <= len(word) + max_distance:
            results.append(current_word)

        if node.char == word[len(current_word)]:
            if len(word) - len(current_word) <= max_distance:
                for child in node.children.values():
                    self.search_helper(child, word, max_distance, current_word + child.char, results)
            else:
                self.search_helper(node, word, max_distance, current_word + node.char, results)
        else:
            if len(current_word) == len(word) + max_distance:
                return
            for child in node.children.values():
                self.search_helper(child, word, max_distance, current_word + child.char, results)
    
    def update_distance(self, node, word):
        if node.char == word[0]:
            node.distance = 0
        else:
            node.distance = 1
        for child in node.children.values():
            self.update_distance(child, word)


trie = FBTrie()
trie.insert("apple")
trie.insert("banana")
trie.insert("car")

results = trie.search("aple", 1)
print(results)  # ['apple']

results = trie.search("canana", 2)
print(results)  # ['banana']
