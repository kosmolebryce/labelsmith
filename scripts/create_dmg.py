import logging
import os
import subprocess
import toml
from pathlib import Path

logger = logging.getLogger("labelsmith")

def get_version():
    try:
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        pyproject_data = toml.load(pyproject_path)
        return pyproject_data["tool"]["poetry"]["version"]
    except Exception as e:
        logging.error(f"Failed to read version from pyproject.toml: {e}")
        return "0.0.0"  # Fallback version

def create_dmg(version):
    logging.info("Creating DMG...")
    
    app_name = "Shyft.app"
    dmg_name = f"Shyft-{version}.dmg"
    source_dir = "./Shyft.app"
    dest_dir = "./output"
    background_img = "./src/labelsmith/shyft/resources/dmg-background.png"

    # Ensure source directory exists
    if not os.path.exists(source_dir):
        logging.error(f"Source directory does not exist: {source_dir}")
        return

    # Ensure destination directory exists, or create it
    os.makedirs(dest_dir, exist_ok=True)

    # Ensure background image exists
    if not os.path.exists(background_img):
        logging.error(f"Background image does not exist: {background_img}")
        return

    # Create the DMG
    cmd = [
        "create-dmg",
        "--volname", "Shyft Installer",
        "--background", background_img,
        "--window-size", "600", "400",
        "--icon-size", "100",
        "--app-drop-link", "400", "150",
        "--icon", app_name, "200", "150",
        f"{dest_dir}/{dmg_name}",
        source_dir
    ]

    try:
        subprocess.run(cmd, check=True)
        logging.info(f"DMG created successfully: {dest_dir}/{dmg_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to create DMG: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during DMG creation: {e}")

if __name__ == "__main__":
    v = get_version()
    create_dmg(v)
