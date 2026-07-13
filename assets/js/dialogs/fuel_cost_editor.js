document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#fuel-cost-editor');
    const title = document.querySelector('#fuel-cost-editor-title');
    const countryCodeInput = document.querySelector('#fuel-cost-editor-country-code');
    const countryInput = document.querySelector('#fuel-cost-editor-country');
    const countrySelect = document.querySelector('#fuel-cost-editor-country-select');
    const currencySelect = document.querySelector('#fuel-cost-editor-currency');
    const cancelButtons = dialog?.querySelectorAll('[data-fuel-cost-editor-cancel]');
    let resolveResult = null;
    let currencies = [];

    if (!layer || !dialog || !title || !countryCodeInput || !countryInput || !countrySelect || !currencySelect || !cancelButtons?.length) {
        return;
    }

    const priceFields = ['petrol_95', 'petrol_98', 'diesel', 'lpg'];
    let countryPresets = [];

    const loadCurrencies = (countries = []) => {
        const map = new Map();
        countries.forEach((country) => {
            if (!country.currency) {
                return;
            }

            const names = map.get(country.currency) || [];
            names.push(country.country);
            map.set(country.currency, names);
        });

        currencies = Array.from(map.entries())
            .sort(([left], [right]) => left.localeCompare(right))
            .map(([currency, names]) => ({
                currency,
                label: currency === 'EUR' ? 'EUR (strefa euro)' : `${currency} (${names.join(', ')})`
            }));
    };

    const renderCurrencies = (selected) => {
        currencySelect.replaceChildren();
        currencies.forEach((item) => {
            const option = document.createElement('option');
            option.value = item.currency;
            option.textContent = item.label;
            currencySelect.append(option);
        });

        if (!Array.from(currencySelect.options).some((option) => option.value === selected)) {
            const option = document.createElement('option');
            option.value = selected || 'EUR';
            option.textContent = selected || 'EUR';
            currencySelect.append(option);
        }

        currencySelect.value = selected || 'EUR';
    };

    const renderCountries = (selected) => {
        countrySelect.replaceChildren();
        countryPresets.forEach((country) => {
            const option = document.createElement('option');
            option.value = country.country_code;
            option.textContent = `${country.country} (${country.country_code})`;
            option.dataset.country = country.country;
            option.dataset.currency = country.currency;
            countrySelect.append(option);
        });

        countrySelect.value = Array.from(countrySelect.options).some((option) => option.value === selected)
            ? selected
            : countryPresets[0]?.country_code || '';
    };

    const syncCountryFields = (forceCurrency = false) => {
        const selected = countrySelect.selectedOptions[0];

        if (!selected) {
            return;
        }

        countryCodeInput.value = selected.value;
        countryInput.value = selected.dataset.country || selected.textContent || selected.value;

        if (forceCurrency || !currencySelect.value) {
            currencySelect.value = selected.dataset.currency || currencySelect.value || 'EUR';
        }
    };

    const finish = (result) => {
        dialog.setAttribute('aria-hidden', 'true');
        layer.classList.remove('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'true');
        const resolve = resolveResult;
        resolveResult = null;
        resolve?.(result);
    };

    const show = ({ row = null, countries = [] } = {}) => {
        if (resolveResult) {
            resolveResult(null);
        }

        loadCurrencies(countries);
        countryPresets = [...countries].sort((left, right) => (
            (left.country || '').localeCompare(right.country || '', 'pl', { sensitivity: 'base' })
        ));
        dialog.reset();
        title.textContent = row ? 'Edytuj ceny paliw' : 'Dodaj kraj';
        renderCurrencies(row?.currency || 'EUR');
        renderCountries(row?.country_code || countryPresets[0]?.country_code || '');
        syncCountryFields(!row);
        if (row?.currency) {
            currencySelect.value = row.currency;
        }
        priceFields.forEach((field) => {
            dialog.elements[field].value = row?.[field] ?? '';
        });

        dialog.setAttribute('aria-hidden', 'false');
        layer.classList.add('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'false');

        return new Promise((resolve) => {
            resolveResult = resolve;
            window.requestAnimationFrame(() => {
                (row ? dialog.elements.petrol_95 : countrySelect).focus();
            });
        });
    };

    dialog.addEventListener('submit', (event) => {
        event.preventDefault();
        const result = {
            country_code: countryCodeInput.value.trim().toUpperCase(),
            country: countryInput.value.trim(),
            currency: currencySelect.value
        };

        priceFields.forEach((field) => {
            result[field] = dialog.elements[field].value;
        });

        finish(result);
    });
    countrySelect.addEventListener('change', () => syncCountryFields(true));
    cancelButtons.forEach((button) => button.addEventListener('click', () => finish(null)));
    layer.addEventListener('click', (event) => {
        if (event.target === layer && resolveResult) {
            finish(null);
        }
    });

    window.travelManagerFuelCostEditor = { show };
});
