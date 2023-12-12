import pygame

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

