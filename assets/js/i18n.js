(function () {
    'use strict';

    const DEFAULT_LOCALE = 'en_US';
    const SUPPORTED_LOCALES = new Set(['en_US', 'pl_PL']);
    const KEY_PATTERN = /^[A-Z][A-Z0-9_]*(?:\.[A-Z][A-Z0-9_]*)+$/;
    const requestedLocale = String(window.TRAVEL_MANAGER_LANGUAGE || '');
    const locale = SUPPORTED_LOCALES.has(requestedLocale) ? requestedLocale : DEFAULT_LOCALE;
    const catalogs = new Map();
    const missingWarnings = new Set();
    let loaded = false;

    const find = (catalog, key) => {
        let value = catalog;
        for (const part of key.split('.')) {
            if (!value || typeof value !== 'object' || !(part in value)) return null;
            value = value[part];
        }
        return typeof value === 'string' ? value : null;
    };

    const interpolate = (value, parameters) => value.replace(
        /\{([A-Za-z_][A-Za-z0-9_]*)\}/g,
        (match, key) => Object.prototype.hasOwnProperty.call(parameters, key)
            ? String(parameters[key])
            : match
    );

    const loadCatalog = async (catalogLocale) => {
        const response = await fetch(`/assets/languages/${catalogLocale}.json`, {
            cache: 'no-cache',
            headers: { 'Accept': 'application/json' }
        });
        if (!response.ok) throw new Error(`Language request failed: ${response.status}`);
        const catalog = await response.json();
        catalogs.set(catalogLocale, catalog);
    };

    const warnMissing = (key) => {
        if (!loaded || missingWarnings.has(key)) return;
        missingWarnings.add(key);
        window.console?.warn(`Missing translation key: ${key}`);
    };

    const ready = Promise.all([
        loadCatalog(DEFAULT_LOCALE),
        ...(locale === DEFAULT_LOCALE ? [] : [loadCatalog(locale)])
    ]).then(() => {
        loaded = true;
        document.documentElement.lang = locale.slice(0, 2);
        document.dispatchEvent(new CustomEvent('travel-manager:language-ready', {
            detail: { locale }
        }));
    }).catch((error) => {
        loaded = true;
        window.console?.error('Unable to load language catalog.', error);
    });

    window.i18n = Object.freeze({
        locale,
        ready,
        has(key) {
            if (!KEY_PATTERN.test(key)) return false;
            return find(catalogs.get(locale), key) !== null
                || find(catalogs.get(DEFAULT_LOCALE), key) !== null;
        },
        t(key, parameters = {}) {
            if (!KEY_PATTERN.test(key)) {
                throw new Error(`Invalid translation key: ${key}`);
            }
            const value = find(catalogs.get(locale), key)
                ?? find(catalogs.get(DEFAULT_LOCALE), key);
            if (value === null) {
                warnMissing(key);
                return key;
            }
            return interpolate(value, parameters);
        }
    });
}());
