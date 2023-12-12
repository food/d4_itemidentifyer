import json

def load_required_item_list():
    """
    Load the required item list from a JSON file.

    This function reads the required item list from a JSON file located at "data/required.json"
    and returns the loaded data. The loaded data is expected to contain information about
    the required items, including their attributes and classes.

    Returns:
        dict: A dictionary containing information about the required items.

    Raises:
        FileNotFoundError: If the specified JSON file is not found.
        json.JSONDecodeError: If there is an issue decoding the JSON data.
    """
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
    """
    Load game scope data from a JSON file.

    This function reads the game scope data from a JSON file located at "data/game_scope_data.json"
    and returns the loaded data. The loaded data is expected to contain information about
    the game's scope, including slots and attributes.

    Returns:
        dict: A dictionary containing information about the game's scope.

    Raises:
        FileNotFoundError: If the specified JSON file is not found.
        json.JSONDecodeError: If there is an issue decoding the JSON data.
    """
    try:
        with open("data/game_scope_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: The specified JSON file ('data/game_scope_data.json') was not found.")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        raise