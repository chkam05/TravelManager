(function (window) {
    'use strict';

    const pointInRing = ([lng, lat], ring) => {
        let inside = false;
        for (let index = 0, previous = ring.length - 1; index < ring.length; previous = index++) {
            const first = ring[index];
            const second = ring[previous];
            if (!Array.isArray(first) || !Array.isArray(second)) continue;
            const cross = (lng - first[0]) * (second[1] - first[1])
                - (lat - first[1]) * (second[0] - first[0]);
            if (
                Math.abs(cross) < 1e-10
                && lng >= Math.min(first[0], second[0])
                && lng <= Math.max(first[0], second[0])
                && lat >= Math.min(first[1], second[1])
                && lat <= Math.max(first[1], second[1])
            ) return true;
            const intersects = ((first[1] > lat) !== (second[1] > lat))
                && lng < (second[0] - first[0]) * (lat - first[1])
                    / ((second[1] - first[1]) || Number.EPSILON) + first[0];
            if (intersects) inside = !inside;
        }
        return inside;
    };

    const pointInPolygon = (point, polygon) => Array.isArray(polygon)
        && polygon.length > 0
        && pointInRing(point, polygon[0])
        && polygon.slice(1).every((hole) => !pointInRing(point, hole));

    const geometryPolygons = (coverage) => {
        if (coverage?.type === 'Polygon' && Array.isArray(coverage.coordinates)) {
            return [coverage.coordinates];
        }
        if (coverage?.type === 'MultiPolygon' && Array.isArray(coverage.coordinates)) {
            return coverage.coordinates;
        }
        return [];
    };

    const coverageContains = (coverage, point) => geometryPolygons(coverage)
        .some((polygon) => pointInPolygon(point, polygon));

    const contains = (metadata, center) => {
        const bounds = metadata?.bounds;
        const lat = Number(center?.lat);
        const lng = Number(center?.lng);
        const bounded = Array.isArray(bounds)
            && bounds.length === 4
            && [lat, lng, ...bounds].every(Number.isFinite)
            && lng >= bounds[0] && lng <= bounds[2]
            && lat >= bounds[1] && lat <= bounds[3];
        return bounded && (!metadata?.coverage
            || coverageContains(metadata.coverage, [lng, lat]));
    };

    const area = (metadata) => {
        const bounds = metadata.bounds;
        return Math.abs((bounds[2] - bounds[0]) * (bounds[3] - bounds[1]));
    };

    const viewportBounds = (value) => {
        if (Array.isArray(value) && value.length === 4) return value.map(Number);
        if (
            value && ['getWest', 'getSouth', 'getEast', 'getNorth']
                .every((name) => typeof value[name] === 'function')
        ) {
            return [
                Number(value.getWest()), Number(value.getSouth()),
                Number(value.getEast()), Number(value.getNorth())
            ];
        }
        return null;
    };

    const containsViewport = (metadata, viewport) => {
        const bounds = metadata?.bounds;
        const visible = viewportBounds(viewport);
        const bounded = Array.isArray(bounds) && visible
            && [...bounds, ...visible].every(Number.isFinite)
            && bounds[0] <= visible[0] && bounds[1] <= visible[1]
            && bounds[2] >= visible[2] && bounds[3] >= visible[3];
        if (!bounded || !metadata?.coverage) return bounded;
        return sampleViewport(visible, 3).every((point) => (
            coverageContains(metadata.coverage, point)
        ));
    };

    const sampleViewport = (visible, divisions = 2) => {
        const points = [];
        for (let x = 0; x <= divisions; x += 1) {
            for (let y = 0; y <= divisions; y += 1) {
                points.push([
                    visible[0] + (visible[2] - visible[0]) * x / divisions,
                    visible[1] + (visible[3] - visible[1]) * y / divisions
                ]);
            }
        }
        return points;
    };

    const pointInsideViewport = ([lng, lat], visible) => (
        lng >= visible[0] && lng <= visible[2]
        && lat >= visible[1] && lat <= visible[3]
    );

    const segmentsIntersect = (a, b, c, d) => {
        if (
            Math.max(a[0], b[0]) < Math.min(c[0], d[0])
            || Math.max(c[0], d[0]) < Math.min(a[0], b[0])
            || Math.max(a[1], b[1]) < Math.min(c[1], d[1])
            || Math.max(c[1], d[1]) < Math.min(a[1], b[1])
        ) return false;
        const cross = (first, second, third) => (
            (second[0] - first[0]) * (third[1] - first[1])
            - (second[1] - first[1]) * (third[0] - first[0])
        );
        const first = cross(a, b, c);
        const second = cross(a, b, d);
        const third = cross(c, d, a);
        const fourth = cross(c, d, b);
        return ((first <= 0 && second >= 0) || (first >= 0 && second <= 0))
            && ((third <= 0 && fourth >= 0) || (third >= 0 && fourth <= 0));
    };

    const boundaryCrossesViewport = (coverage, visible) => {
        const corners = [
            [visible[0], visible[1]], [visible[2], visible[1]],
            [visible[2], visible[3]], [visible[0], visible[3]]
        ];
        const edges = corners.map((point, index) => (
            [point, corners[(index + 1) % corners.length]]
        ));
        return geometryPolygons(coverage).some((polygon) => polygon.some((ring) => (
            ring.slice(1).some((point, index) => edges.some(([first, second]) => (
                segmentsIntersect(ring[index], point, first, second)
            )))
        )));
    };

    const intersectsViewport = (metadata, viewport) => {
        const bounds = metadata?.bounds;
        const visible = viewportBounds(viewport);
        const bounded = Array.isArray(bounds) && visible
            && [...bounds, ...visible].every(Number.isFinite)
            && bounds[0] <= visible[2] && bounds[2] >= visible[0]
            && bounds[1] <= visible[3] && bounds[3] >= visible[1];
        if (!bounded || !metadata?.coverage) return bounded;
        if (sampleViewport(visible, 2).some((point) => (
            coverageContains(metadata.coverage, point)
        ))) return true;
        return geometryPolygons(metadata.coverage).some((polygon) => (
            polygon.some((ring) => ring.some((point) => (
                pointInsideViewport(point, visible)
            )))
        )) || boundaryCrossesViewport(metadata.coverage, visible);
    };

    const forViewport = (items, viewport) => {
        const candidates = (Array.isArray(items) ? items : [])
            .filter((item) => intersectsViewport(item.metadata, viewport));
        const containing = candidates
            .filter((item) => containsViewport(item.metadata, viewport))
            .sort((first, second) => (
                area(first.metadata) - area(second.metadata)
                || String(first.id).localeCompare(String(second.id))
            ));
        if (containing.length) {
            const exact = containing.filter((item) => item.metadata?.coverage);
            if (exact.length) return [exact[0]];
            const parent = containing.find((item) => {
                const covered = new Set(item.metadata?.coveredMapIds || []);
                return containing.every((candidate) => (
                    candidate.id === item.id
                    || covered.has(String(candidate.metadata?.id || candidate.id).replace(/^offline_/, ''))
                ));
            });
            return parent ? [parent] : containing;
        }
        return candidates.sort((first, second) => (
            area(first.metadata) - area(second.metadata)
            || String(first.id).localeCompare(String(second.id))
        ));
    };

    const coversViewport = (items, viewport) => {
        const visible = viewportBounds(viewport);
        if (!visible) return false;
        const points = sampleViewport(visible, 4);
        return points.every(([lng, lat]) => (Array.isArray(items) ? items : [])
            .some((item) => contains(item.metadata, {lat, lng})));
    };

    const smallestContaining = (items, center) => (Array.isArray(items) ? items : [])
        .filter((item) => contains(item.metadata, center))
        .sort((first, second) => (
            area(first.metadata) - area(second.metadata)
            || String(first.id).localeCompare(String(second.id))
        ))[0] || null;

    window.travelManagerOfflineMapSelection = Object.freeze({
        contains,
        smallestContaining,
        containsViewport,
        intersectsViewport,
        forViewport,
        coversViewport
    });
})(window);
