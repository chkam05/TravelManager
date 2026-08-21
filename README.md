# Travel Manager

Travel Manager brings maps, place search, route planning, car profiles, travel costs, and Polish public transport together in one application. It runs as a native desktop window and can also expose its interface to a browser on a trusted local network.

[Polska wersja dokumentacji](README-pl_PL.md)

![Travel Manager map and main menu](doc/map.png)

> Screenshots are illustrative. Displayed data, available operator features, colours, and interface language may differ depending on the current settings and external data sources.

## What you can do

- Explore OpenStreetMap using standard, cycling, and humanitarian map styles.
- Search for places by name or category and inspect detailed OpenStreetMap information.
- Display favourite places, OpenStreetMap notes, map objects, and public GPS traces as optional layers.
- Create routes for cars, bicycles, and pedestrians, reorder points, reverse routes, and save them for later.
- Estimate fuel usage and trip cost with a selected car profile and country-specific fuel prices.
- Add refuelling markers for economical, average, and dynamic driving styles.
- Request car routes that avoid toll roads when the routing service supports it.
- Maintain detailed car profiles, including an image, technical data, fuel types, consumption, and odometer entries.
- Browse fuel prices for Poland and other European countries, convert currencies, and enter custom values.
- Browse public transport operators, lines, stops, timetables, journeys, announcements, and vehicle positions where supplied by the operator.
- Organise favourite places with custom tags, colours, and emoji.
- Import and export routes, favourites and tags, cars, and fuel-price data as JSON.
- Choose English or Polish and customise the theme, accent, routes, and public transport colours.

## Map and places

Use the search field to find an address or place. Advanced search can narrow results by an OpenStreetMap category, while clicking the map performs a reverse lookup. The place panel groups identification, address, contact, services, access, and technical tags; a selected place can be added to favourites, used as a route point, or exported to JSON.

![Selected place information on the map](doc/place_info.png)

The layer panel controls the base map, favourite tags, OpenStreetMap notes, nearby map data, and public GPS traces. The legend explains supported symbols, lines, and areas.

## Routes and cars

A route may contain from 2 to 25 ordered points. The route panel supports walking, cycling, and driving profiles, point reordering, route reversal, turn-by-turn steps, route saving, and an option to avoid toll roads. For car routes, the active car profile supplies fuel type, tank capacity, and consumption values used by cost and refuelling estimates.

![Planned car route with refuelling estimates](doc/route.png)

Car profiles store both everyday and technical information. A profile can be selected as active, edited, assigned an image, or deleted.

![Active car details on the map](doc/car_map.png)

![Car profile editor](doc/car_edit.png)

## Fuel prices and travel costs

The fuel-price view contains petrol 95, petrol 98, diesel, and LPG prices by country. Data can be refreshed, searched, sorted, converted to another currency, or overridden manually. Travel Manager uses the selected fuel type and the active car's minimum and maximum consumption to calculate a cost range for a route.

![Fuel prices and currency conversion](doc/fuel_costs.png)

Automatic data currently comes from the European Commission Weekly Oil Bulletin, AutoCentrum for Poland, and Frankfurter exchange rates. Availability and update dates depend on those services.

## Public transport

Travel Manager has configured integrations for 35 Polish public transport areas. Operators are grouped under their original Polish city, voivodeship, and company names. You can update cached data, browse lines and stops, inspect timetables and journeys, and open supported routes on the map.

![Public transport operator selection](doc/public_transport_carriers.png)

Some operators additionally provide announcements, platforms, live or recently reported vehicle positions, vehicle details, and route geometry. Capabilities vary by provider; the interface only exposes functions supported by the selected data source.

![Public transport route and selected vehicle](doc/public_transport_map.png)

## First run and settings

English is used for a new configuration, and Home opens after startup by default. The language can be changed from the Home header or under **Settings → Application**.

Settings are divided into:

- **Appearance** — light or dark theme, accent colour, route colours, and separate marker colours for buses, trams, trolleybuses, metro, and trains.
- **Routes** — preferred cost currency, fuel-price and consumption defaults, refuelling markers, and toll-road routing.
- **Public transport** — background vehicle updates and refresh interval.
- **Backup** — JSON import and export for selected data categories.
- **Application** — language, Home startup behaviour, and local-network mode.

## Requirements

- Python 3.10 or newer when running from source.
- Internet access for map tiles, place search, route calculation, fuel and exchange-rate updates, and public transport downloads.
- A WebView backend supported by pywebview:
  - WebView2 or a supported Qt backend on Windows,
  - the native WebKit implementation on macOS,
  - WebKitGTK or a supported Qt backend on Linux.

Linux distributions may require WebKitGTK or Qt packages from the system package manager.

## Installation from source

Clone the repository, enter its directory, and create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running

Use the platform helper:

```bash
./run.sh
```

or on Windows:

```bat
run.bat
```

The application can also be started directly:

```bash
python app.py
```

By default, the local service listens at `http://127.0.0.1:5000` and opens in a desktop window.

### Command-line options

| Option | Windows form | Meaning |
|---|---|---|
| `--ip ADDRESS` | `/ip ADDRESS` | IPv4 address on which the service listens. |
| `--port PORT` | `/port PORT` | TCP port in the `1–65535` range. |
| `--lang {EN,PL}` | `/lang {EN,PL}` | Forces the application language for the current run without changing saved settings. |
| `--no-window` | `/no-window` | Runs the HTTP service without a native window. |
| `--help`, `-h` | `/help`, `/h` | Displays translated command-line help. |

Example:

```bash
python app.py --ip 192.168.1.20 --port 8080 --no-window
```

