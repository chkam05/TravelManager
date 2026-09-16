const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const {readFileSync} = require('node:fs');

const window = {};
vm.runInNewContext(readFileSync('assets/js/layers/offline_map_selection.js', 'utf8'), {window});
const selection = window.travelManagerOfflineMapSelection;

test('coverage includes boundary points and rejects positions outside a package', () => {
    const map = {bounds: [14, 49, 24, 55]};
    assert.equal(selection.contains(map, {lat: 49, lng: 14}), true);
    assert.equal(selection.contains(map, {lat: 56, lng: 20}), false);
});

test('the smallest map containing the current centre wins', () => {
    const result = selection.smallestContaining([
        {id: 'country', metadata: {bounds: [14, 49, 24, 55]}},
        {id: 'region', metadata: {bounds: [18, 49.5, 20, 51]}}
    ], {lat: 50, lng: 19});
    assert.equal(result.id, 'region');
});

test('no package is selected outside all installed bounds', () => {
    assert.equal(selection.smallestContaining([
        {id: 'region', metadata: {bounds: [18, 49.5, 20, 51]}}
    ], {lat: 40, lng: 10}), null);
});
