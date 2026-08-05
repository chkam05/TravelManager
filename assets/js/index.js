document.addEventListener('DOMContentLoaded', async () => {
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
    let notificationTimer = null;
    const carButtonViews = new Set(['map', 'car-profiles']);

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
                ? (activeCarProfile.name || [activeCarProfile.brand, activeCarProfile.model].filter(Boolean).join(' ') || 'Samochód')
                : 'Samochód';
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

    const showView = (viewName) => {
        const target = document.querySelector(`[data-app-view="${viewName}"]`);

        if (!target) {
            return false;
        }

        document.querySelectorAll('[data-app-view]').forEach((view) => {
            const active = view === target;
            view.classList.toggle('app-view--active', active);
            view.hidden = !active;
        });

        navigationButtons.forEach((button) => {
            const active = button.dataset.navigationView === viewName;
            button.classList.toggle('side-menu__item--active', active);
            button.setAttribute('aria-current', active ? 'page' : 'false');
        });

        currentView = viewName;
        appShell.dataset.currentView = viewName;

        updateHeaderView(viewName);

        setMenuOpen(false);

        if (viewName === 'map') {
            window.setTimeout(() => window.travelManagerMap?.map?.invalidateSize(), 0);
        }

        document.dispatchEvent(new CustomEvent('travel-manager:app-view-changed', {
            detail: { view: viewName }
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
            showView(viewButton.dataset.navigationView);
            return;
        }

        const actionButton = event.target.closest('[data-navigation-action]');

        if (actionButton?.dataset.navigationAction === 'new-route') {
            showView('map');
            await window.travelManagerRouteDetailsPanel?.startNewRoute();
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
            showNotification('Zmiany zostały zapisane.');
            return;
        }

        showNotification('Nie udało się zapisać zmian.', 'error');
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
            mapView.textContent = 'Nie udało się załadować widoku.';
        }
    }

    document.dispatchEvent(new CustomEvent('travel-manager:views-ready'));
    window.lucide?.createIcons({
        attrs: {
            'stroke-width': 1.7
        }
    });

    window.travelManagerNavigation = { showView };

    document.addEventListener('travel-manager:car-profiles-changed', (event) => {
        activeCarProfile = event.detail?.activeCarProfile || null;
        updateCarButton();
    });
});
