import multiprocessing
import tkinter as tk
import logging
from labelsmith.shyft.gui.main_window import ShyftGUI
from labelsmith.shyft.utils.system_utils import get_modifier_key, modkey_backspace, modkey_shift_backspace
from labelsmith.shyft.core.nltk_manager import initialize_nltk
from labelsmith.shyft.utils.log_config import configure_logging
from labelsmith.shyft.constants import APP_AUTHOR, APP_DATA_DIR, APP_NAME, DATA_FILE_PATH, CONFIG_FILE, LOGS_DIR

logger = configure_logging(debug=True)

def run_tkinter_app():
    logger.debug("Starting Tkinter application")
    root = tk.Tk()
    app = ShyftGUI(root)
    modkey = get_modifier_key()

    # Move shortcuts setup to after ShyftGUI initialization
    setup_shortcuts(root, app, modkey)

    logger.debug("Entering Tkinter main loop")
    
    root.mainloop()

def setup_shortcuts(root, app, modkey):
    logger.debug("Setting up shortcuts")
    shortcuts = {
        "a": app.autolog,
        "d": app.delete_shift,
        "e": app.edit_shift,
        "n": app.manual_entry,
        "l": app.view_logs,
        "t": app.calculate_totals,
        "q": app.on_quit,
        "r": app.refresh_view,
    }

    for key, func in shortcuts.items():
        root.bind(f"<{modkey}-{key}>", func)
        root.bind(f"<{modkey}-{key.upper()}>", func)

    root.bind_all(f"<{modkey}-BackSpace>", modkey_backspace)
    root.bind_all(f"<{modkey}-Shift-BackSpace>", modkey_shift_backspace)
    root.bind_all(f"<{modkey}-Shift-BackSpace>", modkey_shift_backspace, add='+')

    root.bind_all(f"<{modkey}-m>", app.minimize_window)
    logger.debug("Shortcuts setup complete")

def main():
    try:
        nltk_available = initialize_nltk()
    except Exception as e:
        logger.error(f"Failed to initialize NLTK: {e}")
        nltk_available = False
    
    process = multiprocessing.Process(target=run_tkinter_app)
    process.start()
    
    logger.info(f"Application started. NLTK WordNet available: {nltk_available}")
    logger.info(f"""
`APP_NAME`: {APP_NAME}
`APP_AUTHOR`: {APP_AUTHOR}
`APP_DATA_DIR`: {APP_DATA_DIR}
`CONFIG_FILE`: {CONFIG_FILE}
`DATA_FILE_PATH`: {DATA_FILE_PATH}
`LOGS_DIR`: {LOGS_DIR}
""")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()