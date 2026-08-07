document.addEventListener('travel-manager:views-ready', () => {
    const root = document.querySelector('[data-appearance-settings]');
    const themeButtons = root?.querySelectorAll('[data-appearance-theme]');
    const presetButtons = root?.querySelectorAll('[data-appearance-color]');
    const recentHost = root?.querySelector('[data-appearance-recent-colors]');
    const addButton = root?.querySelector('[data-appearance-add-color]');
    const mapColorHosts = root?.querySelectorAll('[data-appearance-map-color]');
    const vehicleColorHosts = root?.querySelectorAll('[data-appearance-vehicle-color]');
    let appearance = {
        theme: 'light', primary_color: '#1F6FAE', recent_colors: [],
        route_point_color: '#1F6FAE', route_color: '#1F6FAE',
        public_transport_route_color: '#1F6FAE',
        vehicle_colors: { bus: '#1F6FAE', tram: '#D73535', trolley: '#10893E', metro: '#704BA4', train: '#C24D0F' }
    };
    let openPicker = null;

    if (!root || !themeButtons?.length || !presetButtons?.length || !recentHost || !addButton) return;

    const presets = Array.from(presetButtons, (button) => ({
        color: button.dataset.appearanceColor,
        label: (button.title || button.dataset.appearanceColor).replace(/\s+\(#[0-9A-Fa-f]{6}\)$/, '')
    }));
    const displayColor = (color) => (
        presets.find((preset) => preset.color === color)?.label || color
    );
    const isPreset = (color) => presets.some((preset) => preset.color === color);
    const colorValue = (host) => host.dataset.appearanceMapColor
        ? appearance[host.dataset.appearanceMapColor]
        : appearance.vehicle_colors?.[host.dataset.appearanceVehicleColor];

    const apply = () => {
        document.body.dataset.theme = appearance.theme;
        document.body.style.setProperty('--accent-color', appearance.primary_color);
        document.body.style.setProperty('--route-point-color', appearance.route_point_color);
        document.body.style.setProperty('--route-color', appearance.route_color);
        document.body.style.setProperty('--public-transport-route-color', appearance.public_transport_route_color);
        Object.entries(appearance.vehicle_colors || {}).forEach(([type, color]) => {
            document.body.style.setProperty(`--public-transport-vehicle-${type}-color`, color);
        });
        document.querySelectorAll('[data-theme-stylesheet]').forEach((stylesheet) => {
            stylesheet.disabled = stylesheet.dataset.themeStylesheet !== appearance.theme;
        });
        themeButtons.forEach((button) => button.setAttribute('aria-checked', String(button.dataset.appearanceTheme === appearance.theme)));
        presetButtons.forEach((button) => button.setAttribute('aria-checked', String(button.dataset.appearanceColor === appearance.primary_color)));
        [...mapColorHosts, ...vehicleColorHosts].forEach((host) => {
            const color = colorValue(host);
            host.querySelector('[data-color-combobox-swatch]')?.style.setProperty('--appearance-color-value', color);
            const value = host.querySelector('[data-color-combobox-value]');
            if (value) {
                value.textContent = displayColor(color);
                value.title = displayColor(color);
            }
        });
    };

    const patch = async (payload) => {
        const response = await fetch('/api/settings/appearance', {
            method: 'PATCH',
            headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        if (!response.ok || data.status !== 'ok') throw new Error(data.message || 'Nie udało się zapisać wyglądu.');
        appearance = data.appearance;
        apply();
        renderRecent();
        renderOpenMenu();
        document.dispatchEvent(new CustomEvent('travel-manager:appearance-changed', { detail: appearance }));
    };

    const customRecentColors = () => (
        (appearance.recent_colors || []).filter((color) => !isPreset(color))
    );
    const withRecentColor = (color) => (
        isPreset(color)
            ? customRecentColors()
            : [color, ...customRecentColors().filter((item) => item !== color)].slice(0, 5)
    );

    const selectAccentColor = (color, remember = false) => {
        patch({
            primary_color: color,
            recent_colors: remember ? withRecentColor(color) : customRecentColors()
        }).catch((error) => window.travelManagerAlert?.(error.message, 'error'));
    };

    const selectMapColor = (host, color, remember = false) => {
        const payload = {
            recent_colors: remember ? withRecentColor(color) : customRecentColors()
        };
        if (host.dataset.appearanceMapColor) {
            payload[host.dataset.appearanceMapColor] = color;
        } else {
            payload.vehicle_colors = {
                ...(appearance.vehicle_colors || {}),
                [host.dataset.appearanceVehicleColor]: color
            };
        }
        patch(payload).catch((error) => window.travelManagerAlert?.(error.message, 'error'));
    };

    const removeRecentColor = (color) => {
        patch({ recent_colors: customRecentColors().filter((item) => item !== color) })
            .catch((error) => window.travelManagerAlert?.(error.message, 'error'));
    };

    const renderRecent = () => {
        recentHost.replaceChildren();
        const colors = customRecentColors();
        if (!colors.length) {
            const empty = document.createElement('span');
            empty.className = 'appearance-settings__empty';
            empty.textContent = 'Brak ostatnio używanych kolorów.';
            recentHost.append(empty);
            return;
        }
        colors.forEach((color) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'color-tile';
            button.setAttribute('aria-label', `Wybierz kolor ${color}`);
            button.title = color;
            const swatch = document.createElement('span');
            swatch.className = 'color-tile__swatch';
            swatch.style.setProperty('--color-tile-value', color);
            button.append(swatch);
            button.addEventListener('click', () => selectAccentColor(color));
            recentHost.append(button);
        });
    };

    const closeColorPicker = () => {
        if (!openPicker) return;
        openPicker.menu.hidden = true;
        openPicker.menu.classList.remove('appearance-color-combobox__menu--up');
        openPicker.menu.style.removeProperty('max-height');
        openPicker.button.setAttribute('aria-expanded', 'false');
        openPicker = null;
    };

    const appendColorOption = (menu, color, label, onSelect) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'appearance-color-combobox__option';
        button.setAttribute('role', 'option');
        button.title = label;
        const swatch = document.createElement('span');
        swatch.className = 'appearance-color-combobox__swatch';
        swatch.style.setProperty('--appearance-color-value', color);
        const text = document.createElement('span');
        text.textContent = label;
        button.append(swatch, text);
        button.addEventListener('click', () => { closeColorPicker(); onSelect(color); });
        menu.append(button);
    };

    const renderPickerMenu = (host, menu) => {
        menu.replaceChildren();
        const presetGroup = document.createElement('div');
        presetGroup.className = 'appearance-color-combobox__group';
        presetGroup.setAttribute('role', 'group');
        presetGroup.setAttribute('aria-label', 'Gotowe kolory');
        presets.forEach((preset) => appendColorOption(presetGroup, preset.color, preset.label, (color) => selectMapColor(host, color)));
        menu.append(presetGroup);

        const separator = document.createElement('div');
        separator.className = 'appearance-color-combobox__separator';
        separator.setAttribute('role', 'separator');
        menu.append(separator);

        const recentGroup = document.createElement('div');
        recentGroup.className = 'appearance-color-combobox__group';
        recentGroup.setAttribute('role', 'group');
        recentGroup.setAttribute('aria-label', 'Ostatnio używane kolory');
        const recent = customRecentColors();
        if (!recent.length) {
            const empty = document.createElement('span');
            empty.className = 'appearance-color-combobox__empty';
            empty.textContent = 'Brak ostatnio używanych kolorów';
            recentGroup.append(empty);
        }
        recent.forEach((color) => {
            const row = document.createElement('div');
            row.className = 'appearance-color-combobox__recent';
            appendColorOption(row, color, color, (selected) => selectMapColor(host, selected));
            const remove = document.createElement('button');
            remove.type = 'button';
            remove.className = 'appearance-color-combobox__remove';
            remove.setAttribute('aria-label', `Usuń kolor ${color} z ostatnio używanych`);
            remove.title = 'Usuń z ostatnio używanych';
            remove.innerHTML = '<i data-lucide="trash-2" aria-hidden="true"></i>';
            remove.addEventListener('click', (event) => { event.stopPropagation(); removeRecentColor(color); });
            row.append(remove);
            recentGroup.append(row);
        });
        menu.append(recentGroup);

        const separatorBeforeCustom = separator.cloneNode();
        menu.append(separatorBeforeCustom);
        const custom = document.createElement('button');
        custom.type = 'button';
        custom.className = 'appearance-color-combobox__custom';
        custom.innerHTML = '<i data-lucide="palette" aria-hidden="true"></i><span>Wybierz własny kolor…</span>';
        custom.addEventListener('click', async () => {
            const initial = colorValue(host);
            closeColorPicker();
            const color = await window.travelManagerColorPicker?.show(initial);
            if (color) selectMapColor(host, color, true);
        });
        menu.append(custom);
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };

    const renderOpenMenu = () => {
        if (openPicker) renderPickerMenu(openPicker.host, openPicker.menu);
    };

    const createColorPicker = (host) => {
        host.className = 'appearance-color-combobox';
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'appearance-color-combobox__button';
        button.setAttribute('aria-haspopup', 'listbox');
        button.setAttribute('aria-expanded', 'false');
        button.setAttribute('aria-label', `Wybierz kolor: ${host.dataset.appearanceColorLabel}`);
        button.innerHTML = '<span class="appearance-color-combobox__swatch" data-color-combobox-swatch></span><span data-color-combobox-value></span><i data-lucide="chevron-down" aria-hidden="true"></i>';
        const menu = document.createElement('div');
        menu.className = 'appearance-color-combobox__menu';
        menu.setAttribute('role', 'listbox');
        menu.hidden = true;
        button.addEventListener('click', () => {
            const shouldOpen = openPicker?.host !== host;
            closeColorPicker();
            if (!shouldOpen) return;
            renderPickerMenu(host, menu);
            menu.hidden = false;
            const buttonRect = button.getBoundingClientRect();
            const menuHeight = Math.min(menu.scrollHeight, 340);
            const spaceBelow = window.innerHeight - buttonRect.bottom - 12;
            const spaceAbove = buttonRect.top - 12;
            const openUp = spaceBelow < menuHeight && spaceAbove > spaceBelow;
            const availableSpace = Math.max(120, openUp ? spaceAbove : spaceBelow);
            menu.classList.toggle('appearance-color-combobox__menu--up', openUp);
            menu.style.maxHeight = `${Math.min(340, availableSpace)}px`;
            button.setAttribute('aria-expanded', 'true');
            openPicker = { host, button, menu };
        });
        host.append(button, menu);
    };

    [...mapColorHosts, ...vehicleColorHosts].forEach(createColorPicker);
    document.addEventListener('click', (event) => {
        if (openPicker && !openPicker.host.contains(event.target)) closeColorPicker();
    });
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && openPicker) { const button = openPicker.button; closeColorPicker(); button.focus(); }
    });
    themeButtons.forEach((button) => button.addEventListener('click', () => patch({ theme: button.dataset.appearanceTheme }).catch((error) => window.travelManagerAlert?.(error.message, 'error'))));
    presetButtons.forEach((button) => button.addEventListener('click', () => selectAccentColor(button.dataset.appearanceColor)));
    addButton.addEventListener('click', async () => { const color = await window.travelManagerColorPicker?.show(appearance.primary_color); if (color) selectAccentColor(color, true); });
    fetch('/api/settings/appearance', { headers: { 'Accept': 'application/json' } })
        .then((response) => response.json()).then((data) => { if (data.appearance) appearance = data.appearance; apply(); renderRecent(); }).catch(() => { apply(); renderRecent(); });
});
