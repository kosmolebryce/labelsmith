import configparser
import logging
from labelsmith.shyft.constants import CONFIG_FILE

logger = logging.getLogger("labelsmith")

def load_config():
    # Add debug logging
    logger.debug("Loading configuration")
    
    config = configparser.ConfigParser()
    if CONFIG_FILE.exists():
        config.read(CONFIG_FILE)
        logger.debug(f"Configuration loaded from {CONFIG_FILE}")
    else:
        logger.warning(f"Configuration file {CONFIG_FILE} does not exist. Using default settings.")
    
    # Add default sections and values if they don't exist
    if 'Settings' not in config:
        config['Settings'] = {}
    if 'tax_rate' not in config['Settings']:
        config['Settings']['tax_rate'] = '0.27'
    
    if 'Colors' not in config:
        config['Colors'] = {}
    if 'time_color' not in config['Colors']:
        config['Colors']['time_color'] = '#A78C7B'
    if 'bg_color' not in config['Colors']:
        config['Colors']['bg_color'] = '#FFBE98'
    if 'btn_text_color' not in config['Colors']:
        config['Colors']['btn_text_color'] = '#A78C7B'
    
    if 'Theme' not in config:
        config['Theme'] = {}

    if 'selected' not in config['Theme'] and platform.system() == "Darwin":
        config['Theme']['selected'] = 'aqua'

    if 'timer_topmost' not in config['Theme']:
        config['Theme']['timer_topmost'] = 'True'
    
    if 'Window' not in config:
        config['Window'] = {}
        config['Window']['height'] = 100
        config['Window']['width'] = 125
    
    # Add debug logging
    logger.debug("Configuration loading complete")
    
    return config

def update_color_setting(config, color_type, color_code):
    logger.debug(f"Updating color setting: {color_type} = {color_code}")
    if 'Colors' not in config:
        config['Colors'] = {}
    config['Colors'][color_type] = color_code
    save_config(config)

def save_config(config):
    logger.debug("Saving configuration")
    with open(CONFIG_FILE, "w") as config_file:
        config.write(config_file)
    logger.debug(f"Configuration saved to {CONFIG_FILE}")
    
    # Add a verification step
    verify_config = configparser.ConfigParser()
    verify_config.read(CONFIG_FILE)
    logger.debug(f"Verification: timer_topmost in saved config is {verify_config['Theme'].get('timer_topmost', 'Not found')}")

def update_theme_setting(config, theme_name):
    config['Theme']['selected'] = theme_name
    save_config(config)
    logger.info(f"Updated theme to: {theme_name}")

def update_timer_topmost_setting(config, is_topmost):
    config['Theme']['timer_topmost'] = str(is_topmost)
    save_config(config)
    logger.info(f"Updated timer_topmost to: {is_topmost}")
