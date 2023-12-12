from overlay import Overlay
from background_task import BackgroundTask
from data_loader import load_game_scope_data, load_required_item_list
from PyQt5.QtWidgets import QApplication
import sys

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
