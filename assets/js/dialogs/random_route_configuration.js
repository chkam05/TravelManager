document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#random-route-configuration');
    const areaInput = dialog?.querySelector('[name="area_km"]');
    const lengthInput = dialog?.querySelector('[name="length_km"]');
    const transportInput = dialog?.querySelector('[name="transport"]');
    const preferenceInput = dialog?.querySelector('[name="preference"]');
    let resolver = null;

    if (!layer || !dialog || !areaInput || !lengthInput || !transportInput || !preferenceInput) {
        return;
    }

    const finish = (value) => {
        dialog.setAttribute('aria-hidden', 'true');
        layer.classList.remove('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'true');
        const resolve = resolver;
        resolver = null;
        resolve?.(value);
    };

    dialog.addEventListener('submit', (event) => {
        event.preventDefault();
        if (!dialog.reportValidity()) return;
        finish({
            area_km: Number(areaInput.value),
            length_km: Number(lengthInput.value),
            transport: transportInput.value,
            preference: preferenceInput.value
        });
    });
    dialog.querySelectorAll('[data-random-route-cancel]').forEach((button) => {
        button.addEventListener('click', () => finish(null));
    });
    const updatePreferenceOptions = () => {
        const highways = preferenceInput.querySelector('option[value="highways"]');
        if (highways) highways.disabled = transportInput.value !== 'car';
        if (preferenceInput.value === 'highways' && transportInput.value !== 'car') {
            preferenceInput.value = 'standard';
        }
    };
    transportInput.addEventListener('change', updatePreferenceOptions);

    window.travelManagerRandomRouteConfiguration = {
        show: (configuration = {}) => new Promise((resolve) => {
            if (resolver) resolver(null);
            resolver = resolve;
            areaInput.value = configuration.area_km || 25;
            lengthInput.value = configuration.length_km || 80;
            transportInput.value = configuration.transport || 'car';
            preferenceInput.value = configuration.preference || 'standard';
            updatePreferenceOptions();
            layer.classList.add('dialog-layer--open');
            layer.setAttribute('aria-hidden', 'false');
            dialog.setAttribute('aria-hidden', 'false');
            window.setTimeout(() => areaInput.focus(), 0);
        })
    };
});
