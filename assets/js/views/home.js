document.addEventListener('travel-manager:views-ready', () => {
    const input = document.querySelector('[data-home-open-on-startup]');
    const languageSelect = document.querySelector('[data-home-language]');

    if (!input && !languageSelect) {
        return;
    }

    const setOpenOnStartup = (value) => {
        if (input) input.checked = value === true;
    };

    const setLanguage = (value) => {
        if (!languageSelect) return;
        const supported = Array.from(languageSelect.options).some(
            (option) => option.value === value
        );
        languageSelect.value = supported ? value : languageSelect.options[0]?.value;
    };

    fetch('/api/settings/ui', {
        headers: { 'Accept': 'application/json' }
    })
        .then((response) => response.json())
        .then((data) => {
            setOpenOnStartup(data?.ui?.open_home_on_startup);
            setLanguage(data?.ui?.language);
        })
        .catch(() => {});

    if (input) {
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
                    throw new Error(window.i18n.t('HOME_VIEW.SETTING_SAVE_FAILED'));
                }

                document.dispatchEvent(new CustomEvent('travel-manager:ui-settings-changed', {
                    detail: payload
                }));
            }).catch(() => {
                input.checked = !input.checked;
            });
        });
    }

    if (languageSelect) {
        languageSelect.addEventListener('change', () => {
            const previousLanguage = window.i18n.locale;
            const payload = { language: languageSelect.value };
            languageSelect.disabled = true;

            fetch('/api/settings/ui', {
                method: 'PATCH',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            }).then((response) => {
                if (!response.ok) {
                    throw new Error(window.i18n.t('HOME_VIEW.SETTING_SAVE_FAILED'));
                }

                window.location.reload();
            }).catch(() => {
                setLanguage(previousLanguage);
                languageSelect.disabled = false;
            });
        });
    }

    document.addEventListener('travel-manager:ui-settings-changed', (event) => {
        if (Object.hasOwn(event.detail || {}, 'open_home_on_startup')) {
            setOpenOnStartup(event.detail.open_home_on_startup);
        }
        if (Object.hasOwn(event.detail || {}, 'language')) {
            setLanguage(event.detail.language);
        }
    });
});
