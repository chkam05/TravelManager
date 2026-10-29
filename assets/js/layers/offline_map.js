(function (window) {
    'use strict';

    const MAP_ID_PATTERN = /^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/;
    const ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';

    const fallbackStyles = {
        water: { color: '#7db7d8', weight: 1, fill: true, fillColor: '#a8d5ea', fillOpacity: 1 },
        landuse: { color: '#c4d6b0', weight: 0.5, fill: true, fillColor: '#dce8cf', fillOpacity: 0.75 },
        buildings: { color: '#b8aea4', weight: 1, fill: true, fillColor: '#d8d0c8', fillOpacity: 0.85 },
        roads: { color: '#ffffff', weight: 2.5, opacity: 0.95 },
        railways: { color: '#686868', weight: 1.5, opacity: 0.9, dashArray: '5,4' },
        boundaries: { color: '#8b6ca8', weight: 1.25, opacity: 0.85, dashArray: '6,4' },
        // Point labels need a separate text renderer. Drawing them as circles
        // produces unexplained dark spots across the map.
        places: [],
        pois: []
    };

    const finiteNumber = (value) => {
        const number = Number(value);
        return Number.isFinite(number) ? number : null;
    };

    const validateMetadata = (metadata) => {
        const id = String(metadata?.id || '');
        const minZoom = finiteNumber(metadata?.min_zoom);
        const maxZoom = finiteNumber(metadata?.max_zoom);
        const displayMaxZoom = finiteNumber(metadata?.display_max_zoom ?? maxZoom);
        const bounds = Array.isArray(metadata?.bounds)
            ? metadata.bounds.map(finiteNumber)
            : [];

        if (!MAP_ID_PATTERN.test(id)) {
            throw new TypeError('Invalid offline map id.');
        }
        if (
            !Number.isInteger(minZoom)
            || !Number.isInteger(maxZoom)
            || minZoom < 0
            || maxZoom > 22
            || minZoom > maxZoom
            || !Number.isInteger(displayMaxZoom)
            || displayMaxZoom < maxZoom
            || displayMaxZoom > 19
        ) {
            throw new TypeError('Invalid offline map zoom range.');
        }
        if (
            bounds.length !== 4
            || bounds.some((value) => value === null)
            || bounds[0] < -180
            || bounds[2] > 180
            || bounds[1] < -90
            || bounds[3] > 90
            || bounds[0] > bounds[2]
            || bounds[1] > bounds[3]
        ) {
            throw new TypeError('Invalid offline map bounds.');
        }
        return { id, minZoom, maxZoom, displayMaxZoom, bounds };
    };

    const create = (metadata, options = {}) => {
        const L = window.L;

        if (!L?.vectorGrid?.protobuf || !L?.canvas?.tile) {
            throw new Error('Leaflet.VectorGrid is unavailable.');
        }

        const validated = validateMetadata(metadata);
        const [west, south, east, north] = validated.bounds;
        const url = `/api/offline-maps/${encodeURIComponent(validated.id)}/tiles/{z}/{x}/{y}.pbf`;
        const layerOptions = {
            rendererFactory: L.canvas.tile,
            vectorTileLayerStyles: options.styles
                || window.travelManagerOfflineMapStyles?.standard?.()
                || fallbackStyles,
            minNativeZoom: validated.minZoom,
            // Detailed levels are real API requests generated and cached on
            // demand; do not let GridLayer stretch the z14 canvas.
            maxNativeZoom: validated.displayMaxZoom,
            maxZoom: validated.displayMaxZoom,
            bounds: L.latLngBounds([[south, west], [north, east]]),
            attribution: ATTRIBUTION,
            interactive: options.interactive === true
        };
        if (options.pane) layerOptions.pane = options.pane;
        const layer = L.vectorGrid.protobuf(url, layerOptions);
        const activityId = `offline-tiles:${validated.id}`;
        const neighbourActivityId = `offline-neighbours:${validated.id}`;
        let activityTimer = null;
        let activityVisible = false;
        let requestedTiles = 0;
        let finishedTiles = 0;
        const knownTiles = new Set();
        const neighbourQueue = [];
        let neighbourWorkers = 0;
        let neighbourCurrent = 0;
        let neighbourTotal = 0;
        let neighbourActive = false;
        const coordinateKey = ({z, x, y}) => `${z}:${x}:${y}`;
        const tileCentre = ({z, x, y}) => {
            const scale = 2 ** z;
            const longitude = (x + 0.5) / scale * 360 - 180;
            const latitude = Math.atan(Math.sinh(
                Math.PI * (1 - 2 * (y + 0.5) / scale)
            )) * 180 / Math.PI;
            return [longitude, latitude];
        };
        const insideCoverage = (coords) => {
            const [longitude, latitude] = tileCentre(coords);
            return longitude >= west && longitude <= east
                && latitude >= south && latitude <= north;
        };
        const neighbourProgress = () => ({
            id: neighbourActivityId,
            mapId: validated.id,
            kind: 'neighbours',
            current: neighbourCurrent,
            total: neighbourTotal,
            percent: neighbourTotal > 0
                ? Math.min(100, Math.floor(100 * neighbourCurrent / neighbourTotal))
                : 0
        });
        const reportNeighbours = (eventName) => document.dispatchEvent(
            new CustomEvent(eventName, {detail: neighbourProgress()})
        );
        const runNeighbourQueue = () => {
            while (neighbourWorkers < 3 && neighbourQueue.length) {
                const coords = neighbourQueue.shift();
                neighbourWorkers += 1;
                fetch(url
                    .replace('{z}', String(coords.z))
                    .replace('{x}', String(coords.x))
                    .replace('{y}', String(coords.y)), {
                    headers: {'Accept': 'application/vnd.mapbox-vector-tile'}
                }).catch(() => null).finally(() => {
                    neighbourWorkers -= 1;
                    neighbourCurrent += 1;
                    reportNeighbours('travel-manager:offline-map-tiles-progress');
                    if (!neighbourQueue.length && neighbourWorkers === 0) {
                        neighbourActive = false;
                        reportNeighbours('travel-manager:offline-map-tiles-finished');
                        neighbourCurrent = 0;
                        neighbourTotal = 0;
                    } else {
                        runNeighbourQueue();
                    }
                });
            }
        };
        const prefetchNeighbours = (origin) => {
            if (!origin || origin.z <= validated.maxZoom) return;
            const limit = 2 ** origin.z;
            for (let offsetY = -1; offsetY <= 1; offsetY += 1) {
                for (let offsetX = -1; offsetX <= 1; offsetX += 1) {
                    if (offsetX === 0 && offsetY === 0) continue;
                    const coords = {
                        z: origin.z,
                        x: origin.x + offsetX,
                        y: origin.y + offsetY
                    };
                    const key = coordinateKey(coords);
                    if (
                        coords.x < 0 || coords.y < 0
                        || coords.x >= limit || coords.y >= limit
                        || knownTiles.has(key) || !insideCoverage(coords)
                    ) continue;
                    knownTiles.add(key);
                    neighbourQueue.push(coords);
                    neighbourTotal += 1;
                }
            }
            if (!neighbourQueue.length) return;
            if (!neighbourActive) {
                neighbourActive = true;
                reportNeighbours('travel-manager:offline-map-tiles-started');
            } else {
                reportNeighbours('travel-manager:offline-map-tiles-progress');
            }
            runNeighbourQueue();
        };
        const tileProgress = () => ({
            id: activityId,
            mapId: validated.id,
            current: finishedTiles,
            total: requestedTiles,
            percent: requestedTiles > 0
                ? Math.min(100, Math.floor(100 * finishedTiles / requestedTiles))
                : 0
        });
        const reportTileActivity = () => {
            if (!activityVisible) return;
            document.dispatchEvent(new CustomEvent(
                'travel-manager:offline-map-tiles-progress',
                {detail: tileProgress()}
            ));
        };
        const finishTileActivity = () => {
            window.clearTimeout(activityTimer);
            activityTimer = null;
            if (!activityVisible) return;
            finishedTiles = Math.max(finishedTiles, requestedTiles);
            reportTileActivity();
            activityVisible = false;
            document.dispatchEvent(new CustomEvent(
                'travel-manager:offline-map-tiles-finished',
                {detail: tileProgress()}
            ));
        };
        layer.on('loading', () => {
            finishTileActivity();
            requestedTiles = 0;
            finishedTiles = 0;
            activityTimer = window.setTimeout(() => {
                activityTimer = null;
                activityVisible = true;
                document.dispatchEvent(new CustomEvent(
                    'travel-manager:offline-map-tiles-started',
                    {detail: tileProgress()}
                ));
            }, 350);
        });
        layer.on('tileloadstart', (event) => {
            if (event.coords) knownTiles.add(coordinateKey(event.coords));
            requestedTiles += 1;
            reportTileActivity();
        });
        layer.on('tileload tileerror', (event) => {
            finishedTiles = Math.min(requestedTiles, finishedTiles + 1);
            reportTileActivity();
            if (event.type === 'tileload') prefetchNeighbours(event.coords);
        });
        layer.on('load remove', finishTileActivity);

        layer.travelManagerOfflineMap = {
            id: validated.id,
            name: String(metadata?.name || validated.id),
            bounds: [...validated.bounds],
            minZoom: validated.minZoom,
            nativeMaxZoom: validated.maxZoom,
            maxZoom: validated.displayMaxZoom
        };
        return layer;
    };

    window.travelManagerOfflineMapLayer = Object.freeze({
        attribution: ATTRIBUTION,
        create,
        isSupported: () => Boolean(
            window.L?.vectorGrid?.protobuf && window.L?.canvas?.tile
        )
    });
})(window);
