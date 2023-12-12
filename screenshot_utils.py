import pyautogui
from PIL import Image

def take_screenshot():
    """Take screenshot of the whole screen"""
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

