const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const {readFileSync} = require('node:fs');

const window = {};
vm.runInNewContext(readFileSync('assets/js/layers/offline_map_selection.js', 'utf8'), {window});
const selection = window.travelManagerOfflineMapSelection;
const rectangle = (west, south, east, north) => ({
    type: 'Polygon',
    coordinates: [[
        [west, south], [east, south], [east, north],
        [west, north], [west, south]
    ]]
});

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

test('adjacent packages intersecting one viewport are selected together', () => {
    const result = selection.forViewport([
        {id: 'west', metadata: {
            bounds: [18, 49, 20, 51], coverage: rectangle(18, 49, 19, 51)
        }},
        {id: 'east', metadata: {
            bounds: [18.5, 49, 20.5, 51], coverage: rectangle(19, 49, 20.5, 51)
        }}
    ], [18.5, 49.5, 19.5, 50.5]);
    assert.deepEqual(Array.from(result, (item) => item.id), ['east', 'west']);
    assert.equal(selection.coversViewport(result, [18.5, 49.5, 19.5, 50.5]), true);
});

test('one parent package is preferred when it contains the whole viewport', () => {
    const result = selection.forViewport([
        {id: 'country', metadata: {bounds: [14, 49, 24, 55]}},
        {id: 'region', metadata: {bounds: [18, 49.5, 20, 51]}}
    ], [17, 49.5, 21, 51.5]);
    assert.deepEqual(Array.from(result, (item) => item.id), ['country']);
});

test('overlapping legacy bounds keep sibling regions side by side', () => {
    const result = selection.forViewport([
        {id: 'first', metadata: {bounds: [18, 49, 20, 51]}},
        {id: 'second', metadata: {bounds: [18.5, 49, 20.5, 51]}}
    ], [19, 49.5, 19.5, 50.5]);
    assert.deepEqual(Array.from(result, (item) => item.id), ['first', 'second']);
});
