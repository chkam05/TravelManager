document.addEventListener('travel-manager:views-ready', () => {
    const panel = document.querySelector('#layer-panel');
    const toolsPanel = document.querySelector('#layer-tools-panel');
    if (!panel || !toolsPanel) return;
    const control = (selector) =>
        panel.querySelector(selector) || toolsPanel.querySelector(selector);
    const state = window.travelManagerLayerEditorState.create();
    const selectedIds = new Set();
    const targets = () =>
        (state.layer?.elements || []).filter(
            (e) =>
                !e.hidden &&
                !e.locked &&
                (selectedIds.has(e.id) || e === state.selected)
        );
    let map = window.travelManagerMap?.map,
        preview = null,
        editGroup = null,
        vertexGroup = null,
        menuElement = null,
        lengthUnit = 'm',
        areaUnit = 'm2';
    const title = control('[data-layer-title]'),
        list = control('[data-layer-elements]'),
        width = control('[data-layer-width]'),
        lineStyle = control('[data-layer-line-style]'),
        color = control('[data-layer-color]'),
        backgroundColor = control('[data-layer-background-color]'),
        finish = control('[data-draw-finish]'),
        elementMenu = control('[data-layer-element-menu]'),
        splitButton = control('[data-layer-split]'),
        deleteNodeButton = control('[data-element-delete]'),
        toggleCurveButton = control('[data-layer-toggle-curve]'),
        closeCurveButton = control('[data-layer-close-curve]'),
        grabber = control('[data-layer-panel-grabber]');
    let endDrag = null,
        lastPointer = null,
        menuTrigger = null;
    const coordinateTooltip = document.createElement('div');
    coordinateTooltip.className = 'layer-drawing-coordinate-tooltip';
    coordinateTooltip.hidden = true;
    const coordinateX = document.createElement('span');
    const coordinateY = document.createElement('span');
    coordinateTooltip.append(coordinateX, coordinateY);
    (document.body || panel).append(coordinateTooltip);
    const hideCoordinateTooltip = () => {
        coordinateTooltip.hidden = true;
    };
    const setDrawingCursor = (active) => {
        map?.getContainer?.().classList.toggle(
            'layer-map--drawing', Boolean(active)
        );
    };
    const showCoordinateTooltip = (event, point) => {
        if (!state.mode || state.transitioning) {
            hideCoordinateTooltip();
            return;
        }
        coordinateX.textContent = `X: ${point.lng.toFixed(6)}`;
        coordinateY.textContent = `Y: ${point.lat.toFixed(6)}`;
        const original = event.originalEvent;
        const mapRect = map.getContainer?.().getBoundingClientRect() || {
            left: 0, top: 0
        };
        const cursor = original && Number.isFinite(original.clientX)
            ? { x: original.clientX, y: original.clientY }
            : (() => {
                const position = map.latLngToContainerPoint(event.latlng);
                return { x: mapRect.left + position.x, y: mapRect.top + position.y };
            })();
        coordinateTooltip.hidden = false;
        const rect = coordinateTooltip.getBoundingClientRect();
        coordinateTooltip.style.left = `${Math.max(8, Math.min(cursor.x + 14, window.innerWidth - rect.width - 8))}px`;
        coordinateTooltip.style.top = `${Math.max(8, Math.min(cursor.y + 14, (window.innerHeight || 800) - rect.height - 8))}px`;
    };
    const saveButton = control('[data-layer-save]'),
        status = control('[data-layer-status]');
    const undoButton = control('[data-layer-undo]');
    const redoButton = control('[data-layer-redo]');
    const historyBlocked = () =>
        Boolean(
            state.saving ||
            state.transitioning ||
            state.mode ||
            endDrag ||
            state.renamingId !== null
        );
    const syncHistory = () => {
        undoButton.disabled = historyBlocked() || state.historyIndex <= 0;
        redoButton.disabled =
            historyBlocked() || state.historyIndex >= state.history.length - 1;
    };
    const recordChange = () => {
        state.recordChange();
        syncHistory();
    };
    const restoreHistory = (direction) => {
        if (
            historyBlocked() ||
            document
                .querySelector('#dialog-layer')
                ?.classList.contains('dialog-layer--open')
        )
            return;
        if (!state.restoreHistory(direction)) return;
        closeMenu();
        selectedIds.clear();
        select(state.selected);
        setStatus(hasChanges() ? 'UNSAVED_STATUS' : null);
    };
    undoButton.onclick = () => restoreHistory(-1);
    redoButton.onclick = () => restoreHistory(1);
    const fitLayerButton = control('[data-layer-fit]');
    const showOnMap = (elements) => {
        if (!map || !elements?.length || state.mode || endDrag) return false;
        const available = map.getSize();
        const narrow = window.innerWidth <= 900;
        const leftPadding = narrow
            ? 24
            : Math.min(
                  panel.getBoundingClientRect().width + 36,
                  available.x * 0.55
              );
        const topPadding = Math.min(
            toolsPanel.getBoundingClientRect().height + 24,
            available.y * 0.35
        );
        const bottomPadding = narrow
            ? Math.min(
                  panel.getBoundingClientRect().height + 24,
                  available.y * 0.35
              )
            : 24;
        return window.travelManagerLayerRenderer.fit(map, elements, {
            paddingTopLeft: [24, topPadding],
            paddingBottomRight: [leftPadding, bottomPadding],
        });
    };
    fitLayerButton.onclick = () => {
        if (!state.transitioning) showOnMap(state.layer?.elements);
    };
    control('[data-element-menu-fit]').onclick = () => {
        if (menuElement) showOnMap([menuElement]);
        closeMenu(true);
    };
    const captureDraft = () => {
        if (!state.layer || !hasChanges()) return null;
        const layer = structuredClone(state.layer);
        if (state.renamingId !== null) {
            const element = layer.elements.find(
                (item) => item.id === state.renamingId
            );
            const name = list.querySelector('input')?.value.trim();
            if (element && name) element.name = name;
        }
        return {
            version: 1,
            layer,
            baseline: state.persistedSnapshot
                ? JSON.parse(state.persistedSnapshot)
                : null,
            mode: state.mode,
            drawing: state.drawing.map((point) => [point.lat, point.lng]),
            continuationId: state.continuation?.id || null,
            continuationVertex: state.continuationVertex,
            style: {
                color: color.style.getPropertyValue('--color') || '#1F6FAE',
                background_color:
                    backgroundColor.style.getPropertyValue('--color') ||
                    '#1F6FAE38',
                width: Math.max(
                    1,
                    Math.min(20, Math.round(Number(width.value) || 4))
                ),
                line_style: lineStyle.value || 'solid',
            },
        };
    };
    const draftClient = window.travelManagerLayerDraft.create(
        captureDraft,
        () => setStatus('DRAFT_FAILED', true)
    );
    const onEditorInput = () => {
        if (!state.transitioning) draftClient.schedule();
    };
    panel.addEventListener('input', onEditorInput);
    toolsPanel.addEventListener('input', onEditorInput);
    const setStatus = (key, error = false) => {
        status.textContent = key ? window.i18n.t(`LAYER_EDITOR.${key}`) : '';
        status.hidden = !key;
        status.dataset.error = String(error);
        if (key !== 'DRAFT_FAILED' && state.layer && !state.transitioning)
            draftClient.schedule();
    };
    const hasSketch = () => state.drawing.length > (state.continuation ? 1 : 0);
    const hasPendingName = () =>
        state.renamingId !== null &&
        Boolean(list.querySelector('input')?.value.trim()) &&
        list.querySelector('input').value.trim() !==
            (state.layer.elements.find((e) => e.id === state.renamingId)
                ?.name || '');
    const hasChanges = () => state.hasChanges(hasSketch(), hasPendingName());
    const uid = () => crypto.randomUUID?.() || `${Date.now()}${Math.random()}`;
    const api = window.travelManagerLayerApi.request;
    const listLayers = () => window.travelManagerCustomLayers.list();
    const announceEditing = (id) =>
        document.dispatchEvent(
            new CustomEvent('travel-manager:custom-layer-editing-changed', {
                detail: { id: id || null },
            })
        );
    const {
        curveSegment,
        ensureSegments,
        sampled,
        moveNode,
        geometryMetrics,
        makeSegments,
        splitSegment,
        deleteVertex,
        toggleSegment,
        continueElement,
    } = window.travelManagerLayerGeometry;
    const accent = () =>
        getComputedStyle(document.body)
            .getPropertyValue('--accent-color')
            .trim() || '#1F6FAE';
    const elementViews = new Map();
    const resetGroups = () => {
        elementViews.clear();
        editGroup?.remove();
        vertexGroup?.remove();
        editGroup = map ? L.layerGroup().addTo(map) : null;
        vertexGroup = map ? L.layerGroup().addTo(map) : null;
    };
    const hint = control('[data-layer-hint]');
    const canDraw = (tool) =>
        !state.transitioning &&
        !selectedIds.size &&
        (!state.selected ||
            (state.selectedVertex !== null &&
                isEndpoint(state.selected, state.selectedVertex) &&
                tool !== 'area' &&
                tool !== 'point'));
    const isEndpoint = (e, index) =>
        e &&
        e.type !== 'area' &&
        e.type !== 'point' &&
        (index === 0 || index === e.points.length - 1);
    const toggleIcon = () => {
        const curve =
            state.selected &&
            state.selectedSegment !== null &&
            state.selected.segments?.[state.selectedSegment]?.type === 'curve';
        toggleCurveButton.innerHTML = curve
            ? '<svg class="lucide lucide-line-dot-right-horizontal" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12h13"></path><circle cx="19" cy="12" r="2"></circle></svg>'
            : '<svg class="lucide lucide-spline-pointer" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4v4"></path><path d="M3 6h4"></path><path d="M6 18c4-8 8-8 12 0"></path><path d="m16 16 2 2 2-2"></path></svg>';
    };
    const syncActions = () => {
        control('[data-group-copy]').disabled =
            !selectedIds.size ||
            Boolean(state.mode || endDrag || state.transitioning);
        control('[data-group-delete]').disabled =
            control('[data-group-copy]').disabled || !targets().length;

        const chosen = (state.layer?.elements || []).filter((e) =>
            selectedIds.has(e.id)
        );
        const blocked = Boolean(state.mode || endDrag || state.transitioning);
        for (const action of ['hide', 'lock'])
            control(`[data-group-${action}]`).disabled =
                !chosen.length || blocked;
        control('[data-group-all]').disabled =
            blocked || !state.layer?.elements.some((e) => !e.hidden);
        const all = state.layer?.elements.filter((e) => !e.hidden) || [];
        const setLabel = (selector, key, icon) => {
            const button = control(selector);
            const label = window.i18n.t(`LAYER_EDITOR.${key}`);
            button.title = label;
            button.setAttribute('aria-label', label);
            button.innerHTML = `<i data-lucide="${icon}" aria-hidden="true"></i>`;
        };
        setLabel(
            '[data-group-all]',
            all.length && all.every((e) => selectedIds.has(e.id))
                ? 'DESELECT_ALL'
                : 'SELECT_ALL',
            'list-checks'
        );
        setLabel(
            '[data-group-lock]',
            chosen.length && chosen.every((e) => e.locked)
                ? 'UNLOCK_SELECTED'
                : 'LOCK_SELECTED',
            chosen.length && chosen.every((e) => e.locked)
                ? 'lock-open'
                : 'lock'
        );
        window.lucide?.createIcons();
        const segment = state.selected && state.selectedSegment !== null;
        splitButton.disabled = !segment;
        toggleCurveButton.disabled = !segment;
        closeCurveButton.disabled = !(
            state.selected &&
            state.selected.type !== 'area' &&
            state.selected.points.length >= 3
        );
        deleteNodeButton.disabled = state.selectedVertex === null;
        backgroundColor.disabled = Boolean(
            state.selected && state.selected.type !== 'area'
        );
        toolsPanel.querySelectorAll('[data-draw]').forEach((button) => {
            button.disabled = !canDraw(button.dataset.draw);
            const active = button.dataset.draw === state.mode;
            button.classList.toggle('is-active', active);
            button.setAttribute('aria-pressed', String(active));
        });
        hint.hidden = true;
        hint.textContent = state.mode
            ? window.i18n.t(
                  state.continuation
                      ? 'LAYER_EDITOR.CONTINUE_HINT'
                      : 'LAYER_EDITOR.DRAW_HINT'
              )
            : '';
        fitLayerButton.disabled =
            !state.layer?.elements.length ||
            Boolean(state.mode || endDrag || state.transitioning);
        toggleIcon();
        syncHistory();
    };
    const select = (e, vertex = null, segment = null) => {
        if (state.transitioning || state.mode || e?.locked || e?.hidden) return;
        commitPendingName();
        selectedIds.clear();
        state.selected = e;
        state.selectedVertex = vertex;
        state.selectedSegment = segment;
        width.value = e?.width || width.value;
        lineStyle.value = e?.line_style || 'solid';
        color.style.setProperty('--color', e?.color || '#1F6FAE');
        backgroundColor.style.setProperty(
            '--color',
            e?.background_color || '#1F6FAE38'
        );
        syncActions();
        render();
        renderMap();
    };
    const clearSelection = () => {
        selectedIds.clear();
        commitPendingName();
        state.selected = null;
        state.selectedVertex = null;
        state.selectedSegment = null;
        syncActions();
        render();
        renderMap();
    };
    let snapping = true;
    const snapButton = control('[data-layer-snap]');
    snapButton.classList.add('is-active');
    snapButton.onclick = () => {
        snapping = !snapping;
        snapButton.setAttribute('aria-pressed', String(snapping));
        snapButton.classList.toggle('is-active', snapping);
        clearSnap();
    };
    control('[data-layer-info]').onclick = () =>
        window.travelManagerDialogs.yesNo({
            title: window.i18n.t('LAYER_EDITOR.TOOLS_TITLE'),
            description: [
                'DRAW_HINT',
                'CONTINUE_HINT',
                'SNAP_HINT',
                'MOVE_SHAPE_HINT',
                'MULTI_HINT',
            ]
                .map((key) => window.i18n.t(`LAYER_EDITOR.${key}`))
                .join('\n\n'),
            icon: 'info',
            information: true,
            yesLabel: window.i18n.t('COMMON.CLOSE'),
        });
    let snapMarker = null;
    const clearSnap = () => {
        snapMarker?.remove();
        snapMarker = null;
    };
    const snapPosition = (position, event, excluded = null) => {
        const target =
            !snapping || event?.altKey || event?.originalEvent?.altKey
                ? null
                : window.travelManagerLayerGeometry.snap(
                      map,
                      position,
                      state.layer.elements.filter(
                          (e) =>
                              !Array.isArray(excluded) || !excluded.includes(e)
                      ),
                      Array.isArray(excluded) ? null : excluded
                  );
        if (!target) {
            clearSnap();
            return position;
        }
        const point = L.latLng(target.point);
        if (snapMarker) snapMarker.setLatLng(point);
        else
            snapMarker = L.circleMarker(point, {
                radius: 10,
                color: '#f59e0b',
                weight: 3,
                fillOpacity: 0,
                interactive: false,
            }).addTo(map);
        return point;
    };
    const bindDrag = (handle, element, selectHandle, update, whole = false) => {
        const target = handle.getElement();
        if (!target) return;
        target.style.touchAction = 'none';
        target.addEventListener('pointerdown', (event) => {
            if (
                state.transitioning ||
                state.mode ||
                element.locked ||
                element.hidden ||
                (whole && !event.shiftKey) ||
                event.button !== 0 ||
                event.isPrimary === false
            )
                return;
            event.preventDefault();
            event.stopPropagation();
            endDrag?.();
            const moveWhole =
                whole || (element.type === 'point' && event.shiftKey);
            const moving =
                moveWhole && selectedIds.has(element.id)
                    ? targets()
                    : [element];
            const originals = moving.map((e) =>
                structuredClone({ points: e.points, segments: e.segments })
            );
            const origin = map.mouseEventToLatLng(event);
            const wasDirty = state.dirty,
                draggingEnabled = map.dragging.enabled();
            if (!(moveWhole && selectedIds.has(element.id))) selectHandle();
            map.dragging.disable();
            const move = (next) => {
                if (next.pointerId !== event.pointerId || state.transitioning)
                    return;
                next.preventDefault();
                const latlng = snapPosition(
                    map.mouseEventToLatLng(next),
                    next,
                    moving
                );
                if (
                    !Number.isFinite(latlng.lat) ||
                    !Number.isFinite(latlng.lng) ||
                    Math.abs(latlng.lat) > 90 ||
                    Math.abs(latlng.lng) > 180
                )
                    return;
                if (moveWhole) {
                    const candidates = moving.map(() => ({}));
                    if (
                        !candidates.every((candidate, index) =>
                            window.travelManagerLayerGeometry.translate(
                                candidate,
                                originals[index],
                                [
                                    latlng.lat - origin.lat,
                                    latlng.lng - origin.lng,
                                ]
                            )
                        )
                    )
                        return;
                    moving.forEach((e, index) =>
                        Object.assign(e, candidates[index])
                    );
                } else update([latlng.lat, latlng.lng]);
                state.dirty = true;
                setStatus('UNSAVED_STATUS');
                moving.forEach((e) => renderMap(e));
            };
            const stop = (next, cancel = false) => {
                if (
                    next?.pointerId !== undefined &&
                    next.pointerId !== event.pointerId
                )
                    return;
                document.removeEventListener('pointermove', move);
                document.removeEventListener('pointerup', stop);
                document.removeEventListener('pointercancel', cancelDrag);
                window.removeEventListener('blur', cancelDrag);
                document.removeEventListener('keydown', cancelKey);
                if (cancel) {
                    moving.forEach((e, index) =>
                        Object.assign(e, originals[index])
                    );
                    state.dirty = wasDirty;
                    setStatus(hasChanges() ? 'UNSAVED_STATUS' : null);
                }
                clearSnap();
                endDrag = null;
                if (!cancel) recordChange();
                syncHistory();
                if (draggingEnabled) map.dragging.enable();
                render();
                renderMap();
            };
            const cancelKey = (next) => {
                if (next.key !== 'Escape') return;
                next.preventDefault();
                next.stopPropagation();
                stop(undefined, true);
            };
            const cancelDrag = (next) => stop(next, true);
            endDrag = () => stop();
            syncHistory();
            document.addEventListener('pointermove', move, { passive: false });
            document.addEventListener('pointerup', stop);
            document.addEventListener('pointercancel', cancelDrag);
            window.addEventListener('blur', cancelDrag);
            document.addEventListener('keydown', cancelKey);
        });
    };
    const renderMap = (changed = null) => {
        if (!map || !state.layer) return;
        if (changed && elementViews.has(changed.id)) {
            const view = elementViews.get(changed.id),
                sample = window.travelManagerLayerGeometry.geometry(changed);
            view.visual.update(sample);
            view.hits.forEach((hit, index) =>
                hit.setLatLngs(sample.segments[index])
            );
            view.vertices.forEach((marker, index) =>
                marker.setLatLng(changed.points[index])
            );
            view.highlights.forEach(({ line, index }) =>
                line.setLatLngs(sample.segments[index])
            );
            view.controls.forEach(({ guide, handle, index, key, endpoint }) => {
                const control = changed.segments[index][key];
                handle.setLatLng(control);
                guide.setLatLngs([changed.points[endpoint], control]);
            });
            return;
        }
        resetGroups();
        state.layer.elements.forEach((e) => {
            if (e.hidden) return;
            if (e.locked) {
                window.travelManagerLayerRenderer.create(
                    state.layer,
                    e,
                    editGroup,
                    map
                );
                return;
            }
            ensureSegments(e);
            const sample = window.travelManagerLayerGeometry.geometry(e);
            const view = {
                hits: [],
                vertices: [],
                controls: [],
                highlights: [],
                visual: null,
            };
            sample.segments.forEach((points, i) => {
                const hit = L.polyline(points, {
                    color: e.color,
                    weight: Math.max(e.width, 10),
                    opacity: 0.001,
                }).addTo(editGroup);
                hit.on('click', (event) => {
                    L.DomEvent.stopPropagation(event);
                    if (state.mode) mapClick(event);
                    else select(e, null, i);
                });
                bindDrag(hit, e, () => select(e), null, true);
                view.hits.push(hit);
                if (
                    selectedIds.has(e.id) ||
                    (e === state.selected && state.selectedSegment === i)
                )
                    view.highlights.push({
                        index: i,
                        line: L.polyline(points, {
                            color: accent(),
                            weight: Math.max(e.width, 4) + 5,
                            opacity: 0.72,
                            interactive: false,
                        }).addTo(editGroup),
                    });
            });
            view.visual = window.travelManagerLayerRenderer.create(
                state.layer,
                e,
                editGroup,
                map,
                sample
            );
            e.points.forEach((point, index) => {
                const active =
                    e === state.selected && index === state.selectedVertex;
                const marker = L.circleMarker(point, {
                    radius: active ? 8 : 6,
                    color: active ? accent() : e.color,
                    fillColor: active ? accent() : '#fff',
                    fillOpacity: 1,
                    weight: 3,
                }).addTo(vertexGroup);
                marker.on('click', (event) => {
                    L.DomEvent.stopPropagation(event);
                    if (state.mode) mapClick(event);
                    else select(e, index, null);
                });
                bindDrag(
                    marker,
                    e,
                    () => select(e, index, null),
                    (position) => moveNode(e, index, position)
                );
                view.vertices.push(marker);
            });
            if (
                e === state.selected &&
                state.selectedSegment !== null &&
                e.segments[state.selectedSegment]?.type === 'curve'
            ) {
                const i = state.selectedSegment,
                    next = (i + 1) % e.points.length;
                [
                    [i, 'control1'],
                    [next, 'control2'],
                ].forEach(([endpoint, key]) => {
                    const control = e.segments[i][key];
                    const guide = L.polyline([e.points[endpoint], control], {
                        color: accent(),
                        weight: 1.5,
                        dashArray: '5 5',
                        interactive: false,
                    }).addTo(vertexGroup);
                    const handle = L.circleMarker(control, {
                        radius: 7,
                        color: accent(),
                        fillColor: '#fff',
                        fillOpacity: 1,
                        weight: 2,
                    }).addTo(vertexGroup);
                    bindDrag(
                        handle,
                        e,
                        () => {},
                        (position) => {
                            e.segments[i][key] = position;
                        }
                    );
                    view.controls.push({
                        guide,
                        handle,
                        index: i,
                        key,
                        endpoint,
                    });
                });
            }
            elementViews.set(e.id, view);
        });
    };
    const closeMenu = (restoreFocus = false) => {
            elementMenu.setAttribute('aria-hidden', 'true');
            menuElement = null;
            if (restoreFocus) menuTrigger?.focus();
            menuTrigger = null;
        },
        removeElement = (e) => {
            if (e.locked) return;
            state.layer.elements = state.layer.elements.filter(
                (item) => item !== e
            );
            if (state.selected === e) {
                state.selected = null;
                state.selectedVertex = null;
                state.selectedSegment = null;
            }
            recordChange();
            setStatus('UNSAVED_STATUS');
            syncActions();
            closeMenu();
            render();
            renderMap();
        };
    const metricValue = (value) =>
        new Intl.NumberFormat(window.i18n.locale.replace('_', '-'), {
            maximumFractionDigits: value < 100 ? 1 : 0,
        }).format(value);
    const convertedMetric = (value, unit) =>
            value *
            ({
                mm: 1000,
                cm: 100,
                m: 1,
                km: 0.001,
                mm2: 1000000,
                cm2: 10000,
                m2: 1,
                km2: 0.000001,
            }[unit] || 1),
        unitLabel = (unit) => unit.replace('2', '²');
    const back = control('[data-layer-back]');
    back.onclick = () => {
        if (!state.mode && !state.transitioning) clearSelection();
    };
    const highlightPoints = () => {
        const count = state.selected?.points.length || 0;
        Array.from(list.children).forEach((row) => {
            if (row.dataset.pointIndex === undefined) return;
            const index = Number(row.dataset.pointIndex);
            const active =
                index === state.selectedVertex ||
                (state.selectedSegment !== null &&
                    (index === state.selectedSegment ||
                        index === (state.selectedSegment + 1) % count));
            row.classList.toggle('is-selected', active);
            row.setAttribute('aria-current', String(active));
        });
    };
    const renderPoints = (element) => {
        const heading = document.createElement('h3');
        heading.textContent =
            element.name || window.i18n.t('LAYER_EDITOR.POINTS');
        list.append(heading);
        if (element.type === 'point') {
            for (const [key, tag, label, max] of [
                ['icon', 'input', 'POINT_ICON', 32],
                ['note', 'textarea', 'POINT_NOTE', 4000],
            ]) {
                const field = document.createElement('label');
                field.className = 'layer-panel__point-note';
                const caption = document.createElement('span');
                caption.textContent = window.i18n.t(`LAYER_EDITOR.${label}`);
                const input = document.createElement(tag);
                input.value = element[key] || '';
                input.maxLength = max;
                input.onchange = () => {
                    if (
                        state.transitioning ||
                        element.locked ||
                        state.selected !== element
                    )
                        return;
                    element[key] = input.value.slice(0, max);
                    recordChange();
                    setStatus('UNSAVED_STATUS');
                    renderMap();
                };
                input.onkeydown = (event) => {
                    if (event.key === 'Escape') {
                        event.preventDefault();
                        event.stopPropagation();
                        input.value = element[key] || '';
                        back.focus();
                    }
                };
                field.append(caption, input);
                list.append(field);
            }
        }
        element.points.forEach((point, index) => {
            const row = document.createElement('div');
            row.className = 'layer-panel__point';
            row.dataset.pointIndex = String(index);
            const label = document.createElement('span');
            label.textContent = `${index + 1}`;
            row.append(label);
            [1, 0].forEach((axis) => {
                const field = document.createElement('label');
                const caption = document.createElement('span');
                caption.textContent = axis === 1 ? 'X:' : 'Y:';
                caption.title = window.i18n.t(
                    axis === 1 ? 'LAYER_EDITOR.COORD_X' : 'LAYER_EDITOR.COORD_Y'
                );
                const input = document.createElement('input');
                input.type = 'number';
                input.step = 'any';
                const limit = axis === 1 ? 180 : 90;
                input.min = String(-limit);
                input.max = String(limit);
                input.value = String(point[axis]);
                input.setAttribute(
                    'aria-label',
                    `${index + 1}: ${caption.title}`
                );
                input.onfocus = () => {
                    if (state.mode || state.transitioning) return;
                    state.selectedVertex = index;
                    state.selectedSegment = null;
                    syncActions();
                    highlightPoints();
                    renderMap();
                };
                input.onchange = () => {
                    const value = Number(input.value);
                    if (
                        state.mode ||
                        state.transitioning ||
                        state.selected !== element
                    )
                        return;
                    if (
                        !input.value.trim() ||
                        !Number.isFinite(value) ||
                        Math.abs(value) > limit
                    ) {
                        input.value = String(element.points[index][axis]);
                        setStatus('INVALID_COORDINATE', true);
                        return;
                    }
                    if (value === element.points[index][axis]) return;
                    const next = [...element.points[index]];
                    next[axis] = value;
                    moveNode(element, index, next);
                    state.selectedVertex = index;
                    state.selectedSegment = null;
                    recordChange();
                    setStatus('UNSAVED_STATUS');
                    syncActions();
                    highlightPoints();
                    renderMap();
                };
                input.onkeydown = (event) => {
                    if (event.key === 'Escape') {
                        event.preventDefault();
                        event.stopPropagation();
                        input.value = String(element.points[index][axis]);
                        back.focus();
                    } else if (event.key === 'Enter') {
                        event.preventDefault();
                        event.stopPropagation();
                        input.onchange();
                        back.focus();
                    }
                };
                field.append(caption, input);
                row.append(field);
            });
            list.append(row);
        });
        syncHistory();
    };
    function render() {
        if (!state.layer) return;
        back.hidden = !state.selected;
        title.textContent = state.layer.name;
        list.replaceChildren();
        if (state.selected && state.renamingId === null) {
            renderPoints(state.selected);
            highlightPoints();
            return;
        }
        state.layer.elements.forEach((e, i) => {
            const row = document.createElement('div');
            row.className = `layer-panel__element${e === state.selected ? ' is-selected' : ''}`;
            const display = e.name || `${e.type} ${i + 1}`;
            if (state.renamingId === e.id) {
                const editor = document.createElement('div'),
                    input = document.createElement('input'),
                    save = document.createElement('button');
                editor.className = 'layer-panel__rename';
                input.value = display;
                save.className = 'layer-panel__rename-save';
                save.innerHTML = '<i data-lucide="check"></i>';
                save.setAttribute('aria-label', window.i18n.t('COMMON.SAVE'));
                input.setAttribute(
                    'aria-label',
                    window.i18n.t('LAYER_EDITOR.RENAME')
                );
                const commit = () => {
                    if (input.value.trim()) {
                        e.name = input.value.trim();
                        recordChange();
                        setStatus('UNSAVED_STATUS');
                    }
                    state.renamingId = null;
                    render();
                    renderMap();
                };
                save.onclick = commit;
                input.onkeydown = (event) => {
                    event.stopPropagation();
                    if (event.key === 'Enter') event.preventDefault();
                    if (event.key === 'Enter') commit();
                    if (event.key === 'Escape') {
                        state.renamingId = null;
                        render();
                    }
                };
                editor.append(input, save);
                row.append(editor);
                setTimeout(() => input.focus());
            } else {
                const name = document.createElement('span'),
                    metrics = document.createElement('span'),
                    length = document.createElement('small'),
                    area = document.createElement('small'),
                    more = document.createElement('button'),
                    values = geometryMetrics(e);
                name.className = 'layer-panel__element-name';
                name.textContent =
                    display +
                    (e.hidden
                        ? ` · ${window.i18n.t('LAYER_EDITOR.HIDDEN')}`
                        : '') +
                    (e.locked
                        ? ` · ${window.i18n.t('LAYER_EDITOR.LOCKED')}`
                        : '');
                metrics.className = 'layer-panel__element-metrics';
                length.textContent = window.i18n.t(
                    e.type === 'area'
                        ? 'LAYER_EDITOR.PERIMETER_VALUE'
                        : 'LAYER_EDITOR.LENGTH_VALUE',
                    {
                        value: metricValue(
                            convertedMetric(values.length, lengthUnit)
                        ),
                        unit: unitLabel(lengthUnit),
                    }
                );
                area.textContent = window.i18n.t('LAYER_EDITOR.AREA_VALUE', {
                    value: metricValue(convertedMetric(values.area, areaUnit)),
                    unit: unitLabel(areaUnit),
                });
                if (e.type !== 'point') metrics.append(length);
                else metrics.textContent = e.icon || '📍';
                if (e.type === 'area') metrics.append(area);
                more.className = 'layer-panel__element-more';
                more.setAttribute(
                    'aria-label',
                    window.i18n.t('LAYER_EDITOR.ELEMENT_ACTIONS', {
                        name: display,
                    })
                );
                more.setAttribute('aria-haspopup', 'menu');
                more.innerHTML = '<i data-lucide="ellipsis"></i>';
                more.onclick = (event) => {
                    event.stopPropagation();
                    menuElement = e;
                    for (const [key, label, icon] of [
                        [
                            'hidden',
                            e.hidden ? 'SHOW_ELEMENT' : 'HIDE_ELEMENT',
                            e.hidden ? 'eye' : 'eye-off',
                        ],
                        [
                            'locked',
                            e.locked ? 'UNLOCK_ELEMENT' : 'LOCK_ELEMENT',
                            e.locked ? 'lock-open' : 'lock',
                        ],
                    ]) {
                        const button = control(`[data-element-menu-${key}]`);
                        button.replaceChildren();
                        const image = document.createElement('i');
                        image.setAttribute('data-lucide', icon);
                        image.setAttribute('aria-hidden', 'true');
                        const text = document.createElement('span');
                        text.textContent = window.i18n.t(
                            `LAYER_EDITOR.${label}`
                        );
                        button.append(image, text);
                    }
                    window.lucide?.createIcons();
                    control('[data-element-menu-rename]').disabled = Boolean(
                        e.locked
                    );
                    control('[data-element-menu-delete]').disabled = Boolean(
                        e.locked
                    );
                    menuTrigger = more;
                    const a = more.getBoundingClientRect(),
                        p = panel.getBoundingClientRect();
                    elementMenu.setAttribute('aria-hidden', 'false');
                    const size = elementMenu.getBoundingClientRect();
                    elementMenu.style.left = `${Math.max(8, Math.min(a.right - p.left - size.width, p.width - size.width - 8))}px`;
                    elementMenu.style.top = `${Math.max(8, Math.min(a.bottom - p.top + 5, p.height - size.height - 8))}px`;
                    elementMenu.querySelector('button')?.focus();
                };
                row.tabIndex = 0;
                row.setAttribute('aria-label', display);
                row.onkeydown = (event) => {
                    if (event.target !== row) return;
                    if (event.key === 'Enter' || event.key === ' ') {
                        event.preventDefault();
                        event.stopPropagation();
                        select(e);
                        back.focus();
                    }
                    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
                        event.preventDefault();
                        list.children[
                            Math.max(
                                0,
                                Math.min(
                                    state.layer.elements.length - 1,
                                    i + (event.key === 'ArrowDown' ? 1 : -1)
                                )
                            )
                        ]?.focus();
                    }
                };
                row.onclick = () => select(e);
                const check = document.createElement('input');
                check.type = 'checkbox';
                check.checked = selectedIds.has(e.id);
                check.disabled = Boolean(e.hidden || state.mode);
                check.setAttribute(
                    'aria-label',
                    `${window.i18n.t('LAYER_EDITOR.SELECT_SHAPE')}: ${display}`
                );
                check.onclick = (event) => event.stopPropagation();
                check.onchange = () => {
                    if (
                        e.hidden ||
                        state.mode ||
                        state.transitioning ||
                        endDrag
                    )
                        return;
                    commitPendingName();
                    if (check.checked) selectedIds.add(e.id);
                    else selectedIds.delete(e.id);
                    state.selected = null;
                    state.selectedVertex = null;
                    state.selectedSegment = null;
                    syncActions();
                    highlightPoints();
                    renderMap();
                };
                row.append(check, name, metrics, more);
            }
            list.append(row);
        });
        window.lucide?.createIcons();
        syncHistory();
    }
    const stopDrawing = (commit = true, closeShape = false) => {
        if (commit && hasSketch()) {
            const distinct = new Set(
                state.drawing.map((p) => `${p.lat},${p.lng}`)
            ).size;
            if (distinct < (state.mode === 'area' ? 3 : 2)) {
                setStatus('INVALID_DRAWING', true);
                return false;
            }
        }
        preview?.remove();
        preview = null;
        if (commit && state.drawing.length >= 2) {
            let points = state.drawing.map((p) => [p.lat, p.lng]),
                segments = makeSegments(
                    points,
                    state.mode === 'curve' ? 'curve' : 'line',
                    state.mode === 'area'
                );
            if (state.continuation) {
                continueElement(
                    state.continuation,
                    points,
                    segments,
                    state.continuationVertex === 0,
                    closeShape
                );
            } else
                state.layer.elements.push({
                    id: uid(),
                    name: '',
                    type:
                        state.mode === 'area'
                            ? 'area'
                            : state.mode === 'line'
                              ? 'line'
                              : 'route',
                    points,
                    color: color.style.getPropertyValue('--color') || '#1F6FAE',
                    background_color:
                        backgroundColor.style.getPropertyValue('--color') ||
                        '#1F6FAE38',
                    line_style: lineStyle.value || 'solid',
                    width: Number(width.value) || 4,
                    segments,
                });
            recordChange();
            setStatus('UNSAVED_STATUS');
        }
        state.drawing = [];
        lastPointer = null;
        clearSnap();
        state.continuation = null;
        state.continuationVertex = null;
        state.mode = null;
        hideCoordinateTooltip();
        setDrawingCursor(false);
        finish.hidden = true;
        syncActions();
        render();
        renderMap();
        return true;
    };
    const startDrawing = (next) => {
        if (!canDraw(next)) return;
        if (state.mode && !stopDrawing()) return;
        state.mode = next;
        setDrawingCursor(true);
        state.continuation =
            next !== 'area' && state.selectedVertex !== null
                ? state.selected
                : null;
        state.continuationVertex = state.continuation
            ? state.selectedVertex
            : null;
        state.drawing = state.continuation
            ? [L.latLng(state.continuation.points[state.continuationVertex])]
            : [];
        finish.hidden = next === 'line' || next === 'curve' || next === 'point';
        state.selected = null;
        state.selectedVertex = null;
        state.selectedSegment = null;
        syncActions();
        renderMap();
    };
    const near = (a, b) =>
        map
            .latLngToContainerPoint(a)
            .distanceTo(map.latLngToContainerPoint(b)) <= 12;
    const mapClick = (event) => {
        if (!state.mode || state.transitioning) return;
        const point = snapPosition(event.latlng, event);
        if (state.mode === 'point') {
            const element = {
                id: uid(),
                name: window.i18n.t('LAYER_EDITOR.NEW_POINT'),
                type: 'point',
                points: [[point.lat, point.lng]],
                segments: [],
                note: '',
                icon: '📍',
                color: color.style.getPropertyValue('--color') || '#1F6FAE',
                width: 4,
            };
            state.layer.elements.push(element);
            state.mode = null;
            hideCoordinateTooltip();
            setDrawingCursor(false);
            preview?.remove();
            preview = null;
            clearSnap();
            recordChange();
            setStatus('UNSAVED_STATUS');
            select(element);
            return;
        }
        if (
            state.mode === 'area' &&
            state.drawing.length >= 3 &&
            near(state.drawing[0], point)
        ) {
            stopDrawing();
            return;
        }
        if (state.continuation) {
            const opposite = L.latLng(
                state.continuation.points[
                    state.continuationVertex === 0
                        ? state.continuation.points.length - 1
                        : 0
                ]
            );
            const distinct = new Set(
                [
                    ...state.continuation.points,
                    ...state.drawing.map((p) => [p.lat, p.lng]),
                ].map((p) => p.join(','))
            ).size;
            if (distinct >= 3 && near(opposite, point)) {
                state.drawing.push(opposite);
                stopDrawing(true, true);
                return;
            }
        }
        if (
            state.drawing.length &&
            state.drawing[state.drawing.length - 1].lat === point.lat &&
            state.drawing[state.drawing.length - 1].lng === point.lng
        )
            return;
        state.drawing.push(point);
        setStatus('UNSAVED_STATUS');
        if (
            (state.mode === 'line' || state.mode === 'curve') &&
            state.drawing.length === 2
        )
            stopDrawing();
    };
    const mapMove = (event) => {
        if (!state.mode || state.transitioning) {
            hideCoordinateTooltip();
            return;
        }
        lastPointer = event.latlng;
        event = { ...event, latlng: snapPosition(event.latlng, event) };
        showCoordinateTooltip(event, event.latlng);
        preview?.remove();
        preview = null;
        if (!state.drawing.length) {
            preview = L.circleMarker(event.latlng, {
                radius: 6,
                color: color.style.getPropertyValue('--color') || '#1F6FAE',
                weight: 2,
                fillColor: color.style.getPropertyValue('--color') || '#1F6FAE',
                fillOpacity: 0.35,
                interactive: false,
            }).addTo(map);
            return;
        }
        const points = [...state.drawing, event.latlng],
            options = {
                color: color.style.getPropertyValue('--color') || '#1F6FAE',
                fillColor:
                    backgroundColor.style.getPropertyValue('--color') ||
                    '#1F6FAE38',
                weight: Number(width.value) || 4,
                dashArray: '5 5',
                fillOpacity: 1,
                interactive: false,
            };
        preview = (
            state.mode === 'area' && points.length > 2
                ? L.polygon(points, options)
                : L.polyline(
                      state.mode === 'curve'
                          ? sampled(
                                [points[0].lat, points[0].lng],
                                [event.latlng.lat, event.latlng.lng],
                                curveSegment(
                                    [points[0].lat, points[0].lng],
                                    [event.latlng.lat, event.latlng.lng]
                                )
                            )
                          : points,
                      options
                  )
        ).addTo(map);
    };
    const commitPendingName = () => {
        if (state.renamingId === null) return;
        const value = list.querySelector('input')?.value.trim();
        const element = state.layer.elements.find(
            (item) => item.id === state.renamingId
        );
        if (element && value && element.name !== value) {
            element.name = value;
            recordChange();
            setStatus('UNSAVED_STATUS');
        }
        state.renamingId = null;
    };
    const save = () => {
        if (state.saving) return state.saving;
        if (!state.layer) return Promise.resolve(false);
        commitPendingName();
        if (state.mode && !stopDrawing()) return Promise.resolve(false);
        // Keep a stable client ID even if the server saved a request whose response was lost.
        if (!state.layer.id) state.layer.id = uid();
        const snapshot = JSON.stringify(state.layer),
            currentLayer = state.layer;
        saveButton.disabled = true;
        panel.setAttribute('aria-busy', 'true');
        setStatus('SAVING');
        undoButton.disabled = true;
        redoButton.disabled = true;
        state.saving = (async () => {
            try {
                await window.travelManagerCustomLayers.save(
                    JSON.parse(snapshot)
                );
                // Do not replace live objects: selection and active drag handlers refer to them.
                if (state.layer === currentLayer) {
                    state.acceptSnapshot(snapshot);
                    const selectedId = state.selected?.id;
                    state.selected =
                        state.layer.elements.find(
                            (element) => element.id === selectedId
                        ) || null;
                    if (!state.selected) {
                        state.selectedVertex = null;
                        state.selectedSegment = null;
                    }
                    closeMenu();
                    syncActions();
                    if (state.renamingId === null) render();
                    renderMap();
                    announceEditing(state.layer.id);
                    setStatus(hasChanges() ? 'SAVED_WITH_CHANGES' : 'SAVED');
                }
                return true;
            } catch (error) {
                setStatus(
                    error.status === 400 ? 'INVALID_DATA' : 'SAVE_FAILED',
                    true
                );
                return false;
            } finally {
                state.saving = null;
                syncHistory();
                saveButton.disabled = false;
                panel.setAttribute('aria-busy', 'false');
            }
        })();
        return state.saving;
    };
    const confirmLeave = async () => {
        if (!state.layer) return true;
        if (state.saving && !(await state.saving)) return false;
        if (!hasChanges()) {
            await draftClient.clear();
            return true;
        }
        const result = await window.travelManagerDialogs.saveDiscardCancel({
            title: window.i18n.t('LAYER_EDITOR.UNSAVED_TITLE'),
            description: window.i18n.t('LAYER_EDITOR.UNSAVED_TEXT'),
        });
        if (result === 'discard') {
            await draftClient.clear();
            return true;
        }
        if (result === 'save' && (await save()) && !hasChanges()) {
            await draftClient.clear();
            return true;
        }
        return false;
    };
    const resetEditor = () => {
        selectedIds.clear();
        clearSnap();
        endDrag?.();
        stopDrawing(false);
        editGroup?.remove();
        vertexGroup?.remove();
        elementViews.clear();
        editGroup = null;
        vertexGroup = null;
        state.selected = null;
        state.selectedVertex = null;
        state.selectedSegment = null;
        state.renamingId = null;
        closeMenu();
        state.dirty = false;
        state.persistedSnapshot = null;
        state.layer = null;
        state.resetHistory();
        syncHistory();
        setStatus(null);
    };
    const transition = async (action) => {
        if (state.transitioning) return false;
        state.transitioning = true;
        panel.inert = true;
        toolsPanel.inert = true;
        try {
            if (!(await confirmLeave())) return false;
            return (await action()) !== false;
        } catch (error) {
            window.travelManagerAlert?.(
                window.i18n.t('LAYER_EDITOR.DRAFT_FAILED'),
                'error'
            );
            return false;
        } finally {
            state.transitioning = false;
            if (state.dirty) draftClient.schedule();
            panel.inert = false;
            toolsPanel.inert = !toolsPanel.classList.contains('is-open');
            syncActions();
        }
    };
    const close = () =>
        transition(async () => {
            resetEditor();
            panel.classList.remove('is-open');
            toolsPanel.classList.remove('is-open');
            toolsPanel.setAttribute('aria-hidden', 'true');
            panel.setAttribute('aria-hidden', 'true');
            announceEditing(null);
        });
    const open = (value, { duplicate = false } = {}) =>
        transition(async () => {
            let recovered = await draftClient.load();
            if (recovered) {
                const choice =
                    await window.travelManagerDialogs.saveDiscardCancel({
                        title: window.i18n.t('LAYER_EDITOR.RECOVER_TITLE'),
                        description: window.i18n.t(
                            'LAYER_EDITOR.RECOVER_TEXT',
                            { name: recovered.layer.name }
                        ),
                        yesLabel: window.i18n.t('LAYER_EDITOR.RESTORE'),
                        noLabel: window.i18n.t('LAYER_EDITOR.DISCARD'),
                    });
                if (choice === 'cancel') return false;
                if (choice === 'discard') {
                    await draftClient.clear();
                    recovered = null;
                } else value = recovered.layer;
            }
            map = window.travelManagerMap?.map || map;
            const ui = await fetch('/api/settings/ui', {
                headers: { Accept: 'application/json' },
            })
                .then((response) => (response.ok ? response.json() : {}))
                .catch(() => ({}));
            const storedWidth = Number(ui.ui?.layer_editor_panel_width);
            if (storedWidth > 0 && !widthPending) preferredWidth = storedWidth;
            applyPanelWidth();
            lengthUnit = ui.ui?.layer_length_unit || 'm';
            areaUnit = ui.ui?.layer_area_unit || 'm2';
            if (
                value &&
                value.id === state.layer?.id &&
                state.persistedSnapshot !== null
            )
                value = JSON.parse(state.persistedSnapshot);
            const number = value
                ? 1
                : (await listLayers().catch(() => [])).length + 1;
            resetEditor();
            state.layer = value
                ? structuredClone(value)
                : {
                      id: uid(),
                      name: window.i18n.t('LAYER_EDITOR.NEW_LAYER', { number }),
                      icon: '',
                      show_title: false,
                      elements: [],
                  };
            if (duplicate && !recovered) {
                state.layer.id = uid();
                state.layer.name += ` (${window.i18n.t('LAYER_EDITOR.COPY_SUFFIX')})`;
                state.layer.elements.forEach((element) => {
                    element.id = uid();
                });
            }
            state.layer.elements.forEach(ensureSegments);
            state.persistedSnapshot =
                duplicate && !recovered ? null : JSON.stringify(state.layer);
            if (duplicate && !recovered) state.dirty = true;
            if (recovered) {
                state.persistedSnapshot = recovered.baseline
                    ? JSON.stringify(recovered.baseline)
                    : null;
                state.dirty =
                    JSON.stringify(state.layer) !== state.persistedSnapshot;
                state.mode = recovered.mode;
                setDrawingCursor(Boolean(state.mode));
                state.drawing = recovered.drawing.map((point) =>
                    L.latLng(point)
                );
                state.continuation =
                    state.layer.elements.find(
                        (item) => item.id === recovered.continuationId
                    ) || null;
                state.continuationVertex = recovered.continuationVertex;
                width.value = recovered.style.width || 4;
                lineStyle.value = recovered.style.line_style || 'solid';
                color.style.setProperty(
                    '--color',
                    recovered.style.color || '#1F6FAE'
                );
                backgroundColor.style.setProperty(
                    '--color',
                    recovered.style.background_color || '#1F6FAE38'
                );
                finish.hidden =
                    !state.mode ||
                    state.mode === 'line' ||
                    state.mode === 'curve';
            }
            state.resetHistory();
            syncActions();
            window.travelManagerLayerDetailsPanel?.close();
            window.travelManagerPlaceDetailsPanel?.close(false);
            window.travelManagerRouteDetailsPanel?.close(false);
            panel.classList.add('is-open');
            toolsPanel.classList.add('is-open');
            toolsPanel.setAttribute('aria-hidden', 'false');
            window.travelManagerPublicTransportVehiclePanel?.close();
            panel.setAttribute('aria-hidden', 'false');
            announceEditing(state.layer.id);
            render();
            renderMap();
            if (value && !state.mode) showOnMap(state.layer.elements);
            if (state.drawing.length) {
                const points = state.drawing.map((point) => [
                    point.lat,
                    point.lng,
                ]);
                preview = L.layerGroup().addTo(map);
                L.polyline(points, {
                    color: recovered.style.color || '#1F6FAE',
                    dashArray: '5 5',
                    interactive: false,
                }).addTo(preview);
                points.forEach((point) =>
                    L.circleMarker(point, {
                        radius: 4,
                        color: recovered.style.color || '#1F6FAE',
                        interactive: false,
                    }).addTo(preview)
                );
                map.fitBounds(points, {
                    maxZoom: 16,
                    padding: [24, 24],
                    animate: false,
                });
            }
            if (recovered) setStatus('DRAFT_RESTORED');
            else if (duplicate) setStatus('UNSAVED_STATUS');
        });
    window.addEventListener('beforeunload', (event) => {
        if (hasChanges() || state.saving) {
            draftClient.flush().catch(() => {});
            event.preventDefault();
            event.returnValue = '';
        }
    });
    toolsPanel
        .querySelectorAll('[data-draw]')
        .forEach(
            (button) =>
                (button.onclick = () => startDrawing(button.dataset.draw))
        );
    finish.onclick = () => stopDrawing();
    color.onclick = async () => {
        const session = state.layer,
            chosen = targets();
        const next = await window.travelManagerColorPicker?.show(
            color.style.getPropertyValue('--color')
        );
        if (next && session === state.layer && !state.transitioning) {
            color.style.setProperty('--color', next);
            draftClient.schedule();
            if (
                chosen.length &&
                chosen.every(
                    (target) =>
                        state.layer.elements.includes(target) &&
                        !target.locked &&
                        !target.hidden
                )
            ) {
                chosen.forEach((target) => {
                    target.color = next;
                });
                recordChange();
                setStatus('UNSAVED_STATUS');
                renderMap();
            }
        }
    };
    backgroundColor.onclick = async () => {
        const session = state.layer,
            chosen = targets();
        const next = await window.travelManagerColorPicker?.show(
            backgroundColor.style.getPropertyValue('--color')
        );
        if (next && session === state.layer && !state.transitioning) {
            backgroundColor.style.setProperty('--color', next);
            draftClient.schedule();
            if (
                chosen.length &&
                chosen.every(
                    (target) =>
                        state.layer.elements.includes(target) &&
                        !target.locked &&
                        !target.hidden
                )
            ) {
                chosen
                    .filter((target) => target.type === 'area')
                    .forEach((target) => {
                        target.background_color = next;
                    });
                recordChange();
                setStatus('UNSAVED_STATUS');
                renderMap();
            }
        }
    };
    width.onchange = () => {
        width.value = Math.max(1, Math.min(20, Number(width.value) || 4));
        if (targets().length) {
            targets().forEach((target) => {
                target.width = Number(width.value);
            });
            recordChange();
            setStatus('UNSAVED_STATUS');
            renderMap();
        }
    };
    lineStyle.onchange = () => {
        if (targets().length) {
            targets().forEach((target) => {
                target.line_style = lineStyle.value;
            });
            recordChange();
            setStatus('UNSAVED_STATUS');
            renderMap();
        }
    };
    deleteNodeButton.onclick = () => {
        if (!state.selected || state.selectedVertex === null) return;
        const retained = deleteVertex(state.selected, state.selectedVertex);
        if (!retained) {
            state.layer.elements = state.layer.elements.filter(
                (e) => e !== state.selected
            );
            state.selected = null;
        }
        state.selectedVertex = null;
        recordChange();
        setStatus('UNSAVED_STATUS');
        syncActions();
        render();
        renderMap();
    };
    splitButton.onclick = () => {
        if (!state.selected || state.selectedSegment === null) return;
        state.selectedVertex = splitSegment(
            state.selected,
            state.selectedSegment
        );
        state.selectedSegment = null;
        recordChange();
        setStatus('UNSAVED_STATUS');
        syncActions();
        render();
        renderMap();
    };
    toggleCurveButton.onclick = () => {
        if (!state.selected || state.selectedSegment === null) return;
        toggleSegment(state.selected, state.selectedSegment);
        recordChange();
        setStatus('UNSAVED_STATUS');
        syncActions();
        render();
        renderMap();
    };
    closeCurveButton.onclick = () => {
        if (
            !state.selected ||
            state.selected.type === 'area' ||
            state.selected.points.length < 3
        )
            return;
        state.selected.type = 'area';
        ensureSegments(state.selected);
        state.selectedVertex = null;
        state.selectedSegment = state.selected.segments.length - 1;
        recordChange();
        setStatus('UNSAVED_STATUS');
        syncActions();
        render();
        renderMap();
    };
    control('[data-layer-edit-name]').onclick = async () => {
        const session = state.layer;
        const value = await window.travelManagerLayerNameEditor?.show({
            name: state.layer.name,
            icon: state.layer.icon || '',
            showTitle: state.layer.show_title === true,
        });
        if (
            value &&
            session === state.layer &&
            !state.transitioning &&
            (value.name !== state.layer.name ||
                value.icon !== (state.layer.icon || '') ||
                value.showTitle !== (state.layer.show_title === true))
        ) {
            state.layer.name = value.name;
            state.layer.icon = value.icon;
            state.layer.show_title = value.showTitle;
            recordChange();
            setStatus('UNSAVED_STATUS');
            render();
            renderMap();
        }
    };
    saveButton.onclick = () => {
        if (!state.transitioning) return save();
    };
    ['hidden', 'locked'].forEach((flag) => {
        control(`[data-element-menu-${flag}]`).onclick = () => {
            if (!menuElement || state.transitioning || state.mode || endDrag)
                return;
            menuElement[flag] = !menuElement[flag];
            if (state.selected === menuElement) {
                state.selected = null;
                state.selectedVertex = null;
                state.selectedSegment = null;
            }
            closeMenu();
            recordChange();
            setStatus('UNSAVED_STATUS');
            syncActions();
            render();
            renderMap();
        };
    });
    const groupAction = (copy) => {
        if (state.mode || state.transitioning || endDrag || !selectedIds.size)
            return;
        const chosen = copy
            ? state.layer.elements.filter((e) => selectedIds.has(e.id))
            : targets();
        if (copy) {
            const clones = chosen.map((e) => ({
                ...structuredClone(e),
                id: uid(),
                name: `${e.name || ''} (${window.i18n.t('LAYER_EDITOR.COPY_SUFFIX')})`,
            }));
            state.layer.elements.push(...clones);
            selectedIds.clear();
            clones.forEach((e) => selectedIds.add(e.id));
        } else {
            state.layer.elements = state.layer.elements.filter(
                (e) => !chosen.includes(e)
            );
            selectedIds.clear();
        }
        recordChange();
        setStatus('UNSAVED_STATUS');
        syncActions();
        render();
        renderMap();
    };
    control('[data-group-all]').onclick = () => {
        if (state.mode || state.transitioning || endDrag) return;
        const eligible = state.layer.elements.filter((e) => !e.hidden);
        const all = eligible.every((e) => selectedIds.has(e.id));
        clearSelection();
        if (!all) eligible.forEach((e) => selectedIds.add(e.id));
        syncActions();
        render();
        renderMap();
    };
    for (const [action, flag] of [
        ['hide', 'hidden'],
        ['lock', 'locked'],
    ]) {
        control(`[data-group-${action}]`).onclick = () => {
            if (state.mode || state.transitioning || endDrag) return;
            const chosen = state.layer.elements.filter((e) =>
                selectedIds.has(e.id)
            );
            if (!chosen.length) return;
            const value = flag === 'hidden' || !chosen.every((e) => e.locked);
            chosen.forEach((e) => {
                e[flag] = value;
            });
            if (flag === 'hidden') selectedIds.clear();
            recordChange();
            setStatus('UNSAVED_STATUS');
            syncActions();
            render();
            renderMap();
        };
    }
    control('[data-group-copy]').onclick = () => groupAction(true);
    control('[data-group-delete]').onclick = () => groupAction(false);
    control('[data-element-menu-duplicate]').onclick = () => {
        if (!menuElement || state.transitioning || state.mode || endDrag)
            return;
        const copy = structuredClone(menuElement);
        copy.id = uid();
        copy.name = `${copy.name || window.i18n.t('LAYER_EDITOR.POINTS')} (${window.i18n.t('LAYER_EDITOR.COPY_SUFFIX')})`;
        state.layer.elements.push(copy);
        closeMenu();
        recordChange();
        setStatus('UNSAVED_STATUS');
        select(copy);
    };
    control('[data-element-menu-rename]').onclick = () => {
        if (menuElement && !menuElement.locked) {
            state.renamingId = menuElement.id;
            closeMenu();
            render();
        }
    };
    control('[data-element-menu-delete]').onclick = () =>
        menuElement && removeElement(menuElement);
    control('[data-layer-close]').onclick = close;
    let preferredWidth = 380,
        widthPending = false,
        widthWrite = Promise.resolve();
    try {
        const stored = Number(
            localStorage.getItem('travel-manager-layer-panel-width')
        );
        if (Number.isFinite(stored) && stored > 0) preferredWidth = stored;
    } catch (error) {}
    const applyPanelWidth = () => {
        const available = Math.max(
            1,
            window.innerWidth - (window.innerWidth <= 560 ? 16 : 36)
        );
        const value = Math.max(
            Math.min(300, available),
            Math.min(preferredWidth, 680, available)
        );
        panel.style.setProperty('--layer-panel-width', `${value}px`);
        toolsPanel.style.setProperty('--layer-sidebar-width', `${value}px`);
    };
    const persistPanelWidth = () => {
        const value = Math.round(preferredWidth);
        widthPending = true;
        try {
            localStorage.setItem(
                'travel-manager-layer-panel-width',
                String(value)
            );
        } catch (error) {}
        widthWrite = widthWrite
            .catch(() => {})
            .then(() =>
                api('/api/settings/ui', {
                    method: 'PATCH',
                    body: JSON.stringify({ layer_editor_panel_width: value }),
                })
            )
            .then(() => {
                if (preferredWidth === value) widthPending = false;
            })
            .catch(() => {
                setStatus('WIDTH_SAVE_FAILED', true);
            });
    };
    applyPanelWidth();
    window.addEventListener('resize', applyPanelWidth);
    grabber?.addEventListener('pointerdown', (event) => {
        if (event.button !== 0 || event.isPrimary === false) return;
        event.preventDefault();
        const startX = event.clientX,
            startWidth = panel.getBoundingClientRect().width,
            original = preferredWidth;
        panel.classList.add('is-resizing');
        const move = (next) => {
            if (next.pointerId !== event.pointerId) return;
            preferredWidth = Math.max(
                300,
                Math.min(680, startWidth + startX - next.clientX)
            );
            applyPanelWidth();
        };
        const stop = (next, cancel = false) => {
            if (
                next?.pointerId !== undefined &&
                next.pointerId !== event.pointerId
            )
                return;
            document.removeEventListener('pointermove', move);
            document.removeEventListener('pointerup', stop);
            document.removeEventListener('pointercancel', cancelResize);
            window.removeEventListener('blur', cancelResize);
            panel.classList.remove('is-resizing');
            if (cancel) {
                preferredWidth = original;
                applyPanelWidth();
            } else persistPanelWidth();
        };
        const cancelResize = (next) => stop(next, true);
        document.addEventListener('pointermove', move);
        document.addEventListener('pointerup', stop);
        document.addEventListener('pointercancel', cancelResize);
        window.addEventListener('blur', cancelResize);
    });
    document.addEventListener('click', (event) => {
        if (
            !elementMenu.contains(event.target) &&
            !event.target.closest('.layer-panel__element-more')
        )
            closeMenu();
    });
    document.addEventListener('keydown', (event) => {
        if (
            event.defaultPrevented ||
            state.transitioning ||
            document
                .querySelector('#dialog-layer')
                ?.classList.contains('dialog-layer--open') ||
            panel.getAttribute('aria-hidden') === 'true'
        )
            return;
        if (
            event.target?.closest?.(
                'input,textarea,select,[contenteditable="true"]'
            )
        )
            return;
        if (
            (event.ctrlKey || event.metaKey) &&
            !event.altKey &&
            ['z', 'y'].includes(event.key.toLowerCase())
        ) {
            event.preventDefault();
            restoreHistory(
                event.key.toLowerCase() === 'y' || event.shiftKey ? 1 : -1
            );
            return;
        }
        if (
            state.mode &&
            ['Escape', 'Enter', 'Backspace'].includes(event.key)
        ) {
            event.preventDefault();
            if (event.key === 'Escape') {
                stopDrawing(false);
                setStatus(hasChanges() ? 'UNSAVED_STATUS' : null);
            } else if (event.key === 'Enter') stopDrawing();
            else {
                if (state.drawing.length > (state.continuation ? 1 : 0))
                    state.drawing.pop();
                preview?.remove();
                preview = null;
                if (state.drawing.length && lastPointer)
                    mapMove({ latlng: lastPointer });
                setStatus(hasChanges() ? 'UNSAVED_STATUS' : null);
            }
            return;
        }
        if (event.key !== 'Escape' || endDrag) return;
        if (elementMenu.getAttribute('aria-hidden') === 'false') {
            event.preventDefault();
            closeMenu(true);
            return;
        }
        if (state.selected || selectedIds.size) {
            event.preventDefault();
            clearSelection();
        }
    });
    window.travelManagerLayerEditor = {
        open,
        close,
        duplicate: (layer) => open(layer, { duplicate: true }),
        isDrawing: () => Boolean(state.mode),
        clearSelectionOnMapClick: () => {
            if (state.transitioning) return true;
            if (!state.selected && !selectedIds.size) return false;
            clearSelection();
            return true;
        },
    };
    setTimeout(() => {
        map = window.travelManagerMap?.map || map;
        if (map) {
            map.on('click', mapClick);
            map.on('mousemove', mapMove);
            map.getContainer?.().addEventListener('mouseleave', hideCoordinateTooltip);
        }
    }, 0);
});
