import pyautogui
import keyboard
import pytesseract
import pygame
from PIL import Image
import json

def take_screenshot():
    """Take screenshot of the whole screen"""

    # Take a screenshot and return it
    return pyautogui.screenshot()


def crop_image(screenshot, from_mouse): 
    """
    Crop the input screenshot based on the specified region around the mouse cursor.

    Args:
        screenshot (Image.Image): The input screenshot (Pillow Image object).
        from_mouse (str): Direction from which to crop. Either "left" or "right".

    Returns:
        Image.Image: The cropped region as a new Pillow Image object.

    Raises:
        ValueError: If the "from_mouse" parameter is not "left" or "right".
    """

    # Get screenshot height
    height = screenshot.height
    
    # Get mouse positions
    mouse_x, mouse_y = pyautogui.position()

    # cut screenshot frome mouse position to -600px    
    if from_mouse == "left":
        XS = mouse_x - 600
        XE = mouse_x
        YS = 100
        YE = height - 250 # not rewuierd part of the screenshot, so minimize data
        return screenshot.crop((XS, YS, XE, YE))
    elif from_mouse == "right":
        # cut screenshot frome mouse position to +600px    
        print(f"from_mouse: {from_mouse}")
        XS = mouse_x
        XE = mouse_x + 600
        YS = 100
        YE = height - 250 # not rewuierd part of the screenshot, so minimize data
        print(XS, XE, YS, YE)
        return screenshot.crop((XS, YS, XE, YE))
    else:
        raise ValueError("Invalid value for 'from_mouse'. Use 'left' or 'right'.")


def extract_text_from_image(screenshot):
    """
    Extract text content from the provided screenshot.

    Args:
        screenshot (Image.Image): The input screenshot (Pillow Image object).

    Returns:
        str: Extracted text content.

    Raises:
        pytesseract.TesseractError: If Tesseract OCR encounters an error during text extraction.
    """

    # Convert the PIL-Imageobject to RGB colors
    image_data = screenshot.convert("RGB")

    # Save the screenshot as a temporary JPEG file
    #timestamp = time.strftime("%Y%m%d%H%M%S")
    #filename = f"screenshot_{timestamp}_{random.randint(1, 10)}.jpg"
    filename = "tmp.jpg"
    #image_data.save(filename, "JPEG", quality=50)
    image_data.save(filename, "JPEG", quality=95)

    try:
        # Use Tesseract OCR to extract text from the saved image
        extracted_text = pytesseract.image_to_string(Image.open(filename))
        return extracted_text
    except pytesseract.TesseractError as e:
        # Handle Tesseract OCR errors
        raise pytesseract.TesseractError(f"Error during text extraction: {str(e)}")
    finally:
        # Clean up: Remove the temporary JPEG file
        Image.open(filename).close()


def find_string_in_text(text, search_string):
    """
    Check if a specific string is present in the given text.

    Args:
        text (str): The input text in which the search will be performed.
        search_string (str): The string to search for within the input text.

    Returns:
        bool: True if the search string is found in the text, False otherwise.

    Example:
        >>> find_string_in_text("This is a sample text.", "sample")
        True
        >>> find_string_in_text("Another example.", "test")
        False
    """

    return search_string in text


def check_attributes(text):
    """
    Check if the given OCR text corresponds to required attributes for specific item classes.

    Args:
        text (str): The OCR text to be checked.

    Returns:
        None

    Prints:
        - The recognized item class if found.
        - The OCR text and a message if the item type is not found in the required list.
        - Success or fail messages based on attribute checks.

    Example:
        >>> check_attributes("Some OCR text")
    """

    found = False
    item_in_inventar = None

    usable_item_list = get_usable_items_for_class()

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
        return
    
    print(f"item_in_inventar: {item_in_inventar}")

    if item_in_inventar == "Ring":
        recired_item_attr = requiredItems["bis"]["ring"]
        recired_item_attr2 = requiredItems["bis"]["ring2"]
        print(f"recired_item_attr: {recired_item_attr}")
        print(f"recired_item_attr2: {recired_item_attr2}")
        if unique_check(recired_item_attr, text) or none_unique_check(recired_item_attr, text) or unique_check(recired_item_attr2, text) or none_unique_check(recired_item_attr2, text):
            play_sound("success")
        else:
            play_sound("fail")
    else:
        item_in_inventar = "weapon" if check_item_is_weapon_or_offhand(item_in_inventar, "weapon") else item_in_inventar
        item_in_inventar = "offhand" if check_item_is_weapon_or_offhand(item_in_inventar, "offhand") else item_in_inventar
        recired_item_attr = requiredItems["bis"][item_in_inventar.lower()]
        print(f"recired_item_attr: {recired_item_attr}")

        if unique_check(recired_item_attr, text) or none_unique_check(recired_item_attr, text):
            play_sound("success")
        else:
            play_sound("fail")


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


