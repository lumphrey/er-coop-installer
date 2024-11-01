import re
import os
import logging


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


def main():
    log_level = logging.DEBUG
    logging.basicConfig(
        level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    er_path = find_game_path()
    logging.info('ER path: %s', er_path)


if __name__ == '__main__':
    main()
