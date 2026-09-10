const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const source = (name) => fs.readFileSync(path.join(root, name), 'utf8');

test('public transport downloads are shared and are not aborted on navigation', () => {
    const broker = source('assets/js/components/public_transport_requests.js');
    const view = source('assets/js/views/public_transport.js');
    const panel = source('assets/js/panels/public_transport.js');

    assert.match(broker, /const active = new Map\(\)/);
    assert.match(broker, /active\.get\(requestKey\)/);
    assert.match(broker, /public-transport-background-download/);
    assert.match(broker, /pending-downloads/);
    assert.match(broker, /backgroundProvider/);
    assert.match(broker, /new DOMParser\(\)\.parseFromString/);
    assert.match(broker, /\.public-transport-error p/);
    assert.doesNotMatch(view, /new AbortController\(\)/);
    assert.match(view, /state\.current !== next/);
    assert.match(panel, /identity !== JSON\.stringify/);
    assert.match(panel, /setForeground\(state\.requestKey, false\)/);
});

test('panel uses the dedicated all-lines URL instead of a line timetable URL', () => {
    const panel = source('assets/js/panels/public_transport.js');
    const lineStop = source('templates/public_transport/line_stop.html');
    const styles = source('assets/css/views/public_transport.css');

    assert.match(lineStop, /'stop_lines_url': timetable\.stop_lines_url/);
    assert.match(panel, /state\.metadata\.stop_lines_url \|\| state\.url/);
    assert.match(styles, /\.public-transport-stops__platform-actions \{[\s\S]*display: flex/);
    assert.match(styles, /\.public-transport-stops__platform-actions button \{[\s\S]*width: auto/);
});

test('stop-line cards separate primary actions from direction details', () => {
    const template = source('templates/public_transport/stop_lines.html');
    const styles = source('assets/css/views/public_transport.css');

    assert.match(template, /public-transport-stop-lines__primary/);
    assert.match(template, /public-transport-stop-lines__primary[\s\S]*public-transport-stop-lines__header-actions/);
    assert.match(template, /public-transport-stop-lines__details/);
    assert.match(template, /public-transport-stop-lines__direction/);
    assert.match(template, /PUBLIC_TRANSPORT_VIEW\.DIRECTION/);
    assert.match(template, /public-transport-stop-lines__summary/);
    assert.match(styles, /\.public-transport-stop-lines__primary \{[\s\S]*display: flex/);
    assert.match(styles, /\.public-transport-stop-lines__primary \{[\s\S]*flex-wrap: nowrap/);
    assert.match(styles, /\.public-transport-stop-lines__primary > \.public-transport-line-pill \{[\s\S]*height: 36px/);
    assert.match(styles, /\.public-transport-stop-lines__primary > \.public-transport-stop-lines__header-actions \{[\s\S]*height: 36px/);
    assert.match(styles, /\.public-transport-stop-lines__header-actions > button \{[\s\S]*height: 36px/);
    assert.match(styles, /\.public-transport-stop-lines__primary \.public-transport-line-pill__identity strong,[\s\S]*text-overflow: ellipsis;[\s\S]*white-space: nowrap/);
    assert.match(styles, /\.public-transport-stop-lines__details \{[\s\S]*display: grid/);
});

test('download UI exposes background and cancellation actions', () => {
    const dialog = source('templates/dialogs/download_status.html');
    const dialogScript = source('assets/js/dialogs/download_status.js');
    const view = source('assets/js/views/public_transport.js');
    assert.match(dialog, /data-download-status-background/);
    assert.match(dialog, /data-download-status-cancel/);
    assert.match(dialogScript, /\/cancel/);
    assert.match(view, /data-public-transport-download-background/);
    assert.match(view, /data-public-transport-download-cancel/);
    assert.match(view, /data-public-transport-download-actions hidden/);
    assert.match(view, /progress\.status === 'downloading'[\s\S]*Boolean\(progress\.item\)/);
});

test('rail providers never present timetable updates as GPS positions', () => {
    const providers = source('resources/public_transport/public_transport_providers.py');
    assert.match(providers, /CAPABILITY_SHOW_VEHICLE_POSITIONS: False/);
});

test('carrier list supports selecting only providers that should be updated', () => {
    const header = source('templates/public_transport/headers/carriers.html');
    const carriers = source('templates/public_transport/carriers.html');
    const view = source('assets/js/views/public_transport.js');

    assert.match(header, /data-public-transport-select-providers/);
    assert.match(header, /data-public-transport-select-all hidden/);
    assert.match(header, /data-public-transport-update-selected hidden disabled/);
    assert.match(header, /data-public-transport-cancel-selection hidden/);
    assert.doesNotMatch(header, /data-public-transport-refresh-all/);
    assert.match(carriers, /public-transport-carriers__selection/);
    assert.match(carriers, /data-public-transport-update-source/);
    assert.match(view, /selectedProviders: new Set\(\)/);
    assert.match(view, /providerTiles\(\)\.filter\(\(tile\) => state\.selectedProviders\.has/);
    assert.match(view, /providers\.reduce\(\(sources, tile\)/);
    assert.match(view, /tile\.dataset\.publicTransportUpdateSource/);
});

test('municipal and railway navigation share a mode-aware transport view', () => {
    const navigation = source('assets/js/index.js');
    const menu = source('templates/index/index.html');
    const home = source('templates/views/home.html');
    const carriers = source('templates/public_transport/carriers.html');
    const view = source('assets/js/views/public_transport.js');

    assert.match(menu, /data-public-transport-mode="\{\{ navigation_target \}\}"/);
    assert.match(home, /data-public-transport-mode="\{\{ navigation_target \}\}"/);
    assert.match(carriers, /data-public-transport-mode="\{\{ provider\.mode \}\}"/);
    assert.match(navigation, /publicTransportMode: viewButton\.dataset\.publicTransportMode/);
    assert.match(navigation, /buttonMode === currentPublicTransportMode/);
    assert.match(view, /tile\.dataset\.publicTransportMode === state\.transportMode/);
    assert.match(view, /HEADER\.RAILWAYS/);
    assert.match(view, /function syncCarrierRegions\(\)/);
    assert.match(view, /publicTransportMode !== state\.transportMode/);
});

test('train line tiles show route endpoints in the main view and panel', () => {
    const lines = source('templates/public_transport/lines.html');
    const viewStyles = source('assets/css/views/public_transport.css');
    const panelStyles = source('assets/css/panels/public_transport.css');

    assert.match(lines, /line\.type\.value == 'train' and line\.direction/);
    assert.match(lines, /title="\{\{ line\.direction \}\}"/);
    assert.match(lines, /public-transport-lines__direction/);
    assert.match(viewStyles, /\.public-transport-lines__direction \{/);
    assert.match(panelStyles, /\.public-transport-panel \.public-transport-lines__tile:has\(\.public-transport-lines__direction\)/);
});

test('public transport panel switches between city and railway providers', () => {
    const template = source('templates/panels/public_transport.html');
    const lines = source('templates/panels/public_transport/lines.html');
    const panel = source('assets/js/panels/public_transport.js');
    const dropdown = source('assets/js/components/public_transport_provider_dropdown.js');

    assert.match(template, /data-public-transport-panel-mode="city"/);
    assert.match(template, /data-public-transport-panel-mode="rail"/);
    assert.match(lines, /data-mode="\{\{ provider\.mode \}\}"/);
    assert.match(panel, /const applyTransportMode = \(mode, selectFirst = false\)/);
    assert.match(panel, /providerSelect\.dispatchEvent\(new Event\('change'/);
    assert.match(dropdown, /setMode: \(mode\) =>/);
    assert.match(dropdown, /heading\.hidden = !hasVisibleOption/);
    assert.match(panel, /providersByMode: \{ city: '', rail: '' \}/);
    assert.match(panel, /state\.providersByMode\[state\.transportMode\]/);
    assert.match(panel, /mode: state\.transportMode/);
    assert.match(panel, /data\?\.selected_public_transport_mode|data\?\.mode === 'rail'/);
});

test('batch updates use the shared request broker when moved to background', () => {
    const dialogScript = source('assets/js/dialogs/download_status.js');
    const view = source('assets/js/views/public_transport.js');
    const panel = source('assets/js/panels/public_transport.js');
    const navigation = source('assets/js/index.js');

    assert.match(dialogScript, /travel-manager:public-transport-download-background/);
    assert.match(dialogScript, /const reopen = \(source = ''\) =>/);
    assert.match(dialogScript, /isRunning: \(\) => running/);
    assert.match(view, /travelManagerPublicTransportRequests\.request/);
    assert.match(view, /setForeground\(task\.key, !background\)/);
    assert.match(view, /travel-manager:public-transport-download-cancel/);
    assert.match(view, /leavePublicTransport\(\)/);
    assert.match(panel, /travelManagerDownloadStatus\?\.reopen\('panel'\)/);
    assert.match(panel, /event\.detail\?\.origin === 'panel'/);
    assert.match(navigation, /const leavePublicTransport = \(\) => showView/);
});

test('opening the carrier list resets its scroll position', () => {
    const view = source('assets/js/views/public_transport.js');

    assert.match(view, /const showCarriers = \(\) =>[\s\S]*content\.scrollTo\(\{ top: 0, left: 0 \}\)/);
    assert.match(view, /const showCarriers = \(\) =>[\s\S]*content\.scrollTo\(\{ top: 0, left: 0 \}\);\s*view\.scrollTop = 0;/);
    assert.match(view, /appContent\?\.scrollTo\(\{ top: 0, left: 0 \}\)/);
});

test('only the background download glyph rotates, not its framed icon box', () => {
    const broker = source('assets/js/components/public_transport_requests.js');
    const styles = source('assets/css/views/public_transport.css');

    assert.match(broker, /public-transport-background-download__icon/);
    assert.match(styles, /\.public-transport-background-download__icon svg[\s\S]*animation: download-status-spin/);
    assert.doesNotMatch(styles, /\.public-transport-background-download svg\s*\{[\s\S]*animation: download-status-spin/);
});

test('line tiles derive a safe shared width from the longest train name', () => {
    const sizing = source('assets/js/components/public_transport_line_tiles.js');
    const viewStyles = source('assets/css/views/public_transport.css');
    const panelStyles = source('assets/css/panels/public_transport.css');
    const index = source('templates/index/index.html');
    const lines = source('templates/public_transport/lines.html');
    const stops = source('templates/public_transport/stops.html');
    const accent = source('assets/css/common_accent.css');

    assert.match(index, /public_transport_line_tiles\.js/);
    assert.match(sizing, /querySelectorAll\('\.public-transport-lines__number'\)/);
    assert.match(sizing, /Math\.max\(minimum, longest \+ 22\)/);
    assert.match(viewStyles, /--public-transport-line-tile-min-width: 92px/);
    assert.match(viewStyles, /minmax\(min\(100%, var\(--public-transport-line-tile-width/);
    assert.match(viewStyles, /overflow-wrap: anywhere/);
    assert.match(panelStyles, /--public-transport-line-tile-min-width: 72px/);
    assert.match(lines, /public-transport-lines__train-number/);
    assert.match(lines, /public-transport-lines__train-name/);
    assert.match(stops, /public-transport-line-pill__number/);
    assert.match(stops, /public-transport-line-pill__name/);
    assert.match(sizing, /--public-transport-stop-line-width/);
    assert.doesNotMatch(accent, /\.public-transport-stops__item,[\s\S]{0,100}\):is\(:hover/);
});

test('line lists expose four client-side natural sorting modes', () => {
    const sorting = source('assets/js/components/public_transport_line_sort.js');
    const mainHeader = source('templates/public_transport/headers/lines.html');
    const panel = source('templates/panels/public_transport/lines.html');
    const lines = source('templates/public_transport/lines.html');

    assert.match(sorting, /numeric: true/);
    assert.match(sorting, /'name-asc'/);
    assert.match(sorting, /'name-desc'/);
    assert.match(sorting, /'number-asc'/);
    assert.match(sorting, /'number-desc'/);
    assert.match(mainHeader, /data-public-transport-line-sort/);
    assert.match(panel, /data-public-transport-panel-line-sort/);
    assert.match(lines, /data-line-number=/);
    assert.match(lines, /data-line-name="\{\{ line\.sort_name \}\}"/);
    assert.match(sorting, /field === 'name' && Boolean\(leftValue\) !== Boolean\(rightValue\)/);
    assert.match(sorting, /return leftValue \? -1 : 1/);
});

test('settings containers remain transparent without cards or shadows', () => {
    const styles = source('assets/css/views/settings.css');
    assert.match(styles, /\.settings-view__body \{\s*background: var\(--surface-muted\);/);
    assert.match(styles, /\.appearance-settings,[\s\S]*\.settings-view__group-header,[\s\S]*\.settings-view__group \{[\s\S]*border: 0;[\s\S]*background: transparent;[\s\S]*box-shadow: none;/);
    for (const theme of ['assets/css/common_light.css', 'assets/css/common_dark.css']) {
        assert.match(source(theme), /\[class\$="__group"\]:not\(\.settings-view__group\)/);
        assert.match(source(theme), /\[class\$="-panel"\]:not\(\.settings-view__tab-panel\)/);
    }
});
