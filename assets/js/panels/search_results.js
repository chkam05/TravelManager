document.addEventListener('travel-manager:views-ready', () => {
    const panel = document.querySelector('#search-results-panel');
    const title = document.querySelector('#search-results-panel-title');
    const subtitle = document.querySelector('#search-results-panel-subtitle');
    const status = document.querySelector('#search-results-panel-status');
    const retryButton = document.querySelector('#search-results-panel-retry');
    const list = document.querySelector('#search-results-panel-list');
    const closeButton = document.querySelector('[data-search-results-panel-close]');
    const grabber = document.querySelector('[data-search-results-panel-grabber]');

    if (!panel || !title || !subtitle || !status || !retryButton || !list || !closeButton) {
        return;
    }

    const state = {
        results: [],
        retryHandler: null
    };

    const patchUiSettings = (data) => fetch('/api/settings/ui', {
        method: 'PATCH',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).catch(() => {});

    const loadUiSettings = async () => {
        try {
            const response = await fetch('/api/settings/ui', {
                headers: { 'Accept': 'application/json' }
            });
            const data = response.ok ? await response.json() : null;
            const width = Number(data?.ui?.search_results_panel_width);

            if (Number.isFinite(width) && width > 0) {
                panel.style.setProperty('--search-results-panel-width', `${width}px`);
            }
        } catch (error) {
            // Defaults keep the panel usable.
        }
    };

    const coordinatesOf = (result) => {
        const element = result.element || result.favourite?.place_data || {};
        const latitude = Number(result.latitude ?? result.favourite?.latitude ?? element?.coordinates?.latitude);
        const longitude = Number(result.longitude ?? result.favourite?.longitude ?? element?.coordinates?.longitude);

        return { latitude, longitude };
    };

    const close = () => {
        panel.classList.remove('search-results-panel--open');
        panel.setAttribute('aria-hidden', 'true');
    };

    const open = () => {
        panel.classList.add('search-results-panel--open');
        panel.setAttribute('aria-hidden', 'false');
        window.travelManagerLegendDetailsPanel?.close();
        window.travelManagerLayerDetailsPanel?.close();
    };

    const setStatus = (message) => {
        status.textContent = message || '';
    };

    const setRetry = (handler = null) => {
        state.retryHandler = handler;
        retryButton.hidden = !handler;
    };

    const resultTitle = (result) => (
        result.title
        || result.favourite?.name
        || result.element?.name?.name
        || result.element?.display_name
        || 'Wynik wyszukiwania'
    );

    const resultSubtitle = (result) => (
        result.subtitle
        || result.favourite?.place_data?.display_name
        || result.element?.display_name
        || result.favourite?.tag?.name
        || ''
    );

    const resultIcon = (result) => {
        if (result.favourite) {
            return result.favourite.icon || result.favourite.tag?.icon || '⭐';
        }

        return '⌖';
    };

    const elementForResult = (result) => {
        const coordinates = coordinatesOf(result);
        const element = result.element || result.favourite?.place_data || {};

        return {
            ...element,
            display_name: element.display_name || resultSubtitle(result) || resultTitle(result),
            coordinates: {
                ...(element.coordinates || {}),
                latitude: coordinates.latitude,
                longitude: coordinates.longitude
            }
        };
    };

    const showResult = (result) => {
        if (result.favourite) {
            window.travelManagerMap?.showFavourite(result.favourite);
            return;
        }

        window.travelManagerMap?.showElement(elementForResult(result), resultTitle(result));
    };

    const addToRoute = (result) => {
        const element = elementForResult(result);
        const routePanel = window.travelManagerRouteDetailsPanel;

        if (routePanel?.isActive()) {
            routePanel.addElement(resultTitle(result), element);
        } else {
            routePanel?.openWithDestination(resultTitle(result), element);
        }

        close();
    };

    const addToFavourites = async (result) => {
        const element = elementForResult(result);
        const existing = window.travelManagerFavourites?.findByElement(element);
        const editorResult = await window.travelManagerFavouritesEditor?.show({
            name: existing?.name || resultTitle(result),
            tagId: existing?.tag_id || '',
            icon: existing?.icon || null,
            editing: Boolean(existing)
        });

        if (!editorResult) {
            return;
        }

        await window.travelManagerFavourites?.save({
            favourite: existing,
            element,
            name: editorResult.name,
            tagId: editorResult.tagId,
            icon: editorResult.icon
        });
    };

    const createAction = (icon, label, onClick) => {
        const button = document.createElement('button');
        button.className = 'search-results-panel__action';
        button.type = 'button';
        button.title = label;
        button.setAttribute('aria-label', label);
        button.innerHTML = `<i data-lucide="${icon}" aria-hidden="true"></i>`;
        button.addEventListener('click', (event) => {
            event.stopPropagation();
            onClick();
        });

        return button;
    };

    const render = () => {
        list.replaceChildren();

        if (!state.results.length) {
            const empty = document.createElement('p');
            empty.className = 'search-results-panel__empty';
            empty.textContent = 'Brak wyników w wybranym obszarze.';
            list.append(empty);
            return;
        }

        state.results.forEach((result) => {
            const coordinates = coordinatesOf(result);
            const item = document.createElement('article');
            item.className = 'search-results-panel__item';
            item.tabIndex = 0;

            const icon = document.createElement('span');
            icon.className = 'search-results-panel__item-icon';
            icon.textContent = resultIcon(result);

            const content = document.createElement('div');
            content.className = 'search-results-panel__item-content';

            const itemTitle = document.createElement('strong');
            itemTitle.className = 'search-results-panel__item-title';
            itemTitle.textContent = resultTitle(result);

            const itemSubtitle = document.createElement('span');
            itemSubtitle.className = 'search-results-panel__item-subtitle';
            itemSubtitle.textContent = resultSubtitle(result);

            const coordinateText = document.createElement('span');
            coordinateText.className = 'search-results-panel__item-coordinates';
            coordinateText.textContent = Number.isFinite(coordinates.latitude) && Number.isFinite(coordinates.longitude)
                ? `${coordinates.latitude.toFixed(6)}, ${coordinates.longitude.toFixed(6)}`
                : '-';

            const actions = document.createElement('div');
            actions.className = 'search-results-panel__item-actions';
            actions.append(createAction(
                window.travelManagerRouteDetailsPanel?.isActive() ? 'plus' : 'route',
                window.travelManagerRouteDetailsPanel?.isActive() ? 'Dodaj do trasy' : 'Trasa',
                () => addToRoute(result)
            ));

            if (!result.favourite) {
                actions.append(
                    createAction('star', 'Dodaj do ulubionych', () => addToFavourites(result))
                );
            }

            content.append(itemTitle, itemSubtitle, coordinateText);
            item.append(icon, content, actions);
            item.addEventListener('dblclick', () => showResult(result));
            item.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    showResult(result);
                }
            });
            list.append(item);
        });

        window.lucide?.createIcons({
            attrs: { 'stroke-width': 1.7 }
        });
    };

    const show = ({ title: nextTitle = 'Wyniki wyszukiwania', subtitle: nextSubtitle = '', results = [] } = {}) => {
        state.results = Array.isArray(results) ? results : [];
        title.textContent = nextTitle;
        subtitle.textContent = nextSubtitle;
        setRetry(null);
        setStatus(`${state.results.length} wyników`);
        render();
        open();
    };

    const showLoading = ({ title: nextTitle = 'Wyniki wyszukiwania', subtitle: nextSubtitle = '' } = {}) => {
        state.results = [];
        title.textContent = nextTitle;
        subtitle.textContent = nextSubtitle;
        setRetry(null);
        setStatus('Szukam...');
        list.replaceChildren();

        const loading = document.createElement('p');
        loading.className = 'search-results-panel__loading';
        loading.textContent = 'Wyszukiwanie trwa, zaraz coś tu wyląduje.';
        list.append(loading);
        open();
    };

    const showError = ({
        title: nextTitle = 'Wyniki wyszukiwania',
        subtitle: nextSubtitle = 'Nie udało się wykonać wyszukiwania.',
        message = 'Nie udało się wykonać wyszukiwania.',
        retry = null
    } = {}) => {
        state.results = [];
        title.textContent = nextTitle;
        subtitle.textContent = nextSubtitle;
        setRetry(retry);
        setStatus(message);
        list.replaceChildren();

        const empty = document.createElement('p');
        empty.className = 'search-results-panel__empty';
        empty.textContent = 'Możesz ponowić wyszukiwanie albo zmienić obszar mapy.';
        list.append(empty);
        open();
        window.lucide?.createIcons({
            attrs: { 'stroke-width': 1.7 }
        });
    };

    const resize = {
        startX: 0,
        startWidth: 0
    };

    const getPanelBounds = () => {
        const computed = window.getComputedStyle(panel);

        return {
            min: Number.parseFloat(computed.minWidth) || 260,
            max: Number.parseFloat(computed.maxWidth) || 620
        };
    };

    const onPointerMove = (event) => {
        const bounds = getPanelBounds();
        const nextWidth = resize.startWidth + resize.startX - event.clientX;
        const width = Math.min(Math.max(nextWidth, bounds.min), bounds.max);

        panel.style.setProperty('--search-results-panel-width', `${width}px`);
    };

    const stopResize = () => {
        panel.classList.remove('search-results-panel--resizing');
        document.removeEventListener('pointermove', onPointerMove);
        document.removeEventListener('pointerup', stopResize);
        patchUiSettings({
            search_results_panel_width: Math.round(panel.getBoundingClientRect().width)
        });
    };

    if (grabber) {
        grabber.addEventListener('pointerdown', (event) => {
            event.preventDefault();
            resize.startX = event.clientX;
            resize.startWidth = panel.getBoundingClientRect().width;
            panel.classList.add('search-results-panel--resizing');
            document.addEventListener('pointermove', onPointerMove);
            document.addEventListener('pointerup', stopResize);
        });
    }

    closeButton.addEventListener('click', close);
    retryButton.addEventListener('click', () => {
        if (state.retryHandler) {
            state.retryHandler();
        }
    });
    loadUiSettings();

    window.travelManagerSearchResultsPanel = {
        close,
        open,
        showError,
        showLoading,
        setStatus,
        show
    };
});
