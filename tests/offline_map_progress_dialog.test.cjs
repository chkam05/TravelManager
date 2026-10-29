const test = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');

const source = readFileSync('assets/js/dialogs/offline_map_progress.js', 'utf8');
const template = readFileSync('templates/dialogs/offline_map_progress.html', 'utf8');
const css = readFileSync('assets/css/dialogs/offline_map_progress.css', 'utf8');

test('offline map progress covers every durable pipeline stage', () => {
    for (const stage of ['preparing', 'downloading', 'analysing', 'building_tiles', 'optimising', 'installing', 'completed', 'failed', 'cancelled']) {
        assert.match(source, new RegExp(`${stage}:`));
    }
    assert.match(template, /data-offline-map-progress-bar/);
    assert.match(template, /data-offline-map-progress-steps/);
    for (const label of ['STEP_DOWNLOADING', 'STEP_ANALYSING', 'STEP_BUILDING_TILES', 'STEP_OPTIMISING', 'STEP_FINALISING']) {
        assert.match(source, new RegExp(label));
    }
    assert.match(source, /'✔'/);
    assert.match(source, /'▶'/);
});

test('progress can continue in background and be cancelled', () => {
    assert.match(template, /data-offline-map-progress-background/);
    assert.match(template, /data-offline-map-progress-cancel/);
    assert.match(source, /\/cancel`, \{method: 'POST'\}/);
    assert.match(source, /travel-manager:offline-map-job-background/);
    assert.match(source, /job\.cancel_requested === true/);
    assert.match(source, /CANCELLING_HEADING/);
    assert.match(source, /OFFLINE_MAP_PROGRESS\.CANCELLING/);
});

test('a failed map job can be resumed from the progress dialog', () => {
    assert.match(template, /data-offline-map-progress-retry/);
    assert.match(source, /retryButton\.hidden = !\['failed', 'cancelled'\]/);
    assert.match(source, /\/resume`/);
    assert.match(source, /show\(data\.job, false\)/);
});

test('active jobs are restored whenever settings is opened', () => {
    assert.match(source, /fetch\('\/api\/offline-maps\/jobs'/);
    assert.match(source, /event\.detail\?\.view === 'settings'/);
    assert.match(source, /activeStatuses\.has\(item\.status\)/);
});

test('a failed job can be recovered after restart without reopening a dismissed error', () => {
    assert.match(source, /const failed = jobs\.find\(/);
    assert.match(source, /dismissedFailures\.has\(item\.id\)/);
    assert.match(source, /dismissedFailures\.add\(job\.id\)/);
});

test('a completed map hides older failed attempts for the same map', () => {
    assert.match(source, /const completedMaps = new Set\(\)/);
    assert.match(source, /completedMaps\.add\(item\.map_id\)/);
    assert.match(source, /!completedMaps\.has\(item\.map_id\)/);
});

test('unknown totals use a continuous full-width indicator and known totals show percentage', () => {
    assert.match(template, /data-offline-map-progress-indeterminate/);
    assert.match(source, /bar\.hidden = !hasTotal/);
    assert.match(source, /indeterminate\.hidden = hasTotal/);
    assert.match(source, /ASSIGNING_TILES/);
    assert.match(source, /ENCODING_TILES/);
    assert.match(css, /offline-map-progress-travel/);
    assert.match(css, /translateX\(400%\)/);
    assert.match(css, /rotate\(360deg\)/);
});
