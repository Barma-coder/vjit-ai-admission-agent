import json
import os

HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(user_query, ai_answer):
    history = load_history()
    history.append({"user": user_query, "assistant": ai_answer})
    # Keep only the last 5 exchanges to avoid cluttering the prompt
    history = history[-5:]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def get_history_string():
    history = load_history()
    if not history:
        return "No previous conversation."
    
    formatted_history = ""
    for entry in history:
        formatted_history += f"Student: {entry['user']}\nAI: {entry['assistant']}\n---\n"
    return formatted_history