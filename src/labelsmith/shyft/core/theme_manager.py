import platform
import tkinter as tk
from tkinter import ttk
import logging
from labelsmith.shyft.core import config_manager

logger = logging.getLogger("labelsmith")
config = config_manager.load_config()

class ThemeManager:
    @staticmethod
    def change_theme(style: ttk.Style, theme_name: str, config) -> None:
        # Add debug logging
        logger.debug(f"Changing theme to {theme_name}")
        
        try:
            style.theme_use(theme_name)
            config_manager.update_theme_setting(config, theme_name)
            logger.info(f"Theme changed to: {theme_name}")
        except tk.TclError as e:
            logger.error(f"Failed to change theme: {e}")

    @staticmethod
    def update_color_scheme(gui, color_type: str, config) -> None:
        logger.debug(f"Updating color scheme for {color_type}")
        logger.debug(f"ThemeManager.update_color_scheme called for {color_type}")
        
        try:
            current_color = getattr(gui, color_type)
            if not current_color:
                current_color = config.get('Colors', color_type, fallback='#FFBE98')
            
            color_code = tk.colorchooser.askcolor(
                title=f"Choose {color_type.replace('_', ' ').title()}", 
                initialcolor=current_color
            )[1]
            
            if color_code:
                setattr(gui, color_type, color_code)
                config_manager.update_color_setting(config, color_type, color_code)
                if gui.timer_window:
                    gui.timer_window.update_colors(gui.time_color, gui.bg_color, gui.btn_text_color)
            
            logger.debug(f"Color scheme updated for {color_type}: {color_code}")
        except Exception as e:
            logger.error(f"Failed to update color scheme: {e}")

    @staticmethod
    def toggle_timer_topmost(gui, config) -> None:
        """
        Toggle the timer window's topmost state.

        Args:
            gui: The main GUI object.
            config (configparser.ConfigParser): The configuration object.
        """
        if gui.timer_window:
            current_topmost_state = gui.timer_window.root.attributes("-topmost")
            new_topmost_state = not current_topmost_state
            gui.timer_window.root.attributes("-topmost", new_topmost_state)
            config_manager.update_timer_topmost_setting(config, new_topmost_state)
            gui.timer_topmost_var.set(new_topmost_state)
            logger.debug(f"Timer topmost state set to {new_topmost_state}.")
        gui.regain_focus()