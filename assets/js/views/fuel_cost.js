document.addEventListener('travel-manager:views-ready', () => {
    const view = document.querySelector('[data-app-view="fuel-cost"]');
    const form = document.querySelector('#fuel-cost-search');
    const searchInput = document.querySelector('#fuel-cost-search-input');
    const updateButton = document.querySelector('#fuel-cost-update');
    const currencySelect = document.querySelector('#fuel-cost-currency');
    const sortFieldSelect = document.querySelector('#fuel-cost-sort-field');
    const sortButton = document.querySelector('#fuel-cost-sort-button');
    const sortMenu = document.querySelector('#fuel-cost-sort-menu');
    const meta = document.querySelector('#fuel-cost-meta');
    const tableBody = document.querySelector('#fuel-cost-table-body');
    const addButton = document.querySelector('#fuel-cost-add');

    if (!view || !form || !searchInput || !updateButton || !currencySelect || !sortFieldSelect || !sortButton || !sortMenu || !meta || !tableBody || !addButton) {
        return;
    }

    const priceFields = ['petrol_95', 'petrol_98', 'diesel', 'lpg'];
    const updateSupportedCodes = new Set([
        'AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR', 'HR', 'HU',
        'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK'
    ]);

    const state = {
        query: '',
        rows: [],
        countries: [],
        rates: {},
        metadata: {},
        selectedCurrency: 'original',
        sortField: 'country',
        sortDirection: 'asc',
        loading: false
    };

    const setSortOpen = (open) => {
        sortMenu.setAttribute('aria-hidden', String(!open));
        sortButton.setAttribute('aria-expanded', String(open));
    };

    const selectedConversionCurrency = () => {
        return state.selectedCurrency === 'original' ? null : state.selectedCurrency;
    };

    const formatDateOnly = (value) => {
        if (!value) {
            return '';
        }

        const parsed = new Date(value);

        if (!Number.isNaN(parsed.getTime())) {
            return parsed.toLocaleDateString('pl-PL');
        }

        const match = String(value).match(/^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})$/);
        const months = {
            january: '01',
            february: '02',
            march: '03',
            april: '04',
            may: '05',
            june: '06',
            july: '07',
            august: '08',
            september: '09',
            october: '10',
            november: '11',
            december: '12'
        };

        if (!match) {
            return String(value);
        }

        const day = match[1].padStart(2, '0');
        const month = months[match[2].toLowerCase()];

        return month ? `${day}.${month}.${match[3]}` : String(value);
    };

    const formatDateTime = (value) => {
        if (!value) {
            return '';
        }

        const parsed = new Date(value);

        if (Number.isNaN(parsed.getTime())) {
            return String(value);
        }

        return parsed.toLocaleString('pl-PL', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    };

    const formatManualDate = (value) => {
        if (!value) {
            return '-';
        }

        return formatDateTime(value);
    };

    const currencyRate = (currency) => {
        if (!currency || currency === 'EUR') {
            return 1;
        }

        const rate = Number(state.rates[currency]);
        return Number.isFinite(rate) && rate > 0 ? rate : 0;
    };

    const convertedPrice = (row, field) => {
        const number = Number(row[field]);

        if (!Number.isFinite(number) || number <= 0) {
            return null;
        }

        const sourceCurrency = row.source_currency || 'EUR';
        const targetCurrency = selectedConversionCurrency() || row.currency || sourceCurrency;

        if (sourceCurrency === targetCurrency) {
            return number;
        }

        const sourceRate = currencyRate(sourceCurrency);
        const targetRate = currencyRate(targetCurrency);

        if (!sourceRate || !targetRate) {
            return null;
        }

        return number / sourceRate * targetRate;
    };

    const displayCurrency = (row) => {
        return selectedConversionCurrency() || row.currency || row.source_currency || 'EUR';
    };

    const formatPrice = (row, field) => {
        const converted = convertedPrice(row, field);

        if (!Number.isFinite(converted) || converted <= 0) {
            return '';
        }

        const currency = displayCurrency(row);

        return new Intl.NumberFormat('pl-PL', {
            style: 'currency',
            currency,
            minimumFractionDigits: 2,
            maximumFractionDigits: 3
        }).format(converted);
    };

    const rawSortValue = (row, field) => {
        const number = convertedPrice(row, field);

        if (!Number.isFinite(number) || number <= 0) {
            return Number.POSITIVE_INFINITY;
        }

        return number;
    };

    const filteredRows = () => {
        const query = state.query.trim().toLocaleLowerCase('pl');
        const rows = query
            ? state.rows.filter((row) => (
                (row.country || '').toLocaleLowerCase('pl').includes(query)
                || (row.country_code || '').toLocaleLowerCase('pl').includes(query)
            ))
            : [...state.rows];

        return rows.sort((left, right) => {
            let result = 0;

            if (state.sortField === 'country') {
                result = (left.country || '').localeCompare(right.country || '', 'pl', { sensitivity: 'base' });
            } else if (state.sortField === 'manual_updated_at') {
                result = new Date(left.manual_updated_at || 0).getTime() - new Date(right.manual_updated_at || 0).getTime();
            } else {
                result = rawSortValue(left, state.sortField) - rawSortValue(right, state.sortField);
            }

            return state.sortDirection === 'asc' ? result : -result;
        });
    };

    const renderCurrencyOptions = () => {
        const selected = state.selectedCurrency;
        currencySelect.replaceChildren();

        const original = document.createElement('option');
        original.value = 'original';
        original.textContent = 'Oryginalne';
        currencySelect.append(original);

        const currencies = new Map();

        state.countries.forEach((country) => {
            if (!country.currency) {
                return;
            }

            const countries = currencies.get(country.currency) || [];
            countries.push(country.country);
            currencies.set(country.currency, countries);
        });

        Array.from(currencies.keys()).sort((left, right) => left.localeCompare(right)).forEach((currency) => {
            const countries = currencies.get(currency) || [];
            const option = document.createElement('option');
            option.value = currency;
            option.textContent = currency === 'EUR'
                ? `${currency} (strefa euro)`
                : `${currency} (${countries.join(', ')})`;
            currencySelect.append(option);
        });

        currencySelect.value = Array.from(currencySelect.options).some((option) => option.value === selected)
            ? selected
            : 'original';
        state.selectedCurrency = currencySelect.value;
    };

    const renderMeta = () => {
        if (state.loading) {
            meta.textContent = 'Ładowanie cen paliw...';
            return;
        }

        const parts = [];

        if (state.metadata.source === 'manual') {
            parts.push('Źródło: dane ręczne');
        } else if (state.metadata.source) {
            parts.push(state.metadata.poland_source
                ? 'Źródło: European Commission Weekly Oil Bulletin + AutoCentrum (Polska)'
                : 'Źródło: European Commission Weekly Oil Bulletin');
        }

        if (state.metadata.updated) {
            parts.push(`Ostatnia aktualizacja: ${formatDateOnly(state.metadata.updated)}`);
        }

        if (state.metadata.loaded_at) {
            parts.push(`Pobrano: ${formatDateTime(state.metadata.loaded_at)}`);
        }

        if (state.metadata.warning) {
            parts.push(state.metadata.warning);
        }

        meta.textContent = parts.join(' | ') || 'Brak pobranych danych. Użyj przycisku „Aktualizuj dane”.';
    };

    const render = () => {
        tableBody.replaceChildren();
        const rows = filteredRows();

        if (!rows.length) {
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            td.className = 'fuel-cost-view__empty';
            td.colSpan = 7;
            td.textContent = state.query ? 'Nie znaleziono kraju.' : 'Brak danych cen paliw.';
            tr.append(td);
            tableBody.append(tr);
            renderMeta();
            return;
        }

        rows.forEach((row) => {
            const tr = document.createElement('tr');
            const country = document.createElement('td');
            country.textContent = row.country || row.country_code || '-';
            tr.append(country);

            priceFields.forEach((field) => {
                const td = document.createElement('td');
                const text = formatPrice(row, field);
                td.textContent = text || '-';

                if (!text) {
                    td.className = 'fuel-cost-view__price-empty';
                }

                tr.append(td);
            });

            const updated = document.createElement('td');
            updated.className = 'fuel-cost-view__manual-date';
            updated.textContent = row.manual ? formatManualDate(row.manual_updated_at) : '-';
            tr.append(updated);

            const actions = document.createElement('td');
            const actionsWrap = document.createElement('div');
            actionsWrap.className = 'fuel-cost-view__row-actions';

            const edit = document.createElement('button');
            edit.className = 'fuel-cost-view__edit';
            edit.type = 'button';
            edit.innerHTML = '<i data-lucide="pencil" aria-hidden="true"></i><span>Edytuj</span>';
            edit.addEventListener('click', () => editRow(row));

            actionsWrap.append(edit);
            actions.append(actionsWrap);
            tr.append(actions);

            tableBody.append(tr);
        });

        renderMeta();
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };

    const loadData = async (force = false, overwriteManual = []) => {
        state.loading = true;
        updateButton.disabled = true;
        render();

        try {
            const params = new URLSearchParams();

            if (force) {
                params.set('force', 'true');
            }

            if (overwriteManual.length) {
                params.set('overwrite_manual', overwriteManual.join(','));
            }

            const query = params.toString();
            const response = await fetch(`/api/fuel-costs${query ? `?${query}` : ''}`, {
                cache: 'no-store',
                headers: { 'Accept': 'application/json' }
            });
            const data = await response.json();

            if (!response.ok || data.status !== 'ok') {
                throw new Error(data.message || `HTTP ${response.status}`);
            }

            state.rows = data.rows || [];
            state.countries = data.countries || [];
            state.rates = data.rates || {};
            state.metadata = data.metadata || {};
            renderCurrencyOptions();
            document.dispatchEvent(new CustomEvent('travel-manager:fuel-costs-changed', {
                detail: {
                    rows: state.rows,
                    rates: state.rates,
                    countries: state.countries,
                    metadata: state.metadata
                }
            }));
        } catch (error) {
            state.metadata = {
                ...state.metadata,
                warning: `Nie udało się pobrać danych: ${error.message}`
            };
        } finally {
            state.loading = false;
            updateButton.disabled = false;
            render();
        }
    };

    const saveManualRow = async (row) => {
        const response = await fetch('/api/fuel-costs/manual', {
            method: row.country_code && state.rows.some((item) => item.country_code === row.country_code) ? 'PATCH' : 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(row)
        });
        const data = await response.json();

        if (!response.ok || data.status !== 'ok') {
            throw new Error(data.message || `HTTP ${response.status}`);
        }

        state.rows = data.rows || [];
        state.countries = data.countries || [];
        state.rates = data.rates || {};
        state.metadata = data.metadata || {};
        renderCurrencyOptions();
        render();
        document.dispatchEvent(new CustomEvent('travel-manager:fuel-costs-changed', {
            detail: {
                rows: state.rows,
                rates: state.rates,
                countries: state.countries,
                metadata: state.metadata
            }
        }));
    };

    async function editRow(row = null) {
        const result = await window.travelManagerFuelCostEditor?.show({
            row,
            countries: state.countries
        });

        if (!result) {
            return;
        }

        try {
            await saveManualRow(result);
        } catch (error) {
            state.metadata = {
                ...state.metadata,
                warning: `Nie udało się zapisać cen: ${error.message}`
            };
            render();
        }
    }

    const manualRowsForUpdate = () => state.rows
        .filter((row) => row.manual)
        .map((row) => ({
            ...row,
            updateAvailable: updateSupportedCodes.has(String(row.country_code || '').toUpperCase())
        }));

    const confirmUpdate = async () => {
        const manualRows = manualRowsForUpdate();

        if (!manualRows.length) {
            await loadData(true);
            return;
        }

        const result = await window.travelManagerFuelUpdateDialog?.show({ rows: manualRows });

        if (result?.action !== 'update') {
            return;
        }

        await loadData(true, result.overwrite || []);
    };

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        state.query = searchInput.value;
        render();
    });

    searchInput.addEventListener('input', () => {
        state.query = searchInput.value;
        render();
    });

    updateButton.addEventListener('click', confirmUpdate);
    addButton.addEventListener('click', () => editRow(null));

    currencySelect.addEventListener('change', () => {
        state.selectedCurrency = currencySelect.value;
        render();
    });

    sortFieldSelect.addEventListener('change', () => {
        state.sortField = sortFieldSelect.value;
        render();
    });

    sortButton.addEventListener('click', () => {
        setSortOpen(sortMenu.getAttribute('aria-hidden') !== 'false');
    });

    sortMenu.addEventListener('click', (event) => {
        const button = event.target.closest('[data-sort-direction]');

        if (!button) {
            return;
        }

        state.sortDirection = button.dataset.sortDirection;
        setSortOpen(false);
        render();
    });

    document.addEventListener('click', (event) => {
        if (!sortMenu.contains(event.target) && !sortButton.contains(event.target)) {
            setSortOpen(false);
        }
    });

    loadData(false);
});
