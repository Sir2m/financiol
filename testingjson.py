import json

# Load user preferences from JSON file
def load_preferences(filepath, user_id):
    with open(filepath, 'r') as file:
        data = json.load(file)
        if user_id not in data['users']:
            # Initialize default preferences for new user
            data['users'][user_id] = {
                "remember_me": False,
                "theme": "light",
                "currency": "USD"
            }
            save_preferences(filepath, user_id, data['users'][user_id])
        return data['users'][user_id]
    
def save_preferences(filepath, user_id, preferences):
    with open(filepath, 'r') as file:
        data = json.load(file)
    data['users'][user_id] = preferences
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)


def update_preferences(filepath, user_id, key, value):
    preferences = load_preferences(filepath, user_id)
    preferences[key] = value
    save_preferences(filepath, user_id, preferences)
