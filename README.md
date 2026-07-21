# Travel Manager

Travel Manager is a cross-platform desktop application for exploring OpenStreetMap data, finding places, planning routes, and estimating travel costs. It combines a Flask backend with a browser-based interface displayed in a native pywebview window.

![Travel Manager screenshot](doc/screenshot.png)

[Polska wersja dokumentacji](README-pl_PL.md)

## Features

- Interactive OpenStreetMap with standard, cycling, and humanitarian map styles
- Place search, reverse geocoding, advanced category search, and detailed OSM object information
- Route planning for cars, bicycles, and pedestrians
- Route distance, duration, and geometry with alternative routing services where available
- Saved routes and favourite places organized with custom tags and emojis
- Car profiles with vehicle details, fuel types, consumption, and odometer entries
- Travel cost estimates based on the selected car profile and fuel prices
- Fuel price data for Poland and European countries, manual price editing, and currency conversion
- Import and export of routes, favourites, tags, and fuel-price data as JSON
- Persistent UI preferences and window size/position
- Native builds for Windows, macOS, and Linux using PyInstaller

## Technology

- Python, Flask, and Werkzeug for the local backend
- pywebview for the native desktop window
- HTML, CSS, and vanilla JavaScript for the interface
- Leaflet and Lucide loaded from CDNs
- OpenStreetMap tiles and data, Nominatim, Overpass API, OSRM, and OpenStreetMap routing services
- AutoCentrum, the European Commission Weekly Oil Bulletin, and Frankfurter for fuel-price and exchange-rate data

## Requirements

- Python 3.10 or newer
- Internet access for map tiles, geocoding, routing, external UI libraries, and fuel-price updates
- A system WebView runtime supported by pywebview

Linux may require additional GUI/WebKit packages supplied by the distribution. See the [pywebview installation guide](https://pywebview.flowrl.com/guide/installation.html) for platform-specific requirements.

## Installation

Clone the repository and enter its directory, then create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running

Run the platform helper:

```bash
./run.sh
```

or on Windows:

```bat
run.bat
```

You can also start the application directly:

```bash
python app.py
```

The Flask service listens locally at `http://127.0.0.1:5000` and is opened automatically in a desktop window. The host and port can be changed in `config.py`.

## Data and privacy

Application data is stored locally in `settings.json` under the operating system's application configuration directory:

- Windows: `%APPDATA%\TravelManager`
- macOS: `~/Library/Application Support/TravelManager`
- Linux: `$XDG_CONFIG_HOME/TravelManager` or `~/.config/TravelManager`

Saved settings include favourites, tags, routes, car profiles, cached fuel prices, UI preferences, and window geometry. Search terms, coordinates, and routing requests are sent to the external map services required for the selected feature. Imported JSON files should therefore come from a trusted source.

## Building a release

Run the build script for the current operating system:

```bash
./build.sh
```

or on Windows:

```bat
build.bat
```

The build process cleans previous outputs, installs or updates build dependencies, creates a platform-specific PyInstaller bundle, and packages it in `bin/release`. Builds must be produced separately on each target operating system.

To remove Python bytecode cache directories, run `cleanup.sh` or `cleanup.bat`.

## Project structure

```text
app.py          Application startup, desktop window, and native JS API
config.py       Application metadata, paths, host, and port
controllers/    Flask endpoints for views, maps, fuel data, and settings
core/           Flask service and shared API/data abstractions
models/         Map and persistent-settings data models
storage/        JSON settings persistence
resources/      OSM dictionaries, enums, legends, emojis, and fuel metadata
templates/      Jinja HTML views, headers, panels, and dialogs
assets/         CSS, JavaScript, icons, and map legend images
build.py        Cross-platform PyInstaller build and packaging workflow
```

## Configuration

Application metadata and runtime settings are centralized in `config.py`, including `APP_NAME`, `APP_DESCRIPTION`, `APP_VERSION`, `HOST`, and `PORT`. Build metadata is derived from these values through `build_conf.py`.

## License

Copyright (C) Kamil Karpiński. This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE).
