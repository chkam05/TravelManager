(() => {
    const active = new Map();
    const foreground = new Set();
    let bubble = null;
    let offlineBubble = null;
    let offlineJob = null;
    const offlineTileTasks = new Map();

    const ensureBubble = () => {
        if (bubble) return bubble;
        bubble = document.createElement('div');
        bubble.className = 'public-transport-background-download';
        bubble.hidden = true;
        bubble.setAttribute('role', 'status');
        bubble.innerHTML = '<span class="public-transport-background-download__icon"><i data-lucide="loader-circle" aria-hidden="true"></i></span><span data-background-download-text></span>';
        document.body.append(bubble);
        return bubble;
    };
    const ensureOfflineBubble = () => {
        if (offlineBubble) return offlineBubble;
        offlineBubble = document.createElement('button');
        offlineBubble.type = 'button';
        offlineBubble.className = 'public-transport-background-download public-transport-background-download--offline';
        offlineBubble.hidden = true;
        offlineBubble.innerHTML = '<span class="public-transport-background-download__icon"><i data-lucide="loader-circle" aria-hidden="true"></i></span><span data-background-download-text></span>';
        offlineBubble.addEventListener('click', () => {
            if (offlineJob) window.travelManagerOfflineMapProgress?.show(offlineJob, false);
        });
        document.body.append(offlineBubble);
        return offlineBubble;
    };
    const render = () => {
        const element = ensureBubble();
        const backgroundCount = [...active.keys()].filter((key) => !foreground.has(key)).length;
        element.hidden = backgroundCount === 0;
        element.querySelector('[data-background-download-text]').textContent = window.i18n?.t(
            'PUBLIC_TRANSPORT_VIEW.BACKGROUND_DOWNLOAD', { count: backgroundCount }
        ) || 'Downloading public transport data in the background…';
        ensureOfflineBubble().classList.toggle(
            'public-transport-background-download--stacked', backgroundCount > 0
        );
        if (!element.hidden) window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };
    const renderOffline = () => {
        const element = ensureOfflineBubble();
        const activeJob = offlineJob && ['queued', 'running'].includes(offlineJob.status);
        const generatingTiles = offlineTileTasks.size > 0;
        element.hidden = !activeJob && !generatingTiles;
        if (element.hidden) return;
        const cancelling = offlineJob?.cancel_requested === true;
        const downloading = activeJob && ['preparing', 'downloading'].includes(offlineJob.stage);
        const tileTasks = [...offlineTileTasks.values()];
        const preparingNeighbours = tileTasks.some(
            (item) => item?.kind === 'neighbours'
        );
        const progressTasks = preparingNeighbours
            ? tileTasks.filter((item) => item?.kind === 'neighbours')
            : tileTasks;
        const tileTotals = progressTasks.reduce((result, item) => ({
            current: result.current + Math.max(0, Number(item.current) || 0),
            total: result.total + Math.max(0, Number(item.total) || 0)
        }), {current: 0, total: 0});
        const tilePercent = tileTotals.total > 0
            ? Math.min(100, Math.floor(100 * tileTotals.current / tileTotals.total))
            : 0;
        element.querySelector('[data-background-download-text]').textContent = window.i18n?.t(
            generatingTiles && !activeJob
                ? preparingNeighbours
                    ? 'OFFLINE_MAP_PROGRESS.BACKGROUND_NEIGHBOUR_TILES_PERCENT'
                    : 'OFFLINE_MAP_PROGRESS.BACKGROUND_TILE_GENERATION_PERCENT'
                : cancelling
                ? 'OFFLINE_MAP_PROGRESS.BACKGROUND_CANCELLING'
                : downloading
                ? 'OFFLINE_MAP_PROGRESS.BACKGROUND_DOWNLOADING'
                : 'OFFLINE_MAP_PROGRESS.BACKGROUND_GENERATING'
        , {percent: tilePercent});
        element.setAttribute('aria-label', element.querySelector('[data-background-download-text]').textContent);
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };
    const key = ({ provider, screen, url = '', refresh = false }) =>
        JSON.stringify([provider, screen, url, Boolean(refresh)]);
    const request = (details) => {
        const requestKey = key(details);
        let promise = active.get(requestKey);
        if (!promise) {
            const params = new URLSearchParams();
            if (details.url) params.set('url', details.url);
            if (details.refresh) params.set('refresh', '1');
            const endpoint = `/api/public-transport/${encodeURIComponent(details.provider)}/${details.screen}`;
            promise = fetch(`${endpoint}${params.size ? `?${params}` : ''}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            }).then(async (response) => {
                const text = await response.text();
                if (!response.ok) {
                    const parsed = new DOMParser().parseFromString(text, 'text/html');
                    const message = parsed.querySelector(
                        '[data-public-transport-error-message], .public-transport-error p'
                    )?.textContent?.trim();
                    throw new Error(message || response.statusText || text);
                }
                return text;
            }).finally(() => {
                active.delete(requestKey);
                foreground.delete(requestKey);
                render();
            });
            active.set(requestKey, promise);
        }
        render();
        return { key: requestKey, promise };
    };
    const setForeground = (requestKey, value) => {
        if (requestKey) value ? foreground.add(requestKey) : foreground.delete(requestKey);
        render();
    };
    const backgroundProvider = (provider) => {
        [...foreground].forEach((requestKey) => {
            try {
                if (JSON.parse(requestKey)[0] === provider) foreground.delete(requestKey);
            } catch (error) { /* Ignore keys from older application versions. */ }
        });
        render();
    };
    window.travelManagerPublicTransportRequests = { request, setForeground, backgroundProvider };

    document.addEventListener('travel-manager:offline-map-job-background', (event) => {
        offlineJob = event.detail || offlineJob; renderOffline(); render();
    });
    document.addEventListener('travel-manager:offline-map-job-updated', (event) => {
        offlineJob = event.detail || offlineJob; renderOffline();
    });
    document.addEventListener('travel-manager:offline-map-job-finished', () => {
        offlineJob = null; renderOffline();
    });
    const tileTaskKey = (detail = {}) => String(detail.id
        || [detail.mapId, detail.zoom, detail.column, detail.row].join(':'));
    document.addEventListener('travel-manager:offline-map-tiles-started', (event) => {
        offlineTileTasks.set(tileTaskKey(event.detail), event.detail || {});
        renderOffline(); render();
    });
    document.addEventListener('travel-manager:offline-map-tiles-progress', (event) => {
        offlineTileTasks.set(tileTaskKey(event.detail), event.detail || {});
        renderOffline(); render();
    });
    document.addEventListener('travel-manager:offline-map-tiles-finished', (event) => {
        offlineTileTasks.delete(tileTaskKey(event.detail));
        renderOffline(); render();
    });

    document.addEventListener('travel-manager:views-ready', async () => {
        await window.i18n.ready;
        try {
            const response = await fetch('/api/offline-maps/jobs', {
                headers: {'Accept': 'application/json'}
            });
            if (!response.ok) return;
            const data = await response.json();
            const recovered = (data.jobs || [])
                .filter((item) => ['queued', 'running'].includes(item.status))
                .sort((a, b) => String(b.updated_at).localeCompare(String(a.updated_at)))[0];
            if (recovered && (!offlineJob || offlineJob.id === recovered.id)) {
                offlineJob = recovered;
                if (document.querySelector('.app-shell')?.dataset.currentView !== 'settings') {
                    window.travelManagerOfflineMapProgress?.show(recovered, true);
                }
                renderOffline(); render();
            }
        } catch (error) { /* The active job remains durable and can be restored later. */ }
    });

    fetch('/api/public-transport/pending-downloads')
        .then((response) => response.ok ? response.json() : { providers: [] })
        .then((data) => (data.providers || []).forEach((provider) => {
            request({ provider, screen: 'lines', refresh: true }).promise
                .catch(() => { /* The partial file remains available for retry. */ });
        }))
        .catch(() => { /* Resumption will be retried on the next launch. */ });
})();
