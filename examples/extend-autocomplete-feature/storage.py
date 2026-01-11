"""This manages the in-memory state of the search dictionary."""

from models import TrieNode, SearchResult

class StorageManager:
    """Handles the persistence and initialization of the Trie."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, weight: int) -> None:
        """Inserts a word into the Trie with a specific popularity weight."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.weight = weight
        node.word = word

    def get_root(self) -> TrieNode:
        """Returns the entry point for the Trie."""
        return self.root

    def load_initial_data(self):
        """Simulates loading data from a database."""
        data = [
            ("apple", 10), ("app", 20), ("applied", 15),
            ("ball", 5), ("bat", 12), ("battery", 30),
            ("banana", 8), ("band", 11), ("bandwidth", 25)
        ]
        for word, weight in data:
            self.insert(word, weight)