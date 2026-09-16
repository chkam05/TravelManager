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
        return { id, minZoom, maxZoom, bounds };
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
            maxNativeZoom: validated.maxZoom,
            maxZoom: validated.maxZoom,
            bounds: L.latLngBounds([[south, west], [north, east]]),
            attribution: ATTRIBUTION,
            interactive: options.interactive === true
        };
        if (options.pane) layerOptions.pane = options.pane;
        const layer = L.vectorGrid.protobuf(url, layerOptions);

        layer.travelManagerOfflineMap = {
            id: validated.id,
            name: String(metadata?.name || validated.id),
            bounds: [...validated.bounds],
            minZoom: validated.minZoom,
            maxZoom: validated.maxZoom
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
