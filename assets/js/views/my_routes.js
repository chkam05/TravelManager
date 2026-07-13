document.addEventListener('travel-manager:views-ready', () => {
    const view = document.querySelector('[data-app-view="my-routes"]');
    const form = document.querySelector('#my-routes-search');
    const searchInput = document.querySelector('#my-routes-search-input');
    const sortButton = document.querySelector('#my-routes-sort-button');
    const sortMenu = document.querySelector('#my-routes-sort-menu');
    const list = document.querySelector('#my-routes-list');
    const menu = document.querySelector('#my-routes-menu');

    if (!view || !form || !searchInput || !sortButton || !sortMenu || !list || !menu) {
        return;
    }

    document.body.append(menu);

    const state = {
        query: '',
        sortDirection: 'asc',
        routes: [],
        menuRouteId: null
    };

    const routeName = (route) => route.name || 'Trasa';

    const formatDistance = (meters) => {
        const value = Number(meters);

        if (!Number.isFinite(value)) {
            return '-';
        }

        return value >= 1000 ? `${(value / 1000).toFixed(1)} km` : `${Math.round(value)} m`;
    };

    const formatDuration = (seconds) => {
        const value = Number(seconds);

        if (!Number.isFinite(value)) {
            return '-';
        }

        const totalMinutes = Math.round(value / 60);
        const hours = Math.floor(totalMinutes / 60);
        const minutes = totalMinutes % 60;

        return hours ? `${hours} godz. ${minutes} min` : `${minutes} min`;
    };

    const setSortOpen = (open) => {
        sortMenu.setAttribute('aria-hidden', String(!open));
        sortButton.setAttribute('aria-expanded', String(open));
    };

    const hideMenu = () => {
        menu.setAttribute('aria-hidden', 'true');
        state.menuRouteId = null;
    };

    const filtered = () => {
        const query = state.query.trim().toLocaleLowerCase();
        const items = query
            ? state.routes.filter((route) => routeName(route).toLocaleLowerCase().includes(query))
            : [...state.routes];

        return items.sort((left, right) => {
            const result = routeName(left).localeCompare(routeName(right), 'pl', { sensitivity: 'base' });
            return state.sortDirection === 'asc' ? result : -result;
        });
    };

    const deleteRoute = async (route) => {
        const accepted = await window.travelManagerDialogs?.yesNo({
            title: 'Usunąć trasę?',
            description: `Trasa „${routeName(route)}” zostanie usunięta.`,
            icon: 'warning'
        });

        if (accepted) {
            await window.travelManagerRoutes?.remove(route.id);
        }
    };

    const editRoute = async (route) => {
        const result = await window.travelManagerRouteEditor?.show({
            name: routeName(route),
            icon: route.icon || '🚗',
            editing: true
        });

        if (result?.action === 'save') {
            await window.travelManagerRoutes?.save({
                ...route,
                name: result.name,
                icon: result.icon || '🚗'
            });
        }
    };

    const showRoute = async (route) => {
        window.travelManagerNavigation?.showView('map');
        window.travelManagerRouteDetailsPanel?.openSavedRoute(route);
    };

    const menuButton = (label, handler, danger = false) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.role = 'menuitem';
        button.textContent = label;

        if (danger) {
            button.dataset.danger = 'true';
        }

        button.addEventListener('click', async () => {
            const route = state.routes.find((item) => item.id === state.menuRouteId);
            hideMenu();

            if (route) {
                await handler(route);
            }
        });

        return button;
    };

    const menuSeparator = () => {
        const element = document.createElement('div');
        element.className = 'my-routes-view__menu-separator';
        element.role = 'separator';
        return element;
    };

    const showMenu = (routeId, anchor) => {
        if (state.menuRouteId === routeId && menu.getAttribute('aria-hidden') === 'false') {
            hideMenu();
            return;
        }

        state.menuRouteId = routeId;
        menu.replaceChildren(
            menuButton('Pokaż trasę', showRoute),
            menuButton('Edytuj trasę', editRoute),
            menuSeparator(),
            menuButton('Usuń trasę', deleteRoute, true)
        );
        menu.setAttribute('aria-hidden', 'false');

        const rect = anchor.getBoundingClientRect();
        const menuRect = menu.getBoundingClientRect();
        const left = Math.min(rect.right - menuRect.width, window.innerWidth - menuRect.width - 10);
        const spaceBelow = window.innerHeight - rect.bottom;
        const top = spaceBelow >= menuRect.height + 6
            ? rect.bottom + 6
            : rect.top - menuRect.height - 6;

        menu.style.left = `${Math.max(10, left)}px`;
        menu.style.top = `${Math.max(10, top)}px`;
        menu.querySelector('[role="menuitem"]')?.focus();
    };

    const render = () => {
        list.replaceChildren();
        const items = filtered();

        if (!items.length) {
            const empty = document.createElement('p');
            empty.className = 'my-routes-view__empty';
            empty.textContent = state.query ? 'Nie znaleziono tras.' : 'Brak zapisanych tras.';
            list.append(empty);
            return;
        }

        items.forEach((route) => {
            const item = document.createElement('article');
            item.className = 'my-routes-view__item';

            const icon = document.createElement('div');
            icon.className = 'my-routes-view__icon';
            icon.textContent = route.icon || '🚗';

            const title = document.createElement('div');
            title.className = 'my-routes-view__title';
            title.textContent = routeName(route);
            title.title = routeName(route);

            const distance = document.createElement('div');
            distance.className = 'my-routes-view__distance';
            distance.textContent = formatDistance(route.distance);

            const duration = document.createElement('div');
            duration.className = 'my-routes-view__duration';
            duration.textContent = formatDuration(route.duration);

            const more = document.createElement('button');
            more.className = 'my-routes-view__more';
            more.type = 'button';
            more.textContent = '...';
            more.setAttribute('aria-label', `Opcje trasy ${routeName(route)}`);
            more.addEventListener('click', (event) => {
                event.stopPropagation();
                showMenu(route.id, more);
            });

            item.append(icon, title, distance, duration, more);
            list.append(item);
        });
    };

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        state.query = searchInput.value;
        render();
    });
    searchInput.addEventListener('input', () => {
        state.query = searchInput.value;
        render();
    });
    sortButton.addEventListener('click', () => {
        setSortOpen(sortMenu.getAttribute('aria-hidden') !== 'false');
    });
    sortMenu.addEventListener('click', (event) => {
        const button = event.target.closest('[data-sort-direction]');

        if (!button) {
            return;
        }

        state.sortDirection = button.dataset.sortDirection;
        setSortOpen(false);
        render();
    });
    document.addEventListener('click', (event) => {
        if (!sortMenu.contains(event.target) && !sortButton.contains(event.target)) {
            setSortOpen(false);
        }

        if (!menu.contains(event.target)) {
            hideMenu();
        }
    });
    document.addEventListener('travel-manager:app-view-changed', hideMenu);
    document.addEventListener('travel-manager:routes-changed', (event) => {
        state.routes = event.detail?.routes || [];
        render();
    });
    window.travelManagerRoutes?.list().then((routes) => {
        state.routes = routes;
        render();
    }).catch(() => render());
});
