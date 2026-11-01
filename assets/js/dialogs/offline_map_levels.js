document.addEventListener('travel-manager:views-ready', () => {
    const t = window.i18n.t;
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#offline-map-levels');
    const title = dialog?.querySelector('[data-offline-map-levels-title]');
    const status = dialog?.querySelector('[data-offline-map-levels-status]');
    const list = dialog?.querySelector('[data-offline-map-levels-list]');
    const generate = dialog?.querySelector('[data-offline-map-levels-generate]');
    const remove = dialog?.querySelector('[data-offline-map-levels-delete]');
    const closeButton = dialog?.querySelector('[data-offline-map-levels-close]');
    if (!layer || !dialog || !title || !status || !list || !generate || !remove || !closeButton) return;
    let map = null;
    let levels = [];
    const selected = () => [...list.querySelectorAll('input:checked')].map((input) => Number(input.value));
    const refreshButtons = () => {
        const values = selected();
        generate.disabled = !values.length;
        remove.disabled = !values.some((zoom) => zoom !== 10);
    };
    const close = () => {
        dialog.setAttribute('aria-hidden', 'true');
        layer.classList.remove('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'true');
        map = null;
    };
    const render = () => {
        list.replaceChildren(...levels.map((level) => {
            const label = document.createElement('label');
            label.className = `offline-map-levels__row${level.zoom === 15 ? ' offline-map-levels__row--detail-start' : ''}`;
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox'; checkbox.value = String(level.zoom);
            checkbox.addEventListener('change', refreshButtons);
            const zoom = document.createElement('span'); zoom.className = 'offline-map-levels__zoom'; zoom.textContent = `x${level.zoom}`;
            const state = document.createElement('span'); state.className = 'offline-map-levels__state';
            state.textContent = t(`OFFLINE_MAP_LEVELS.STATUS_${String(level.status).toUpperCase()}`);
            const count = document.createElement('span'); count.className = 'offline-map-levels__count';
            count.textContent = level.tile_count ? t('OFFLINE_MAP_LEVELS.TILE_COUNT', {count: new Intl.NumberFormat().format(level.tile_count)}) : '';
            label.append(checkbox, zoom, state, count); return label;
        }));
        refreshButtons();
        window.lucide?.createIcons({attrs: {'stroke-width': 1.7}});
    };
    const load = async () => {
        status.textContent = t('OFFLINE_MAP_LEVELS.LOADING');
        const response = await fetch(`/api/offline-maps/${encodeURIComponent(map.id)}/levels`, {headers: {Accept: 'application/json'}});
        const data = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(data.message || t('OFFLINE_MAP_LEVELS.LOAD_FAILED'));
        levels = data.levels || []; status.textContent = ''; render();
    };
    const open = async (item) => {
        map = item; title.textContent = t('OFFLINE_MAP_LEVELS.MAP_TITLE', {name: item.name});
        layer.classList.add('dialog-layer--open'); layer.setAttribute('aria-hidden', 'false');
        dialog.setAttribute('aria-hidden', 'false'); list.replaceChildren();
        try { await load(); } catch (error) { status.textContent = error.message; }
    };
    generate.addEventListener('click', async () => {
        const values = selected(); if (!map || !values.length) return;
        generate.disabled = true; remove.disabled = true;
        try {
            const response = await fetch(`/api/offline-maps/${encodeURIComponent(map.id)}/levels`, {
                method: 'POST', headers: {Accept: 'application/json', 'Content-Type': 'application/json'},
                body: JSON.stringify({levels: values})
            });
            const data = await response.json().catch(() => ({}));
            if (!response.ok) throw new Error(data.message || t('OFFLINE_MAP_LEVELS.GENERATE_FAILED'));
            if (data.job) { close(); document.dispatchEvent(new CustomEvent('travel-manager:offline-map-job-started', {detail: data.job})); }
            else await load();
        } catch (error) { status.textContent = error.message; refreshButtons(); }
    });
    remove.addEventListener('click', async () => {
        const values = selected().filter((zoom) => zoom !== 10); if (!map || !values.length) return;
        const accepted = await window.travelManagerDialogs?.yesNo({
            title: t('OFFLINE_MAP_LEVELS.DELETE_TITLE'), description: t('OFFLINE_MAP_LEVELS.DELETE_CONFIRM', {levels: values.map((zoom) => `x${zoom}`).join(', ')}),
            icon: 'trash-2', yesLabel: t('COMMON.DELETE')
        });
        if (!accepted) return;
        generate.disabled = true; remove.disabled = true;
        try {
            const response = await fetch(`/api/offline-maps/${encodeURIComponent(map.id)}/levels`, {
                method: 'DELETE', headers: {Accept: 'application/json', 'Content-Type': 'application/json'},
                body: JSON.stringify({levels: values})
            });
            const data = await response.json().catch(() => ({}));
            if (!response.ok) throw new Error(data.message || t('OFFLINE_MAP_LEVELS.DELETE_FAILED'));
            await load(); await window.travelManagerMap?.refreshOfflineMaps();
        } catch (error) { status.textContent = error.message; refreshButtons(); }
    });
    closeButton.addEventListener('click', close);
    document.addEventListener('travel-manager:offline-map-levels-requested', (event) => open(event.detail));
    window.travelManagerOfflineMapLevels = {open, close};
});
