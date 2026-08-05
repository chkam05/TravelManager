document.addEventListener('travel-manager:views-ready', () => {
    const input = document.querySelector('[data-home-open-on-startup]');

    if (!input) {
        return;
    }

    const setValue = (value) => {
        input.checked = value === true;
    };

    fetch('/api/settings/ui', {
        headers: { 'Accept': 'application/json' }
    })
        .then((response) => response.json())
        .then((data) => setValue(data?.ui?.open_home_on_startup))
        .catch(() => {});

    input.addEventListener('change', () => {
        const payload = { open_home_on_startup: input.checked };

        fetch('/api/settings/ui', {
            method: 'PATCH',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        }).then((response) => {
            if (!response.ok) {
                throw new Error('Nie udało się zapisać ustawienia.');
            }

            document.dispatchEvent(new CustomEvent('travel-manager:ui-settings-changed', {
                detail: payload
            }));
        }).catch(() => {
            input.checked = !input.checked;
        });
    });

    document.addEventListener('travel-manager:ui-settings-changed', (event) => {
        if (Object.hasOwn(event.detail || {}, 'open_home_on_startup')) {
            setValue(event.detail.open_home_on_startup);
        }
    });
});
