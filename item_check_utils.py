from text_utils import find_string_in_text, find_string_in_text_bin_response, pattern_found
from sound_utils import play_sound
from data_loader import load_game_scope_data, load_required_item_list

def check_attributes(text):
    """
    Check the attributes of an item based on the provided text.

    Args:
        text (str): The text to analyze.

    Returns:
        bool: True if the item has the required attributes, False otherwise.
    """
    found = False
    item_in_inventar = None
    LEGENDARY = "Legendary"
    game_scope_data = load_game_scope_data()
    required_items = load_required_item_list()
    usable_item_list = get_usable_items_for_class(game_scope_data, required_items)

    for item_class in usable_item_list:
        if find_string_in_text(text, item_class):
            print(f"Item is: {item_class}")
            found = True
            item_in_inventar = item_class
            break  # Break the loop once an item is found

    #  If item is unknown print ocr text
    if found == False:
        print(text)
        print("Item type not found in require list")
        return False
    
    print(f"item_in_inventar: {item_in_inventar}")

    if item_in_inventar == "Ring":
        recired_item_attr = required_items["bis"]["ring"]
        recired_item_attr2 = required_items["bis"]["ring2"]
        print(f"recired_item_attr: {recired_item_attr}")
        print(f"recired_item_attr2: {recired_item_attr2}")
        if unique_check(recired_item_attr, text) or none_unique_check(recired_item_attr, text) or unique_check(recired_item_attr2, text) or none_unique_check(recired_item_attr2, text):
            play_sound("success")
            return True
        else:
            # Check for aspect
            if find_string_in_text(text, LEGENDARY):
                for aspect in game_scope_data["aspects"]:
                    if pattern_found(game_scope_data["aspects"][aspect]["regex"], text):
                        print("ASPECT FOUND")
                        play_sound("success")
                        return True
            
            print(text, LEGENDARY)
            play_sound("fail")
            return False
    else:
        if(required_items["class"] != "barbarian"):
            item_in_inventar = "weapon" if check_item_is_weapon_or_offhand(item_in_inventar, "weapon", game_scope_data, required_items) else item_in_inventar
            item_in_inventar = "offhand" if check_item_is_weapon_or_offhand(item_in_inventar, "offhand", game_scope_data, required_items) else item_in_inventar
            #print(required_items["bis"])
            #print(item_in_inventar.lower())
            recired_item_attr = required_items["bis"][item_in_inventar.lower()]
        else:
            item_is_barbarian_weapon(item_in_inventar, game_scope_data)
            recired_item_attr = required_items["bis"]["ring"]

        print(f"recired_item_attr: {recired_item_attr}")

        if unique_check(recired_item_attr, text) or none_unique_check(recired_item_attr, text):
            play_sound("success")
            return True
        else:
            # Check for aspect
            if find_string_in_text(text, LEGENDARY):
                for aspect in game_scope_data["aspects"]:
                    if pattern_found(game_scope_data["aspects"][aspect]["regex"], text):
                        print("ASPECT FOUND")
                        play_sound("success")
                        return True

            play_sound("fail")
            return False


def get_usable_items_for_class(game_scope_data, required_items):
    """
    Get the usable items for the current class.

    Returns:
        list: The list of usable items for the class.
    """
    generally_values = get_last_values(game_scope_data["slots"]["generally"])
    classs_values = get_last_values(game_scope_data["slots"][required_items["class"]])

    # Convert arrays to sets and perform union
    merged_set = set(generally_values).union(classs_values)

    # Convert the result back to a list adn return
    return list(merged_set)


def unique_check(recired_item_attr, text):
    """
    Check if the given OCR text contains the unique name specified in the required item attributes.

    Args:
        recired_item_attr (dict): The required item attributes containing a "unique" key and a "name" key.
        text (str): The OCR text to be checked.

    Returns:
        bool: True if the OCR text contains the unique name, False otherwise.

    Example:
        >>> unique_check({"unique": True, "name": "Unique Item"}, "OCR text containing Unique Item")
    """
    return recired_item_attr.get("unique") and find_string_in_text(text, recired_item_attr["name"]) # TDO O and OO fix!


def none_unique_check(recired_item_attr, text):
    """
    Check if the given OCR text meets the criteria for a non-unique item based on the required item attributes.

    Args:
        recired_item_attr (dict): The required item attributes containing "unique," "attribut1," "attribut2," "attribut3," "attribut4," and "min_match_count" keys.
        text (str): The OCR text to be checked.

    Returns:
        bool: True if the OCR text meets the criteria for a non-unique item, False otherwise.

    Example:
        >>> none_unique_check({"unique": False, "attribut1": "Attribute1", "attribut2": "Attribute2", "min_match_count": 2}, "OCR text containing Attribute1 and Attribute2")
    """
    return recired_item_attr.get("unique") == None and(find_string_in_text_bin_response(text, recired_item_attr["attribut1"]) +
        find_string_in_text_bin_response(text, recired_item_attr["attribut2"]) + 
        find_string_in_text_bin_response(text, recired_item_attr["attribut3"]) +
        find_string_in_text_bin_response(text, recired_item_attr["attribut4"]) >= recired_item_attr["min_match_count"])


def check_item_is_weapon_or_offhand(item, type, game_scope_data, required_items):
    """
    Check if the provided item is a weapon or offhand of the specified type.

    Args:
        item (str): The item to check.
        type (str): The type of the item.

    Returns:
        bool: True if the item is of the specified type, False otherwise.
    """
    return item in game_scope_data["slots"][required_items["class"]][type]


def item_is_barbarian_weapon(item, game_scope_data):
    """
    Check if the provided item is a weapon for the barbarian class.

    Args:
        item (str): The item to check.

    Returns:
        list: A list of weapon types the item belongs to.
    """
    weapon_type_list = []
    weapon_type_list.append("bludgeoning_weapon") if item in game_scope_data["slots"]["barbarian"]["bludgeoning_weapon"] else None
    weapon_type_list.append("slashing_weapon") if item in game_scope_data["slots"]["barbarian"]["slashing_weapon"] else None
    weapon_type_list.append("dual_wield_weapon_1") if item in game_scope_data["slots"]["barbarian"]["dual_wield_weapon_1"] else None
    weapon_type_list.append("dual_wield_weapon_2") if item in game_scope_data["slots"]["barbarian"]["dual_wield_weapon_2"] else None

    return weapon_type_list


def get_last_values(data):
    """
    Get the last values from the provided data.

    Args:
        data (dict): The data to analyze.

    Returns:
        list: The list of last values.
    """
    result = []
    for key, value in data.items():
        if isinstance(value, dict):
            result.extend(get_last_values(value))
        elif isinstance(value, list):
            result.extend(value)
    return result


