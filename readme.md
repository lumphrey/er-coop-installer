# Elden Ring Mod Installer

Automates installation of mods for Elden Ring.

## Features

- **Automatic Game Path Detection**: Identifies the installation path of Elden Ring within Steam library folders.
- **Mod Installation**: Copies mod files to the appropriate game directory.
- **Shortcut Creation**: Generates a desktop shortcut for launching Elden Ring with mods.

## Requirements

- **Python 3.8+**
- **Steam Installation**: Ensure that Steam and Elden Ring are installed on your system.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/lumphrey/er-coop-installer.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare Mod Files**:
   - Place the mod files in a folder named `modengine2`, located in the same directory as this script.

2. **Run the Installer (development)**:
   - Execute the application by running the following command:
     ```bash
     python elden_ring_mod_installer.py
     ```
## Functions

- **parse_vdf_library_folders(vdf_path)**: Parses the `libraryfolders.vdf` file to extract Steam library paths.
- **find_game_path()**: Searches through Steam library folders to locate the Elden Ring installation.
- **get_resource_path(relative_path)**: Resolves paths for resources, compatible with PyInstaller for executable packaging.
- **install_mods(game_dir)**: Copies mod files from `modengine2` to the Elden Ring mods folder.
- **create_launcher_shortcut(mod_folder_dir)**: Creates a Windows shortcut to launch Elden Ring with mods enabled.

## Example

1. Run the script:
   ```bash
   python elden_ring_mod_installer.py
   ```
2. If successful, a shortcut will be created in the `AppData\Local\Elden Ring - Seamless Coop` directory.
3. Use this shortcut to launch Elden Ring with mods.

# Development
## Build Windows executable
```
pyinstaller --onefile --add-data "src\modengine2;modengine2" src\installer.py
```

## Troubleshooting

- **VDF File Not Found**: Ensure Steam is installed, and the `libraryfolders.vdf` file exists in the default location. Update the `steam_default_path` variable if necessary.
- **Mod Installation Fails**: Verify that the `modengine2` folder contains the correct mod files.
