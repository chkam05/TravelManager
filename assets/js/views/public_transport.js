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
        const progress = screen === 'stops'
            ? `
                <div class="public-transport-view__progress">
                    <progress value="0" max="1" data-public-transport-progress></progress>
                    <span data-public-transport-progress-text>Przygotowywanie listy miast…</span>
                </div>
            `
            : '';

        content.innerHTML = `
            <div class="public-transport-view__loading">
                <i data-lucide="loader-circle" aria-hidden="true"></i>
                <span>Ładowanie danych…</span>
                ${progress}
            </div>
        `;
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };

    const pollStopsProgress = async () => {
        clearProgressTimer();

        if (!state.loading || state.current.screen !== 'stops') {
            return;
        }

        try {
            const response = await fetch(`${endpoint('stops-progress')}?t=${Date.now()}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const progress = await response.json();
            const bar = content.querySelector('[data-public-transport-progress]');
            const text = content.querySelector('[data-public-transport-progress-text]');

            if (bar && progress.total > 0) {
                bar.max = progress.total;
                bar.value = progress.status === 'complete'
                    ? progress.current
                    : Math.max(0, progress.current - 1);
            }

            if (text && progress.status === 'downloading') {
                const position = progress.total > 0
                    ? ` (${progress.current}/${progress.total})`
                    : '';
                text.textContent = progress.city
                    ? `Pobieranie „${progress.city}”${position}…`
                    : 'Pobieranie listy miast…';
            }
        } catch (error) {
            // The main request remains responsible for reporting download errors.
        }

        if (state.loading && state.current.screen === 'stops') {
            state.progressTimer = window.setTimeout(pollStopsProgress, 300);
        }
    };

    const selectedDateFromUrl = (url) => {
        const match = String(url || '').match(/\/(20\d{6})\//);

        if (!match) {
            return '';
        }

        return `${match[1].slice(0, 4)}-${match[1].slice(4, 6)}-${match[1].slice(6, 8)}`;
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

    const fillDateSelect = (header, metadata, screen) => {
        const select = header.querySelector('[data-public-transport-date]');
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
                details.textContent = `Kierunek: ${metadata.direction || '—'} · stanowisko ${metadata.platform || '—'}`;
            } else if (screen === 'ride') {
                const platform = metadata.platform ? ` · stanowisko ${metadata.platform}` : '';
                details.textContent = `Odjazd ${metadata.departure || '—'}${platform}`;
            } else if (screen === 'stop-lines') {
                details.textContent = `Stanowisko ${metadata.platform || '—'} · ${metadata.directions_count || 0} kierunków`;
            }
        }

        const directionSelect = header.querySelector('[data-public-transport-direction-select]');
        const directionField = directionSelect?.closest('label');
        const directions = Array.isArray(metadata.directions) ? metadata.directions : [];

        if (directionSelect) {
            directionSelect.replaceChildren();
            directions.forEach((direction, index) => {
                const option = document.createElement('option');
                option.value = String(index);
                option.textContent = direction;
                directionSelect.append(option);
            });
        }

        if (directionField) {
            directionField.hidden = !directions.length;
        }

        const mapButton = header.querySelector('[data-public-transport-map]');
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

        if (mapButton) {
            mapButton.hidden = !hasCoordinates;
            mapButton.dataset.name = metadata.stop || 'Przystanek';
            mapButton.dataset.latitude = hasCoordinates ? String(latitude) : '';
            mapButton.dataset.longitude = hasCoordinates ? String(longitude) : '';
        }

        const routeButton = header.querySelector('[data-public-transport-route]');
        const route = Array.isArray(metadata.route)
            ? metadata.route.filter((point) => (
                Number.isFinite(Number(point.latitude))
                && Number.isFinite(Number(point.longitude))
            ))
            : [];

        if (routeButton) {
            routeButton.hidden = route.length < 2;
            routeButton.dataset.route = JSON.stringify(route);
            routeButton.dataset.name = metadata.line
                ? `Przebieg linii ${metadata.line}`
                : 'Przebieg przejazdu';
        }

        fillDateSelect(header, metadata, screen);
        header.querySelector('form')?.reset();
    };

    const enhanceFragment = (screen) => {
        updateHeader(screen);
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
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

        if (screen === 'stops') {
            pollStopsProgress();
        }

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

    const showOnMap = (name, latitude, longitude) => {
        const lat = Number(latitude);
        const lon = Number(longitude);

        if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
            return;
        }

        window.travelManagerNavigation?.showView('map');
        window.setTimeout(() => {
            window.travelManagerMap?.showElement({
                place_id: `public-transport:${lat}:${lon}`,
                display_name: name || 'Przystanek',
                name: { name: name || 'Przystanek' },
                coordinates: {
                    latitude: lat,
                    longitude: lon
                }
            }, name || 'Przystanek');
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
                window.travelManagerMap?.showPublicTransportRoute(
                    points,
                    name || 'Przebieg przejazdu'
                );
            }, 0);
        } catch (error) {
            // Invalid route metadata is ignored.
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
            content.querySelectorAll('[data-public-transport-direction]').forEach((section) => {
                section.hidden = section.dataset.publicTransportDirection !== direction.value;
            });
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
                mapAction.dataset.longitude
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
                window.travelManagerPublicTransportAnnouncement?.open(
                    JSON.parse(announcement.dataset.publicTransportAnnouncement)
                );
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
