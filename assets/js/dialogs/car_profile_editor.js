document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#car-profile-editor');
    const title = document.querySelector('#car-profile-editor-title');
    const odometer = document.querySelector('#car-profile-editor-odometer');
    const addOdometer = document.querySelector('#car-profile-editor-add-odometer');
    const selectImage = document.querySelector('#car-profile-editor-select-image');
    const removeImage = document.querySelector('#car-profile-editor-remove-image');
    const imagePreview = document.querySelector('#car-profile-editor-image-preview');
    const imagePreviewImg = document.querySelector('#car-profile-editor-image-preview-img');
    const imageName = document.querySelector('#car-profile-editor-image-name');
    const cancelButtons = dialog?.querySelectorAll('[data-car-profile-editor-cancel]');
    let resolveResult = null;
    let editingProfile = null;
    const hpPerKw = 1.359621617;

    if (!layer || !dialog || !title || !odometer || !addOdometer || !selectImage || !removeImage || !imagePreview || !imagePreviewImg || !imageName || !cancelButtons?.length) {
        return;
    }

    const field = (name) => dialog.elements[name];
    const numberOrNull = (value) => {
        const number = Number(value);
        return Number.isFinite(number) && value !== '' ? number : null;
    };

    const displayName = (profile) => profile.name?.trim()
        || [profile.brand, profile.model].filter(Boolean).join(' ')
        || 'Samochód';

    const setValue = (name, value) => {
        if (field(name)) {
            field(name).value = value ?? '';
        }
    };

    const syncPowerFromHp = () => {
        const hp = numberOrNull(field('power_hp')?.value);

        if (hp !== null && field('power_kw')) {
            field('power_kw').value = (hp / hpPerKw).toFixed(2);
        }
    };

    const syncPowerFromKw = () => {
        const kw = numberOrNull(field('power_kw')?.value);

        if (kw !== null && field('power_hp')) {
            field('power_hp').value = String(Math.round(kw * hpPerKw));
        }
    };

    const setImage = (image, name = '') => {
        setValue('image', image || '');
        imageName.textContent = image ? (name || 'Wybrane zdjęcie') : 'Brak zdjęcia';
        imagePreview.hidden = !image;
        removeImage.hidden = !image;
        imagePreviewImg.src = image || '';
    };

    const addOdometerRow = (entry = {}) => {
        const row = document.createElement('div');
        row.className = 'car-profile-editor__odometer-row';

        const distance = document.createElement('input');
        distance.type = 'number';
        distance.min = '0';
        distance.step = '1';
        distance.placeholder = 'Przebieg km';
        distance.value = entry.distance ?? '';

        const date = document.createElement('input');
        date.type = 'date';
        date.value = entry.date || '';

        const remove = document.createElement('button');
        remove.className = 'car-profile-editor__odometer-remove';
        remove.type = 'button';
        remove.textContent = 'X';
        remove.addEventListener('click', () => row.remove());

        row.append(distance, date, remove);
        odometer.append(row);
    };

    const readOdometer = () => Array.from(odometer.querySelectorAll('.car-profile-editor__odometer-row'))
        .map((row) => {
            const inputs = row.querySelectorAll('input');
            return {
                distance: numberOrNull(inputs[0]?.value) || 0,
                date: inputs[1]?.value || ''
            };
        })
        .filter((entry) => entry.distance || entry.date);

    const finish = (result) => {
        dialog.setAttribute('aria-hidden', 'true');
        layer.classList.remove('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'true');
        const resolve = resolveResult;
        resolveResult = null;
        resolve?.(result);
    };

    const show = async (profile = null) => {
        if (resolveResult) {
            resolveResult(null);
        }

        editingProfile = profile;
        title.textContent = profile ? 'Edytuj samochód' : 'Dodaj samochód';
        dialog.reset();
        odometer.replaceChildren();
        setImage(profile?.image || '');

        [
            'name', 'brand', 'model', 'version', 'generation', 'body_type',
            'drive_type', 'transmission_type', 'registration_number',
            'fuel_type', 'secondary_fuel_type'
        ].forEach((name) => setValue(name, profile?.[name] || ''));
        [
            'production_year', 'engine_capacity', 'power_hp', 'power_kw',
            'max_speed', 'fuel_tank_capacity', 'min_consumption', 'max_consumption'
        ].forEach((name) => setValue(name, profile?.[name] ?? ''));

        if (!profile?.fuel_type) {
            setValue('fuel_type', '95');
        }

        (profile?.odometer_entries || []).forEach(addOdometerRow);

        dialog.setAttribute('aria-hidden', 'false');
        layer.classList.add('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'false');

        return new Promise((resolve) => {
            resolveResult = resolve;
            window.requestAnimationFrame(() => field('brand')?.focus());
        });
    };

    addOdometer.addEventListener('click', () => addOdometerRow());
    field('power_hp')?.addEventListener('input', syncPowerFromHp);
    field('power_kw')?.addEventListener('input', syncPowerFromKw);
    selectImage.addEventListener('click', async () => {
        const result = await window.pywebview?.api?.select_car_image?.();

        if (result?.status === 'selected') {
            setImage(result.image, result.name);
        }
    });
    removeImage.addEventListener('click', () => setImage(''));
    dialog.addEventListener('submit', (event) => {
        event.preventDefault();
        const profile = {
            ...(editingProfile || {}),
            name: field('name').value.trim(),
            brand: field('brand').value.trim(),
            model: field('model').value.trim(),
            version: field('version').value.trim(),
            generation: field('generation').value.trim(),
            production_year: numberOrNull(field('production_year').value),
            body_type: field('body_type').value.trim(),
            engine_capacity: numberOrNull(field('engine_capacity').value),
            power_hp: numberOrNull(field('power_hp').value),
            power_kw: numberOrNull(field('power_kw').value),
            max_speed: numberOrNull(field('max_speed').value),
            drive_type: field('drive_type').value,
            transmission_type: field('transmission_type').value,
            fuel_tank_capacity: numberOrNull(field('fuel_tank_capacity').value),
            odometer_entries: readOdometer(),
            registration_number: field('registration_number').value.trim(),
            fuel_type: field('fuel_type').value,
            secondary_fuel_type: field('secondary_fuel_type').value,
            min_consumption: numberOrNull(field('min_consumption').value),
            max_consumption: numberOrNull(field('max_consumption').value),
            image: field('image').value
        };

        if (!profile.name) {
            profile.name = displayName(profile);
        }

        finish(profile);
    });
    cancelButtons.forEach((button) => button.addEventListener('click', () => finish(null)));
    layer.addEventListener('click', (event) => {
        if (event.target === layer && resolveResult) {
            finish(null);
        }
    });
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && resolveResult) {
            finish(null);
        }
    });

    window.travelManagerCarProfileEditor = { show };
});
