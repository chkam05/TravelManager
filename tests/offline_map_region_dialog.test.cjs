const test = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');

const source = readFileSync('assets/js/dialogs/offline_map_region.js', 'utf8');
const template = readFileSync('templates/dialogs/offline_map_region.html', 'utf8');

test('region dialog exposes hierarchical selectors and map metadata', () => {
    for (const hook of ['continent', 'country', 'region', 'max-zoom', 'summary']) {
        assert.match(template, new RegExp(`data-offline-map-${hook}`));
    }
    assert.match(source, /\/api\/offline-maps\/catalog/);
    assert.match(source, /source_updated_at/);
    assert.match(source, /estimated_map_size/);
});

test('preflight prevents duplicate and oversized downloads', () => {
    assert.match(source, /data\.installed/);
    assert.match(source, /data\.active_job/);
    assert.match(source, /!data\.enough_space/);
    assert.match(source, /submit\.disabled = Boolean\(problem\)/);
});

test('submitting starts one durable offline map job', () => {
    assert.match(source, /fetch\('\/api\/offline-maps\/jobs'/);
    assert.match(source, /region_id: regionSelect\.value/);
    assert.match(source, /travel-manager:offline-map-job-started/);
});

test('map sizes at least one gibibyte use two-decimal GB formatting', () => {
    assert.match(source, /bytes >= 1024 \*\* 3/);
    assert.match(source, /minimumFractionDigits: 2, maximumFractionDigits: 2/);
});
