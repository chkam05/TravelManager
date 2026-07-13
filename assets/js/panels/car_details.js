document.addEventListener('travel-manager:views-ready', () => {
    const panel = document.querySelector('#car-details-panel');
    const title = document.querySelector('#car-details-panel-title');
    const content = document.querySelector('#car-details-panel-content');
    const photo = document.querySelector('#car-details-panel-photo');
    const photoImg = document.querySelector('#car-details-panel-photo-img');
    const closeButton = document.querySelector('[data-car-details-panel-close]');
    const grabber = document.querySelector('[data-car-details-panel-grabber]');
    const useButton = document.querySelector('#car-details-panel-use');
    const editButton = document.querySelector('#car-details-panel-edit');
    const deleteButton = document.querySelector('#car-details-panel-delete');
    const valueFields = Object.fromEntries(
        [...document.querySelectorAll('[data-car-detail-value]')]
            .map((field) => [field.dataset.carDetailValue, field])
    );

    if (!panel || !title || !content || !photo || !photoImg || !closeButton || !useButton || !editButton || !deleteButton) {
        return;
    }

    let currentProfile = null;

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
            const width = Number(data?.ui?.car_details_panel_width);

            if (Number.isFinite(width) && width > 0) {
                panel.style.setProperty('--car-details-panel-width', `${width}px`);
            }
        } catch (error) {
            // The default panel width remains usable.
        }
    };

    const name = (profile) => profile?.name || [profile?.brand, profile?.model].filter(Boolean).join(' ') || 'Samochód';
    const value = (data) => data === null || data === undefined || data === '' ? '-' : String(data);
    const setValue = (field, data) => {
        if (valueFields[field]) {
            valueFields[field].textContent = value(data);
        }
    };

    const setOdometer = (entries) => {
        const field = valueFields.odometer_entries;

        if (!field) {
            return;
        }

        field.replaceChildren();
        const items = entries || [];

        if (!items.length) {
            field.textContent = '-';
            return;
        }

        items.forEach((entry, index) => {
            if (index > 0) {
                field.appendChild(document.createElement('br'));
            }

            field.append(`${entry.distance || 0} km${entry.date ? ` (${entry.date})` : ''}`);
        });
    };

    const render = () => {
        if (!currentProfile) {
            return;
        }

        title.textContent = name(currentProfile);
        photo.hidden = !currentProfile.image;
        photoImg.src = currentProfile.image || '';
        photoImg.alt = currentProfile.image ? name(currentProfile) : '';

        setValue('name', name(currentProfile));
        setValue('brand', currentProfile.brand);
        setValue('model', currentProfile.model);
        setValue('version', currentProfile.version);
        setValue('generation', currentProfile.generation);
        setValue('production_year', currentProfile.production_year);
        setValue('registration_number', currentProfile.registration_number);
        setValue('body_type', currentProfile.body_type);
        setValue('engine_capacity', currentProfile.engine_capacity ? `${currentProfile.engine_capacity} cm3` : '');
        setValue('power_hp', currentProfile.power_hp ? `${currentProfile.power_hp} KM` : '');
        setValue('power_kw', currentProfile.power_kw ? `${currentProfile.power_kw} kW` : '');
        setValue('max_speed', currentProfile.max_speed ? `${currentProfile.max_speed} km/h` : '');
        setValue('drive_type', currentProfile.drive_type);
        setValue('transmission_type', currentProfile.transmission_type);
        setValue('fuel_tank_capacity', currentProfile.fuel_tank_capacity ? `${currentProfile.fuel_tank_capacity} L` : '');
        setValue('fuel_type', currentProfile.fuel_type);
        setValue('secondary_fuel_type', currentProfile.secondary_fuel_type);
        setValue('min_consumption', currentProfile.min_consumption ? `${currentProfile.min_consumption} L/100km` : '');
        setValue('max_consumption', currentProfile.max_consumption ? `${currentProfile.max_consumption} L/100km` : '');
        setOdometer(currentProfile.odometer_entries);

        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };

    const open = (profile) => {
        currentProfile = profile;
        render();
        panel.classList.add('car-details-panel--open');
        panel.setAttribute('aria-hidden', 'false');
    };

    const close = () => {
        panel.classList.remove('car-details-panel--open');
        panel.setAttribute('aria-hidden', 'true');
    };

    useButton.addEventListener('click', async () => {
        if (currentProfile) {
            await window.travelManagerCarProfiles?.setActive(currentProfile.id);
        }
    });
    editButton.addEventListener('click', async () => {
        if (!currentProfile) {
            return;
        }

        const result = await window.travelManagerCarProfileEditor?.show(currentProfile);
        if (result) {
            currentProfile = await window.travelManagerCarProfiles?.save(result);
            render();
        }
    });
    deleteButton.addEventListener('click', async () => {
        if (!currentProfile) {
            return;
        }

        const accepted = await window.travelManagerDialogs?.yesNo({
            title: 'Usunąć samochód?',
            description: `Profil „${name(currentProfile)}” zostanie usunięty.`,
            icon: 'warning'
        });

        if (accepted) {
            await window.travelManagerCarProfiles?.remove(currentProfile.id);
            close();
        }
    });
    closeButton.addEventListener('click', close);

    const resize = { startX: 0, startWidth: 0 };
    const onPointerMove = (event) => {
        const computed = window.getComputedStyle(panel);
        const min = Number.parseFloat(computed.minWidth) || 300;
        const max = Number.parseFloat(computed.maxWidth) || 680;
        const width = Math.min(Math.max(resize.startWidth + resize.startX - event.clientX, min), max);
        panel.style.setProperty('--car-details-panel-width', `${width}px`);
    };
    const stopResize = () => {
        panel.classList.remove('car-details-panel--resizing');
        document.removeEventListener('pointermove', onPointerMove);
        document.removeEventListener('pointerup', stopResize);
        patchUiSettings({
            car_details_panel_width: Math.round(panel.getBoundingClientRect().width)
        });
    };

    grabber?.addEventListener('pointerdown', (event) => {
        event.preventDefault();
        resize.startX = event.clientX;
        resize.startWidth = panel.getBoundingClientRect().width;
        panel.classList.add('car-details-panel--resizing');
        document.addEventListener('pointermove', onPointerMove);
        document.addEventListener('pointerup', stopResize);
    });

    document.addEventListener('travel-manager:car-profiles-changed', (event) => {
        if (!currentProfile) {
            return;
        }

        currentProfile = (event.detail?.profiles || []).find((profile) => profile.id === currentProfile.id) || currentProfile;
        render();
    });

    loadUiSettings();

    window.travelManagerCarDetailsPanel = { close, open };
});
