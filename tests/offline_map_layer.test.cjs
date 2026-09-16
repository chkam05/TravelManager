const test = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const vm = require('node:vm');

const source = readFileSync('assets/js/layers/offline_map.js', 'utf8');
const stylesSource = readFileSync('assets/js/layers/offline_map_styles.js', 'utf8');

function harness() {
    const calls = [];
    const window = {
        L: {
            canvas: {tile: {renderer: true}},
            latLngBounds: (bounds) => ({bounds}),
            vectorGrid: {
                protobuf: (url, options) => {
                    const layer = {url, options};
                    calls.push(layer);
                    return layer;
                }
            }
        }
    };
    const context = {window, URL, TypeError, Error};
    vm.runInNewContext(stylesSource, context);
    vm.runInNewContext(source, context);
    return {api: window.travelManagerOfflineMapLayer, calls, window};
}

const metadata = {
    id: 'poland-a1b2c3',
    name: 'Polska',
    bounds: [14.0, 49.0, 24.2, 54.9],
    min_zoom: 3,
    max_zoom: 14
};

test('offline map factory targets only the local vector tile endpoint', () => {
    const {api, calls} = harness();
    const layer = api.create(metadata);

    assert.equal(calls.length, 1);
    assert.equal(
        layer.url,
        '/api/offline-maps/poland-a1b2c3/tiles/{z}/{x}/{y}.pbf'
    );
    assert.equal(layer.options.minNativeZoom, 3);
    assert.equal(layer.options.maxNativeZoom, 14);
    assert.equal(layer.options.maxZoom, 14);
    assert.equal(
        JSON.stringify(layer.options.bounds.bounds),
        JSON.stringify([[49, 14], [54.9, 24.2]])
    );
    assert.match(layer.options.attribution, /OpenStreetMap/);
    assert.equal(Object.hasOwn(layer.options, 'pane'), false);
    assert.equal(layer.travelManagerOfflineMap.name, 'Polska');
});

test('factory forwards explicit styles and keeps interaction opt-in', () => {
    const {api} = harness();
    const styles = {roads: {color: 'red'}};
    const layer = api.create(metadata, {styles, interactive: true, pane: 'tilePane'});

    assert.equal(layer.options.vectorTileLayerStyles, styles);
    assert.equal(layer.options.interactive, true);
    assert.equal(layer.options.pane, 'tilePane');
    assert.equal(layer.options.getFeatureId, undefined);
});

test('invalid ids, zooms and bounds are rejected before constructing a URL', () => {
    const {api, calls} = harness();
    const invalid = [
        {...metadata, id: '../secret'},
        {...metadata, min_zoom: 15, max_zoom: 14},
        {...metadata, bounds: [20, 50, 10, 51]},
        {...metadata, bounds: [14, 49, Number.NaN, 55]}
    ];

    invalid.forEach((item) => assert.throws(() => api.create(item), TypeError));
    assert.equal(calls.length, 0);
});

test('support detection fails cleanly when the vendored plugin is absent', () => {
    const {api, window} = harness();
    assert.equal(api.isSupported(), true);
    delete window.L.vectorGrid;
    assert.equal(api.isSupported(), false);
    assert.throws(() => api.create(metadata), /unavailable/);
});

test('standard offline style covers every generated layer without theme switching', () => {
    const {api, window} = harness();
    const first = window.travelManagerOfflineMapStyles.standard();
    const second = window.travelManagerOfflineMapStyles.standard();
    const expected = [
        'water', 'landuse', 'buildings', 'roads', 'railways',
        'boundaries', 'places', 'pois'
    ];

    assert.deepEqual(Object.keys(first).sort(), expected.sort());
    assert.notEqual(first, second);
    assert.equal(first.water.fillColor, '#aad3df');
    assert.equal(first.roads({highway: 'motorway'}, 8).color, '#e8928f');
    assert.equal(first.roads({highway: 'residential'}, 15).color, '#ffffff');
    assert.equal(api.create(metadata).options.vectorTileLayerStyles.water.fillColor, '#aad3df');
    assert.equal(first.places.length, 0);
    assert.equal(first.pois.length, 0);
    assert.doesNotMatch(stylesSource, /prefers-color-scheme|data-theme|dark/i);
});
