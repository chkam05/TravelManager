const test = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');

const requests = readFileSync('assets/js/components/public_transport_requests.js', 'utf8');
const progress = readFileSync('assets/js/dialogs/offline_map_progress.js', 'utf8');
const styles = readFileSync('assets/css/views/public_transport.css', 'utf8');

test('offline maps have a separate clickable background indicator', () => {
    assert.match(requests, /createElement\('button'\)/);
    assert.match(requests, /public-transport-background-download--offline/);
    assert.match(requests, /travelManagerOfflineMapProgress\?\.show\(offlineJob, false\)/);
});

test('background label distinguishes downloading from local generation', () => {
    assert.match(requests, /BACKGROUND_DOWNLOADING/);
    assert.match(requests, /BACKGROUND_GENERATING/);
    assert.match(requests, /\['preparing', 'downloading'\]\.includes\(offlineJob\.stage\)/);
});

test('on-demand tile generation reuses the offline background indicator', () => {
    assert.match(requests, /const offlineTileTasks = new Map\(\)/);
    assert.match(requests, /travel-manager:offline-map-tiles-started/);
    assert.match(requests, /travel-manager:offline-map-tiles-progress/);
    assert.match(requests, /travel-manager:offline-map-tiles-finished/);
    assert.match(requests, /BACKGROUND_TILE_GENERATION_PERCENT/);
    assert.match(requests, /BACKGROUND_NEIGHBOUR_TILES_PERCENT/);
    assert.match(requests, /item\?\.kind === 'neighbours'/);
    assert.match(requests, /tileTotals\.current \/ tileTotals\.total/);
});

test('restored map jobs wait for translations and the progress dialog', () => {
    assert.match(requests, /addEventListener\('travel-manager:views-ready', async \(\) => \{/);
    assert.match(requests, /await window\.i18n\.ready;[\s\S]*fetch\('\/api\/offline-maps\/jobs'/);
    assert.match(requests, /travelManagerOfflineMapProgress\?\.show\(recovered, true\)/);
});

test('GTFS and offline indicators stack without sharing state', () => {
    assert.match(requests, /const backgroundCount/);
    assert.match(requests, /let offlineJob = null/);
    assert.match(styles, /public-transport-background-download--stacked/);
});

test('only the glyph inside the framed icon rotates', () => {
    assert.match(styles, /public-transport-background-download__icon svg[\s\S]*animation:/);
    assert.doesNotMatch(styles, /public-transport-background-download__icon\s*\{[^}]*animation:/);
    assert.match(progress, /travel-manager:offline-map-job-updated/);
});
