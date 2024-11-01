import re
import os
import logging
import shutil
import sys
import subprocess
import win32com.client


def parse_vdf_library_folders(vdf_path):
    library_paths = []

    try:
        with open(vdf_path, "r", encoding="utf-8") as file:
            vdf_content = file.read()

        # Match paths in the VDF file (i.e., lines with "path" followed by the folder path)
        library_entries = re.findall(
            r'"\d+"\s*{\s*"path"\s*"([^"]+)"', vdf_content)

        # Add the extracted paths to library_paths list
        for path in library_entries:
            library_paths.append(path)

    except FileNotFoundError:
        print(f"VDF file not found: {vdf_path}")
    except Exception as e:
        print(f"Error reading VDF file: {e}")

    return library_paths


def find_game_path():
    # Path to Steam's libraryfolders.vdf file (usually within default Steam installation)
    steam_default_path = r"C:\Program Files (x86)\Steam"
    library_folders_path = os.path.join(
        steam_default_path, "steamapps", "libraryfolders.vdf")

    library_paths = parse_vdf_library_folders(library_folders_path)
    if not library_paths:
        logging.error("No library paths found in VDF file.")
        return None

    # Check each library folder for Elden Ring
    for library in library_paths:
        elden_ring_path = os.path.join(
            library, "steamapps", "common", "ELDEN RING")
        if os.path.exists(elden_ring_path):
            return elden_ring_path

    logging.error("Elden Ring not found in any Steam library folder.")
    return None


def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def install_mods(game_dir):
    source_dir = get_resource_path(r"modengine2")

    destination_dir = f"{game_dir}/game/coop_mods"
    logging.info("Installing mods to: %s", destination_dir)
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)

    return destination_dir


def create_launcher_shortcut(mod_folder_dir):
    # Path to the .bat file
    bat_file_path = f"{mod_folder_dir}/launchmod_eldenring.bat"

    # Path to the desktop
    shortcut_folder = os.path.join(
        os.environ["USERPROFILE"], "AppData", "Local", "Elden Ring - Seamless Coop")
    os.makedirs(shortcut_folder, exist_ok=True)

    # Shortcut name and target location
    shortcut_path = os.path.join(
        shortcut_folder, "ELDEN RING - Seamless Coop Launcher.lnk")

    # Create the shortcut
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = bat_file_path  # Path to the .bat file
    shortcut.WorkingDirectory = os.path.dirname(
        bat_file_path)  # Optional: Set working directory
    shortcut.Save()

    logging.info("Created desktop shortcut: %s", shortcut_path)

    return shortcut_folder


def main():
    log_level = logging.DEBUG
    logging.basicConfig(
        level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    er_path = find_game_path()
    logging.info('Elden Ring path: %s', er_path)

    mod_folder_path = install_mods(er_path)
    shortcut_path = create_launcher_shortcut(mod_folder_path)
    subprocess.Popen(f'explorer "{shortcut_path}"')


if __name__ == '__main__':
    main()
