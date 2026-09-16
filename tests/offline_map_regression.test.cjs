const test = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');

const source = (path) => readFileSync(path, 'utf8');

test('a missing vector tile is treated as an empty tile by the local renderer', () => {
    const vectorGrid = source(
        'assets/vendor/leaflet-vectorgrid/Leaflet.VectorGrid.bundled.min.js'
    );

    // The backend deliberately returns 204 for a coordinate without data. The
    // vendored renderer must resolve every non-successful/empty response to an
    // empty layer collection instead of rejecting the whole map redraw.
    assert.match(
        vectorGrid,
        /t\.ok\?t\.blob\(\)\.then\([\s\S]*?:\{layers:\[\]\}/
    );
});

test('offline base maps do not replace existing online maps or overlays', () => {
    const map = source('assets/js/views/map.js');

    for (const address of [
        'tile.openstreetmap.org',
        'tile-cyclosm.openstreetmap.fr',
        'tile.openstreetmap.fr/hot',
        'gps-tile.openstreetmap.org/lines'
    ]) {
        assert.match(map, new RegExp(address.replaceAll('.', '\\.')));
    }
    assert.match(map, /window\.travelManagerLayerRenderer\.createCollection/);
    assert.match(map, /const routePointsLayer = L\.layerGroup\(\)\.addTo\(map\)/);
    assert.match(map, /let publicTransportRouteLayer = null/);
    assert.match(map, /let publicTransportVehicleLayer = null/);
    assert.match(map, /let publicTransportStopLayer = null/);
});

test('routing and the layer editor retain their map integration hooks', () => {
    const map = source('assets/js/views/map.js');
    const editor = source('assets/js/panels/layer.js');

    assert.match(map, /window\.travelManagerRouteDetailsPanel/);
    assert.match(map, /routeDetailsPanel\.consumeElement/);
    assert.match(map, /new URL\('\/api\/map\/reverse'/);
    assert.match(editor, /window\.travelManagerMap/);
    assert.match(editor, /travelManagerLayerRenderer/);
    assert.match(editor, /travelManagerCustomLayers/);
});

test('city and railway GTFS continue to use the shared provider API', () => {
    const view = source('assets/js/views/public_transport.js');
    const panel = source('assets/js/panels/public_transport.js');

    assert.match(view, /transportMode: 'city'/);
    assert.match(
        view,
        /event\.detail\?\.publicTransportMode === 'rail' \? 'rail' : 'city'/
    );
    assert.match(panel, /transportMode: 'city'/);
    assert.match(view, /`\/api\/public-transport\/\$\{provider\}\/\$\{screen\}`/);
    assert.match(panel, /`\/api\/public-transport\/\$\{state\.provider\}\/\$\{screen\}`/);
    assert.match(view, /applyTransportMode\(nextMode\)/);
    assert.match(panel, /const rememberedMode = data\?\.mode === 'rail' \? 'rail' : 'city'/);
});
