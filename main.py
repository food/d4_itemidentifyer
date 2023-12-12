import pyautogui
import keyboard
import pytesseract
import pygame
from PIL import Image
import json
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import QtGui
import threading


def take_screenshot():
    """Take screenshot of the whole screen"""
    # Take a screenshot and return it
    return pyautogui.screenshot()


def crop_image(screenshot, from_mouse, mouse_x): 
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
    Check the attributes of an item based on the provided text.

    Args:
        text (str): The text to analyze.

    Returns:
        bool: True if the item has the required attributes, False otherwise.
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
        return False
    
    print(f"item_in_inventar: {item_in_inventar}")

    if item_in_inventar == "Ring":
        recired_item_attr = requiredItems["bis"]["ring"]
        recired_item_attr2 = requiredItems["bis"]["ring2"]
        print(f"recired_item_attr: {recired_item_attr}")
        print(f"recired_item_attr2: {recired_item_attr2}")
        if unique_check(recired_item_attr, text) or none_unique_check(recired_item_attr, text) or unique_check(recired_item_attr2, text) or none_unique_check(recired_item_attr2, text):
            play_sound("success")
            return True
        else:
            play_sound("fail")
            return False
    else:
        if(requiredItems["class"] != "barbarian"):
            item_in_inventar = "weapon" if check_item_is_weapon_or_offhand(item_in_inventar, "weapon") else item_in_inventar
            item_in_inventar = "offhand" if check_item_is_weapon_or_offhand(item_in_inventar, "offhand") else item_in_inventar
            print(requiredItems["bis"])
            print(item_in_inventar.lower())
            recired_item_attr = requiredItems["bis"][item_in_inventar.lower()]
        else:
            item_is_barbarian_weapon(item_in_inventar)
            recired_item_attr = requiredItems["bis"]["ring"]

        print(f"recired_item_attr: {recired_item_attr}")

        if unique_check(recired_item_attr, text) or none_unique_check(recired_item_attr, text):
            play_sound("success")
            return True
        else:
            play_sound("fail")
            return False


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
    Load the required item list from a JSON file.

    This function reads the required item list from a JSON file located at "data/required.json"
    and assigns it to the global variable `requiredItems`. The loaded data is expected to contain
    information about the required items, including their attributes and classes.

    Global Variables:
        requiredItems: A dictionary containing information about the required items.

    Raises:
        FileNotFoundError: If the specified JSON file is not found.
        json.JSONDecodeError: If there is an issue decoding the JSON data.
    """
    global requiredItems
    try:
        with open("data/required.json", "r") as file:
            requiredItems = json.load(file)
    except FileNotFoundError:
        print("Error: The specified JSON file ('data/required.json') was not found.")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        raise


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
    """
    Load game scope data from a JSON file.

    This function reads the game scope data from a JSON file located at "data/game_scope_data.json"
    and assigns it to the global variable `game_scope_data`. The loaded data is expected to contain
    information about the game's scope, including slots and attributes.

    Global Variables:
        game_scope_data: A dictionary containing information about the game's scope.

    Raises:
        FileNotFoundError: If the specified JSON file is not found.
        json.JSONDecodeError: If there is an issue decoding the JSON data.
    """
    global game_scope_data
    try:
        with open("data/game_scope_data.json", "r") as file:
            game_scope_data = json.load(file)
    except FileNotFoundError:
        print("Error: The specified JSON file ('data/game_scope_data.json') was not found.")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        raise


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


def get_usable_items_for_class():
    """
    Get the usable items for the current class.

    Returns:
        list: The list of usable items for the class.
    """
    generally_values = get_last_values(game_scope_data["slots"]["generally"])
    classs_values = get_last_values(game_scope_data["slots"][requiredItems["class"]])

    # Convert arrays to sets and perform union
    merged_set = set(generally_values).union(classs_values)

    # Convert the result back to a list adn return
    return list(merged_set)


def check_item_is_weapon_or_offhand(item, type):
    """
    Check if the provided item is a weapon or offhand of the specified type.

    Args:
        item (str): The item to check.
        type (str): The type of the item.

    Returns:
        bool: True if the item is of the specified type, False otherwise.
    """
    return item in game_scope_data["slots"][requiredItems["class"]][type]

def item_is_barbarian_weapon(item):
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

class Square:
    """
    Represents a square with positional and color attributes.

    Attributes:
        x (int): The x-coordinate of the top-left corner of the square.
        y (int): The y-coordinate of the top-left corner of the square.
        width (int): The width of the square.
        height (int): The height of the square.
        color: The color of the square.

    Methods:
        __init__: Initializes a new instance of the Square class.
    """
    def __init__(self, x, y, width, height, color):
        """
        Initializes a new instance of the Square class.

        Args:
            x (int): The x-coordinate of the top-left corner of the square.
            y (int): The y-coordinate of the top-left corner of the square.
            width (int): The width of the square.
            height (int): The height of the square.
            color: The color of the square.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
