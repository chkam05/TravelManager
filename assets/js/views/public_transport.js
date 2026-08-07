document.addEventListener('travel-manager:views-ready', () => {
    const view = document.querySelector('[data-app-view="public-transport"]');
    const content = view?.querySelector('#public-transport-content');
    const headers = Array.from(view?.querySelectorAll('[data-public-transport-header]') || []);

    if (!view || !content || !headers.length) {
        return;
    }

    const carrierMarkup = content.innerHTML;
    const state = {
        provider: '',
        current: { screen: 'carriers', url: '' },
        history: [],
        root: 'lines',
        request: null,
        progressTimer: null,
        loading: false
    };

    const normalize = (value) => String(value || '')
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLocaleLowerCase('pl-PL')
        .trim();

    const endpoint = (screen) => {
        const provider = encodeURIComponent(state.provider);
        return `/api/public-transport/${provider}/${screen}`;
    };

    const showHeader = (screen) => {
        headers.forEach((header) => {
            const active = header.dataset.publicTransportHeader === screen;
            header.hidden = !active;
            header.classList.toggle('public-transport-header--active', active);
        });
    };

    const clearProgressTimer = () => {
        window.clearTimeout(state.progressTimer);
        state.progressTimer = null;
    };

    const renderLoading = (screen) => {
        content.innerHTML = `
            <div class="public-transport-view__loading">
                <i data-lucide="loader-circle" aria-hidden="true"></i>
                <span>Ładowanie danych…</span>
                <div class="public-transport-view__progress">
                    <progress value="0" max="1" data-public-transport-progress hidden></progress>
                    <span data-public-transport-progress-text>Przygotowywanie danych…</span>
                </div>
            </div>
        `;
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };

    const pollDownloadProgress = async () => {
        clearProgressTimer();

        if (!state.loading) {
            return;
        }

        try {
            const response = await fetch(`${endpoint('progress')}?t=${Date.now()}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const progress = await response.json();
            const bar = content.querySelector('[data-public-transport-progress]');
            const text = content.querySelector('[data-public-transport-progress-text]');
            const hasMultipleItems = progress.total > 1;

            if (bar) {
                bar.hidden = !hasMultipleItems;
                if (hasMultipleItems) {
                    bar.max = progress.total;
                    bar.value = progress.status === 'complete'
                        ? progress.total
                        : Math.max(0, progress.current - 1);
                }
            }

            if (text && progress.status === 'downloading') {
                const position = progress.total > 0
                    ? ` (${progress.current}/${progress.total})`
                    : '';
                const retry = progress.attempt > 1
                    ? ` — próba ${progress.attempt}/${progress.max_attempts}`
                    : '';
                text.textContent = progress.item
                    ? `Pobieranie „${progress.item}”${position}${retry}…`
                    : 'Przygotowywanie danych…';
            }
        } catch (error) {
            // The main request remains responsible for reporting download errors.
        }

        if (state.loading) {
            state.progressTimer = window.setTimeout(pollDownloadProgress, 250);
        }
    };

    const selectedDateFromUrl = (url) => {
        const pathMatch = String(url || '').match(/\/(20\d{6})\//);

        if (pathMatch) {
            return `${pathMatch[1].slice(0, 4)}-${pathMatch[1].slice(4, 6)}-${pathMatch[1].slice(6, 8)}`;
        }

        try {
            return new URL(String(url || '')).searchParams.get('data') || '';
        } catch (error) {
            return '';
        }
    };

    const fragmentMetadata = () => {
        const element = content.querySelector('[data-public-transport-metadata]');

        if (!element) {
            return {};
        }

        try {
            return JSON.parse(element.textContent || '{}');
        } catch (error) {
            return {};
        }
    };

    const setLinePill = (header, metadata) => {
        const pill = header.querySelector('[data-public-transport-header-line-pill]');

        if (!pill) {
            return;
        }

        const icon = document.createElement('i');
        icon.dataset.lucide = metadata.type === 'tram' ? 'tram-front' : 'bus';
        icon.setAttribute('aria-hidden', 'true');
        const number = document.createElement('strong');
        number.textContent = metadata.line || '';
        pill.replaceChildren(icon, number);
        pill.className = `public-transport-line-pill public-transport-line-pill--${metadata.type || 'bus'}`;
    };

    const fillDateSelect = (scope, metadata, screen) => {
        const select = scope.querySelector('[data-public-transport-date]');
        const field = select?.closest('label');
        const dates = Array.isArray(metadata.dates) ? metadata.dates : [];

        if (!select || !field) {
            return;
        }

        select.replaceChildren();
        dates.forEach((item) => {
            const option = document.createElement('option');
            option.value = item.url;
            option.dataset.date = item.date;
            option.dataset.screen = item.screen || screen;
            option.textContent = item.label;
            select.append(option);
        });

        const selectedDate = selectedDateFromUrl(state.current.url);
        const selected = Array.from(select.options).find(
            (option) => option.dataset.date === selectedDate
        );

        if (selected) {
            select.value = selected.value;
        }

        field.hidden = !dates.length;
    };

    const updateHeader = (screen) => {
        showHeader(screen);
        const header = headers.find(
            (item) => item.dataset.publicTransportHeader === screen
        );

        if (!header) {
            return;
        }

        const metadata = fragmentMetadata();
        setLinePill(header, metadata);

        header.querySelectorAll('[data-public-transport-header-line]').forEach((element) => {
            element.textContent = metadata.line || '';
        });
        header.querySelectorAll('[data-public-transport-header-stop]').forEach((element) => {
            element.textContent = metadata.stop || '';
        });

        const details = header.querySelector('[data-public-transport-header-details]');

        if (details) {
            if (screen === 'line-stop') {
                const platform = metadata.show_platforms
                    ? ` · stanowisko ${metadata.platform || '—'}`
                    : '';
                details.textContent = `Kierunek: ${metadata.direction || '—'}${platform}`;
            } else if (screen === 'ride') {
                const platform = metadata.show_platforms && metadata.platform
                    ? ` · stanowisko ${metadata.platform}`
                    : '';
                details.textContent = `Odjazd ${metadata.departure || '—'}${platform}`;
            } else if (screen === 'stop-lines') {
                const platform = metadata.show_platforms
                    ? `Stanowisko ${metadata.platform || '—'} · `
                    : '';
                details.textContent = `${platform}${metadata.directions_count || 0} kierunków`;
            }
        }

        const controlScope = content.querySelector('.public-transport-detail') || header;
        const control = (selector) => controlScope.querySelector(selector) || header.querySelector(selector);
        const directionSelect = control('[data-public-transport-direction-select]');
        const directionField = directionSelect?.closest('label');
        const directions = Array.isArray(metadata.directions) ? metadata.directions : [];
        const routeVariants = metadata.route_variants
            && typeof metadata.route_variants === 'object'
            ? Object.entries(metadata.route_variants)
            : [];
        const routeVariantGroups = metadata.route_variant_groups || {};

        if (directionSelect) {
            const options = routeVariants.length
                ? routeVariants.map(([name, url]) => ({
                    label: name,
                    value: url,
                    group: routeVariantGroups[name] || 'standard'
                }))
                : directions.map((name, index) => ({
                    label: name,
                    value: String(index)
                }));
            if (routeVariants.length && window.travelManagerRouteVariantDropdown) {
                window.travelManagerRouteVariantDropdown.enhance(
                    directionSelect,
                    options,
                    state.current.url,
                    (value) => {
                        directionSelect.value = value;
                        directionSelect.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                );
            } else {
                directionSelect.replaceChildren();
                options.forEach((optionData) => {
                    const option = document.createElement('option');
                    option.value = optionData.value;
                    option.textContent = optionData.label;
                    directionSelect.append(option);
                });
            }
        }

        if (directionField) {
            directionField.hidden = !directions.length && !routeVariants.length;
            const label = directionField.querySelector('span');

            if (label) {
                label.textContent = metadata.direction_label || 'Kierunek';
            }
        }

        const mapButton = control('[data-public-transport-map]');
        const latitude = Number(metadata.latitude);
        const longitude = Number(metadata.longitude);
        const hasCoordinates = (
            metadata.latitude !== null
            && metadata.latitude !== undefined
            && metadata.latitude !== ''
            && metadata.longitude !== null
            && metadata.longitude !== undefined
            && metadata.longitude !== ''
            && Number.isFinite(latitude)
            && Number.isFinite(longitude)
        );
        const canSearchStop = Boolean(
            metadata.show_stop_map && metadata.stop
        );

        if (mapButton) {
            mapButton.hidden = !hasCoordinates && !canSearchStop;
            mapButton.dataset.name = metadata.stop || 'Przystanek';
            mapButton.dataset.query = metadata.stop || '';
            mapButton.dataset.latitude = hasCoordinates ? String(latitude) : '';
            mapButton.dataset.longitude = hasCoordinates ? String(longitude) : '';
        }

        const routeButton = control('[data-public-transport-route]');
        const route = Array.isArray(metadata.route)
            ? metadata.route.filter((point) => (
                Number.isFinite(Number(point.latitude))
                && Number.isFinite(Number(point.longitude))
            ))
            : [];

        if (routeButton) {
            const canShowRoute = Boolean(metadata.show_route_map && route.length >= 2);
            routeButton.hidden = !canShowRoute;
            routeButton.disabled = !canShowRoute;
            routeButton.dataset.route = JSON.stringify(route);
            routeButton.dataset.name = metadata.line
                ? `Przebieg linii ${metadata.line}`
                : 'Przebieg przejazdu';
        }

        const vehiclesButton = control(
            '[data-public-transport-vehicles]'
        );

        if (vehiclesButton) {
            const canShowVehicles = Boolean(
                metadata.show_vehicle_positions
                && metadata.line
            );
            vehiclesButton.hidden = !canShowVehicles;
            vehiclesButton.disabled = !canShowVehicles;
            vehiclesButton.dataset.line = metadata.line || '';
            vehiclesButton.dataset.type = metadata.type || '';
            vehiclesButton.dataset.feed = metadata.vehicle_feed || '';
        }

        fillDateSelect(controlScope.querySelector('[data-public-transport-date]') ? controlScope : header, metadata, screen);
        header.querySelector('form')?.reset();
    };

    const fitDepartureTiles = () => {
        const grids = Array.from(
            content.querySelectorAll('.public-transport-line-stop__departures')
        );
        const buttons = grids.flatMap(
            (grid) => Array.from(grid.querySelectorAll(':scope > button'))
        );

        if (!grids.length || !buttons.length) {
            return;
        }

        const measurement = document.createElement('div');
        measurement.className = 'public-transport-line-stop__departures';
        Object.assign(measurement.style, {
            position: 'absolute',
            left: '-10000px',
            top: '0',
            display: 'flex',
            width: 'max-content',
            visibility: 'hidden',
            pointerEvents: 'none'
        });
        buttons.forEach((button) => {
            const clone = button.cloneNode(true);
            clone.style.width = 'max-content';
            clone.style.flex = 'none';
            measurement.append(clone);
        });
        content.append(measurement);

        const intrinsicWidth = Math.ceil(Math.max(
            74,
            ...Array.from(measurement.children).map(
                (button) => button.getBoundingClientRect().width
            )
        ));
        measurement.remove();

        const availableWidth = Math.max(
            74,
            Math.min(...grids.map((grid) => grid.clientWidth - 26))
        );
        const tileWidth = Math.min(intrinsicWidth, availableWidth);
        grids.forEach((grid) => grid.style.setProperty(
            '--public-transport-departure-width',
            `${tileWidth}px`
        ));
    };

    const enhanceFragment = (screen) => {
        updateHeader(screen);
        initializeDetailSidebar();
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
        if (screen === 'line-stop') {
            window.requestAnimationFrame(fitDepartureTiles);
        }
    };

    const initializeDetailSidebar = () => {
        const shell = content.querySelector('[data-public-transport-detail-sidebar]');
        const grabber = shell?.querySelector('[data-public-transport-detail-sidebar-grabber]');
        if (!shell || !grabber) return;
        const resize = { x: 0, width: 0 };
        const move = (event) => {
            const computed = getComputedStyle(shell);
            const min = parseFloat(computed.minWidth) || 260;
            const max = parseFloat(computed.maxWidth) || 620;
            const width = Math.min(Math.max(resize.width + resize.x - event.clientX, min), max);
            shell.style.setProperty('--public-transport-detail-sidebar-width', `${width}px`);
        };
        const stop = () => {
            shell.classList.remove('public-transport-detail__sidebar-shell--resizing');
            document.removeEventListener('pointermove', move);
            document.removeEventListener('pointerup', stop);
        };
        grabber.addEventListener('pointerdown', (event) => {
            event.preventDefault();
            resize.x = event.clientX;
            resize.width = shell.getBoundingClientRect().width;
            shell.classList.add('public-transport-detail__sidebar-shell--resizing');
            document.addEventListener('pointermove', move);
            document.addEventListener('pointerup', stop);
        });
    };

    const loadScreen = async (
        screen,
        url = '',
        pushHistory = true,
        refresh = false
    ) => {
        const next = { screen, url };

        if (pushHistory && state.current?.screen !== 'carriers') {
            state.history.push(state.current);
        }

        state.current = next;
        state.request?.abort();
        state.request = new AbortController();
        state.loading = true;
        clearProgressTimer();
        showHeader(screen);
        renderLoading(screen);

        const params = new URLSearchParams();

        if (url) {
            params.set('url', url);
        }
        if (refresh) {
            params.set('refresh', '1');
        }

        pollDownloadProgress();

        try {
            const response = await fetch(`${endpoint(screen)}${params.size ? `?${params}` : ''}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                signal: state.request.signal
            });
            const html = await response.text();

            if (state.current !== next) {
                return;
            }

            state.loading = false;
            clearProgressTimer();
            content.innerHTML = html;
            enhanceFragment(screen);
        } catch (error) {
            if (error.name === 'AbortError') {
                return;
            }

            state.loading = false;
            clearProgressTimer();
            content.innerHTML = `
                <div class="public-transport-error" role="alert">
                    <i data-lucide="circle-alert" aria-hidden="true"></i>
                    <h2>Nie udało się załadować widoku</h2>
                    <p data-public-transport-error-message></p>
                    <button type="button" data-public-transport-retry>
                        <i data-lucide="refresh-cw" aria-hidden="true"></i>
                        <span>Spróbuj ponownie</span>
                    </button>
                </div>
            `;
            content.querySelector('[data-public-transport-error-message]').textContent = error.message;
            enhanceFragment(screen);
        }
    };

    const showCarriers = () => {
        state.request?.abort();
        state.loading = false;
        clearProgressTimer();
        state.provider = '';
        state.current = { screen: 'carriers', url: '' };
        state.history = [];
        content.innerHTML = carrierMarkup;
        showHeader('carriers');
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };

    const loadRoot = (root) => {
        state.root = root;
        state.history = [];
        loadScreen(root, '', false);
    };

    const goBack = () => {
        const previous = state.history.pop();

        if (previous) {
            loadScreen(previous.screen, previous.url, false);
        } else if (state.provider) {
            loadRoot(state.root);
        } else {
            showCarriers();
        }
    };

    const filterItems = (screen, query) => {
        const words = normalize(query).split(/\s+/).filter(Boolean);
        const items = Array.from(content.querySelectorAll('[data-public-transport-filter-item]'));

        items.forEach((item) => {
            const value = normalize(item.dataset.search);
            item.hidden = !words.every((word) => value.includes(word));
        });

        const groupSelector = screen === 'lines'
            ? '.public-transport-lines__group'
            : screen === 'stops'
                ? '.public-transport-stops__city'
                : '';

        if (groupSelector) {
            content.querySelectorAll(groupSelector).forEach((group) => {
                const hasMatch = Boolean(
                    group.querySelector('[data-public-transport-filter-item]:not([hidden])')
                );
                group.hidden = !hasMatch;

                if (screen === 'stops') {
                    const collapse = group.querySelector('[data-public-transport-collapse]');
                    const target = collapse
                        ? document.getElementById(collapse.getAttribute('aria-controls'))
                        : null;
                    const expanded = words.length > 0 && hasMatch;

                    collapse?.setAttribute('aria-expanded', String(expanded));
                    if (target) {
                        target.hidden = !expanded;
                    }
                }
            });
        }
    };

    const showOnMap = async (name, latitude, longitude, query = '') => {
        let element;
        const hasCoordinates = (
            latitude !== ''
            && longitude !== ''
            && Number.isFinite(Number(latitude))
            && Number.isFinite(Number(longitude))
        );

        if (hasCoordinates) {
            const lat = Number(latitude);
            const lon = Number(longitude);
            element = {
                place_id: `public-transport:${lat}:${lon}`,
                display_name: name || 'Przystanek',
                name: { name: name || 'Przystanek' },
                coordinates: {
                    latitude: lat,
                    longitude: lon
                }
            };
        } else {
            const suffix = (
                state.provider === 'czestochowa'
                && !normalize(query).includes('czestochowa')
            )
                ? ', Częstochowa'
                : '';
            const searchQuery = `${query || name || 'Przystanek'}${suffix}`;
            try {
                const params = new URLSearchParams({ q: searchQuery });
                const response = await fetch(`/api/map/search?${params}`, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const data = await response.json();
                element = data.place?.selected || data.place?.elements?.[0];
                if (!response.ok || !element?.coordinates) {
                    throw new Error(
                        data.message || 'Nie znaleziono położenia przystanku.'
                    );
                }
            } catch (error) {
                window.travelManagerAlert?.(error.message, 'error');
                return;
            }
        }

        window.travelManagerNavigation?.showView('map');
        window.setTimeout(() => {
            const opensStopView = state.current.screen === 'line-stop';
            const lineHistory = [...state.history].reverse().find((item) => item?.screen === 'line');
            window.travelManagerPublicTransportPanel?.open({
                provider: state.provider,
                screen: opensStopView ? 'line-stop' : 'lines',
                url: opensStopView ? state.current.url : '',
                showStop: opensStopView,
                stopCoordinates: element.coordinates,
                lineUrl: lineHistory?.url || ''
            });
            if (!opensStopView) {
                window.travelManagerMap?.showPublicTransportStop(
                    element.coordinates.latitude,
                    element.coordinates.longitude,
                    name || 'Przystanek'
                );
            }
        }, 0);
    };

    const showRouteOnMap = (name, value) => {
        try {
            const points = JSON.parse(value || '[]');

            if (!Array.isArray(points) || points.length < 2) {
                return;
            }

            window.travelManagerNavigation?.showView('map');
            window.setTimeout(() => {
                window.travelManagerPublicTransportPanel?.open({
                    provider: state.provider,
                    screen: state.current.screen === 'line' ? 'line' : 'lines',
                    url: state.current.screen === 'line' ? state.current.url : '',
                    showRoute: state.current.screen === 'line'
                });
            }, 0);
        } catch (error) {
            // Invalid route metadata is ignored.
        }
    };

    const showVehiclesOnMap = async (line, transportType = '', feed = '') => {
        try {
            const params = new URLSearchParams({ line });
            if (transportType) params.set('type', transportType);
            if (feed) params.set('feed', feed);
            const response = await fetch(`${endpoint('vehicles')}?${params}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || 'Nie udało się pobrać pozycji pojazdów.'
                );
            }
            if (!Array.isArray(data.positions) || !data.positions.length) {
                throw new Error(`Brak aktywnych pojazdów linii ${line}.`);
            }

            window.travelManagerNavigation?.showView('map');
            window.setTimeout(() => {
                window.travelManagerPublicTransportPanel?.open({
                    provider: state.provider,
                    screen: state.current.screen === 'line' ? 'line' : 'lines',
                    url: state.current.screen === 'line' ? state.current.url : '',
                    vehicles: state.current.screen === 'line' ? data.positions : []
                });
            }, 0);
        } catch (error) {
            window.travelManagerAlert?.(error.message, 'error');
        }
    };

    view.querySelectorAll('[data-public-transport-search]').forEach((form) => {
        const input = form.querySelector('input');
        const run = () => filterItems(form.dataset.publicTransportSearch, input?.value || '');

        form.addEventListener('submit', (event) => {
            event.preventDefault();
            run();
        });
        input?.addEventListener('input', run);
    });

    view.addEventListener('change', (event) => {
        const direction = event.target.closest('[data-public-transport-direction-select]');

        if (direction) {
            if (/^https?:\/\//.test(direction.value)) {
                loadScreen('line', direction.value, false);
                return;
            }
            content.querySelectorAll('[data-public-transport-direction]').forEach((section) => {
                section.hidden = section.dataset.publicTransportDirection !== direction.value;
            });
            const metadata = fragmentMetadata();
            const route = Array.isArray(metadata.routes?.[Number(direction.value)])
                ? metadata.routes[Number(direction.value)]
                : metadata.route;
            const routeButton = content.querySelector('[data-public-transport-route]');
            if (routeButton && Array.isArray(route)) {
                routeButton.dataset.route = JSON.stringify(route);
                const canShowRoute = Boolean(metadata.show_route_map && route.length >= 2);
                routeButton.hidden = !canShowRoute;
                routeButton.disabled = !canShowRoute;
            }
            return;
        }

        const date = event.target.closest('[data-public-transport-date]');
        const option = date?.selectedOptions[0];

        if (option?.value) {
            loadScreen(option.dataset.screen || state.current.screen, option.value, false);
        }
    });

    view.addEventListener('click', (event) => {
        const provider = event.target.closest('[data-public-transport-provider]');

        if (provider) {
            state.provider = provider.dataset.publicTransportProvider;
            state.root = 'lines';
            state.history = [];
            loadScreen('lines', '', false);
            return;
        }

        if (event.target.closest('[data-public-transport-carriers]')) {
            showCarriers();
            return;
        }

        const root = event.target.closest('[data-public-transport-root]');

        if (root) {
            loadRoot(root.dataset.publicTransportRoot);
            return;
        }

        if (event.target.closest('[data-public-transport-refresh]')) {
            loadScreen(state.current.screen, state.current.url, false, true);
            return;
        }

        const mapAction = event.target.closest('[data-public-transport-map]');

        if (mapAction) {
            showOnMap(
                mapAction.dataset.name,
                mapAction.dataset.latitude,
                mapAction.dataset.longitude,
                mapAction.dataset.query
            );
            return;
        }

        const routeAction = event.target.closest('[data-public-transport-route]');

        if (routeAction) {
            showRouteOnMap(
                routeAction.dataset.name,
                routeAction.dataset.route
            );
            return;
        }

        const vehiclesAction = event.target.closest(
            '[data-public-transport-vehicles]'
        );

        if (vehiclesAction?.dataset.line) {
            showVehiclesOnMap(
                vehiclesAction.dataset.line,
                vehiclesAction.dataset.type || '',
                vehiclesAction.dataset.feed || ''
            );
            return;
        }

        const collapse = event.target.closest('[data-public-transport-collapse]');

        if (collapse) {
            const target = document.getElementById(collapse.getAttribute('aria-controls'));
            const expanded = collapse.getAttribute('aria-expanded') === 'true';
            collapse.setAttribute('aria-expanded', String(!expanded));

            if (target) {
                target.hidden = expanded;
            }
            return;
        }

        const stopToggle = event.target.closest('.public-transport-stops__toggle');

        if (stopToggle) {
            const target = document.getElementById(stopToggle.getAttribute('aria-controls'));
            const expanded = stopToggle.getAttribute('aria-expanded') === 'true';
            stopToggle.setAttribute('aria-expanded', String(!expanded));

            if (target) {
                target.hidden = expanded;
            }
            return;
        }

        if (event.target.closest('[data-public-transport-back]')) {
            goBack();
            return;
        }

        if (event.target.closest('[data-public-transport-retry]')) {
            loadScreen(state.current.screen, state.current.url, false);
            return;
        }

        const announcement = event.target.closest('[data-public-transport-announcement]');

        if (announcement) {
            try {
                const summary = JSON.parse(
                    announcement.dataset.publicTransportAnnouncement
                );
                const dialog = window.travelManagerPublicTransportAnnouncement;
                dialog?.open({
                    ...summary,
                    content: summary.content || 'Pobieranie treści komunikatu…'
                });
                if (!summary.url || summary.content) {
                    return;
                }
                const params = new URLSearchParams({ url: summary.url });
                fetch(`${endpoint('announcement')}?${params}`, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                    .then(async (response) => {
                        const data = await response.json();
                        if (!response.ok) {
                            throw new Error(data.error || 'Nie udało się pobrać komunikatu.');
                        }
                        return data;
                    })
                    .then((details) => dialog?.update(details))
                    .catch((error) => dialog?.update({
                        ...summary,
                        content: error.message
                    }));
            } catch (error) {
                // Invalid announcement metadata is ignored.
            }
            return;
        }

        const action = event.target.closest('[data-public-transport-action]');

        if (action?.dataset.url) {
            loadScreen(action.dataset.publicTransportAction, action.dataset.url);
        }
    });

    showHeader('carriers');
});
