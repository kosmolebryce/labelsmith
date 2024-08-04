import logging
import tkinter as tk
from tkinter import ttk, messagebox
from labelsmith.shyft.core import config_manager
from labelsmith.shyft.core.theme_manager import ThemeManager
from labelsmith.shyft.utils.plotting import Plotting

plotter = Plotting()
logger = logging.getLogger("labelsmith")

def setup_menu(gui):
    logger.debug("Starting setup_menu in menu.py")
    
    gui.menu_bar = tk.Menu(gui.root)
    logger.debug("Created menu_bar")
    
    setup_file_menu(gui)
    logger.debug("File menu setup complete")
    
    setup_theme_menu(gui)
    logger.debug("Theme menu setup complete")
    
    setup_view_menu(gui)
    logger.debug("View menu setup complete")
    
    setup_settings_menu(gui)
    logger.debug("Settings menu setup complete")
    
    gui.root.config(menu=gui.menu_bar)
    logger.debug("Root menu configuration complete")
    
    logger.debug("Finished setup_menu in menu.py")

def setup_file_menu(gui):
    gui.file_menu = tk.Menu(gui.menu_bar, tearoff=0)
    gui.file_menu.add_command(label="Plot productivity", command=plotter.plot_productivity_default)
    gui.menu_bar.add_cascade(label="File", menu=gui.file_menu)

def setup_theme_menu(gui):
    gui.theme_menu = tk.Menu(gui.menu_bar, tearoff=0)
    themes = ["default", "classic", "alt", "clam"]
    for theme in themes:
        gui.theme_menu.add_command(label=theme.capitalize(), command=lambda t=theme: change_theme(gui, t))
    if gui.root.tk.call("tk", "windowingsystem") == "aqua":
        gui.theme_menu.add_command(label="Aqua", command=lambda: change_theme(gui, "aqua"))
    gui.menu_bar.add_cascade(label="Theme", menu=gui.theme_menu)

def setup_view_menu(gui):
    gui.view_menu = tk.Menu(gui.menu_bar, tearoff=0)
    gui.view_menu.add_checkbutton(
        label="Timer Always on Top",
        command=gui.toggle_timer_topmost,
        variable=gui.timer_topmost_var
    )
    gui.menu_bar.add_cascade(label="View", menu=gui.view_menu)

def setup_settings_menu(gui):
    logger.debug("Starting setup_settings_menu")
    gui.settings_menu = tk.Menu(gui.menu_bar, tearoff=0)
    gui.settings_menu.add_command(label="Stopclock Timestring Color", command=lambda: gui.choose_color("time_color"))
    gui.settings_menu.add_command(label="Stopclock Background Color", command=lambda: gui.choose_color("bg_color"))
    gui.settings_menu.add_command(label="Stopclock Button Text Color", command=lambda: gui.choose_color("btn_text_color"))
    gui.menu_bar.add_cascade(label="Settings", menu=gui.settings_menu)
    logger.debug("Finished setup_settings_menu")

def change_theme(gui, theme_name):
    ThemeManager.change_theme(gui.style, theme_name, gui.config)

def choose_color(gui, color_type):
    logger.debug(f"Choosing color for {color_type}")
    
    current_color = getattr(gui, color_type)
    # Use tk.colorchooser and specify the parent window
    color_code = tk.colorchooser.askcolor(
        title=f"Choose {color_type.replace('_', ' ').title()}", 
        initialcolor=current_color,
        parent=gui.root
    )[1]
    logger.debug(f"Color chooser returned: {color_code}")

def enable_topmost_menu(gui):
    gui.view_menu.entryconfig("Timer Always on Top", state="normal")

def disable_topmost_menu(gui):
    gui.view_menu.entryconfig("Timer Always on Top", state="disabled")

def disable_theme_menu(gui):
    gui.menu_bar.entryconfig("Theme", state="disabled")

def enable_theme_menu(gui):
    gui.menu_bar.entryconfig("Theme", state="normal")