The same options can be passed through `run.sh` or `run.bat`. In `--no-window` mode, open the printed URL in a browser and stop the service with `Ctrl+C`.

Binding to an address other than localhost makes the application and its locally stored data reachable from other devices on that network. Use this only on a trusted network. The **Move to network** setting can select the active network interface after an application restart; an explicit CLI address takes precedence.

## Local data and privacy

The application persists its state in `settings.json` under the platform configuration directory:

| System | Location |
|---|---|
| Windows | `%APPDATA%\TravelManager\settings.json` |
| macOS | `~/Library/Application Support/TravelManager/settings.json` |
| Linux | `$XDG_CONFIG_HOME/TravelManager/settings.json` or `~/.config/TravelManager/settings.json` |

The file contains user settings, window geometry, appearance, routes, favourites, tags, car profiles, fuel data, and public transport caches. Writes are protected by a lock and replace the file atomically.

Search queries, coordinates, route points, and feature-specific requests are sent to the relevant external services. Public transport and fuel data are cached locally. Imported JSON should come from a trusted source, especially when the service is available over a network.

## Technical overview

### Runtime architecture

```text
app.py
├── CommandLineManager          CLI parsing, validation, and translated messages
├── Service                     local threaded Flask/Werkzeug server
│   ├── controllers/            pages and JSON API endpoints
│   ├── services/               application-level domain services
│   ├── templates/              Jinja views, panels, and dialogs
│   └── assets/                 browser-side JavaScript, CSS, icons, and catalogues
├── SettingsStorage             typed JSON persistence and transfer operations
└── WebViewWindow               native window and JavaScript bridge
```

The browser interface requests view fragments and JSON data from the local Flask service. Controllers validate the boundary payloads and delegate downloading, conversion, storage, and resource mapping to the corresponding classes. The same service can be displayed in pywebview or opened in a regular browser.

### Technology

- Python, Flask, Werkzeug, and Jinja for the local service and server-rendered fragments.
- pywebview for the native desktop window and file-dialog bridge.
- Vanilla JavaScript and CSS for the client interface.
- Leaflet and Lucide distributed with the application under `assets/vendor`.
- OpenStreetMap, Nominatim, Overpass, OSRM-compatible services, and Valhalla for map and routing features.
- GTFS, GTFS Realtime, operator APIs, and provider-specific HTML/JSON sources for public transport.
- European Commission, AutoCentrum, and Frankfurter data for fuel prices and currencies.
- PyInstaller for platform-specific release bundles.

External services retain ownership of their data and may enforce their own availability, usage, and attribution rules.

### Project structure

```text
app.py             Application composition and lifecycle
config.py          Metadata, resource paths, default host, and port
controllers/       Flask page and JSON API controllers
core/              Service runtime, i18n, base API/data classes, and WebView window
services/          Domain services shared by controllers
models/            Typed map, route, transport, settings, and transfer models
storage/           Thread-safe settings persistence
resources/         Stable dictionaries, enums, menu definitions, and source metadata
utils/             Downloaders, converters, CLI, language audit, and runtime helpers
templates/         Jinja index, views, headers, panels, and dialogs
assets/            JavaScript, CSS, languages, icons, images, and vendored libraries
tests/             Unit and regression tests
doc/               Documentation screenshots and supporting files
build.py           PyInstaller build and packaging workflow
```

### Configuration

`config.py` contains `APP_NAME`, `APP_DESCRIPTION`, `APP_VERSION`, application paths, `HOST`, `PORT`, and the service startup timeout. `build_conf.py` derives package metadata and build paths from those values.

Runtime UI settings belong to typed models under `models/settings` and are persisted through `SettingsStorage`; they should not be added as ad-hoc constants to `config.py`.

### Localisation

Translation catalogues are stored in:

- `assets/languages/en_US.json`
- `assets/languages/pl_PL.json`

English is the fallback locale. Each catalogue uses component or resource groups, and every key segment must be a stable English `UPPER_CASE` identifier, for example `PANEL_CAR_DETAILS.FUEL_TYPE`. Both catalogues must contain the same keys and named placeholders.

Use `t('GROUP.KEY')` in Jinja and browser JavaScript, `translate('GROUP.KEY')` in a Flask request, and `LanguageService` or `CommandLineManager` outside a request context. Proper names for Polish public transport regions, cities, and operators intentionally remain in their original form in both locales.

Dynamic translation key patterns are tracked by the reserved-key registry expected at `doc/i18n_reserved_keys.txt`. The language audit reports missing keys, duplicate JSON keys, mismatched placeholders, invalid names, and unreferenced entries:

```bash
python3 utils/languages_manager.py
```

To add a locale, add it to `resources/language_enum.py`, register its catalogue path in `resources/language_definitions.py`, and provide its `SETTINGS_APPLICATION.LANGUAGE_<ENUM_NAME>` label in every catalogue. The backend passes the resulting definitions to the browser and language selectors automatically.

### Tests

Run the complete unit and regression suite with:

```bash
python3 -m unittest discover -s tests
```

The suite also exercises the language audit, so the reserved-key registry must be present and current.

### Building a release

Build for the current operating system with:

```bash
./build.sh
```

or on Windows:

```bat
build.bat
```

The build workflow removes earlier build outputs, installs or updates build dependencies, creates a platform-specific PyInstaller bundle, and packages it under `bin/release`. Each target must be built on its own operating system. Use `cleanup.sh` or `cleanup.bat` to remove Python bytecode caches.

## License

Copyright (C) Kamil Karpiński. Licensed under the [GNU General Public License v3.0](LICENSE).
