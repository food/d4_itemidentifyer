import json

def load_required_item_list():
    try:
        with open("data/required.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: The specified JSON file ('data/required.json') was not found.")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        raise


def load_game_scope_data():
    try:
        with open("data/game_scope_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: The specified JSON file ('data/game_scope_data.json') was not found.")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        raise