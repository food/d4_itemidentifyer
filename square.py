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