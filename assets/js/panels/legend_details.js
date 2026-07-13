document.addEventListener('travel-manager:views-ready', () => {
    const panel = document.querySelector('#legend-details-panel');
    const tabs = document.querySelector('#legend-details-panel-tabs');
    const content = document.querySelector('#legend-details-panel-content');
    const closeButton = document.querySelector('[data-legend-details-panel-close]');
    const grabber = document.querySelector('[data-legend-details-panel-grabber]');

    if (!panel || !tabs || !content || !closeButton) {
        return;
    }

    const state = {
        activeTab: 'symbols',
        loaded: false,
        loading: false,
        tabs: []
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
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                return;
            }

            const data = await response.json();
            const width = Number(data?.ui?.legend_details_panel_width);

            if (Number.isFinite(width) && width > 0) {
                panel.style.setProperty('--legend-details-panel-width', `${width}px`);
            }
        } catch (error) {
            // Missing persisted UI settings should not block panel rendering.
        }
    };

    const setStatus = (message) => {
        content.replaceChildren();

        const status = document.createElement('p');
        status.className = 'legend-details-panel__status';
        status.textContent = message;

        content.append(status);
    };

    const loadLegend = async () => {
        if (state.loaded || state.loading) {
            return;
        }

        state.loading = true;
        setStatus('Ładowanie legendy...');

        try {
            const response = await fetch('/api/map/legend', {
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Legend request failed: ${response.status}`);
            }

            const data = await response.json();
            state.tabs = data?.legend?.tabs || [];
            state.loaded = true;
        } catch (error) {
            state.tabs = [];
            setStatus('Nie udało się załadować legendy.');
        } finally {
            state.loading = false;
        }
    };

    const createLegendImage = (item) => {
        const cell = document.createElement('div');
        cell.className = 'legend-details-panel__image-cell';

        if (!item.image) {
            const fallback = document.createElement('span');
            fallback.className = 'legend-details-panel__image--missing';
            fallback.setAttribute('aria-hidden', 'true');
            cell.append(fallback);

            return cell;
        }

        const image = document.createElement('img');
        image.className = 'legend-details-panel__image';
        image.src = item.image;
        image.alt = '';
        image.loading = 'lazy';
        image.decoding = 'async';
        image.addEventListener('error', () => {
            image.remove();
            const fallback = document.createElement('span');
            fallback.className = 'legend-details-panel__image--missing';
            fallback.setAttribute('aria-hidden', 'true');
            cell.append(fallback);
        }, { once: true });

        cell.append(image);

        return cell;
    };

    const createLegendItem = (item) => {
        const row = document.createElement('div');
        row.className = 'legend-details-panel__item';

        const description = document.createElement('p');
        description.className = 'legend-details-panel__description';
        description.textContent = item.title || item.id || '-';

        row.append(createLegendImage(item), description);

        return row;
    };

    const createSection = (group) => {
        const section = document.createElement('section');
        section.className = 'legend-details-panel__section';

        const heading = document.createElement('h3');
        heading.className = 'legend-details-panel__section-title';
        heading.textContent = group.title || group.id || 'Legenda';

        const list = document.createElement('div');
        list.className = 'legend-details-panel__list';

        (group.items || []).forEach((item) => {
            list.append(createLegendItem(item));
        });

        section.append(heading, list);

        return section;
    };

    const activeTab = () => state.tabs.find((tab) => tab.id === state.activeTab) || state.tabs[0] || null;

    const renderTabs = () => {
        tabs.replaceChildren();

        state.tabs.forEach((tab) => {
            const button = document.createElement('button');
            button.className = 'legend-details-panel__tab';
            button.classList.toggle('legend-details-panel__tab--active', tab.id === state.activeTab);
            button.type = 'button';
            button.textContent = tab.label || tab.id;
            button.setAttribute('role', 'tab');
            button.setAttribute('aria-selected', String(tab.id === state.activeTab));
            button.addEventListener('click', () => {
                state.activeTab = tab.id;
                render();
            });

            tabs.append(button);
        });
    };

    const render = () => {
        const tab = activeTab();

        if (!tab) {
            setStatus('Brak danych legendy.');
            return;
        }

        state.activeTab = tab.id;
        renderTabs();
        content.replaceChildren();

        (tab.groups || []).forEach((group) => {
            content.append(createSection(group));
        });

        if (!content.children.length) {
            setStatus('Brak elementów w tej zakładce.');
        }
    };

    const open = async () => {
        panel.classList.add('legend-details-panel--open');
        panel.setAttribute('aria-hidden', 'false');
        window.travelManagerLayerDetailsPanel?.close();

        await loadLegend();

        if (state.loaded) {
            render();
        }
    };

    const close = () => {
        panel.classList.remove('legend-details-panel--open');
        panel.setAttribute('aria-hidden', 'true');
    };

    closeButton.addEventListener('click', close);

    const resize = {
        startX: 0,
        startWidth: 0
    };

    const getPanelBounds = () => {
        const computed = window.getComputedStyle(panel);

        return {
            min: Number.parseFloat(computed.minWidth) || 280,
            max: Number.parseFloat(computed.maxWidth) || 680
        };
    };

    const onPointerMove = (event) => {
        const bounds = getPanelBounds();
        const nextWidth = resize.startWidth + resize.startX - event.clientX;
        const width = Math.min(Math.max(nextWidth, bounds.min), bounds.max);

        panel.style.setProperty('--legend-details-panel-width', `${width}px`);
    };

    const stopResize = () => {
        panel.classList.remove('legend-details-panel--resizing');
        document.removeEventListener('pointermove', onPointerMove);
        document.removeEventListener('pointerup', stopResize);
        patchUiSettings({
            legend_details_panel_width: Math.round(panel.getBoundingClientRect().width)
        });
    };

    if (grabber) {
        grabber.addEventListener('pointerdown', (event) => {
            event.preventDefault();

            resize.startX = event.clientX;
            resize.startWidth = panel.getBoundingClientRect().width;

            panel.classList.add('legend-details-panel--resizing');
            document.addEventListener('pointermove', onPointerMove);
            document.addEventListener('pointerup', stopResize);
        });
    }

    loadUiSettings();
    setStatus('Legenda mapy jest gotowa do wyświetlenia.');

    window.travelManagerLegendDetailsPanel = {
        close,
        open
    };
});
