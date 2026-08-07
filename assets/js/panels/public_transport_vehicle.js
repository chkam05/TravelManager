document.addEventListener('travel-manager:views-ready', () => {
    const panel = document.querySelector('#public-transport-vehicle-panel');
    const line = panel?.querySelector('[data-vehicle-panel-line]');
    const closeButton = panel?.querySelector('[data-vehicle-panel-close]');
    const trip = panel?.querySelector('[data-vehicle-panel-trip]');
    const sidePanels = [
        ['.car-details-panel', 'car-details-panel--open'],
        ['.place-details-panel', 'place-details-panel--open'],
        ['.search-results-panel', 'search-results-panel--open'],
        ['.route-details-panel', 'route-details-panel--open'],
        ['.public-transport-panel', 'public-transport-panel--open'],
        ['.layer-details-panel', 'layer-details-panel--open'],
        ['.legend-details-panel', 'legend-details-panel--open']
    ].map(([selector, openClass]) => ({
        element: document.querySelector(selector),
        openClass
    })).filter((item) => item.element);
    let selectedKey = '';
    if (!panel || !line || !trip || !closeButton) return;

    const updateAvailableWidth = () => {
        const leftEdges = sidePanels
            .filter(({ element, openClass }) => element.classList.contains(openClass))
            .map(({ element }) => {
                const style = getComputedStyle(element);
                const right = Number.parseFloat(style.right) || 0;
                return window.innerWidth - right - element.getBoundingClientRect().width;
            });
        const leftEdge = leftEdges.length ? Math.min(...leftEdges) : window.innerWidth;
        const rightInset = Math.max(18, window.innerWidth - leftEdge + 14);
        panel.style.setProperty('--public-transport-vehicle-panel-right', `${rightInset}px`);
    };

    const panelObserver = new MutationObserver(updateAvailableWidth);
    sidePanels.forEach(({ element }) => panelObserver.observe(element, {
        attributes: true,
        attributeFilter: ['class', 'style', 'aria-hidden']
    }));
    const resizeObserver = new ResizeObserver(updateAvailableWidth);
    sidePanels.forEach(({ element }) => resizeObserver.observe(element));
    window.addEventListener('resize', updateAvailableWidth);
    updateAvailableWidth();

    const vehicleKey = (vehicle) => {
        const source = vehicle?.source_code || '';
        if (vehicle?.vehicle_id) return `${source}:${vehicle.vehicle_id}`;
        return `${source}:${vehicle?.vehicle_label || ''}:${vehicle?.trip_id || ''}`;
    };
    const close = () => {
        selectedKey = '';
        panel.classList.remove('public-transport-vehicle-panel--open');
        panel.setAttribute('aria-hidden', 'true');
        document.dispatchEvent(new CustomEvent('travel-manager:public-transport-vehicle-deselected'));
    };
    const fieldValue = (vehicle, field) => {
        if (field === 'vehicle_label') {
            const fleetNumber = String(vehicle?.vehicle_label || vehicle?.vehicle_id || '').trim();
            const registrationNumber = String(vehicle?.license_plate || '').trim();
            if (!registrationNumber || registrationNumber === fleetNumber) return fleetNumber;
            return fleetNumber ? `${fleetNumber} / ${registrationNumber}` : registrationNumber;
        }
        if (field !== 'recorded_at') return String(vehicle?.[field] || '').trim();
        if (!vehicle?.recorded_at) return '';
        const date = new Date(vehicle.recorded_at);
        return Number.isNaN(date.getTime()) ? '' : date.toLocaleTimeString('pl-PL');
    };
    const render = (vehicle) => {
        if (!vehicle) return;
        selectedKey = vehicleKey(vehicle);
        line.textContent = vehicle.line ? `Linia ${vehicle.line}` : 'Pojazd';
        trip.textContent = vehicle.trip_id ? `ID kursu: ${vehicle.trip_id}` : '';
        trip.hidden = !vehicle.trip_id;
        panel.querySelectorAll('[data-vehicle-panel-field]').forEach((field) => {
            const value = fieldValue(vehicle, field.dataset.vehiclePanelField);
            field.hidden = !value;
            field.querySelector('dd').textContent = value;
        });
        panel.classList.add('public-transport-vehicle-panel--open');
        panel.setAttribute('aria-hidden', 'false');
    };

    closeButton.addEventListener('click', close);
    document.addEventListener('travel-manager:public-transport-vehicle-selected', (event) => render(event.detail?.vehicle));
    document.addEventListener('travel-manager:public-transport-vehicles-updated', (event) => {
        if (!selectedKey) return;
        const vehicle = (event.detail?.vehicles || []).find((item) => vehicleKey(item) === selectedKey);
        if (vehicle) render(vehicle);
    });
    document.addEventListener('travel-manager:public-transport-vehicles-cleared', close);
    window.travelManagerPublicTransportVehiclePanel = { close };
});
