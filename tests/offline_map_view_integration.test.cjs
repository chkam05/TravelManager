const test = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');

const mapSource = readFileSync('assets/js/views/map.js', 'utf8');
const panelSource = readFileSync('assets/js/panels/layer_details.js', 'utf8');
const panelTemplate = readFileSync('templates/panels/layer_details.html', 'utf8');
const mapTemplate = readFileSync('templates/views/map.html', 'utf8');

test('installed offline maps are appended to the base-layer registry', () => {
    assert.match(mapSource, /getJson\('\/api\/offline-maps'\)/);
    assert.match(mapSource, /travelManagerOfflineMapLayer\.create\(metadata\)/);
    assert.match(mapSource, /const id = `offline_\$\{metadata\.id\}`/);
    assert.match(mapSource, /travel-manager:base-layers-changed/);
});

test('the layer panel renders dynamic offline base-layer radios', () => {
    assert.match(panelTemplate, /data-offline-base-layers/);
    assert.match(panelSource, /input\.name = 'map_base_layer'/);
    assert.match(panelSource, /input\.dataset\.baseLayer = layer\.id/);
    assert.match(panelSource, /travel-manager:base-layer-changed/);
});

test('offline coverage is checked after layer and viewport changes', () => {
    assert.match(mapSource, /packageBounds\.contains\(map\.getBounds\(\)\)/);
    assert.match(mapSource, /MAP_VIEW\.OFFLINE_OUTSIDE_COVERAGE/);
    assert.match(mapSource, /map\.on\('moveend zoomend',[\s\S]*updateOfflineCoverageWarning\(\)/);
});

test('only the registered standard tile layer is added to the map', () => {
    const matches = mapSource.match(/L\.tileLayer\('https:\/\/tile\.openstreetmap\.org\/\{z\}\/\{x\}\/\{y\}\.png'/g) || [];
    assert.equal(matches.length, 1);
});

test('offline map testing can be toggled without loading an online base layer', () => {
    assert.match(mapTemplate, /data-map-tool="offline-test"/);
    assert.match(mapSource, /offlineTestMode && !baseLayers\[nextLayer\]\.offline/);
    assert.match(mapSource, /offlineTestMode = !offlineTestMode/);
    assert.match(mapSource, /setBaseLayer\(selected\?\.id \|\| layerState\.map_base_layer/);
    assert.doesNotMatch(mapSource, /\n    setBaseLayer\('standard'\);\n\n    Promise\.all/);
});

test('installed map sorting converts app locale to a valid browser locale', () => {
    assert.throws(() => new Intl.Collator('pl_PL'), RangeError);
    assert.doesNotThrow(() => new Intl.Collator('pl_PL'.replace('_', '-')));
    assert.match(mapSource, /TRAVEL_MANAGER_I18N\?\.locale\?\.replace\('_', '-'\)/);
});
