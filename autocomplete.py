class TrieNode:
    def __init__(self):
        self.children = {}
        self.top_matches = []  # List of (frequency, word)

class AutocompleteSystem:
    def __init__(self):
        self.root = TrieNode()
        self.word_freqs = {}  # Keep track of exact freq of each word

    def insert(self, word: str, freq: int):
        self.word_freqs[word] = freq
        
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            
            # Update top_matches for this node
            self._update_top_matches(node, word, freq)
            
    def _update_top_matches(self, node: TrieNode, word: str, freq: int):
        # Remove the word if it already exists in top_matches to update its freq
        node.top_matches = [m for m in node.top_matches if m[1] != word]
        node.top_matches.append((freq, word))
        # Sort by frequency descending, then lexicographically ascending
        node.top_matches.sort(key=lambda x: (-x[0], x[1]))
        # Keep only top 5
        if len(node.top_matches) > 5:
            node.top_matches.pop()

    def get_suggestions(self, prefix: str):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # O(L) operation since top_matches are already computed and stored
        return [match[1] for match in node.top_matches]

if __name__ == "__main__":
    trie = AutocompleteSystem()
    data = [
        ("apple", 10),
        ("app", 15),
        ("ape", 7),
        ("apex", 12),
        ("apply", 9),
        ("application", 8),
        ("apt", 6)
    ]

    for word, freq in data:
        trie.insert(word, freq)

    print("Top suggestions for 'ap':", trie.get_suggestions("ap"))
