import pyautogui
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from square import Square
from screenshot_utils import take_screenshot, crop_image
from ocr_utils import extract_text_from_image
from item_check_utils import check_attributes
from text_utils import find_string_in_text
import keyboard
import sys

class BackgroundTask(QThread):
    """
    Asynchronous background task for item checking.

    Attributes:
        overlay_signal (pyqtSignal): Signal for emitting overlay updates.

    Methods:
        run: Main method representing the task's execution.
    """
    overlay_signal = pyqtSignal(Square)

    item_ok = QtGui.QColor(0, 255, 0, 100)
    item_crap = QtGui.QColor(255, 0, 0, 100)

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
                        self.overlay_signal.emit(Square(mouse_x, mouse_y, 50, 50, self.item_ok))
                    else:
                        self.overlay_signal.emit(Square(mouse_x, mouse_y, 50, 50, self.item_crap))
                else:
                    # Crop screenshot from mouse to right side
                    cropped_screenshot = crop_image(screenshot, "right", mouse_x)
                    # get text from the screenshot
                    text = extract_text_from_image(cropped_screenshot)
                    if find_string_in_text(text, itembox_identifyer_string):
                        print("Found on right side")
                        if check_attributes(text):
                            self.overlay_signal.emit(Square(mouse_x, mouse_y, 50, 50, self.item_ok))
                        else:
                            self.overlay_signal.emit(Square(mouse_x, mouse_y, 50, 50, self.item_crap))
                    else:
                        print("No Item found!")

            # Exit if Q was pressed
            if keyboard.is_pressed("q"):
                print("Programm wird beendet.")
                sys.exit()