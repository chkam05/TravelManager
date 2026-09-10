(() => {
    const dashArray = (style) =>
        style === 'dashed'
            ? '12 8'
            : style === 'dotted'
              ? '1 8'
              : style === 'dash-dot'
                ? '12 7 2 7'
                : null;
    const segmentCount = (e) =>
        e.type === 'area' ? e.points.length : Math.max(0, e.points.length - 1);
    const lineSegment = () => ({ type: 'line' });
    const controls = (a, b) => {
        const dy = Number(b[0]) - Number(a[0]),
            dx = Number(b[1]) - Number(a[1]);
        return [
            [Number(a[0]) + dy / 3, Number(a[1]) + dx / 3],
            [Number(a[0]) + (2 * dy) / 3, Number(a[1]) + (2 * dx) / 3],
        ];
    };
    const curveSegment = (a, b) => {
        const [control1, control2] = controls(a, b);
        return { type: 'curve', control1, control2 };
    };
    const ensureSegments = (e) => {
        const count = segmentCount(e);
        if (!Array.isArray(e.segments)) e.segments = [];
        while (e.segments.length < count) e.segments.push(lineSegment());
        if (e.segments.length > count) e.segments.splice(count);
        e.segments.forEach((item, index) => {
            if (item?.type !== 'curve' && item?.type !== 'line')
                e.segments[index] = lineSegment();
        });
    };
    const sampled = (a, b, segment) => {
        if (segment?.type !== 'curve') return [a, b];
        const c1 = segment.control1 || controls(a, b)[0],
            c2 = segment.control2 || controls(a, b)[1],
            points = [];
        for (let i = 0; i <= 24; i++) {
            const t = i / 24,
                u = 1 - t;
            points.push([
                u ** 3 * a[0] +
                    3 * u * u * t * c1[0] +
                    3 * u * t * t * c2[0] +
                    t ** 3 * b[0],
                u ** 3 * a[1] +
                    3 * u * u * t * c1[1] +
                    3 * u * t * t * c2[1] +
                    t ** 3 * b[1],
            ]);
        }
        return points;
    };
    const titlePosition = (geometry, closed, distance) => {
        if (!geometry.length) return null;
        if (closed && geometry.length >= 3) {
            let twiceArea = 0,
                latSum = 0,
                lngSum = 0;
            geometry.forEach((point, index) => {
                const next = geometry[(index + 1) % geometry.length],
                    cross = point[1] * next[0] - next[1] * point[0];
                twiceArea += cross;
                lngSum += (point[1] + next[1]) * cross;
                latSum += (point[0] + next[0]) * cross;
            });
            if (Math.abs(twiceArea) > 1e-12)
                return [latSum / (3 * twiceArea), lngSum / (3 * twiceArea)];
        }
        if (geometry.length === 1) return geometry[0];
        const lengths = [];
        let total = 0;
        for (let i = 1; i < geometry.length; i++) {
            const length = distance(geometry[i - 1], geometry[i]);
            lengths.push(length);
            total += length;
        }
        let travelled = 0;
        for (let i = 0; i < lengths.length; i++) {
            if (travelled + lengths[i] >= total / 2) {
                const ratio = lengths[i]
                    ? (total / 2 - travelled) / lengths[i]
                    : 0;
                return [
                    geometry[i][0] +
                        (geometry[i + 1][0] - geometry[i][0]) * ratio,
                    geometry[i][1] +
                        (geometry[i + 1][1] - geometry[i][1]) * ratio,
                ];
            }
            travelled += lengths[i];
        }
        return geometry[geometry.length - 1];
    };
    const moveNode = (e, index, next) => {
        const previous = e.points[index],
            delta = [next[0] - previous[0], next[1] - previous[1]];
        e.points[index] = next;
        ensureSegments(e);
        const attached = [];
        if (index < e.segments.length)
            attached.push([e.segments[index], 'control1']);
        const before =
            index === 0 && e.type === 'area'
                ? e.segments.length - 1
                : index - 1;
        if (before >= 0) attached.push([e.segments[before], 'control2']);
        attached.forEach(([segment, key]) => {
            if (segment.type === 'curve' && segment[key])
                segment[key] = [
                    segment[key][0] + delta[0],
                    segment[key][1] + delta[1],
                ];
        });
    };
    const geometryMetrics = (e) => {
        ensureSegments(e);
        const boundary = geometry(e).boundary;
        const radians = (value) => (value * Math.PI) / 180,
            R = 6371000,
            distance = (a, b) => {
                const lat1 = radians(a[0]),
                    lat2 = radians(b[0]),
                    dLat = lat2 - lat1,
                    dLon = radians(b[1] - a[1]),
                    h =
                        Math.sin(dLat / 2) ** 2 +
                        Math.cos(lat1) *
                            Math.cos(lat2) *
                            Math.sin(dLon / 2) ** 2;
                return 2 * R * Math.atan2(Math.sqrt(h), Math.sqrt(1 - h));
            };
        let length = 0;
        for (let i = 1; i < boundary.length; i++)
            length += distance(boundary[i - 1], boundary[i]);
        let area = 0;
        if (e.type === 'area' && boundary.length > 2) {
            for (let i = 0; i < boundary.length; i++) {
                const a = boundary[i],
                    b = boundary[(i + 1) % boundary.length];
                area +=
                    radians(b[1] - a[1]) *
                    (2 + Math.sin(radians(a[0])) + Math.sin(radians(b[0])));
            }
            area = Math.abs((area * R * R) / 2);
        }
        return { length, area };
    };
    const makeSegments = (points, type, closed = false) => {
        const count = closed ? points.length : points.length - 1,
            result = [];
        for (let i = 0; i < count; i++)
            result.push(
                type === 'curve'
                    ? curveSegment(points[i], points[(i + 1) % points.length])
                    : lineSegment()
            );
        return result;
    };

    const geometry = (e) => {
        if (e.type === 'point') return { boundary: e.points, segments: [] };
        const boundary = [],
            segments = [];
        for (let i = 0; i < segmentCount(e); i++) {
            const points = sampled(
                e.points[i],
                e.points[(i + 1) % e.points.length],
                e.segments?.[i]
            );
            segments.push(points);
            boundary.push(...points.slice(i ? 1 : 0));
        }
        return { boundary, segments };
    };
    const splitSegment = (element, index) => {
        ensureSegments(element);
        const i = index,
            next = (i + 1) % element.points.length,
            segment = element.segments[i],
            a = element.points[i],
            b = element.points[next];
        if (segment.type === 'curve') {
            const c1 = segment.control1,
                c2 = segment.control2,
                p01 = [(a[0] + c1[0]) / 2, (a[1] + c1[1]) / 2],
                p12 = [(c1[0] + c2[0]) / 2, (c1[1] + c2[1]) / 2],
                p23 = [(c2[0] + b[0]) / 2, (c2[1] + b[1]) / 2],
                p012 = [(p01[0] + p12[0]) / 2, (p01[1] + p12[1]) / 2],
                p123 = [(p12[0] + p23[0]) / 2, (p12[1] + p23[1]) / 2],
                mid = [(p012[0] + p123[0]) / 2, (p012[1] + p123[1]) / 2];
            element.points.splice(i + 1, 0, mid);
            element.segments.splice(
                i,
                1,
                { type: 'curve', control1: p01, control2: p012 },
                { type: 'curve', control1: p123, control2: p23 }
            );
        } else {
            element.points.splice(i + 1, 0, [
                (a[0] + b[0]) / 2,
                (a[1] + b[1]) / 2,
            ]);
            element.segments.splice(i, 1, lineSegment(), lineSegment());
        }
        return index + 1;
    };
    const deleteVertex = (element, index) => {
        ensureSegments(element);
        const closed = element.type === 'area';
        if (closed) {
            const previous =
                (index - 1 + element.segments.length) % element.segments.length;
            element.segments.splice(index, 1);
            if (element.segments.length)
                element.segments[
                    Math.min(previous, element.segments.length - 1)
                ] = lineSegment();
        } else if (index === 0) element.segments.shift();
        else if (index === element.points.length - 1) element.segments.pop();
        else {
            element.segments.splice(index, 1);
            element.segments[index - 1] = lineSegment();
        }
        element.points.splice(index, 1);
        if (element.type === 'area' && element.points.length < 3)
            element.type = 'line';
        ensureSegments(element);
        return element.points.length >= 2;
    };
    const toggleSegment = (element, index) => {
        ensureSegments(element);
        const i = index,
            next = (i + 1) % element.points.length,
            current = element.segments[i];
        element.segments[i] =
            current.type === 'curve'
                ? lineSegment()
                : curveSegment(element.points[i], element.points[next]);
    };
    const continueElement = (
        element,
        points,
        segments,
        prepend,
        closeShape
    ) => {
        if (prepend) {
            points = points.reverse();
            segments = segments.reverse().map((segment) =>
                segment.type === 'curve'
                    ? {
                          ...segment,
                          control1: segment.control2,
                          control2: segment.control1,
                      }
                    : segment
            );
            element.points = [...points, ...element.points.slice(1)];
            element.segments = [...segments, ...element.segments];
        } else {
            element.points = [...element.points, ...points.slice(1)];
            element.segments = [...element.segments, ...segments];
        }
        if (closeShape) {
            element.points.pop();
            element.type = 'area';
        } else element.type = 'route';
        ensureSegments(element);
    };

    const translate = (element, original, delta) => {
        const shifted = (point) => [point[0] + delta[0], point[1] + delta[1]];
        const points = original.points.map(shifted);
        const segments = original.segments.map((segment) =>
            segment.type === 'curve'
                ? {
                      ...segment,
                      control1: shifted(segment.control1),
                      control2: shifted(segment.control2),
                  }
                : { ...segment }
        );
        const coordinates = [
            ...points,
            ...segments.flatMap((segment) =>
                segment.type === 'curve'
                    ? [segment.control1, segment.control2]
                    : []
            ),
        ];
        if (
            coordinates.some(
                (point) =>
                    !point.every(Number.isFinite) ||
                    Math.abs(point[0]) > 90 ||
                    Math.abs(point[1]) > 180
            )
        )
            return false;
        element.points = points;
        element.segments = segments;
        return true;
    };

    // Work in screen pixels so the tolerance stays constant across zoom levels.
    const snap = (map, position, elements, excluded = null, radius = 10) => {
        const cursor = map.latLngToContainerPoint(position);
        let best = null;
        const consider = (pixel, point, kind) => {
            const distance = Math.hypot(pixel.x - cursor.x, pixel.y - cursor.y);
            if (distance <= radius && (!best || distance < best.distance))
                best = { point, kind, distance };
        };
        const targets = elements.filter((e) => !e.hidden && e !== excluded);
        targets.forEach((e) =>
            e.points.forEach((point) =>
                consider(
                    map.latLngToContainerPoint(L.latLng(point)),
                    point,
                    'node'
                )
            )
        );
        // Prefer an actual vertex over an approximate point on a nearby segment.
        if (best) return best;
        targets.forEach((e) =>
            geometry(e).segments.forEach((segment) => {
                for (let i = 1; i < segment.length; i++) {
                    const a = map.latLngToContainerPoint(
                        L.latLng(segment[i - 1])
                    );
                    const b = map.latLngToContainerPoint(L.latLng(segment[i]));
                    const dx = b.x - a.x,
                        dy = b.y - a.y;
                    const length = dx * dx + dy * dy;
                    if (!length) continue;
                    const t = Math.max(
                        0,
                        Math.min(
                            1,
                            ((cursor.x - a.x) * dx + (cursor.y - a.y) * dy) /
                                length
                        )
                    );
                    const pixel = { x: a.x + t * dx, y: a.y + t * dy };
                    if (
                        Math.hypot(pixel.x - cursor.x, pixel.y - cursor.y) >
                        radius
                    )
                        continue;
                    const point = map.containerPointToLatLng([
                        pixel.x,
                        pixel.y,
                    ]);
                    consider(pixel, [point.lat, point.lng], 'segment');
                }
            })
        );
        return best;
    };
    window.travelManagerLayerGeometry = {
        translate,
        snap,
        splitSegment,
        deleteVertex,
        toggleSegment,
        continueElement,
        dashArray,
        segmentCount,
        lineSegment,
        controls,
        curveSegment,
        ensureSegments,
        sampled,
        titlePosition,
        moveNode,
        geometryMetrics,
        makeSegments,
        geometry,
    };
})();
