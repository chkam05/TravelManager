(function () {
    'use strict';

    const configuration = window.TRAVEL_MANAGER_I18N || {};
    const languageDefinitions = Array.isArray(configuration.languages)
        ? configuration.languages
        : [];
    const DEFAULT_LOCALE = languageDefinitions[0]?.locale || '';
    const catalogUrls = new Map(languageDefinitions.map(
        ({ locale, catalog_url: catalogUrl }) => [locale, catalogUrl]
    ));
    const KEY_PATTERN = /^[A-Z][A-Z0-9_]*(?:\.[A-Z][A-Z0-9_]*)+$/;
    const requestedLocale = String(configuration.locale || '');
    const locale = catalogUrls.has(requestedLocale) ? requestedLocale : DEFAULT_LOCALE;
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
        const catalogUrl = catalogUrls.get(catalogLocale);
        if (!catalogUrl) throw new Error(`Unknown language catalog: ${catalogLocale}`);
        const response = await fetch(catalogUrl, {
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
        languages: Object.freeze(languageDefinitions.map(({ locale: value, label_key: labelKey }) => Object.freeze({
            locale: value,
            labelKey
        }))),
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
