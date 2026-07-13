document.addEventListener('travel-manager:views-ready', () => {
    const mapGroup = document.querySelector('[data-settings-group="map"]');
    const panelsGroup = document.querySelector('[data-settings-group="panels"]');
    const layersGroup = document.querySelector('[data-settings-group="layers"]');
    const travelCostsGroup = document.querySelector('[data-settings-group="travel-costs"]');
    const routeFuelGroup = document.querySelector('[data-settings-group="route-fuel"]');
    const routeTollsGroup = document.querySelector('[data-settings-group="route-tolls"]');

    if (!mapGroup || !panelsGroup || !layersGroup || !travelCostsGroup || !routeFuelGroup || !routeTollsGroup) {
        return;
    }

    let saveTimer = null;
    let pendingSettings = {};
    let routeFuelMainInput = null;
    let routeFuelDependentRows = [];
    const dataTransferOptions = [
        { id: 'fuel_costs', label: 'Ceny paliwa' },
        { id: 'routes', label: 'Trasy' },
        { id: 'favourites', label: 'Ulubione i Tagi' }
    ];
    const dataTransferMenu = document.createElement('div');
    dataTransferMenu.className = 'settings-view__context-menu';
    dataTransferMenu.setAttribute('role', 'menu');
    dataTransferMenu.setAttribute('aria-hidden', 'true');
    document.body.append(dataTransferMenu);

    const importFileInput = document.createElement('input');
    importFileInput.type = 'file';
    importFileInput.accept = 'application/json,.json';
    importFileInput.hidden = true;
    document.body.append(importFileInput);

    let activeTransferButton = null;
    let pendingBrowserImportType = null;

    const addValue = (group, label, value) => {
        const row = document.createElement('div');
        row.className = 'settings-view__value';

        const term = document.createElement('dt');
        term.textContent = label;

        const description = document.createElement('dd');
        description.textContent = String(value);

        row.append(term, description);
        group.append(row);
    };

    const yesNo = (value) => value ? 'Włączona' : 'Wyłączona';

    const numberValue = (value) => {
        const number = Number(value);
        return Number.isFinite(number) ? number : 0;
    };

    const patchUiSettings = (data) => fetch('/api/settings/ui', {
        method: 'PATCH',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).catch(() => {});

    const schedulePatch = (data) => {
        pendingSettings = {
            ...pendingSettings,
            ...data
        };
        window.clearTimeout(saveTimer);
        saveTimer = window.setTimeout(() => {
            const payload = pendingSettings;
            pendingSettings = {};
            patchUiSettings(payload);
        }, 250);
    };

    const hideDataTransferMenu = () => {
        dataTransferMenu.classList.remove('settings-view__context-menu--open');
        dataTransferMenu.setAttribute('aria-hidden', 'true');
        activeTransferButton?.setAttribute('aria-expanded', 'false');
        activeTransferButton = null;
    };

    const refreshAfterImport = async (dataType) => {
        if (dataType === 'fuel_costs') {
            const response = await fetch('/api/fuel-costs', {
                headers: { 'Accept': 'application/json' }
            });
            const data = await response.json().catch(() => ({}));

            if (response.ok && data.status === 'ok') {
                document.dispatchEvent(new CustomEvent('travel-manager:fuel-costs-changed', {
                    detail: {
                        rows: data.rows || [],
                        rates: data.rates || {}
                    }
                }));
            }
            return;
        }

        if (dataType === 'routes') {
            await window.travelManagerRoutes?.list(true);
            return;
        }

        if (dataType === 'favourites') {
            await window.travelManagerFavourites?.listTags(true);
            await window.travelManagerFavourites?.list(true);
        }
    };

    const dataTransferLabel = (dataType) => (
        dataTransferOptions.find((option) => option.id === dataType)?.label || 'Dane'
    );

    const downloadJson = (payload, filename) => {
        const blob = new Blob(
            [JSON.stringify(payload, null, 2)],
            { type: 'application/json;charset=utf-8' }
        );
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');

        link.href = url;
        link.download = filename || 'travel-manager-data.json';
        document.body.append(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(url);
    };

    const browserExport = async (dataType) => {
        const response = await fetch(`/api/settings/export/${encodeURIComponent(dataType)}`, {
            headers: { 'Accept': 'application/json' }
        });
        const data = await response.json().catch(() => ({}));

        if (!response.ok || data.status !== 'ok') {
            throw new Error(data.message || 'Nie udało się wyeksportować danych.');
        }

        downloadJson(data.payload, data.filename);
        window.alert(`Wyeksportowano dane: ${dataTransferLabel(dataType)}.`);
    };

    const browserImport = (dataType) => {
        pendingBrowserImportType = dataType;
        importFileInput.value = '';
        importFileInput.click();
    };

    const runDataTransfer = async (mode, dataType) => {
        hideDataTransferMenu();
        const api = window.pywebview?.api;
        const method = mode === 'export' ? 'export_settings_data' : 'import_settings_data';

        if (!api?.[method]) {
            if (mode === 'export') {
                browserExport(dataType).catch((error) => {
                    window.alert(error?.message || 'Nie udało się wyeksportować danych.');
                });
                return;
            }

            browserImport(dataType);
            return;
        }

        try {
            const result = await api[method](dataType);

            if (!result || result.status === 'cancelled') {
                return;
            }

            if (result.status === 'error') {
                window.alert(result.message || 'Nie udało się wykonać operacji.');
                return;
            }

            if (result.status === 'imported') {
                await refreshAfterImport(dataType);
                await loadSettings();
                window.alert(`Zaimportowano dane: ${result.label}.`);
                return;
            }

            if (result.status === 'saved') {
                window.alert(`Wyeksportowano dane: ${result.label}.`);
            }
        } catch (error) {
            if (mode === 'export') {
                browserExport(dataType).catch((fallbackError) => {
                    window.alert(fallbackError?.message || error?.message || 'Nie udało się wyeksportować danych.');
                });
                return;
            }

            browserImport(dataType);
        }
    };

    const showDataTransferMenu = (mode, anchor) => {
        if (
            activeTransferButton === anchor
            && dataTransferMenu.classList.contains('settings-view__context-menu--open')
        ) {
            hideDataTransferMenu();
            return;
        }

        activeTransferButton = anchor;
        anchor.setAttribute('aria-expanded', 'true');
        dataTransferMenu.replaceChildren();

        dataTransferOptions.forEach((option) => {
            const button = document.createElement('button');
            button.className = 'settings-view__context-menu-button';
            button.type = 'button';
            button.role = 'menuitem';
            button.textContent = option.label;
            button.addEventListener('click', () => runDataTransfer(mode, option.id));
            dataTransferMenu.append(button);
        });

        dataTransferMenu.classList.add('settings-view__context-menu--open');
        dataTransferMenu.setAttribute('aria-hidden', 'false');

        const rect = anchor.getBoundingClientRect();
        const menuRect = dataTransferMenu.getBoundingClientRect();
        const left = Math.min(rect.left, window.innerWidth - menuRect.width - 10);
        dataTransferMenu.style.left = `${Math.max(10, left)}px`;
        dataTransferMenu.style.top = `${rect.bottom + 8}px`;
        dataTransferMenu.querySelector('[role="menuitem"]')?.focus();
    };

    const flushPendingSettings = () => {
        window.clearTimeout(saveTimer);

        if (!Object.keys(pendingSettings).length) {
            return;
        }

        const payload = pendingSettings;
        pendingSettings = {};
        patchUiSettings(payload);
    };

    const addNumberSetting = (group, label, field, value, unit, options = {}) => {
        const row = document.createElement('div');
        row.className = 'settings-view__value settings-view__value--control';

        const term = document.createElement('dt');
        term.textContent = label;

        const description = document.createElement('dd');
        description.className = 'settings-view__control';

        const input = document.createElement('input');
        input.className = 'settings-view__input';
        input.type = 'number';
        input.min = '0';
        if (options.max !== undefined) {
            input.max = String(options.max);
        }
        input.step = '0.01';
        input.value = String(numberValue(value));
        input.dataset.settingsField = field;

        const suffix = document.createElement('span');
        suffix.className = 'settings-view__unit';
        suffix.textContent = unit;

        input.addEventListener('input', () => {
            if (options.onInput) {
                options.onInput(numberValue(input.value));
                return;
            }

            schedulePatch({ [field]: numberValue(input.value) });
            document.dispatchEvent(new CustomEvent('travel-manager:ui-settings-changed', {
                detail: { [field]: numberValue(input.value) }
            }));
        });

        description.append(input, suffix);
        row.append(term, description);
        group.append(row);
    };

    const addBooleanSetting = (group, label, field, value, options = {}) => {
        const row = document.createElement('div');
        row.className = 'settings-view__value settings-view__value--control';
        row.dataset.settingsFieldRow = field;

        const term = document.createElement('dt');
        term.textContent = label;

        const description = document.createElement('dd');
        description.className = 'settings-view__control';

        const labelElement = document.createElement('label');
        labelElement.className = 'settings-view__checkbox';

        const input = document.createElement('input');
        input.type = 'checkbox';
        input.checked = Boolean(value);
        input.dataset.settingsField = field;
        input.disabled = Boolean(options.disabled);

        const text = document.createElement('span');
        text.textContent = 'Włączone';

        if (input.disabled) {
            row.classList.add('settings-view__value--disabled');
            labelElement.classList.add('settings-view__checkbox--disabled');
        }

        input.addEventListener('change', () => {
            const payload = { [field]: input.checked };
            schedulePatch(payload);
            document.dispatchEvent(new CustomEvent('travel-manager:ui-settings-changed', {
                detail: payload
            }));

            if (options.onChange) {
                options.onChange(input.checked);
            }
        });

        labelElement.append(input, text);
        description.append(labelElement);
        row.append(term, description);
        group.append(row);

        return {
            row,
            input,
            label: labelElement
        };
    };

    const addPercentSliderSetting = (group, label, field, value, options = {}) => {
        const row = document.createElement('div');
        row.className = 'settings-view__value settings-view__value--control';
        row.dataset.settingsFieldRow = field;

        const term = document.createElement('dt');
        term.textContent = label;

        const description = document.createElement('dd');
        description.className = 'settings-view__control settings-view__control--slider';

        const input = document.createElement('input');
        input.className = 'settings-view__slider';
        input.type = 'range';
        input.min = '0';
        input.max = '100';
        input.step = '1';
        input.value = String(Math.min(100, Math.max(0, Math.round(numberValue(value)))));
        input.dataset.settingsField = field;
        input.disabled = Boolean(options.disabled);

        const labelElement = document.createElement('span');
        labelElement.className = 'settings-view__slider-value';
        labelElement.textContent = `${input.value}%`;

        input.addEventListener('input', () => {
            const percent = numberValue(input.value);
            const payload = { [field]: percent };
            labelElement.textContent = `${Math.round(percent)}%`;
            schedulePatch(payload);
            document.dispatchEvent(new CustomEvent('travel-manager:ui-settings-changed', {
                detail: payload
            }));
        });

        description.append(input, labelElement);
        row.append(term, description);
        group.append(row);

        if (input.disabled) {
            row.classList.add('settings-view__value--disabled');
        }

        return {
            row,
            input,
            label: labelElement
        };
    };

    const loadFuelCostCurrencies = async () => {
        try {
            const response = await fetch('/api/fuel-costs', {
                headers: { 'Accept': 'application/json' }
            });
            const data = await response.json();

            if (!response.ok || data.status !== 'ok') {
                throw new Error(data.message || 'Nie udało się pobrać walut.');
            }

            const currencies = new Map();

            (data.countries || []).forEach((country) => {
                if (!country.currency) {
                    return;
                }

                const countries = currencies.get(country.currency) || [];
                countries.push(country.country);
                currencies.set(country.currency, countries);
            });

            return Array.from(currencies.entries())
                .sort(([left], [right]) => left.localeCompare(right))
                .map(([currency, countries]) => ({
                    currency,
                    label: currency === 'EUR'
                        ? `${currency} (strefa euro)`
                        : `${currency} (${countries.join(', ')})`
                }));
        } catch (error) {
            return [
                { currency: 'EUR', label: 'EUR (strefa euro)' },
                { currency: 'PLN', label: 'PLN (Polska)' }
            ];
        }
    };

    const addTravelCostCurrencySetting = async (group, settings) => {
        const row = document.createElement('div');
        row.className = 'settings-view__value settings-view__value--control';

        const term = document.createElement('dt');
        term.textContent = 'Waluta kosztów trasy';

        const description = document.createElement('dd');
        description.className = 'settings-view__control settings-view__control--fuel-type';

        const select = document.createElement('select');
        select.className = 'settings-view__select';

        const message = document.createElement('span');
        message.className = 'settings-view__hint';
        message.textContent = 'Według kraju zostawia lokalne waluty w tabeli cen, a koszt trasy sumuje w PLN.';

        const countryOption = document.createElement('option');
        countryOption.value = 'country';
        countryOption.textContent = 'Według kraju';
        select.append(countryOption);

        (await loadFuelCostCurrencies()).forEach((item) => {
            const option = document.createElement('option');
            option.value = item.currency;
            option.textContent = item.label;
            select.append(option);
        });

        select.value = Array.from(select.options).some((option) => option.value === settings.travel_cost_currency)
            ? settings.travel_cost_currency
            : 'country';

        select.addEventListener('change', () => {
            const payload = { travel_cost_currency: select.value };
            schedulePatch(payload);
            document.dispatchEvent(new CustomEvent('travel-manager:ui-settings-changed', {
                detail: payload
            }));
        });

        description.append(select, message);
        row.append(term, description);
        group.append(row);
    };

    const loadSettings = async () => {
        mapGroup.replaceChildren();
        panelsGroup.replaceChildren();
        layersGroup.replaceChildren();
        travelCostsGroup.replaceChildren();
        routeFuelGroup.replaceChildren();
        routeTollsGroup.replaceChildren();
        routeFuelMainInput = null;
        routeFuelDependentRows = [];

        try {
            const response = await fetch('/api/settings/ui', {
                headers: { 'Accept': 'application/json' }
            });

            if (!response.ok) {
                throw new Error(`Settings request failed: ${response.status}`);
            }

            const settings = (await response.json()).ui || {};

            addValue(mapGroup, 'Szerokość geograficzna', settings.map_latitude);
            addValue(mapGroup, 'Długość geograficzna', settings.map_longitude);
            addValue(mapGroup, 'Powiększenie', settings.map_zoom);
            addValue(mapGroup, 'Warstwa bazowa', settings.map_base_layer);

            addValue(panelsGroup, 'Szczegóły miejsca', `${settings.place_details_panel_width} px`);
            addValue(panelsGroup, 'Szczegóły trasy', `${settings.route_details_panel_width} px`);
            addValue(panelsGroup, 'Szczegóły samochodu', `${settings.car_details_panel_width} px`);
            addValue(panelsGroup, 'Legenda', `${settings.legend_details_panel_width} px`);
            addValue(panelsGroup, 'Warstwy', `${settings.layer_details_panel_width} px`);

            addValue(layersGroup, 'Notatki mapy', yesNo(settings.layer_map_notes_enabled));
            addValue(layersGroup, 'Dane mapy', yesNo(settings.layer_map_data_enabled));
            addValue(layersGroup, 'Publiczne ślady GPS', yesNo(settings.layer_public_gps_traces_enabled));
            addValue(layersGroup, 'Ulubione miejsca', yesNo(settings.layer_favourites_enabled));
            addValue(
                layersGroup,
                'Widoczne tagi ulubionych',
                Array.isArray(settings.layer_favourite_visible_tag_ids)
                    ? settings.layer_favourite_visible_tag_ids.join(', ') || 'Brak'
                    : 'Wszystkie'
            );

            await addTravelCostCurrencySetting(travelCostsGroup, settings);

            const setRouteFuelDependentsEnabled = (enabled) => {
                routeFuelDependentRows.forEach(({ row, input, label }) => {
                    input.disabled = !enabled;
                    row.classList.toggle('settings-view__value--disabled', !enabled);
                    label?.classList?.toggle('settings-view__checkbox--disabled', !enabled);
                });
            };

            const mainRouteFuel = addBooleanSetting(
                routeFuelGroup,
                'Separatory tankowania',
                'route_fuel_separators_enabled',
                settings.route_fuel_separators_enabled !== false,
                { onChange: setRouteFuelDependentsEnabled }
            );
            routeFuelMainInput = mainRouteFuel.input;
            routeFuelDependentRows.push(addBooleanSetting(
                routeFuelGroup,
                'Jazda ekonomiczna',
                'route_fuel_separator_economic_enabled',
                settings.route_fuel_separator_economic_enabled !== false,
                { disabled: !routeFuelMainInput.checked }
            ));
            routeFuelDependentRows.push(addBooleanSetting(
                routeFuelGroup,
                'Jazda średnia',
                'route_fuel_separator_average_enabled',
                settings.route_fuel_separator_average_enabled !== false,
                { disabled: !routeFuelMainInput.checked }
            ));
            routeFuelDependentRows.push(addBooleanSetting(
                routeFuelGroup,
                'Jazda dynamiczna',
                'route_fuel_separator_dynamic_enabled',
                settings.route_fuel_separator_dynamic_enabled !== false,
                { disabled: !routeFuelMainInput.checked }
            ));
            routeFuelDependentRows.push(addPercentSliderSetting(
                routeFuelGroup,
                'Próg tankowania',
                'route_fuel_separator_threshold_percent',
                settings.route_fuel_separator_threshold_percent ?? 20,
                { disabled: !routeFuelMainInput.checked }
            ));

            addBooleanSetting(
                routeTollsGroup,
                'Uwzględniaj płatne drogi i autostrady',
                'route_toll_roads_enabled',
                settings.route_toll_roads_enabled !== false
            );
        } catch (error) {
            addValue(mapGroup, 'Stan', 'Nie udało się wczytać ustawień.');
        }
    };

    document.addEventListener('travel-manager:app-view-changed', (event) => {
        if (event.detail?.view === 'settings') {
            loadSettings();
        }
    });
    document.addEventListener('travel-manager:settings-save-requested', flushPendingSettings);

    document.querySelector('#settings-export-data')?.addEventListener('click', (event) => {
        showDataTransferMenu('export', event.currentTarget);
    });
    document.querySelector('#settings-import-data')?.addEventListener('click', (event) => {
        showDataTransferMenu('import', event.currentTarget);
    });
    importFileInput.addEventListener('change', async () => {
        const dataType = pendingBrowserImportType;
        const file = importFileInput.files?.[0];
        pendingBrowserImportType = null;

        if (!dataType || !file) {
            return;
        }

        try {
            const payload = JSON.parse(await file.text());
            const response = await fetch(`/api/settings/import/${encodeURIComponent(dataType)}`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            const data = await response.json().catch(() => ({}));

            if (!response.ok || data.status !== 'imported') {
                throw new Error(data.message || 'Nie udało się zaimportować danych.');
            }

            await refreshAfterImport(dataType);
            await loadSettings();
            window.alert(`Zaimportowano dane: ${data.label || dataTransferLabel(dataType)}.`);
        } catch (error) {
            window.alert(error?.message || 'Nie udało się zaimportować danych.');
        }
    });
    document.addEventListener('click', (event) => {
        if (
            !dataTransferMenu.contains(event.target)
            && !event.target.closest('#settings-export-data, #settings-import-data')
        ) {
            hideDataTransferMenu();
        }
    });
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            hideDataTransferMenu();
        }
    });

    document.querySelectorAll('[data-settings-collapse]').forEach((button) => {
        button.addEventListener('click', () => {
            const section = button.closest('[data-settings-section]');
            const expanded = button.getAttribute('aria-expanded') !== 'false';
            const nextExpanded = !expanded;
            const iconName = nextExpanded ? 'chevron-up' : 'chevron-down';

            section?.classList.toggle('settings-view__section--collapsed', !nextExpanded);
            button.setAttribute('aria-expanded', String(nextExpanded));
            button.setAttribute('aria-label', nextExpanded ? 'Zwiń grupę' : 'Rozwiń grupę');
            button.innerHTML = `<i data-lucide="${iconName}" aria-hidden="true"></i>`;
            window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
        });
    });

    loadSettings();
});
