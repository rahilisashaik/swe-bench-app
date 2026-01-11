import unittest
from storage import StorageManager
from engine import AutocompleteEngine
from models import SearchResult

class TestAutocompleteEngine(unittest.TestCase):
    def setUp(self):
        self.db = StorageManager()
        self.db.load_initial_data()
        self.engine = AutocompleteEngine(self.db)

    # --- Simple Cases ---
    def test_basic_prefix(self):
        results = self.engine.get_suggestions("appl")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].word, "applied") # weight 15 > 10

    def test_exact_match_and_children(self):
        results = self.engine.get_suggestions("app")
        # should find 'app', 'apple', 'applied'
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].word, "app") # weight 20 is highest

    def test_weight_sorting(self):
        results = self.engine.get_suggestions("ba")
        # battery(30), bandwidth(25), bat(12), band(11), banana(8), ball(5)
        weights = [r.weight for r in results]
        self.assertEqual(weights, sorted(weights, reverse=True))

    # --- Edge Cases ---
    def test_no_match(self):
        results = self.engine.get_suggestions("xyz")
        self.assertEqual(results, [])

    def test_empty_string(self):
        # Should return all words in the system sorted by weight
        results = self.engine.get_suggestions("")
        self.assertEqual(len(results), 9)
        self.assertEqual(results[0].word, "battery")

    def test_single_character_prefix(self):
        results = self.engine.get_suggestions("b")
        self.assertTrue(all(r.word.startswith("b") for r in results))
        self.assertEqual(len(results), 6)

if __name__ == "__main__":
    unittest.main()