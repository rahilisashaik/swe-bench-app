"""This file defines the data structures used by the system."""

from typing import Dict, List, Optional

class TrieNode:
    """Represents a single character in the prefix tree."""
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False
        self.weight: int = 0
        self.word: Optional[str] = None

class SearchResult:
    """The standard output format for the search engine."""
    def __init__(self, word: str, weight: int):
        self.word = word
        self.weight = weight

    def __repr__(self):
        return f"SearchResult(word='{self.word}', weight={self.weight})"

    def __eq__(self, other):
        if not isinstance(other, SearchResult):
            return False
        return self.word == other.word and self.weight == other.weight