class BackgroundTask(QThread):
    """
    Asynchronous background task for item checking.

    Attributes:
        overlay_signal (pyqtSignal): Signal for emitting overlay updates.

    Methods:
        run: Main method representing the task's execution.
    """
    overlay_signal = pyqtSignal(Square)

    def run(self):
        """
        Main method representing the task's execution.

        The task continuously monitors the keyboard input and takes actions accordingly.
        If the '-' key is pressed, it captures a screenshot and checks for an item in the item window.
        If an item is found, it emits an overlay signal with the corresponding status (item_ok or item_crap).
        The task runs indefinitely until the 'q' key is pressed to exit.
        """
        print("Press '-', to check an hovered item. Press 'Q', to exit.")
        itembox_identifyer_string = "Item Power"

        while True:
            if keyboard.is_pressed("-"):
                # Get mouse positions
                mouse_x, mouse_y = pyautogui.position()

                # Take a screenshot
                screenshot = take_screenshot()
                # Crop screenshot from mouse to left side
                cropped_screenshot = crop_image(screenshot, "left", mouse_x)
                # get text from the screenshotq
                text = extract_text_from_image(cropped_screenshot)

                # check left side from mouse for the item window
                if find_string_in_text(text, itembox_identifyer_string):
                    print("Found on left side")
                    if check_attributes(text):
                        self.overlay_signal.emit(Square(mouse_x, mouse_y, 50, 50, item_ok))
                    else:
                        self.overlay_signal.emit(Square(mouse_x, mouse_y, 50, 50, item_crap))
                else:
                    # Crop screenshot from mouse to right side
                    cropped_screenshot = crop_image(screenshot, "right", mouse_x)
                    # get text from the screenshot
                    text = extract_text_from_image(cropped_screenshot)
                    if find_string_in_text(text, itembox_identifyer_string):
                        print("Found on right side")
                        if check_attributes(text):
                            self.overlay_signal.emit(Square(mouse_x, mouse_y, 50, 50, item_ok))
                        else:
                            self.overlay_signal.emit(Square(mouse_x, mouse_y, 50, 50, item_crap))
                    else:
                        print("No Item found!")

            # Exit if Q was pressed
            if keyboard.is_pressed("q"):
                print("Programm wird beendet.")
                sys.exit()

class Overlay(QWidget):
    """
    Overlay widget for displaying squares.
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.showFullScreen()
        self.initOverlay()
        self.squares = []

    def initOverlay(self):
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for square in self.squares:
            print(square)
            painter.fillRect(square.x, square.y, square.width, square.height, square.color)

    def foo(self, square):
        print(square)
        self.squares.append(square)
        self.update()

game_scope_data = None
requiredItems = None
item_ok = QtGui.QColor(0, 255, 0, 100)
item_crap = QtGui.QColor(255, 0, 0, 100)

def main():
    """
    Main function to run the application.
    """
    load_game_scope_data()
    load_required_item_list()

    app = QApplication(sys.argv)
    overlay = Overlay()
    background_thread = BackgroundTask()
    background_thread.overlay_signal.connect(overlay.foo)
    background_thread.start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()