const test = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');

const template = readFileSync('templates/views/settings/memory.html', 'utf8');
const settings = readFileSync('assets/js/views/settings.js', 'utf8');
const regionDialog = readFileSync('assets/js/dialogs/offline_map_region.js', 'utf8');
const map = readFileSync('assets/js/views/map.js', 'utf8');

test('downloaded maps use a sortable tabular memory list', () => {
    assert.match(template, /data-settings-offline-maps/);
    assert.match(settings, /Intl\.Collator[\s\S]*data\.maps/);
    assert.match(settings, /COLUMN_REGION/);
    assert.match(settings, /source_updated_at/);
    assert.match(settings, /formatBytes\(item\.size\)/);
});

test('map and memory tabs expose their dedicated actions', () => {
    assert.doesNotMatch(settings, /showOfflineMap\(item\.id\)/);
    assert.match(settings, /offline-map-update-requested/);
    assert.match(settings, /data-settings-map-offline-maps/);
    assert.match(settings, /'ellipsis'/);
    assert.doesNotMatch(settings, /CONTINUE_GENERATION/);
    assert.doesNotMatch(settings, /FORCE_SMALLER_TILES/);
    assert.match(settings, /MANAGE_LEVELS/);
    assert.match(settings, /offline-map-levels-requested/);
    assert.match(settings, /export_offline_map/);
    assert.match(regionDialog, /offline-map-update-requested/);
    assert.match(regionDialog, /\/update`/);
    assert.match(settings, /travelManagerDialogs\?\.yesNo/);
    assert.match(settings, /fetch\(`\/api\/offline-maps\/\$\{encodeURIComponent\(item\.id\)\}`/);
});

test('map deletion refreshes both storage and base-layer registries', () => {
    assert.match(settings, /travelManagerMap\?\.refreshOfflineMaps/);
    assert.match(settings, /Promise\.all\(\[loadOfflineMaps\(\), loadStorageUsage\(\)\]\)/);
    assert.match(map, /if \(baseLayers\[previousActiveLayer\]\) setBaseLayer\([\s\S]*previousActiveLayer,[\s\S]*automatic:/);
});
