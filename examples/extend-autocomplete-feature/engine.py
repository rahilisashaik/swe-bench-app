from typing import List
from models import TrieNode, SearchResult
from storage import StorageManager

class AutocompleteEngine:
    def __init__(self, storage: StorageManager):
        self.storage = storage

    def get_suggestions(self, prefix: str) -> List[SearchResult]:
        """
        TODO: Implement this method.
        1. Navigate to the node representing the end of the prefix.
        2. Perform a traversal to find all complete words under that branch.
        3. Wrap results in SearchResult objects.
        4. Sort by weight (descending).
        """
        root = self.storage.get_root()
        node = root
        
        # Step 1: Navigate to the prefix node
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
            
        results = []
        
        # Step 2: Helper function to traverse and collect words
        def collect_words(current_node: TrieNode):
            if current_node.is_end_of_word:
                results.append(SearchResult(current_node.word, current_node.weight))
            
            for char in current_node.children:
                collect_words(current_node.children[char])

        # Step 3: Collect and sort
        collect_words(node)
        results.sort(key=lambda x: x.weight, reverse=True)
        
        return results