document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#fuel-update');
    const list = document.querySelector('#fuel-update-list');
    const cancelButtons = dialog?.querySelectorAll('[data-fuel-update-cancel]');
    let resolveResult = null;

    if (!layer || !dialog || !list || !cancelButtons?.length) {
        return;
    }

    const finish = (result) => {
        dialog.setAttribute('aria-hidden', 'true');
        layer.classList.remove('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'true');
        const resolve = resolveResult;
        resolveResult = null;
        resolve?.(result);
    };

    const render = (rows) => {
        list.replaceChildren();

        if (!rows.length) {
            const empty = document.createElement('p');
            empty.className = 'fuel-update__description';
            empty.textContent = 'Brak ręcznych zmian do sprawdzenia.';
            list.append(empty);
            return;
        }

        rows.forEach((row) => {
            const item = document.createElement('div');
            item.className = 'fuel-update__item';

            const name = document.createElement('div');
            name.className = 'fuel-update__country';
            name.textContent = `${row.country || row.country_code} (${row.country_code})`;

            if (!row.updateAvailable) {
                const warning = document.createElement('span');
                warning.className = 'fuel-update__warning';
                warning.textContent = '! Dane nie zostaną zaktualizowane';
                item.append(name, warning);
            } else {
                const label = document.createElement('label');
                label.className = 'fuel-update__checkbox';

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.value = row.country_code;
                checkbox.dataset.fuelUpdateOverwrite = row.country_code;

                const text = document.createElement('span');
                text.textContent = 'Nadpisz';

                label.append(checkbox, text);
                item.append(name, label);
            }

            list.append(item);
        });
    };

    const show = ({ rows = [] } = {}) => {
        if (resolveResult) {
            resolveResult(null);
        }

        render(rows);
        dialog.setAttribute('aria-hidden', 'false');
        layer.classList.add('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'false');

        return new Promise((resolve) => {
            resolveResult = resolve;
        });
    };

    dialog.addEventListener('submit', (event) => {
        event.preventDefault();
        const overwrite = Array.from(dialog.querySelectorAll('[data-fuel-update-overwrite]:checked'))
            .map((input) => input.value);
        finish({ action: 'update', overwrite });
    });
    cancelButtons.forEach((button) => button.addEventListener('click', () => finish(null)));
    layer.addEventListener('click', (event) => {
        if (event.target === layer && resolveResult) {
            finish(null);
        }
    });

    window.travelManagerFuelUpdateDialog = { show };
});
