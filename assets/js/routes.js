document.addEventListener('travel-manager:views-ready', () => {
    let routes = [];
    let loaded = false;

    const notify = () => {
        document.dispatchEvent(new CustomEvent('travel-manager:routes-changed', {
            detail: {
                routes: routes.map((route) => ({
                    ...route,
                    points: (route.points || []).map((point) => ({ ...point }))
                }))
            }
        }));
    };

    const list = async (force = false) => {
        if (loaded && !force) {
            return routes;
        }

        const response = await fetch('/api/routes', {
            headers: { 'Accept': 'application/json' }
        });

        if (!response.ok) {
            throw new Error('Nie udało się wczytać tras.');
        }

        const data = await response.json();
        routes = data.routes || [];
        loaded = true;
        notify();
        return routes;
    };

    const save = async (route) => {
        const response = await fetch('/api/routes', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(route)
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data?.message || 'Nie udało się zapisać trasy.');
        }

        routes = routes.filter((item) => item.id !== data.route.id);
        routes.push(data.route);
        loaded = true;
        notify();
        return data.route;
    };

    const remove = async (routeId) => {
        const response = await fetch(`/api/routes/${encodeURIComponent(routeId)}`, {
            method: 'DELETE',
            headers: { 'Accept': 'application/json' }
        });
        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(data?.message || 'Nie udało się usunąć trasy.');
        }

        routes = routes.filter((item) => item.id !== routeId);
        notify();
    };

    const get = (routeId) => routes.find((route) => route.id === routeId) || null;

    window.travelManagerRoutes = {
        get,
        list,
        remove,
        save
    };

    list().catch(() => {});
});