def load_required_item_list():
    """
    Load a list of required items with their specifications.

    Returns:
        list: A list of dictionaries representing the required items. Each dictionary contains information such as the item key, 
              whether it"s unique, the name of the item, and additional attributes.

    Example:
        [
            {"key": "Helm", "unique": True, "name": "Godslayer Crown"},
            {"key": "Chest", "min_match_count": 3, "attribut1": "Total Armor", "attribut2": "Damage Reduction from Distant Enemies", 
             "attribut3": "Damage Reduction from Close Enemies", "attribut4": "Damage Reduction from Burning Enemies"},
        ]
    """

    global requiredItems
    with open("data/required.json", "r") as file:
        requiredItems = json.load(file)


def play_sound(status):
    """
    Play a sound based on the provided status.
    https://freesound.org/people/shinephoenixstormcrow/sounds/337050/
    https://freesound.org/people/paththeir/sounds/196196/
    https://freesound.org/people/alphahog/sounds/46189/

    Args:
        status (str): The status indicating the outcome for which the sound should be played. 
                      Should be one of: "success", "fail", or any other value for an error sound.

    Returns:
        None

    Example:
        >>> play_sound("success")
        # Plays the success sound.
    """

    sound_file_path = "./success.mp3"
    if status == "success":
        sound_file_path = "./success.mp3"
    elif status == "fail":
        sound_file_path = "./fail.mp3"
    else: 
        sound_file_path = "./error.wav"

    pygame.mixer.init()
    pygame.mixer.music.load(sound_file_path)
    pygame.mixer.music.play()


def find_string_in_text_bin_response(text, search_string):
    """
    Check if a specific string is present in the given text and return a binary response.

    Args:
        text (str): The input text in which the search will be performed.
        search_string (str): The string to search for within the input text.

    Returns:
        int: Binary response indicating the presence (1) or absence (0) of the search string in the text.

    Example:
        >>> find_string_in_text_bin_response("This is a sample text.", "sample")
        1
        >>> find_string_in_text_bin_response("Another example.", "test")
        0
    """

    return 1 if find_string_in_text(text, search_string) else 0


def load_game_scope_data():
    global game_scope_data
    with open("data/game_scope_data.json", "r") as file:
        game_scope_data = json.load(file)


def get_last_values(data):
    result = []
    for key, value in data.items():
        if isinstance(value, dict):
            result.extend(get_last_values(value))
        elif isinstance(value, list):
            result.extend(value)
    return result


def get_usable_items_for_class():
    """
    Get a list of usable items for the current character class based on the last values in the game scope data.

    Returns:
        list: A list of usable items for the current character class.

    Example:
        >>> get_usable_items_for_class()
        ['Helm', 'Chest', 'Gloves', 'Pants', 'Boots', 'Amulet', 'Ring']
    """

    generally_values = get_last_values(game_scope_data["slots"]["generally"])
    classs_values = get_last_values(game_scope_data["slots"][requiredItems["class"]])

    # Convert arrays to sets and perform union
    merged_set = set(generally_values).union(classs_values)

    # Convert the result back to a list adn return
    return list(merged_set)


def check_item_is_weapon_or_offhand(item, type):
    """
    Check if the given item is either a weapon or an offhand based on the specified type and character class.

    Args:
        item (str): The item to be checked.
        type (str): The type of item to check ("weapon" or "offhand").

    Returns:
        bool: True if the item is of the specified type for the current character class, False otherwise.

    Example:
        >>> check_item_is_weapon_or_offhand("Axe", "weapon")
        True
    """

    values = []
    if(requiredItems["class"] == "barbarian" and type != "offhand"):
        values = get_last_values(game_scope_data["slots"]["barbarian"])
    else:
        values = game_scope_data["slots"][requiredItems["class"]][type]

    return item in values


game_scope_data = None
requiredItems = None

def main():
    print("Press '-', to check an hovered item. Press 'Q', to exit.")
    itembox_identifyer_string = "Item Power"
    load_game_scope_data()
    load_required_item_list()

    while True:
        if keyboard.is_pressed("-"):
        # Take a screenshot
            screenshot = take_screenshot()
            # Crop screenshot from mouse to left side
            cropped_screenshot = crop_image(screenshot, "left")
            # get text from the screenshotq
            text = extract_text_from_image(cropped_screenshot)

            # check left side from mouse for the item window
            if find_string_in_text(text, itembox_identifyer_string):
                print("Found on left side")
                check_attributes(text)
            else:
                # Crop screenshot from mouse to right side
                cropped_screenshot = crop_image(screenshot, "right")
                # get text from the screenshot
                text = extract_text_from_image(cropped_screenshot)
                if find_string_in_text(text, itembox_identifyer_string):
                    print("Found on right side")
                    check_attributes(text)
                else:
                    print("No Item found!")

        # Exit if Q was pressed
        if keyboard.is_pressed("q"):
            print("Programm wird beendet.")
            break


if __name__ == "__main__":
    main()