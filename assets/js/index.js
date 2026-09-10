document.addEventListener('DOMContentLoaded', async () => {
    await window.i18n.ready;
    const menuButton = document.querySelector('.header__menu-button');
    const sideMenu = document.querySelector('#side-menu');
    const appShell = document.querySelector('.app-shell');
    const headerViews = document.querySelectorAll('[data-header-view]');
    const carButtons = document.querySelectorAll('.header__car-button');
    const carButtonTexts = document.querySelectorAll('.header__car-button-text');
    const viewContainers = document.querySelectorAll('[data-app-view][data-view-url]');
    const panelContainers = document.querySelectorAll('[data-panel-url]');
    const dialogLayer = document.querySelector('#dialog-layer');
    const navigationButtons = document.querySelectorAll('[data-navigation-view]');
    let activeCarProfile = null;
    let currentView = appShell?.dataset.currentView || 'map';
    let previousPublicTransportView = currentView === 'home' ? 'home' : 'map';
    let notificationTimer = null;
    const carButtonViews = new Set(['map', 'car-profiles']);

    const renderLocalLucideFallbacks = () => {
        document.querySelectorAll('[data-lucide="layers-plus"]').forEach((element) => {
            const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.setAttribute('class', `${element.className || ''} lucide lucide-layers-plus`.trim());
            svg.setAttribute('viewBox', '0 0 24 24');
            svg.setAttribute('fill', 'none');
            svg.setAttribute('stroke', 'currentColor');
            svg.setAttribute('stroke-width', '1.7');
            svg.setAttribute('stroke-linecap', 'round');
            svg.setAttribute('stroke-linejoin', 'round');
            svg.setAttribute('aria-hidden', 'true');
            svg.innerHTML = '<path d="m12 2 9 5-9 5-9-5 9-5Z"></path><path d="m3 12 9 5 4-2.22"></path><path d="m3 17 9 5 3-1.67"></path><path d="M19 15v6"></path><path d="M16 18h6"></path>';
            element.replaceWith(svg);
        });
    };

    renderLocalLucideFallbacks();
    window.lucide?.createIcons({
        attrs: {
            'stroke-width': 1.7
        }
    });

    document.addEventListener('click', async (event) => {
        const link = event.target.closest('[data-external-url]');

        if (!link) {
            return;
        }

        event.preventDefault();
        const url = link.href;
        const api = window.pywebview?.api;

        if (api?.open_external_url) {
            try {
                const result = await api.open_external_url(url);

                if (result?.status === 'opened') {
                    return;
                }
            } catch (error) {
                // Browser fallback remains available outside the native bridge.
            }
        }

        window.open(url, '_blank', 'noopener,noreferrer');
    });

    const setMenuOpen = (open) => {
        sideMenu?.classList.toggle('side-menu--open', open);
        menuButton?.setAttribute('aria-expanded', String(open));
        sideMenu?.setAttribute('aria-hidden', String(!open));
    };

    const updateCarButton = () => {
        carButtons.forEach((button) => {
            button.hidden = !activeCarProfile || !carButtonViews.has(currentView);
        });

        carButtonTexts.forEach((text) => {
            text.textContent = activeCarProfile
                ? (activeCarProfile.name || [activeCarProfile.brand, activeCarProfile.model].filter(Boolean).join(' ') || window.i18n.t('APP_SHELL.DEFAULT_CAR'))
                : window.i18n.t('APP_SHELL.DEFAULT_CAR');
        });
    };

    const updateHeaderView = (viewName) => {
        headerViews.forEach((headerView) => {
            const active = headerView.dataset.headerView === viewName;
            headerView.classList.toggle('header__view--active', active);
            headerView.hidden = !active;
        });

        updateCarButton();
    };

    menuButton?.addEventListener('click', () => {
        setMenuOpen(!sideMenu?.classList.contains('side-menu--open'));
    });

    document.addEventListener('click', (event) => {
        if (!sideMenu?.classList.contains('side-menu--open')) {
            return;
        }

        if (sideMenu.contains(event.target) || menuButton?.contains(event.target)) {
            return;
        }

        setMenuOpen(false);
    });

    const loadFragment = async (element, url) => {
        if (!element || !url) {
            return;
        }

        const response = await fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (!response.ok) {
            throw new Error(`View request failed: ${response.status}`);
        }

        element.innerHTML = await response.text();
    };

    let currentPublicTransportMode = 'city';

    const showView = (viewName, options = {}) => {
        const target = document.querySelector(`[data-app-view="${viewName}"]`);

        if (!target) {
            return false;
        }

        document.querySelectorAll('[data-app-view]').forEach((view) => {
            const active = view === target;
            view.classList.toggle('app-view--active', active);
            view.hidden = !active;
        });

        if (
            viewName === 'public-transport'
            && ['city', 'rail'].includes(options.publicTransportMode)
        ) {
            currentPublicTransportMode = options.publicTransportMode;
        }

        navigationButtons.forEach((button) => {
            const buttonMode = button.dataset.publicTransportMode || '';
            const active = button.dataset.navigationView === viewName
                && (!buttonMode || buttonMode === currentPublicTransportMode);
            button.classList.toggle('side-menu__item--active', active);
            button.setAttribute('aria-current', active ? 'page' : 'false');
        });

        if (viewName === 'public-transport' && currentView !== 'public-transport') {
            previousPublicTransportView = ['home', 'map'].includes(currentView)
                ? currentView
                : 'map';
        }
        currentView = viewName;
        appShell.dataset.currentView = viewName;

        updateHeaderView(viewName);

        setMenuOpen(false);

        if (viewName === 'map') {
            window.setTimeout(() => window.travelManagerMap?.map?.invalidateSize(), 0);
        }

        document.dispatchEvent(new CustomEvent('travel-manager:app-view-changed', {
            detail: {
                view: viewName,
                publicTransportMode: currentPublicTransportMode
            }
        }));

        return true;
    };

    const showNotification = (message, type = 'success') => {
        let notification = document.querySelector('[data-app-notification]');

        if (!notification) {
            notification = document.createElement('div');
            notification.className = 'app-notification';
            notification.dataset.appNotification = '';
            notification.setAttribute('role', 'status');
            notification.setAttribute('aria-live', 'polite');
            document.body.append(notification);
        }

        window.clearTimeout(notificationTimer);
        notification.className = `app-notification app-notification--${type}`;
        notification.textContent = message;
        notification.hidden = false;
        notificationTimer = window.setTimeout(() => {
            notification.hidden = true;
        }, 3500);
    };

    document.addEventListener('click', async (event) => {
        const viewButton = event.target.closest('[data-navigation-view]');

        if (viewButton) {
            showView(viewButton.dataset.navigationView, {
                publicTransportMode: viewButton.dataset.publicTransportMode
            });
            return;
        }

        const actionButton = event.target.closest('[data-navigation-action]');

        if (actionButton?.dataset.navigationAction === 'new-route') {
            showView('map');
            await window.travelManagerRouteDetailsPanel?.startNewRoute();
        } else if (actionButton?.dataset.navigationAction === 'new-layer') {
            showView('map');
            window.travelManagerLayerEditor?.open();
        }
    });

    document.addEventListener('click', (event) => {
        if (event.target.closest('[data-app-back-to-map]')) {
            showView('map');
        }
    });
    carButtons.forEach((button) => button.addEventListener('click', () => {
        if (activeCarProfile) {
            window.travelManagerCarDetailsPanel?.open(activeCarProfile);
            return;
        }

        showView('car-profiles');
    }));
    document.addEventListener('click', async (event) => {
        const button = event.target.closest('[data-settings-save]');

        if (!button || button.disabled) {
            return;
        }

        button.disabled = true;
        const pendingSaves = [];
        document.dispatchEvent(new CustomEvent('travel-manager:settings-save-requested', {
            detail: {
                waitUntil: (promise) => pendingSaves.push(Promise.resolve(promise))
            }
        }));
        const results = await Promise.all(pendingSaves);
        button.disabled = false;

        if (results.every((result) => result !== false)) {
            showNotification(window.i18n.t('APP_SHELL.SETTINGS_SAVED'));
            return;
        }

        showNotification(window.i18n.t('APP_SHELL.SETTINGS_SAVE_FAILED'), 'error');
    });

    try {
        await Promise.all([
            ...Array.from(viewContainers).map((element) => loadFragment(element, element.dataset.viewUrl)),
            ...Array.from(panelContainers).map((element) => loadFragment(element, element.dataset.panelUrl)),
            loadFragment(dialogLayer, dialogLayer?.dataset.dialogUrl)
        ]);
    } catch (error) {
        const mapView = document.querySelector('[data-app-view="map"]');

        if (mapView) {
            mapView.textContent = window.i18n.t('APP_SHELL.VIEW_LOAD_FAILED');
        }
    }

    document.dispatchEvent(new CustomEvent('travel-manager:views-ready'));
    renderLocalLucideFallbacks();
    window.lucide?.createIcons({
        attrs: {
            'stroke-width': 1.7
        }
    });

    const leavePublicTransport = () => showView(previousPublicTransportView || 'map');
    window.travelManagerNavigation = { showView, leavePublicTransport };

    document.addEventListener('travel-manager:car-profiles-changed', (event) => {
        activeCarProfile = event.detail?.activeCarProfile || null;
        updateCarButton();
    });
});
