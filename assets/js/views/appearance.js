document.addEventListener('travel-manager:views-ready', () => {
    const root = document.querySelector('[data-appearance-settings]');
    const themeButtons = root?.querySelectorAll('[data-appearance-theme]');
    const presetButtons = root?.querySelectorAll('[data-appearance-color]');
    const recentHost = root?.querySelector('[data-appearance-recent-colors]');
    const addButton = root?.querySelector('[data-appearance-add-color]');
    let appearance = { theme: 'light', primary_color: '#1F6FAE', recent_colors: [] };

    if (!root || !themeButtons?.length || !presetButtons?.length || !recentHost || !addButton) return;

    const apply = () => {
        document.body.dataset.theme = appearance.theme;
        document.body.style.setProperty('--accent-color', appearance.primary_color);
        document.querySelectorAll('[data-theme-stylesheet]').forEach((stylesheet) => {
            stylesheet.disabled = stylesheet.dataset.themeStylesheet !== appearance.theme;
        });
        themeButtons.forEach((button) => button.setAttribute('aria-checked', String(button.dataset.appearanceTheme === appearance.theme)));
        presetButtons.forEach((button) => button.setAttribute('aria-checked', String(button.dataset.appearanceColor === appearance.primary_color)));
    };
    const patch = async (payload) => {
        const response = await fetch('/api/settings/appearance', {
            method: 'PATCH',
            headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        if (!response.ok || data.status !== 'ok') throw new Error(data.message || 'Nie udało się zapisać wyglądu.');
        appearance = data.appearance; apply(); renderRecent();
        document.dispatchEvent(new CustomEvent('travel-manager:appearance-changed', { detail: appearance }));
    };
    const selectColor = (color) => {
        const recent = [color, ...(appearance.recent_colors || []).filter((item) => item !== color)].slice(0, 5);
        patch({ primary_color: color, recent_colors: recent }).catch((error) => window.alert(error.message));
    };
    const renderRecent = () => {
        recentHost.replaceChildren();
        const colors = appearance.recent_colors || [];
        if (!colors.length) {
            const empty = document.createElement('span'); empty.className = 'appearance-settings__empty'; empty.textContent = 'Brak ostatnio używanych kolorów.'; recentHost.append(empty); return;
        }
        colors.forEach((color) => {
            const button = document.createElement('button'); button.type = 'button'; button.className = 'color-tile'; button.setAttribute('aria-label', `Wybierz kolor ${color}`); button.title = color;
            const swatch = document.createElement('span'); swatch.className = 'color-tile__swatch'; swatch.style.setProperty('--color-tile-value', color);
            button.append(swatch); button.addEventListener('click', () => selectColor(color)); recentHost.append(button);
        });
    };

    themeButtons.forEach((button) => button.addEventListener('click', () => patch({ theme: button.dataset.appearanceTheme }).catch((error) => window.alert(error.message))));
    presetButtons.forEach((button) => button.addEventListener('click', () => selectColor(button.dataset.appearanceColor)));
    addButton.addEventListener('click', async () => { const color = await window.travelManagerColorPicker?.show(appearance.primary_color); if (color) selectColor(color); });
    fetch('/api/settings/appearance', { headers: { 'Accept': 'application/json' } })
        .then((response) => response.json()).then((data) => { if (data.appearance) appearance = data.appearance; apply(); renderRecent(); }).catch(() => { apply(); renderRecent(); });
});
