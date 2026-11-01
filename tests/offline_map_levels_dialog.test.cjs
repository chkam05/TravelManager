const test = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');

const source = readFileSync('assets/js/dialogs/offline_map_levels.js', 'utf8');
const template = readFileSync('templates/dialogs/offline_map_levels.html', 'utf8');

test('level management overlay exposes x10-x19 multi-selection', () => {
    assert.match(template, /data-offline-map-levels-list/);
    assert.match(template, /data-offline-map-levels-generate/);
    assert.match(template, /data-offline-map-levels-delete/);
    assert.match(source, /range|levels\.map/);
    assert.match(source, /zoom === 15/);
    assert.match(source, /input:checked/);
});

test('generation skips complete levels and x10 cannot be deleted', () => {
    assert.match(source, /method: 'POST'/);
    assert.match(source, /method: 'DELETE'/);
    assert.match(source, /zoom !== 10/);
    assert.match(source, /remove\.disabled = !values\.some/);
});
