(() => {
    const geometry = window.travelManagerLayerGeometry;
    const surfaceColor = () =>
        getComputedStyle(document.body)
            .getPropertyValue('--surface-background')
            .trim() || '#fff';
    const options = (element) => ({
        color: element.color || '#1F6FAE',
        weight:
            element.line_style === 'double'
                ? (Number(element.width) || 4) + 4
                : Number(element.width) || 4,
        dashArray: geometry.dashArray(element.line_style),
        lineCap: element.line_style === 'dotted' ? 'round' : 'butt',
        fillColor: element.background_color || '#1F6FAE38',
        fillOpacity: 1,
        interactive: false,
    });
    // Shape, inner stroke and title are reused while the element's geometry moves.
    const create = (
        layer,
        element,
        group,
        map,
        sampled = geometry.geometry(element)
    ) => {
        const isPoint = element.type === 'point';
        const shape = isPoint
            ? L.circleMarker(element.points[0], {
                  ...options(element),
                  radius: 7,
                  fillOpacity: 1,
              }).addTo(group)
            : (element.type === 'area' ? L.polygon : L.polyline)(
                  sampled.boundary,
                  options(element)
              ).addTo(group);
        const inner =
            !isPoint && element.line_style === 'double'
                ? L.polyline(sampled.boundary, {
                      color: surfaceColor(),
                      weight: Math.max(1, (Number(element.width) || 4) - 1),
                      interactive: false,
                  }).addTo(group)
                : null;
        let title = null;
        const update = (next = geometry.geometry(element)) => {
            if (isPoint) shape.setLatLng(next.boundary[0]);
            else shape.setLatLngs(next.boundary);
            inner?.setLatLngs(next.boundary);
            if (layer.show_title || isPoint) {
                const position = isPoint
                    ? next.boundary[0]
                    : geometry.titlePosition(
                          next.boundary,
                          element.type === 'area',
                          (a, b) => map.distance(a, b)
                      );
                if (position) {
                    const content = document.createElement('span');
                    content.className = 'map-panel__custom-layer-title-content';
                    content.textContent = [
                        isPoint ? element.icon || '📍' : layer.icon,
                        element.name || layer.name,
                        isPoint ? element.note : '',
                    ]
                        .filter(Boolean)
                        .join(' ');
                    if (!title)
                        title = L.tooltip({
                            permanent: true,
                            direction: isPoint ? 'right' : 'center',
                            className: 'map-panel__custom-layer-title',
                            interactive: false,
                        })
                            .setLatLng(position)
                            .setContent(content)
                            .addTo(group);
                    title.setLatLng(position).setContent(content);
                }
            }
            return next;
        };
        update(sampled);
        return { update };
    };
    const createCollection = (group, map, visible = () => true) => {
        let renderId = 0;
        return async () => {
            const current = ++renderId;
            let layers;
            try {
                layers = await window.travelManagerCustomLayers.list();
            } catch (error) {
                return false;
            }
            if (current !== renderId) return false;
            group.clearLayers();
            layers
                .filter(visible)
                .forEach((layer) =>
                    layer.elements
                        .filter((element) => !element.hidden)
                        .forEach((element) =>
                            create(layer, element, group, map)
                        )
                );
            return true;
        };
    };
    const fit = (map, elements, options = {}) => {
        const points = elements
            .filter((element) => !element.hidden)
            .flatMap((element) => geometry.geometry(element).boundary)
            .filter((point) => point.every(Number.isFinite));
        if (!points.length) return false;
        map.fitBounds(points, {
            maxZoom: 16,
            padding: [24, 24],
            animate: false,
            ...options,
        });
        return true;
    };
    window.travelManagerLayerRenderer = {
        create,
        options,
        createCollection,
        fit,
    };
})();
