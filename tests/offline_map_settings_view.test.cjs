const test = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const vm = require('node:vm');

const template = readFileSync('templates/views/settings/map.html', 'utf8');
const settingsSource = readFileSync('assets/js/views/settings.js', 'utf8');
const mapSource = readFileSync('assets/js/views/map.js', 'utf8');
const dialogSource = readFileSync('assets/js/dialogs/offline_map_region.js', 'utf8');
const lucide = require('../assets/vendor/lucide/lucide.min.js');

test('map settings expose all three offline source modes', () => {
    assert.match(template, /data-settings-group="offline-maps"/);
    for (const mode of ['prefer_offline', 'offline_when_disconnected', 'online_only']) {
        assert.match(settingsSource, new RegExp(`value: '${mode}'`));
    }
});

test('offline source changes are applied to the live map', () => {
    assert.match(settingsSource, /travel-manager:ui-settings-changed/);
    assert.match(mapSource, /event\.detail\?\.offline_map_mode/);
});

test('download action is a stable hook for the region dialog', () => {
    assert.match(template, /data-offline-map-download/);
    assert.match(dialogSource, /event\.target\.closest\('\[data-offline-map-download\]'\)/);
    assert.match(dialogSource, /if \(event\.target\.closest\('\[data-offline-map-download\]'\)\) open\(\)/);
    assert.match(template, /data-lucide="map"/);
    assert.ok(lucide.icons.Map);
});

test('clicking download opens the region dialog even if settings initialization fails', () => {
    const listeners = new Map();
    const attributes = new Map([['aria-hidden', 'true']]);
    const classes = new Set();
    const node = () => ({
        value: '', disabled: false, textContent: '',
        replaceChildren() {}, append() {}, addEventListener() {},
        classList: {add() {}, remove() {}, toggle() {}}
    });
    const controls = new Map([
        ...['continent', 'country', 'region', 'max-zoom', 'summary'].map(
            (name) => [`[data-offline-map-${name}]`, node()]
        ),
        ['[data-offline-map-region-status]', node()],
        ['[data-offline-map-region-submit]', node()]
    ]);
    const dialog = {
        querySelector: (selector) => controls.get(selector),
        querySelectorAll: () => [node()],
        addEventListener() {},
        setAttribute: (name, value) => attributes.set(name, value),
        getAttribute: (name) => attributes.get(name)
    };
    const layer = {
        classList: {
            add: (name) => classes.add(name),
            remove: (name) => classes.delete(name)
        },
        setAttribute: (name, value) => attributes.set(`layer:${name}`, value),
        addEventListener() {}
    };
    const document = {
        addEventListener: (name, handler) => listeners.set(name, handler),
        querySelector: (selector) => selector === '#dialog-layer' ? layer
            : selector === '#offline-map-region' ? dialog : null,
        createElement: () => node()
    };
    const window = {
        i18n: {locale: 'pl_PL', t: (key) => key},
        TRAVEL_MANAGER_I18N: {locale: 'pl_PL'}
    };
    vm.runInNewContext(dialogSource, {document, window, Intl, Map, Date, Number, fetch: () => new Promise(() => {})});
    listeners.get('travel-manager:views-ready')();
    listeners.get('click')({target: {closest: (selector) => selector === '[data-offline-map-download]' ? {} : null}});

    assert.equal(attributes.get('aria-hidden'), 'false');
    assert.equal(attributes.get('layer:aria-hidden'), 'false');
    assert.ok(classes.has('dialog-layer--open'));
});
