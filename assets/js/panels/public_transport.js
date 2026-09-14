document.addEventListener('travel-manager:views-ready', () => {
    const t = window.i18n.t;
    const locale = window.i18n.locale.replace('_', '-');
    const panel = document.querySelector('#public-transport-panel');
    const content = panel?.querySelector('[data-public-transport-panel-content]');
    const providerSelect = panel?.querySelector('[data-public-transport-panel-provider]');
    const searchInput = panel?.querySelector('[data-public-transport-panel-search]');
    const title = panel?.querySelector('[data-public-transport-panel-title]');
    const backButton = panel?.querySelector('[data-public-transport-panel-back]');
    const mapButton = panel?.querySelector('[data-public-transport-panel-map]');
    const vehiclesButton = panel?.querySelector('[data-public-transport-panel-vehicles]');
    const stopMapButton = panel?.querySelector('[data-public-transport-panel-stop-map]');
    const liveStatus = panel?.querySelector('[data-public-transport-panel-live-status]');
    const liveStatusText = panel?.querySelector('[data-public-transport-panel-live-status-text]');
    const closeButton = panel?.querySelector('[data-public-transport-panel-close]');
    const grabber = panel?.querySelector('[data-public-transport-panel-grabber]');
    const allLinesButton = panel?.querySelector('[data-public-transport-panel-all-lines]');
    const emptyState = panel?.querySelector('[data-public-transport-panel-empty]');
    const updateButton = panel?.querySelector('[data-public-transport-panel-update]');
    const modeButtons = Array.from(panel?.querySelectorAll('[data-public-transport-panel-mode]') || []);
    const lineSort = window.travelManagerPublicTransportLineSort?.enhance(
        panel?.querySelector('[data-public-transport-panel-line-sort]'),
        () => view('lines')
    );

    if (!panel || !content || !providerSelect || !title || !backButton || !mapButton || !closeButton) return;

    const providerDropdown = window.travelManagerPublicTransportProviderDropdown?.enhance(
        providerSelect
    );

    const state = {
        provider: '', screen: 'lines', url: '', history: [], metadata: {},
        fragment: null, directionIndex: 0, routeVisible: false,
        stopVisible: false, vehiclesVisible: false,
        vehicleBackgroundUpdates: false, vehicleUpdateInterval: 15,
        vehicleTimer: null, vehicleRequestActive: false,
        lineMetadata: null, lineUrl: '', requestKey: null, transportMode: 'city',
        providersByMode: { city: '', rail: '' }
    };
    const view = (screen = state.screen) => content.querySelector(`[data-public-transport-panel-view="${screen}"]`);
    const endpoint = (screen) => `/api/public-transport/${state.provider}/${screen}`;
    const patchUi = (data) => fetch('/api/settings/ui', {
        method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
    }).catch(() => {});
    const saveProvider = (provider) => fetch('/api/settings/public-transport', {
        method: 'PATCH', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider, mode: state.transportMode })
    }).catch(() => {});
    const providerMode = (provider) => String(provider || '').startsWith('rail_') ? 'rail' : 'city';
    const applyTransportMode = (mode, selectFirst = false) => {
        state.transportMode = mode === 'rail' ? 'rail' : 'city';
        modeButtons.forEach((button) => {
            const active = button.dataset.publicTransportPanelMode === state.transportMode;
            button.classList.toggle('public-transport-panel__mode-button--active', active);
            button.setAttribute('aria-checked', String(active));
        });
        providerDropdown?.setMode(state.transportMode);
        const current = providerSelect.selectedOptions[0];
        if (selectFirst || !current || (current.dataset.mode || 'city') !== state.transportMode) {
            const preferred = state.providersByMode[state.transportMode];
            const first = Array.from(providerSelect.options).find(
                (option) => option.value === preferred
                    && (option.dataset.mode || 'city') === state.transportMode
            ) || Array.from(providerSelect.options).find(
                (option) => (option.dataset.mode || 'city') === state.transportMode
            );
            if (first) providerSelect.value = first.value;
        }
        providerDropdown?.sync();
    };
    const metadataFrom = (fragment) => {
        try { return JSON.parse(fragment.querySelector('[data-public-transport-metadata]')?.textContent || '{}'); }
        catch (error) { return {}; }
    };
    const selectedDate = (url) => {
        try { return new URL(url, window.location.origin).searchParams.get('date') || ''; }
        catch (error) { return ''; }
    };
    const setActiveView = () => {
        content.querySelectorAll('[data-public-transport-panel-view]').forEach((item) => {
            item.hidden = item.dataset.publicTransportPanelView !== state.screen;
        });
    };
    const status = (message) => {
        setActiveView();
        const host = view();
        host.querySelectorAll('.public-transport-panel__status').forEach((item) => item.remove());
        const item = document.createElement('p');
        item.className = 'public-transport-panel__status';
        item.textContent = message;
        host.append(item);
    };
    const fillSelect = (select, items, selectedValue, onChange) => {
        select.replaceChildren();
        items.forEach((item) => {
            const option = document.createElement('option');
            option.value = item.value;
            option.textContent = item.label;
            option.dataset.screen = item.screen || '';
            option.dataset.date = item.date || '';
            select.append(option);
        });
        if (items.some((item) => item.value === selectedValue)) select.value = selectedValue;
        select.onchange = () => onChange(select.value, select.selectedOptions[0]);
    };
    const setRouteVisible = (visible) => {
        state.routeVisible = Boolean(visible && state.lineMetadata);
        mapButton.classList.toggle('public-transport-panel__icon-button--active', state.routeVisible);
        mapButton.setAttribute('aria-pressed', String(state.routeVisible));
        const label = state.routeVisible
            ? t('PANEL_PUBLIC_TRANSPORT.HIDE_ROUTE')
            : t('PUBLIC_TRANSPORT_VIEW.SHOW_ON_MAP');
        mapButton.title = label;
        mapButton.setAttribute('aria-label', label);
    };
    const clearRoute = () => {
        window.travelManagerMap?.clearPublicTransportRoute();
        setRouteVisible(false);
    };
    const setStopVisible = (visible) => {
        state.stopVisible = Boolean(visible && state.screen !== 'line' && state.screen !== 'lines');
        stopMapButton?.classList.toggle('public-transport-panel__icon-button--active', state.stopVisible);
        stopMapButton?.setAttribute('aria-pressed', String(state.stopVisible));
        if (stopMapButton) {
            const label = state.stopVisible
                ? t('PANEL_PUBLIC_TRANSPORT.HIDE_STOP')
                : t('PANEL_PUBLIC_TRANSPORT.SHOW_STOP_ON_MAP');
            stopMapButton.title = label;
            stopMapButton.setAttribute('aria-label', label);
            const icon = document.createElement('i');
            icon.dataset.lucide = state.stopVisible ? 'map-pin-off' : 'map-pin';
            icon.setAttribute('aria-hidden', 'true');
            stopMapButton.replaceChildren(icon);
            window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
        }
    };
    const clearStop = () => {
        window.travelManagerMap?.clearPublicTransportStop();
        setStopVisible(false);
    };
    const setVehiclesVisible = (visible) => {
        state.vehiclesVisible = Boolean(visible && state.lineMetadata);
        vehiclesButton?.classList.toggle('public-transport-panel__icon-button--active', state.vehiclesVisible);
        vehiclesButton?.setAttribute('aria-pressed', String(state.vehiclesVisible));
        if (vehiclesButton) {
            const label = state.vehiclesVisible
                ? t('PANEL_PUBLIC_TRANSPORT.HIDE_VEHICLES')
                : t('PANEL_PUBLIC_TRANSPORT.SHOW_VEHICLES_ON_MAP');
            vehiclesButton.title = label;
            vehiclesButton.setAttribute('aria-label', label);
        }
        scheduleVehicleRefresh();
    };
    const clearVehicles = () => {
        window.clearTimeout(state.vehicleTimer); state.vehicleTimer = null;
        window.travelManagerMap?.clearPublicTransportVehicles();
        setVehiclesVisible(false);
    };
    const setLiveStatus = (message = '') => {
        if (!liveStatus || !liveStatusText) return;
        liveStatus.hidden = !state.vehiclesVisible;
        liveStatusText.textContent = message;
    };
    const scheduleVehicleRefresh = () => {
        window.clearTimeout(state.vehicleTimer); state.vehicleTimer = null;
        if (!state.vehiclesVisible) { setLiveStatus(''); return; }
        if (!state.vehicleBackgroundUpdates) {
            setLiveStatus(t('PANEL_PUBLIC_TRANSPORT.BACKGROUND_UPDATES_DISABLED'));
            return;
        }
        setLiveStatus(t('PANEL_PUBLIC_TRANSPORT.WAITING_FOR_NEXT_UPDATE', {
            seconds: state.vehicleUpdateInterval
        }));
        state.vehicleTimer = window.setTimeout(async () => {
            setLiveStatus(t('PANEL_PUBLIC_TRANSPORT.SEARCHING_VEHICLE_POSITIONS'));
            await new Promise((resolve) => window.setTimeout(resolve, 180));
            if (!state.vehiclesVisible) return;
            await refreshVehicles(true);
            scheduleVehicleRefresh();
        }, state.vehicleUpdateInterval * 1000);
    };
    const refreshVehicles = async (silent = false) => {
        const line = state.lineMetadata?.line;
        if (state.vehicleRequestActive || !line) return false;
        state.vehicleRequestActive = true;
        setLiveStatus(t('PANEL_PUBLIC_TRANSPORT.LOADING_VEHICLE_DATA'));
        try {
            const params = new URLSearchParams({ line });
            if (state.lineMetadata?.type) {
                params.set('type', state.lineMetadata.type);
            }
            if (state.lineMetadata?.vehicle_feed) {
                params.set('feed', state.lineMetadata.vehicle_feed);
            }
            const response = await fetch(`${endpoint('vehicles')}?${params}`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
            setLiveStatus(t('PANEL_PUBLIC_TRANSPORT.PROCESSING_VEHICLE_POSITIONS'));
            const data = await response.json();
            if (!response.ok || !Array.isArray(data.positions) || !data.positions.length) {
                throw new Error(
                    data.error || t('PANEL_PUBLIC_TRANSPORT.NO_ACTIVE_VEHICLES', { line })
                );
            }
            window.travelManagerMap?.showPublicTransportVehicles(
                data.positions,
                t('PANEL_PUBLIC_TRANSPORT.VEHICLES_OF_LINE', { line }),
                !silent
            );
            setVehiclesVisible(true);
            return true;
        } catch (error) {
            if (!silent) window.travelManagerAlert?.(error.message, 'error');
            return false;
        } finally { state.vehicleRequestActive = false; }
    };
    const updateHeader = () => {
        setActiveView();
        title.textContent = state.screen === 'lines'
            ? t('PUBLIC_TRANSPORT_VIEW.TITLE')
            : state.screen === 'line'
                ? t('PUBLIC_TRANSPORT_LINES.LINE_NUMBER', {
                    line: state.metadata.line || ''
                })
                : state.metadata.stop || t('PUBLIC_TRANSPORT_LINES.LINE_NUMBER', {
                    line: state.metadata.line || ''
                });
        const isRoot = state.screen === 'lines';
        const route = state.lineMetadata?.routes?.[state.directionIndex]
            || state.lineMetadata?.route
            || [];
        const canShowRoute = Boolean(
            state.lineMetadata?.show_route_map
            && Array.isArray(route)
            && route.length >= 2
        );
        backButton.hidden = isRoot;
        mapButton.hidden = isRoot || !canShowRoute;
        mapButton.disabled = !canShowRoute;
        if (vehiclesButton) vehiclesButton.hidden = isRoot || !state.lineMetadata?.show_vehicle_positions || !state.lineMetadata?.line;
        if (vehiclesButton) vehiclesButton.disabled = !state.lineMetadata?.show_vehicle_positions || !state.lineMetadata?.line;
        if (stopMapButton) {
            const canShowStop = ['line-stop', 'stop-lines'].includes(state.screen)
                && state.metadata?.show_stop_map !== false;
            stopMapButton.hidden = !canShowStop;
            stopMapButton.disabled = !canShowStop;
        }
        if (isRoot) { setRouteVisible(false); setStopVisible(false); setVehiclesVisible(false); }
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };
    const renderLines = () => {
        const host = view('lines').querySelector('[data-public-transport-panel-lines]');
        const lines = state.fragment.querySelector('.public-transport-lines');
        host.replaceChildren(lines
            ? lines.cloneNode(true)
            : document.createTextNode(t('PUBLIC_TRANSPORT_LINES.NO_LINES_SHORT')));
        emptyState.hidden = true;
        host.hidden = false;
        searchInput.closest('label').hidden = false;
        searchInput.value = '';
        window.travelManagerSizePublicTransportLineTiles?.(content);
        lineSort?.apply();
    };
    const renderNoData = () => {
        state.screen = 'lines'; state.url = ''; state.history = []; state.metadata = {};
        updateHeader();
        view('lines').querySelector('[data-public-transport-panel-lines]').hidden = true;
        emptyState.hidden = false;
        searchInput.closest('label').hidden = true;
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };
    const hasLocalData = async () => {
        try {
            const response = await fetch(`${endpoint('availability')}?t=${Date.now()}`);
            return response.ok && Boolean((await response.json()).available);
        } catch (error) { return false; }
    };
    const renderStops = (index) => {
        const host = view('line').querySelector('[data-public-transport-panel-stops]');
        const sections = state.fragment.querySelectorAll('[data-public-transport-direction]');
        const list = sections[index]?.querySelector('.public-transport-line-view__stops');
        host.replaceChildren(list
            ? list.cloneNode(true)
            : document.createTextNode(t('PUBLIC_TRANSPORT_STOPS.NO_STOPS_SHORT')));
    };
    const renderLine = () => {
        const lineView = view('line');
        const directionSelect = lineView.querySelector('[data-public-transport-panel-direction]');
        const directionField = lineView.querySelector('[data-public-transport-panel-direction-field]');
        const directionLabel = lineView.querySelector('[data-public-transport-panel-direction-label]');
        const dateSelect = lineView.querySelector('[data-public-transport-panel-line-date]');
        const dateField = lineView.querySelector('[data-public-transport-panel-line-date-field]');
        const variants = Object.entries(state.metadata.route_variants || {});
        const groups = state.metadata.route_variant_groups || {};
        const directions = variants.length
            ? variants.map(([label, value]) => ({ label, value, group: groups[label] || 'standard' }))
            : (state.metadata.directions || []).map((label, index) => ({ label, value: String(index) }));
        const dates = (state.metadata.dates || []).map((item) => ({ label: item.label, value: item.url, date: item.date }));
        state.lineMetadata = state.metadata;
        state.lineUrl = state.url;
        state.directionIndex = 0;
        directionLabel.textContent = state.metadata.direction_label || t('PUBLIC_TRANSPORT_VIEW.DIRECTION');
        directionField.hidden = !directions.length;
        const changeDirection = (value) => {
            if (/^https?:\/\//.test(value)) { load('line', value, true); return; }
            state.directionIndex = Number(value) || 0;
            renderStops(state.directionIndex);
            if (state.routeVisible) showCurrentRoute();
        };
        if (variants.length && window.travelManagerRouteVariantDropdown) {
            window.travelManagerRouteVariantDropdown.enhance(
                directionSelect,
                directions,
                state.url,
                changeDirection
            );
        } else {
            fillSelect(directionSelect, directions, '0', changeDirection);
        }
        dateField.hidden = !dates.length;
        const currentDate = selectedDate(state.url);
        fillSelect(dateSelect, dates, dates.find((item) => item.date === currentDate)?.value || dates[0]?.value, (value) => {
            load('line', value, true);
        });
        renderStops(0);
        if (state.routeVisible) showCurrentRoute();
    };
    const renderLineStop = () => {
        const stopView = view('line-stop');
        const dateSelect = stopView.querySelector('[data-public-transport-panel-stop-date]');
        const dateField = stopView.querySelector('[data-public-transport-panel-stop-date-field]');
        const departures = stopView.querySelector('[data-public-transport-panel-departures]');
        const dates = (state.metadata.dates || []).map((item) => ({ label: item.label, value: item.url, date: item.date, screen: item.screen }));
        dateField.hidden = !dates.length;
        const currentDate = selectedDate(state.url);
        fillSelect(dateSelect, dates, dates.find((item) => item.date === currentDate)?.value || dates[0]?.value, (value, option) => {
            load(option.dataset.screen || 'line-stop', value, true);
        });
        const days = state.fragment.querySelector('.public-transport-line-stop__days');
        departures.replaceChildren(days
            ? days.cloneNode(true)
            : document.createTextNode(t('PUBLIC_TRANSPORT_VIEW.NO_DEPARTURES')));
    };
    const renderStopLines = () => {
        const host = view('stop-lines').querySelector('[data-public-transport-panel-stop-lines]');
        const list = state.fragment.querySelector('.public-transport-stop-lines__list');
        host.replaceChildren(list
            ? list.cloneNode(true)
            : document.createTextNode(t('PUBLIC_TRANSPORT_STOPS.NO_LINES_AT_STOP')));
    };
    const render = () => {
        content.querySelectorAll('.public-transport-panel__status').forEach((item) => item.remove());
        if (state.screen === 'line') {
            state.lineMetadata = state.metadata;
            state.lineUrl = state.url;
        }
        updateHeader();
        if (state.screen === 'lines') renderLines();
        else if (state.screen === 'line') renderLine();
        else if (state.screen === 'line-stop') renderLineStop();
        else renderStopLines();
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };
    async function load(screen, url = '', push = false, refresh = false) {
        if (push) state.history.push({ screen: state.screen, url: state.url });
        if (screen === 'lines') { clearRoute(); clearVehicles(); clearStop(); state.lineMetadata = null; state.lineUrl = ''; }
        if (screen === 'stop-lines') clearVehicles();
        state.screen = screen;
        state.url = url;
        status(t('PUBLIC_TRANSPORT_VIEW.LOADING_DATA'));
        updateHeader();
        const identity = JSON.stringify([state.provider, screen, url, Boolean(refresh)]);
        window.travelManagerPublicTransportRequests?.setForeground(state.requestKey, false);
        try {
            const task = window.travelManagerPublicTransportRequests.request({
                provider: state.provider, screen, url, refresh
            });
            state.requestKey = task.key;
            window.travelManagerPublicTransportRequests.setForeground(task.key, true);
            const html = await task.promise;
            if (identity !== JSON.stringify([state.provider, state.screen, state.url, Boolean(refresh)])) return false;
            const fragment = document.createElement('div');
            fragment.innerHTML = html;
            state.fragment = fragment; state.metadata = metadataFrom(fragment); render(); return true;
        } catch (error) {
            if (identity === JSON.stringify([state.provider, state.screen, state.url, Boolean(refresh)])) status(error.message);
            return false;
        }
    }
    const showCurrentRoute = () => {
        const metadata = state.lineMetadata || {};
        const route = metadata.routes?.[state.directionIndex] || metadata.route || [];
        window.travelManagerMap?.showPublicTransportRoute(
            route,
            t('PUBLIC_TRANSPORT_LINES.LINE_NUMBER', { line: metadata.line || '' })
        );
        setRouteVisible(true);
    };
    const activateCurrentLine = async () => {
        if (!state.lineMetadata) return;
        showCurrentRoute();
        await refreshVehicles(true);
    };
    const open = async (options = {}) => {
        panel.classList.add('public-transport-panel--open'); panel.setAttribute('aria-hidden', 'false');
        window.travelManagerLegendDetailsPanel?.close(); window.travelManagerLayerDetailsPanel?.close();
        if (window.travelManagerDownloadStatus?.reopen('panel')) return;
        state.provider = options.provider || state.provider || providerSelect.value;
        applyTransportMode(options.mode || providerMode(state.provider));
        if ([...providerSelect.options].some((option) => option.value === state.provider)) providerSelect.value = state.provider;
        providerDropdown?.sync();
        saveProvider(state.provider); state.history = []; clearRoute(); clearStop(); clearVehicles();
        if (!(await hasLocalData())) { renderNoData(); return; }
        const targetScreen = options.screen || 'lines';
        if (options.lineUrl && targetScreen !== 'line') {
            await load('line', options.lineUrl, false);
            state.history = [{ screen: 'line', url: options.lineUrl }];
        }
        await load(targetScreen, options.url || '', false);
        if (state.lineMetadata) {
            showCurrentRoute();
            if (!Array.isArray(options.vehicles) || !options.vehicles.length) {
                await refreshVehicles(true);
            }
        }
        if (state.screen !== 'line' && state.screen !== 'lines') {
            window.travelManagerMap?.showPublicTransportStop(
                options.stopCoordinates?.latitude ?? state.metadata.latitude,
                options.stopCoordinates?.longitude ?? state.metadata.longitude,
                state.metadata.stop || t('PUBLIC_TRANSPORT_RIDE.STOP')
            );
            setStopVisible(true);
        }
        if (Array.isArray(options.vehicles) && options.vehicles.length && state.lineMetadata) {
            window.travelManagerMap?.showPublicTransportVehicles(
                options.vehicles,
                t('PANEL_PUBLIC_TRANSPORT.VEHICLES_OF_LINE', {
                    line: state.lineMetadata.line || ''
                })
            );
            setVehiclesVisible(true);
        }
    };
    const close = () => {
        window.travelManagerPublicTransportRequests?.setForeground(state.requestKey, false);
        panel.classList.remove('public-transport-panel--open'); panel.setAttribute('aria-hidden', 'true');
        clearRoute(); clearStop(); clearVehicles();
        state.lineMetadata = null; state.lineUrl = '';
    };
    providerSelect.addEventListener('change', () => {
        state.provider = providerSelect.value;
        state.providersByMode[state.transportMode] = state.provider;
        saveProvider(state.provider); state.history = []; clearRoute(); clearStop(); clearVehicles();
        hasLocalData().then((available) => available ? load('lines') : renderNoData());
    });
    modeButtons.forEach((button) => button.addEventListener('click', () => {
        const mode = button.dataset.publicTransportPanelMode;
        if (mode === state.transportMode) return;
        applyTransportMode(mode, true);
        providerSelect.dispatchEvent(new Event('change', { bubbles: true }));
    }));
    updateButton?.addEventListener('click', async () => {
        window.travelManagerDownloadStatus?.show(state.provider, 'panel');
        try {
            const loaded = await load('lines', '', false, true);
            if (!loaded) {
                throw new Error(t('PANEL_PUBLIC_TRANSPORT.LOAD_PUBLIC_TRANSPORT_DATA_FAILED'));
            }
            searchInput.closest('label').hidden = false;
            window.travelManagerDownloadStatus?.finish();
        } catch (error) {
            window.travelManagerDownloadStatus?.finish(error.message);
        }
    });
    searchInput?.addEventListener('input', () => {
        const query = searchInput.value.trim().toLocaleLowerCase(locale);
        view('lines').querySelectorAll('[data-public-transport-filter-item]').forEach((item) => {
            item.hidden = !String(item.dataset.search || '').toLocaleLowerCase(locale).includes(query);
        });
        view('lines').querySelectorAll('.public-transport-lines__group').forEach((group) => {
            group.hidden = !group.querySelector('[data-public-transport-filter-item]:not([hidden])');
        });
    });
    content.addEventListener('click', async (event) => {
        const collapse = event.target.closest('[data-public-transport-collapse]');
        if (collapse) {
            const target = content.querySelector(`#${CSS.escape(collapse.getAttribute('aria-controls') || '')}`);
            const expanded = collapse.getAttribute('aria-expanded') === 'true';
            collapse.setAttribute('aria-expanded', String(!expanded));
            if (target) target.hidden = expanded;
            return;
        }
        const action = event.target.closest('[data-public-transport-action]');
        if (!action) return;
        if (action.dataset.publicTransportAction === 'line') {
            clearRoute(); clearVehicles(); clearStop(); state.lineMetadata = null; state.lineUrl = '';
            const loaded = await load('line', action.dataset.url, true);
            if (loaded) await activateCurrentLine();
        }
        if (action.dataset.publicTransportAction === 'line-stop') {
            const loaded = await load('line-stop', action.dataset.url, true);
            if (loaded) {
                window.travelManagerMap?.showPublicTransportStop(
                    state.metadata.latitude,
                    state.metadata.longitude,
                    state.metadata.stop || t('PUBLIC_TRANSPORT_RIDE.STOP')
                );
                setStopVisible(true);
            }
        }
    });
    backButton.addEventListener('click', () => {
        const previous = state.history.pop();
        const target = previous || { screen: 'lines', url: '' };
        if (target.screen === 'lines') { clearRoute(); clearVehicles(); clearStop(); state.lineMetadata = null; state.lineUrl = ''; }
        load(target.screen, target.url, false);
    });
    mapButton.addEventListener('click', () => {
        if (state.routeVisible) clearRoute(); else showCurrentRoute();
    });
    stopMapButton?.addEventListener('click', () => {
        if (state.stopVisible) clearStop();
        else {
            window.travelManagerMap?.showPublicTransportStop(
                state.metadata.latitude,
                state.metadata.longitude,
                state.metadata.stop || t('PUBLIC_TRANSPORT_RIDE.STOP')
            );
            setStopVisible(true);
        }
    });
    vehiclesButton?.addEventListener('click', async () => {
        if (state.vehiclesVisible) { clearVehicles(); return; }
        await refreshVehicles(false);
    });
    allLinesButton?.addEventListener('click', () => load(
        'stop-lines',
        state.metadata.stop_lines_url || state.url,
        true
    ));
    closeButton.addEventListener('click', close);
    window.addEventListener('travel-manager:public-transport-download-background', (event) => {
        if (event.detail?.origin === 'panel') close();
    });

    // Prevent panel content from scrolling while a select dropdown is being scrolled.
    content.addEventListener('wheel', (event) => {
        if (event.target.closest('select')) event.preventDefault();
    }, { passive: false });
    const resize = { x: 0, width: 0 };
    const move = (event) => {
        const computed = getComputedStyle(panel); const min = parseFloat(computed.minWidth) || 280; const max = parseFloat(computed.maxWidth) || 680;
        panel.style.setProperty('--public-transport-panel-width', `${Math.min(Math.max(resize.width + resize.x - event.clientX, min), max)}px`);
    };
    const stop = () => {
        panel.classList.remove('public-transport-panel--resizing'); document.removeEventListener('pointermove', move); document.removeEventListener('pointerup', stop);
        patchUi({ public_transport_panel_width: Math.round(panel.getBoundingClientRect().width) });
    };
    grabber?.addEventListener('pointerdown', (event) => {
        resize.x = event.clientX; resize.width = panel.getBoundingClientRect().width; panel.classList.add('public-transport-panel--resizing');
        document.addEventListener('pointermove', move); document.addEventListener('pointerup', stop);
    });
    fetch('/api/settings/ui').then((response) => response.json()).then((data) => {
        const width = Number(data?.ui?.public_transport_panel_width);
        if (Number.isFinite(width)) panel.style.setProperty('--public-transport-panel-width', `${width}px`);
        state.vehicleBackgroundUpdates = data?.ui?.public_transport_vehicle_background_updates === true;
        state.vehicleUpdateInterval = Math.min(120, Math.max(5, Number(data?.ui?.public_transport_vehicle_update_interval) || 15));
        return fetch('/api/settings/public-transport');
    }).then((response) => response.json()).then((data) => {
        state.providersByMode = {
            city: String(data?.providers?.city || ''),
            rail: String(data?.providers?.rail || '')
        };
        const rememberedMode = data?.mode === 'rail' ? 'rail' : 'city';
        const provider = String(
            state.providersByMode[rememberedMode] || data?.provider || ''
        );
        if ([...providerSelect.options].some((option) => option.value === provider)) {
            providerSelect.value = provider;
        } else {
            const firstCity = Array.from(providerSelect.options).find(
                (option) => (option.dataset.mode || 'city') === 'city'
            );
            if (firstCity) providerSelect.value = firstCity.value;
        }
        applyTransportMode(rememberedMode);
        providerDropdown?.sync();
        state.provider = providerSelect.value;
    }).catch(() => { state.provider = providerSelect.value; });
    document.addEventListener('travel-manager:ui-settings-changed', (event) => {
        const detail = event.detail || {};
        if (Object.hasOwn(detail, 'public_transport_vehicle_background_updates')) {
            state.vehicleBackgroundUpdates = detail.public_transport_vehicle_background_updates === true;
        }
        if (Object.hasOwn(detail, 'public_transport_vehicle_update_interval')) {
            state.vehicleUpdateInterval = Math.min(120, Math.max(5, Number(detail.public_transport_vehicle_update_interval) || 15));
        }
        if (!Object.hasOwn(detail, 'public_transport_vehicle_background_updates') && !Object.hasOwn(detail, 'public_transport_vehicle_update_interval')) return;
        scheduleVehicleRefresh();
    });
    window.travelManagerPublicTransportPanel = { close, open };
});
