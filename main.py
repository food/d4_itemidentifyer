import pyautogui
import keyboard
import time
import pytesseract
import pygame
import time
from PIL import Image
import random
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
    image_data.save(filename, "JPEG", quality=50)

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
    # required_item_list = load_required_item_list()
    found = False
    item_in_inventar = None

    for item in requiredItems:
        if find_string_in_text(text, item["key"]):
            print(f"Item is: {item['key']}")
            found = True
            item_in_inventar = item
            break  # Break the loop once an item is found

    #  If item is unknown print ocr text
    if found == False:
        print(text)
        print("Item type not found in require list")
        return
    
    if item_in_inventar.get("unique") and find_string_in_text(text, item_in_inventar["name"]):
        play_sound("success")
    elif item_in_inventar.get("unique") == False and(find_string_in_text_bin_response(text, item_in_inventar["attribut1"]) +
    find_string_in_text_bin_response(text, item_in_inventar["attribut2"]) + 
    find_string_in_text_bin_response(text, item_in_inventar["attribut3"]) +
    find_string_in_text_bin_response(text, item_in_inventar["attribut4"]) >= item_in_inventar["min_match_count"]):
        play_sound("success")
    else:
        play_sound("fail")


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


def load_classes():
    """
    Load class data from a JSON file and store it in a global variable.

    Reads the content of the "classes.json" file, parses it as JSON, and assigns
    the result to a global variable "classes".

    Global Variable:
        classes (dict): A dictionary containing the loaded class data.

    Example:
        >>> load_classes()
        >>> print(classes)
        {"class1": {"attribute1": "value1", "attribute2": "value2"}, ...}
    """
    global classes
    with open("data/classes.json", "r") as file:
        classes = json.load(file)

classes = None
requiredItems = None

def main():
    print("Press '-', to check an hovered item. Press 'Q', to exit.")
    itembox_identifyer_string = "Item Power"
    load_classes();
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