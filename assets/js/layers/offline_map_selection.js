(function (window) {
    'use strict';

    const contains = (metadata, center) => {
        const bounds = metadata?.bounds;
        const lat = Number(center?.lat);
        const lng = Number(center?.lng);
        return Array.isArray(bounds)
            && bounds.length === 4
            && [lat, lng, ...bounds].every(Number.isFinite)
            && lng >= bounds[0] && lng <= bounds[2]
            && lat >= bounds[1] && lat <= bounds[3];
    };

    const area = (metadata) => {
        const bounds = metadata.bounds;
        return Math.abs((bounds[2] - bounds[0]) * (bounds[3] - bounds[1]));
    };

    const smallestContaining = (items, center) => (Array.isArray(items) ? items : [])
        .filter((item) => contains(item.metadata, center))
        .sort((first, second) => (
            area(first.metadata) - area(second.metadata)
            || String(first.id).localeCompare(String(second.id))
        ))[0] || null;

    window.travelManagerOfflineMapSelection = Object.freeze({
        contains,
        smallestContaining
    });
})(window);
