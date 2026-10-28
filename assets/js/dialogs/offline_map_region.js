document.addEventListener('travel-manager:views-ready', () => {
    const t = window.i18n.t;
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#offline-map-region');
    const continentSelect = dialog?.querySelector('[data-offline-map-continent]');
    const countrySelect = dialog?.querySelector('[data-offline-map-country]');
    const regionSelect = dialog?.querySelector('[data-offline-map-region]');
    const zoomSelect = dialog?.querySelector('[data-offline-map-max-zoom]');
    const zoomNote = dialog?.querySelector('[data-offline-map-zoom-note]');
    const summary = dialog?.querySelector('[data-offline-map-summary]');
    const status = dialog?.querySelector('[data-offline-map-region-status]');
    const submit = dialog?.querySelector('[data-offline-map-region-submit]');
    const closeButtons = dialog?.querySelectorAll('[data-offline-map-region-close]');
    if (!layer || !dialog || !continentSelect || !countrySelect || !regionSelect
        || !zoomSelect || !summary || !status || !submit || !closeButtons?.length) return;

    let regions = new Map();
    let preflight = null;
    let updatingMap = null;
    let requestId = 0;
    const collator = new Intl.Collator(window.i18n.locale.replace('_', '-'), {
        sensitivity: 'base', numeric: true
    });
    const childrenOf = (id) => (regions.get(id)?.children || [])
        .map((childId) => regions.get(childId)).filter(Boolean);
    const descendants = (id) => {
        const result = [];
        const visit = (item, depth) => {
            result.push({item, depth});
            childrenOf(item.id).forEach((child) => visit(child, depth + 1));
        };
        childrenOf(id).forEach((child) => visit(child, 0));
        return result;
    };
    const formatBytes = (value) => {
        if (value === null || value === undefined || value === '') return t('OFFLINE_MAP_REGION.UNKNOWN');
        const bytes = Number(value);
        if (!Number.isFinite(bytes)) return t('OFFLINE_MAP_REGION.UNKNOWN');
        if (bytes >= 1024 ** 3) return `${new Intl.NumberFormat(window.i18n.locale?.replace('_', '-') || undefined, {
            minimumFractionDigits: 2, maximumFractionDigits: 2
        }).format(bytes / 1024 ** 3)} GB`;
        return new Intl.NumberFormat(undefined, {style: 'unit', unit: 'megabyte', maximumFractionDigits: 1})
            .format(bytes / 1024 / 1024);
    };
    const formatDate = (value) => {
        if (!value) return t('OFFLINE_MAP_REGION.UNKNOWN');
        const date = new Date(value);
        return Number.isNaN(date.getTime()) ? t('OFFLINE_MAP_REGION.UNKNOWN') : date.toLocaleDateString();
    };
    const setOptions = (select, items, selected = '') => {
        select.replaceChildren();
        items.forEach(({value, label}) => {
            const option = document.createElement('option');
            option.value = value; option.textContent = label; select.append(option);
        });
        if (items.some((item) => item.value === selected)) select.value = selected;
        select.disabled = !items.length;
    };
    const addSummary = (label, value) => {
        const row = document.createElement('div');
        const term = document.createElement('dt'); term.textContent = label;
        const description = document.createElement('dd'); description.textContent = value;
        row.append(term, description); summary.append(row);
    };
    const selectedRegion = () => regions.get(regionSelect.value);
    const renderSummary = (region, check = null) => {
        summary.replaceChildren();
        if (!region) return;
        addSummary(t('OFFLINE_MAP_REGION.SOURCE'), 'Geofabrik / OpenStreetMap');
        addSummary(t('OFFLINE_MAP_REGION.DATA_DATE'), formatDate(check?.source_modified_at || region.source_updated_at));
        addSummary(t('OFFLINE_MAP_REGION.DOWNLOAD_SIZE'), formatBytes(check?.source_size ?? region.pbf_size));
        addSummary(t('OFFLINE_MAP_REGION.ESTIMATED_SIZE'),
            Number(zoomSelect.value) > 14 ? t('OFFLINE_MAP_REGION.UNKNOWN')
                : formatBytes(check?.estimated_map_size));
        addSummary(t('OFFLINE_MAP_REGION.AVAILABLE_SPACE'), formatBytes(check?.available_space));
    };
    const loadPreflight = async () => {
        const region = selectedRegion();
        const currentRequest = ++requestId;
        preflight = null; status.textContent = ''; status.classList.remove('offline-map-region__status--error');
        submit.disabled = !region?.pbf_url;
        renderSummary(region);
        if (!region?.pbf_url) return;
        try {
            const response = await fetch(`/api/offline-maps/preflight/${encodeURIComponent(region.id)}`, {
                headers: {'Accept': 'application/json'}
            });
            const data = await response.json();
            if (currentRequest !== requestId) return;
            if (!response.ok) throw new Error(data.message || t('OFFLINE_MAP_REGION.PREFLIGHT_FAILED'));
            preflight = data; renderSummary(region, data);
            const problem = data.installed && (!updatingMap || data.map_id !== updatingMap.id)
                ? t('OFFLINE_MAP_REGION.ALREADY_INSTALLED')
                : data.active_job ? t('OFFLINE_MAP_REGION.ALREADY_RUNNING')
                    : !data.enough_space ? t('OFFLINE_MAP_REGION.NOT_ENOUGH_SPACE') : '';
            status.textContent = problem;
            status.classList.toggle('offline-map-region__status--error', Boolean(problem));
            submit.disabled = Boolean(problem);
        } catch (error) {
            if (currentRequest !== requestId) return;
            status.textContent = error.message || t('OFFLINE_MAP_REGION.PREFLIGHT_FAILED');
            status.classList.add('offline-map-region__status--error'); submit.disabled = true;
        }
    };
    const updateRegions = () => {
        const country = regions.get(countrySelect.value);
        const choices = country ? [{item: country, depth: 0}, ...descendants(country.id)] : [];
        setOptions(regionSelect, choices.filter(({item}) => item.pbf_url).map(({item, depth}) => ({
            value: item.id, label: `${'— '.repeat(depth)}${item.name}`
        })));
        loadPreflight();
    };
    const updateCountries = (selectedCountry = '') => {
        const choices = descendants(continentSelect.value)
            .filter(({item}) => item.country_codes?.length && !item.region_codes?.length)
            .sort((a, b) => collator.compare(a.item.name, b.item.name));
        setOptions(countrySelect, choices.map(({item}) => ({value: item.id, label: item.name})), selectedCountry);
        updateRegions();
    };
    const close = () => {
        requestId += 1; dialog.setAttribute('aria-hidden', 'true');
        layer.classList.remove('dialog-layer--open'); layer.setAttribute('aria-hidden', 'true');
    };
    const open = async (mapToUpdate = null) => {
        updatingMap = mapToUpdate?.id ? mapToUpdate : null;
        zoomSelect.value = String(updatingMap?.max_zoom || 14);
        if (zoomNote) zoomNote.textContent = t('OFFLINE_MAP_REGION.ZOOM_NOTE');
        submit.textContent = t(updatingMap ? 'OFFLINE_MAP_REGION.UPDATE_MAP' : 'OFFLINE_MAP_REGION.DOWNLOAD');
        layer.classList.add('dialog-layer--open'); layer.setAttribute('aria-hidden', 'false');
        dialog.setAttribute('aria-hidden', 'false'); status.textContent = t('OFFLINE_MAP_REGION.LOADING'); submit.disabled = true;
        try {
            const response = await fetch('/api/offline-maps/catalog', {headers: {'Accept': 'application/json'}});
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || t('OFFLINE_MAP_REGION.LOAD_FAILED'));
            regions = new Map((data.regions || []).map((item) => [item.id, item]));
            const roots = [...regions.values()].filter((item) => !item.parent_id)
                .sort((a, b) => collator.compare(a.name, b.name));
            setOptions(continentSelect, roots.map((item) => ({value: item.id, label: item.name})));
            updateCountries();
            if (updatingMap) {
                const region = regions.get(updatingMap.region_id);
                if (region) {
                    let ancestor = region;
                    let countryId = region.country_codes?.length && !region.region_codes?.length
                        ? region.id : '';
                    while (ancestor?.parent_id) {
                        const parent = regions.get(ancestor.parent_id);
                        if (!parent) break;
                        if (parent.country_codes?.length && !parent.region_codes?.length) {
                            countryId = parent.id;
                        }
                        if (!parent.parent_id) continentSelect.value = parent.id;
                        ancestor = parent;
                    }
                    updateCountries(countryId);
                    const country = regions.get(countrySelect.value);
                    if (country && (country.id === region.id || descendants(country.id)
                        .some(({item}) => item.id === region.id))) {
                        regionSelect.value = region.id;
                        loadPreflight();
                    }
                    continentSelect.disabled = true;
                    countrySelect.disabled = true;
                    regionSelect.disabled = true;
                } else {
                    status.textContent = t('OFFLINE_MAP_REGION.LOAD_FAILED');
                    status.classList.add('offline-map-region__status--error');
                    submit.disabled = true;
                }
            }
        } catch (error) {
            status.textContent = error.message || t('OFFLINE_MAP_REGION.LOAD_FAILED');
            status.classList.add('offline-map-region__status--error');
        }
    };
    continentSelect.addEventListener('change', () => updateCountries());
    countrySelect.addEventListener('change', updateRegions);
    regionSelect.addEventListener('change', loadPreflight);
    zoomSelect.addEventListener('change', () => renderSummary(selectedRegion(), preflight));
    dialog.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (!preflight || submit.disabled) return;
        submit.disabled = true; status.textContent = t('OFFLINE_MAP_REGION.STARTING');
        try {
            const url = updatingMap
                ? `/api/offline-maps/${encodeURIComponent(updatingMap.id)}/update`
                : '/api/offline-maps/jobs';
            const response = await fetch(url, {
                method: 'POST', headers: {'Accept': 'application/json', 'Content-Type': 'application/json'},
                body: JSON.stringify(updatingMap
                    ? {max_zoom: Number(zoomSelect.value)}
                    : {region_id: regionSelect.value, max_zoom: Number(zoomSelect.value)})
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || t('OFFLINE_MAP_REGION.START_FAILED'));
            close();
            document.dispatchEvent(new CustomEvent('travel-manager:offline-map-job-started', {detail: data.job}));
        } catch (error) {
            status.textContent = error.message || t('OFFLINE_MAP_REGION.START_FAILED');
            status.classList.add('offline-map-region__status--error'); submit.disabled = false;
        }
    });
    closeButtons.forEach((button) => button.addEventListener('click', close));
    layer.addEventListener('click', (event) => { if (event.target === layer && dialog.getAttribute('aria-hidden') === 'false') close(); });
    document.addEventListener('click', (event) => {
        if (event.target.closest('[data-offline-map-download]')) open();
    });
    document.addEventListener('travel-manager:offline-map-download-requested', () => open());
    document.addEventListener('travel-manager:offline-map-update-requested', (event) => open(event.detail));
    window.travelManagerOfflineMapRegionDialog = {open, close};
});
