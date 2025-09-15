from dotenv import load_dotenv
import os
from mem0 import MemoryClient
import logging
import json

# Load environment variables from a .env file if it exists
load_dotenv()


# --- Configuration ---
USER_ID = 'nathan' # Using a consistent user ID

# --- Initialize Client ---
# Initialize the client once and reuse it in your functions.
try:
    mem0 = MemoryClient()
except Exception as e:
    print(f"Error initializing MemoryClient. Have you set your API key? Error: {e}")
    # Exit if we can't initialize the client
    exit()

def add_memory():
    """
    Adds a sample conversation to the user's memory.
    """
    print(f"Adding memory for user_id: '{USER_ID}'...")
    messages = [
        {"role": "user", "content": "Hi, I'm Nathan. I'm an omnivore and I'm allergic to mayonnaise."},
        {"role": "assistant", "content": "Hello Nathan! I see that you're a omnivore with a mayonnaise allergy."}
    ]
    # FIX 1: The variable for the client is 'mem0', not 'client'.
    # I've also changed the hardcoded user_id to use our USER_ID variable for consistency.
    mem0.add(messages, user_id=USER_ID)
    print("Memory added successfully.")


def get_memory_by_query():
    """
    Searches for memories based on a query and prints the results.
    """
    print("\nSearching for memories...")
    # FIX 2: The query string needs an 'f' at the beginning to become an f-string.
    # This allows it to correctly insert the value of the USER_ID variable.
    query = f"What are {USER_ID}'s dietary preferences?"
    print(f"Using query: \"{query}\"")
    
    results = mem0.search(query=query, user_id=USER_ID)

    if not results:
        print("No memories found for that query.")
        return None

    # Process the results into a more readable format
    memories = [
        {
            "memory": result["memory"],
            "updated_at": result["updated_at"]
        }
        for result in results
    ]
    
    # Use json.dumps with indentation for pretty-printing
    memories_str = json.dumps(memories, indent=2)
    print("Found memories:")
    print(memories_str)
    return memories_str


# This block runs when you execute the script directly
if __name__ == "__main__":
    # Configure logging to show informational messages
    logging.basicConfig(level=logging.INFO)

    # FIX 3: The add_memory() function was defined but never called.
    # You need to add memories before you can search for them.
    add_memory()
    
    # Now, call the function to get the memory you just added.
    get_memory_by_query()

