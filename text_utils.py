import re

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


def pattern_found(pattern, text):
    """
    Check if a pattern is found in a string using regular expressions.

    Args:
        pattern (str): The regular expression pattern to search for.
        text (str): The input string in which the search will be performed.

    Returns:
        bool: True if the pattern is found, False otherwise.

    Example:
        >>> pattern_found(r'\d+', 'This string contains a number: 123')
        True
    """
    print("text", text)
    print("pattern", pattern)
    print("regex", re.search(pattern, text, re.IGNORECASE))
    return bool(re.search(pattern, text, re.IGNORECASE))