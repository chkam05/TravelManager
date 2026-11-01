document.addEventListener('travel-manager:views-ready', () => {
    const panel = document.querySelector('#public-transport-route-result');
    const content = panel?.querySelector('[data-route-result-content]');
    const grabber = panel?.querySelector('[data-public-transport-route-result-grabber]');
    if (!panel || !content) return;
    let mapRequestId = 0;
    const icons = { bus: 'bus-front', tram: 'tram-front', train: 'train-front', metro: 'train-front', trolley: 'bus-front', walk: 'footprints', transfer: 'repeat-2' };
    const names = { bus: 'Autobus', tram: 'Tramwaj', train: 'Pociąg', metro: 'Metro', trolley: 'Trolejbus', walk: 'Pieszo', transfer: 'Przesiadka' };
    const button = (icon, label, className) => {
        const item = document.createElement('button'); item.type = 'button'; item.className = className; item.title = label; item.setAttribute('aria-label', label);
        const image = document.createElement('i'); image.dataset.lucide = icon; item.append(image); return item;
    };
    const walkingGeometry = async leg => {
        if (leg.type !== 'walk' || !Array.isArray(leg.geometry) || leg.geometry.length < 2) return leg;
        try {
            const response = await fetch('/api/map/route', {
                method: 'POST',
                headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    transport: 'foot',
                    points: [leg.geometry[0], leg.geometry[leg.geometry.length - 1]].map(point => ({
                        latitude: point[0], longitude: point[1]
                    }))
                })
            });
            const data = await response.json();
            const coordinates = data?.route?.geometry?.coordinates;
            if (!response.ok || data?.status !== 'ok' || !Array.isArray(coordinates)) return leg;
            return {
                ...leg,
                // GeoJSON is longitude/latitude; journey geometry is latitude/longitude.
                geometry: coordinates.map(point => [point[1], point[0]])
            };
        } catch (_error) {
            return leg;
        }
    };
    const showMap = async journey => {
        const requestId = ++mapRequestId;
        window.travelManagerMap?.clearPublicTransportRoute();
        window.travelManagerNavigation?.showView('map');
        const segments = await Promise.all(journey.legs.map(walkingGeometry));
        if (requestId !== mapRequestId) return;
        window.setTimeout(() => {
            if (requestId !== mapRequestId) return;
            window.travelManagerMap?.showPublicTransportJourney(
                segments,
                `${journey.from} – ${journey.to}`
            );
        }, 0);
    };
    const renderLeg = leg => {
        const article = document.createElement('article'); article.className = 'journey-leg';
        const icon = document.createElement('div'); icon.className = 'journey-leg__icon'; icon.innerHTML = `<i data-lucide="${icons[leg.type] || 'route'}" aria-hidden="true"></i>`;
        const body = document.createElement('div'); body.className = 'journey-leg__body';
        const type = document.createElement('div'); type.className = 'journey-leg__type'; type.textContent = leg.type === 'transfer'
            ? 'Przesiadka'
            : leg.type === 'walk'
                ? 'Dojście'
                : `${names[leg.type] || leg.type}: ${leg.line || '—'}`;
        const from = document.createElement('div'); from.className = 'journey-leg__stop'; from.innerHTML = `<span></span><strong></strong>`; from.children[0].textContent = leg.from; from.children[1].textContent = leg.departure;
        const to = document.createElement('div'); to.className = 'journey-leg__stop'; to.innerHTML = `<span></span><strong></strong>`; to.children[0].textContent = leg.to; to.children[1].textContent = leg.arrival;
        const details = document.createElement('div'); details.className = 'journey-leg__details'; details.textContent = `${leg.duration_minutes} min${leg.distance_km == null ? '' : ` · ${leg.distance_km.toFixed(1)} km`}`;
        body.append(type, from, to, details); article.append(icon, body); return article;
    };
    const render = journeys => {
        content.replaceChildren();
        if (!journeys.length) { const empty = document.createElement('p'); empty.className = 'public-transport-route-result__empty'; empty.textContent = 'Nie znaleziono połączeń dla wybranych parametrów.'; content.append(empty); }
        journeys.forEach((journey, index) => {
            const article = document.createElement('article'); article.className = 'journey-result';
            const summary = document.createElement('header'); summary.className = 'journey-result__summary';
            const title = document.createElement('div'); title.className = 'journey-result__title'; title.textContent = `${journey.from} → ${journey.to}`;
            const expand = button(index ? 'chevron-down' : 'chevron-up', 'Rozwiń lub zwiń', 'journey-result__expand');
            const map = button('map', 'Pokaż trasę na mapie', 'journey-result__map');
            const meta = document.createElement('div'); meta.className = 'journey-result__meta';
            meta.innerHTML = `<span></span><span></span><span></span><span></span>`;
            meta.children[0].textContent = journey.date; meta.children[1].textContent = `${journey.departure}–${journey.arrival}`;
            meta.children[2].textContent = `${journey.duration_minutes} min`; meta.children[3].textContent = `${journey.transfers} przesiadek${journey.distance_km == null ? '' : ` · ${journey.distance_km.toFixed(1)} km`}`;
            const legs = document.createElement('div'); legs.className = 'journey-result__legs'; legs.hidden = index > 0; legs.append(...journey.legs.map(renderLeg));
            expand.addEventListener('click', () => { legs.hidden = !legs.hidden; expand.firstElementChild.dataset.lucide = legs.hidden ? 'chevron-down' : 'chevron-up'; window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } }); });
            map.addEventListener('click', async () => {
                map.disabled = true;
                try { await showMap(journey); } finally { map.disabled = false; }
            }); summary.append(title, expand, map, meta); article.append(summary, legs); content.append(article);
        });
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };
    const setOpen = open => {
        panel.classList.toggle('public-transport-route-result--open', open);
        panel.setAttribute('aria-hidden', String(!open));
    };
    const patchUiSettings = data => fetch('/api/settings/ui', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).catch(() => {});
    const resize = { startX: 0, startWidth: 0 };
    const moveResize = event => {
        const computed = window.getComputedStyle(panel);
        const minimum = Number.parseFloat(computed.minWidth) || 300;
        const maximum = Number.parseFloat(computed.maxWidth) || 680;
        const width = Math.min(
            Math.max(resize.startWidth + resize.startX - event.clientX, minimum),
            maximum
        );
        panel.style.setProperty('--public-transport-route-result-width', `${width}px`);
    };
    const stopResize = () => {
        panel.classList.remove('public-transport-route-result--resizing');
        document.removeEventListener('pointermove', moveResize);
        document.removeEventListener('pointerup', stopResize);
        patchUiSettings({
            public_transport_route_result_panel_width: Math.round(
                panel.getBoundingClientRect().width
            )
        });
    };
    grabber?.addEventListener('pointerdown', event => {
        event.preventDefault();
        resize.startX = event.clientX;
        resize.startWidth = panel.getBoundingClientRect().width;
        panel.classList.add('public-transport-route-result--resizing');
        document.addEventListener('pointermove', moveResize);
        document.addEventListener('pointerup', stopResize);
    });
    fetch('/api/settings/ui', { headers: { 'Accept': 'application/json' } })
        .then(response => response.ok ? response.json() : null)
        .then(data => {
            const width = Number(data?.ui?.public_transport_route_result_panel_width);
            if (Number.isFinite(width) && width > 0) {
                panel.style.setProperty('--public-transport-route-result-width', `${width}px`);
            }
        })
        .catch(() => {});
    document.addEventListener('travel-manager:public-transport-route-results', event => {
        mapRequestId += 1;
        window.travelManagerMap?.clearPublicTransportRoute();
        render(event.detail?.journeys || []);
        setOpen(true);
    });
    panel.querySelector('[data-route-result-close]')?.addEventListener('click', () => {
        mapRequestId += 1;
        window.travelManagerMap?.clearPublicTransportRoute();
        setOpen(false);
    });
});
