import pytesseract
from PIL import Image

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
