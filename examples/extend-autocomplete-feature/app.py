from storage import StorageManager
from engine import AutocompleteEngine

def run_app():
    # Initialize system
    db = StorageManager()
    db.load_initial_data()
    
    engine = AutocompleteEngine(db)
    
    # Simulate user input
    user_query = "ba"
    print(f"Searching for prefix: '{user_query}'...")
    
    suggestions = engine.get_suggestions(user_query)
    
    for idx, res in enumerate(suggestions):
        print(f"{idx + 1}. {res.word} (Score: {res.weight})")

if __name__ == "__main__":
    run_app()