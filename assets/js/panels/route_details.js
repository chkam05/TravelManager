document.addEventListener('travel-manager:views-ready', () => {
    const panel = document.querySelector('#route-details-panel');
    const tabs = document.querySelectorAll('[data-route-tab]');
    const tabPanels = document.querySelectorAll('[data-route-tab-panel]');
    const pointsList = document.querySelector('#route-details-panel-points');
    const instructionsList = document.querySelector('#route-details-panel-instructions');
    const status = document.querySelector('#route-details-panel-status');
    const summary = document.querySelector('#route-details-panel-summary');
    const addButton = document.querySelector('#route-details-panel-add');
    const reverseButton = document.querySelector('#route-details-panel-reverse');
    const saveButton = document.querySelector('#route-details-panel-save');
    const editNameButton = document.querySelector('#route-details-panel-edit-name');
    const transportButtons = document.querySelectorAll('[data-route-transport]');
    const fuelSection = document.querySelector('#route-details-panel-fuel');
    const fuelSlider = document.querySelector('#route-details-panel-fuel-slider');
    const fuelLabel = document.querySelector('#route-details-panel-fuel-label');
    const separatorsEnabledInput = document.querySelector('#route-details-panel-separators-enabled');
    const separatorEconomicInput = document.querySelector('#route-details-panel-separator-economic');
    const separatorAverageInput = document.querySelector('#route-details-panel-separator-average');
    const separatorDynamicInput = document.querySelector('#route-details-panel-separator-dynamic');
    const separatorsOptions = document.querySelector('#route-details-panel-separators-options');
    const separatorSettings = document.querySelector('#route-details-panel-separator-settings');
    const tollSettings = document.querySelector('#route-details-panel-toll-settings');
    const tollRoadsEnabledInput = document.querySelector('#route-details-panel-toll-roads-enabled');
    const titleIcon = document.querySelector('#route-details-panel-title-icon');
    const titleText = document.querySelector('#route-details-panel-title-text');
    const closeButton = document.querySelector('[data-route-details-panel-close]');
    const grabber = document.querySelector('[data-route-details-panel-grabber]');
    const menu = document.querySelector('#route-details-panel-menu');

    if (
        !panel
        || !tabs.length
        || !tabPanels.length
        || !pointsList
        || !instructionsList
        || !status
        || !summary
        || !addButton
        || !reverseButton
        || !saveButton
        || !editNameButton
        || !transportButtons.length
        || !fuelSection
        || !fuelSlider
        || !fuelLabel
        || !separatorsEnabledInput
        || !separatorEconomicInput
        || !separatorAverageInput
        || !separatorDynamicInput
        || !separatorsOptions
        || !separatorSettings
        || !tollSettings
        || !tollRoadsEnabledInput
        || !titleIcon
        || !titleText
        || !closeButton
        || !menu
    ) {
        return;
    }

    // Keep the fixed context menu outside the transformed sliding panel.
    document.body.append(menu);

    const state = {
        points: [],
        activeTab: 'points',
        selecting: false,
        selectionMode: 'append',
        draggedId: null,
        menuPointId: null,
        routeRequestId: 0,
        currentRoute: null,
        savedRoute: null,
        transportMode: 'car',
        activeCarProfile: null,
        uiSettings: {},
        fuelCostRows: [],
        fuelCostRates: {},
        travelCostCurrency: 'country',
        countryCache: new Map(),
        fuelSeparatorDetails: new Map(),
        tollRoads: {
            roadsEnabled: true
        },
        fuelSeparators: {
            enabled: true,
            economicEnabled: true,
            averageEnabled: true,
            dynamicEnabled: true,
            thresholdPercent: 20
        },
        initialFuelPercent: 100,
        travelCosts: {
            minConsumption: 0,
            maxConsumption: 0
        }
    };
    const setActiveTab = (tab) => {
        state.activeTab = tab;

        tabs.forEach((button) => {
            const active = button.dataset.routeTab === tab;
            button.classList.toggle('route-details-panel__tab--active', active);
            button.setAttribute('aria-selected', String(active));
        });

        tabPanels.forEach((section) => {
            const active = section.dataset.routeTabPanel === tab;
            section.hidden = !active;
            section.classList.toggle('route-details-panel__tab-panel--active', active);
        });
    };

    const updateFuelSeparatorControls = () => {
        const enabled = state.fuelSeparators.enabled !== false;
        const visible = isCarTransport();

        separatorSettings.hidden = !visible;

        separatorsEnabledInput.checked = enabled;
        separatorEconomicInput.checked = state.fuelSeparators.economicEnabled !== false;
        separatorAverageInput.checked = state.fuelSeparators.averageEnabled !== false;
        separatorDynamicInput.checked = state.fuelSeparators.dynamicEnabled !== false;

        [separatorEconomicInput, separatorAverageInput, separatorDynamicInput].forEach((input) => {
            input.disabled = !enabled;
        });
        separatorsOptions.setAttribute('aria-disabled', String(!enabled));
    };

    const updateTollControls = () => {
        const visible = isCarTransport();
        const roadsEnabled = state.tollRoads.roadsEnabled !== false;

        tollSettings.hidden = !visible;
        tollRoadsEnabledInput.checked = roadsEnabled;
    };

    const patchUiSettings = (data) => fetch('/api/settings/ui', {
        method: 'PATCH',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).catch(() => {});

    const loadUiSettings = async () => {
        try {
            const response = await fetch('/api/settings/ui', {
                headers: { 'Accept': 'application/json' }
            });
            const data = response.ok ? await response.json() : null;
            const width = Number(data?.ui?.route_details_panel_width);

            if (Number.isFinite(width) && width > 0) {
                panel.style.setProperty('--route-details-panel-width', `${width}px`);
            }

            applyTravelCosts(data?.ui || {}, state.activeCarProfile);
        } catch (error) {
            // The default panel width remains usable.
        }
    };

    const applyTravelCosts = (settings = {}, carProfile = state.activeCarProfile) => {
        if (Object.keys(settings).length) {
            state.uiSettings = {
                ...state.uiSettings,
                ...settings
            };
        }

        state.fuelSeparators = {
            ...state.fuelSeparators,
            enabled: settings.route_fuel_separators_enabled ?? state.fuelSeparators.enabled,
            economicEnabled: settings.route_fuel_separator_economic_enabled ?? state.fuelSeparators.economicEnabled,
            averageEnabled: settings.route_fuel_separator_average_enabled ?? state.fuelSeparators.averageEnabled,
            dynamicEnabled: settings.route_fuel_separator_dynamic_enabled ?? state.fuelSeparators.dynamicEnabled,
            thresholdPercent: Math.min(100, Math.max(0, Number(
                settings.route_fuel_separator_threshold_percent ?? state.fuelSeparators.thresholdPercent
            ) || 0))
        };
        state.tollRoads = {
            ...state.tollRoads,
            roadsEnabled: settings.route_toll_roads_enabled ?? state.tollRoads.roadsEnabled
        };

        if (settings.travel_cost_currency) {
            state.travelCostCurrency = settings.travel_cost_currency;
        }

        state.travelCosts = {
            minConsumption: Math.max(0, Number(
                carProfile?.min_consumption ?? 0
            ) || 0),
            maxConsumption: Math.max(0, Number(
                carProfile?.max_consumption ?? 0
            ) || 0)
        };

        updateInitialFuelControls();
        updateFuelSeparatorControls();
        updateTollControls();
    };

    const resetRouteFuelSettings = () => {
        applyTravelCosts(state.uiSettings, state.activeCarProfile);
    };

    const loadFuelCostData = async () => {
        try {
            const response = await fetch('/api/fuel-costs', {
                cache: 'no-store',
                headers: { 'Accept': 'application/json' }
            });
            const data = await response.json();

            if (!response.ok || data.status !== 'ok') {
                throw new Error(data.message || 'Nie udało się pobrać cen paliw.');
            }

            state.fuelCostRows = data.rows || [];
            state.fuelCostRates = data.rates || {};
        } catch (error) {
            state.fuelCostRows = [];
            state.fuelCostRates = {};
        }
    };

    const isCarTransport = () => state.transportMode === 'car';

    const transportLabel = () => ({
        foot: 'Pieszo',
        bicycle: 'Rower',
        car: 'Samochód',
        public: 'Transport publiczny'
    }[state.transportMode] || 'Samochód');

    const updateTransportControls = () => {
        transportButtons.forEach((button) => {
            const active = button.dataset.routeTransport === state.transportMode;
            button.classList.toggle('route-details-panel__transport-button--active', active);
            button.setAttribute('aria-checked', String(active));
        });
    };

    const pointFromElement = (title, element) => {
        const latitude = Number(element?.coordinates?.latitude);
        const longitude = Number(element?.coordinates?.longitude);

        if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
            return null;
        }

        return {
            id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
            title: title || element?.display_name || `${latitude.toFixed(6)}, ${longitude.toFixed(6)}`,
            latitude,
            longitude,
            country_code: element?.address?.country_code || element?.raw_data?.address?.country_code || null
        };
    };

    const setSelecting = (selecting, mode = 'append') => {
        state.selecting = selecting;
        state.selectionMode = mode;
        status.classList.toggle('route-details-panel__status--selecting', selecting);
        status.textContent = selecting
            ? 'Kliknij punkt na mapie albo wyszukaj miejsce w polu u góry.'
            : state.points.length < 2
                ? 'Trasa wymaga co najmniej dwóch punktów.'
                : 'Przeciągnij punkty, aby zmienić ich kolejność.';
        addButton.disabled = selecting;
        reverseButton.disabled = selecting || state.points.length < 2;

        document.dispatchEvent(new CustomEvent('travel-manager:route-selection-changed', {
            detail: { selecting }
        }));
    };

    const formatDistance = (meters) => {
        const value = Number(meters);

        if (!Number.isFinite(value)) {
            return '-';
        }

        return value >= 1000 ? `${(value / 1000).toFixed(1)} km` : `${Math.round(value)} m`;
    };

    const formatDuration = (seconds) => {
        const value = Number(seconds);

        if (!Number.isFinite(value)) {
            return '-';
        }

        const totalMinutes = Math.round(value / 60);
        const hours = Math.floor(totalMinutes / 60);
        const minutes = totalMinutes % 60;

        return hours ? `${hours} godz. ${minutes} min` : `${minutes} min`;
    };

    const formatFuel = (liters) => `${liters.toFixed(2)} l`;

    const fuelFieldForProfile = () => {
        const fuelType = String(state.activeCarProfile?.fuel_type || '').trim().toLowerCase();

        if (fuelType === '98') {
            return 'petrol_98';
        }

        if (fuelType === 'diesel' || fuelType === 'on') {
            return 'diesel';
        }

        if (fuelType === 'gaz' || fuelType === 'lpg') {
            return 'lpg';
        }

        return 'petrol_95';
    };

    const currencyRate = (currency) => {
        if (!currency || currency === 'EUR') {
            return 1;
        }

        const rate = Number(state.fuelCostRates[currency]);
        return Number.isFinite(rate) && rate > 0 ? rate : 0;
    };

    const normalizeCountryCode = (countryCode) => {
        const aliases = {
            MNE: 'ME',
            SRB: 'RS'
        };
        const normalized = String(countryCode || '').trim().toUpperCase();

        return aliases[normalized] || normalized || null;
    };

    const convertMoney = (amount, sourceCurrency, targetCurrency) => {
        const value = Number(amount);
        const source = sourceCurrency || 'EUR';
        const target = targetCurrency || source;

        if (!Number.isFinite(value) || value <= 0) {
            return null;
        }

        if (source === target) {
            return value;
        }

        const sourceRate = currencyRate(source);
        const targetRate = currencyRate(target);

        if (!sourceRate || !targetRate) {
            return null;
        }

        return value / sourceRate * targetRate;
    };

    const exactFuelCostRow = (countryCode) => {
        const normalized = normalizeCountryCode(countryCode);

        return state.fuelCostRows.find((row) => normalizeCountryCode(row.country_code) === normalized) || null;
    };

    const countryNameForCode = (countryCode) => exactFuelCostRow(countryCode)?.country || '';

    const fuelPriceForCountry = (countryCode, options = {}) => {
        const allowFallback = options.allowFallback !== false;
        const field = fuelFieldForProfile();
        const exactRow = exactFuelCostRow(countryCode);
        const exactPrice = Number(exactRow?.[field]);
        const fallbackRow = allowFallback
            ? state.fuelCostRows.find((row) => normalizeCountryCode(row.country_code) === 'PL' && Number(row?.[field]) > 0)
            : null;
        const row = Number.isFinite(exactPrice) && exactPrice > 0
            ? exactRow
            : fallbackRow;
        const price = Number(row?.[field]);

        if (!row || !Number.isFinite(price) || price <= 0) {
            return null;
        }

        const isFallback = row !== exactRow;

        return {
            countryCode: row.country_code,
            country: row.country,
            isFallback,
            price,
            sourceCurrency: row.source_currency || 'EUR',
            countryCurrency: row.currency || row.source_currency || 'EUR',
            displayCurrency: state.travelCostCurrency === 'country'
                ? (row.currency || row.source_currency || 'EUR')
                : state.travelCostCurrency
        };
    };

    const formatMoney = (amount, currency = 'PLN') => (
        new Intl.NumberFormat('pl-PL', {
            style: 'currency',
            currency,
            currencyDisplay: 'code',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(amount)
    );

    const pointCountryCode = (point) => normalizeCountryCode(
        point?.country_code
        || point?.countryCode
        || point?.address?.country_code
        || point?.raw_data?.address?.country_code
    );

    const startPointCountryCode = () => pointCountryCode(state.points[0]);

    const routePointCountryCode = () => startPointCountryCode() || 'PL';

    const routeFuelPrice = () => fuelPriceForCountry(startPointCountryCode());

    const routeCostCurrency = () => 'PLN';

    const moneyComponent = (liters, price, targetCurrency = routeCostCurrency()) => {
        const fuel = Number(liters);

        if (!price || !Number.isFinite(fuel) || fuel <= 0) {
            return null;
        }

        const cost = convertMoney(
            fuel * price.price,
            price.sourceCurrency,
            targetCurrency
        );

        if (!Number.isFinite(cost)) {
            return null;
        }

        return {
            amount: cost,
            currency: targetCurrency,
            country: price.country,
            isFallback: price.isFallback
        };
    };

    const startFuelSummaryText = () => {
        if (!hasFuelRouteParameters()) {
            return '-';
        }

        const tankCapacity = Number(state.activeCarProfile?.fuel_tank_capacity);
        const liters = tankCapacity * Math.min(100, Math.max(0, state.initialFuelPercent)) / 100;
        const price = routeFuelPrice();
        const component = moneyComponent(liters, price, price?.displayCurrency);
        const country = price && !price.isFallback && state.travelCostCurrency === 'country' ? ` (${price.country})` : '';
        const cost = component ? `, ${formatMoney(component.amount, component.currency)}${country}` : '';

        return `${liters.toFixed(1)} l${cost}`;
    };

    const escapeHtml = (data) => {
        const element = document.createElement('span');
        element.textContent = String(data ?? '');
        return element.innerHTML;
    };

    const routeName = (route) => route?.name || 'Trasa';

    const clonePoint = (point) => ({
        id: point.id || `${Date.now()}-${Math.random().toString(16).slice(2)}`,
        title: point.title || `${Number(point.latitude).toFixed(6)}, ${Number(point.longitude).toFixed(6)}`,
        latitude: Number(point.latitude),
        longitude: Number(point.longitude),
        country_code: point.country_code || point.countryCode || null
    });

    const updateSavedControls = () => {
        const saved = Boolean(state.savedRoute?.id);
        saveButton.hidden = false;
        saveButton.setAttribute('aria-label', saved ? 'Zapisz zmiany trasy' : 'Zapisz trasę');
        saveButton.title = saved ? 'Zapisz zmiany' : 'Zapisz trasę';
        editNameButton.hidden = !saved;
        editNameButton.setAttribute('aria-hidden', String(!saved));
        titleIcon.hidden = !saved;
        titleIcon.textContent = state.savedRoute?.icon || '🚗';
        titleText.textContent = saved ? routeName(state.savedRoute) : 'Trasa';
        titleText.title = titleText.textContent;
    };

    const routePayload = (base = {}) => ({
        id: base.id || state.savedRoute?.id || undefined,
        name: base.name || state.savedRoute?.name || '',
        icon: base.icon || state.savedRoute?.icon || '🚗',
        points: state.points.map(clonePoint),
        distance: Number(state.currentRoute?.distance ?? base.distance ?? 0) || 0,
        duration: Number(state.currentRoute?.duration ?? base.duration ?? 0) || 0
    });

    const sameNumber = (left, right, tolerance = 0.000001) => (
        Math.abs(Number(left) - Number(right)) <= tolerance
    );

    const samePoint = (left, right) => (
        String(left?.title || '') === String(right?.title || '')
        && sameNumber(left?.latitude, right?.latitude)
        && sameNumber(left?.longitude, right?.longitude)
    );

    const isSavedRouteUnchanged = () => {
        if (!state.savedRoute?.id) {
            return false;
        }

        const savedPoints = state.savedRoute.points || [];

        return (
            savedPoints.length === state.points.length
            && savedPoints.every((point, index) => samePoint(point, state.points[index]))
        );
    };

    const rangeText = (min, max, formatter) => {
        if (!Number.isFinite(min) || !Number.isFinite(max) || min <= 0 || max <= 0) {
            return '-';
        }

        const low = Math.min(min, max);
        const high = Math.max(min, max);

        return Math.abs(low - high) < 0.005
            ? formatter(low)
            : `${formatter(low)} - ${formatter(high)}`;
    };

    function hasFuelRouteParameters() {
        const tankCapacity = Number(state.activeCarProfile?.fuel_tank_capacity);

        return (
            isCarTransport()
            &&
            Boolean(state.activeCarProfile)
            && Number.isFinite(tankCapacity)
            && tankCapacity > 0
            && state.travelCosts.minConsumption > 0
            && state.travelCosts.maxConsumption > 0
        );
    }

    function updateInitialFuelControls() {
        if (!hasFuelRouteParameters()) {
            fuelSection.hidden = true;
            fuelSection.setAttribute('aria-hidden', 'true');
            return;
        }

        const tankCapacity = Number(state.activeCarProfile.fuel_tank_capacity);
        const percent = Math.min(100, Math.max(0, Number(state.initialFuelPercent) || 0));
        const fuel = tankCapacity * percent / 100;
        const price = routeFuelPrice();
        const component = moneyComponent(fuel, price, price?.displayCurrency);
        const countryText = price && !price.isFallback && state.travelCostCurrency === 'country'
            ? ` (${price.country})`
            : '';
        const costText = component
            ? `, ${formatMoney(component.amount, component.currency)}${countryText}`
            : '';

        state.initialFuelPercent = percent;
        fuelSlider.value = String(Math.round(percent));
        fuelLabel.textContent = `${fuel.toFixed(1)} L. (${Math.round(percent)} %)${costText}`;
        fuelSection.hidden = false;
        fuelSection.setAttribute('aria-hidden', 'false');
    }

    const allFuelDrivingStyles = () => {
        const profile = state.activeCarProfile;
        const minConsumption = Number(profile?.min_consumption);
        const maxConsumption = Number(profile?.max_consumption);

        if (!Number.isFinite(minConsumption) || minConsumption <= 0 || !Number.isFinite(maxConsumption) || maxConsumption <= 0) {
            return [];
        }

        const low = Math.min(minConsumption, maxConsumption);
        const high = Math.max(minConsumption, maxConsumption);
        const average = (low + high) / 2;

        return [
            {
                type: 'economic',
                title: 'Tankowanie: jazda ekonomiczna',
                description: 'Próg tankowania przy minimalnym spalaniu.',
                consumption: low,
                enabled: state.fuelSeparators.economicEnabled
            },
            {
                type: 'average',
                title: 'Tankowanie: jazda średnia',
                description: 'Próg tankowania przy średnim spalaniu.',
                consumption: average,
                enabled: state.fuelSeparators.averageEnabled
            },
            {
                type: 'dynamic',
                title: 'Tankowanie: jazda dynamiczna',
                description: 'Próg tankowania przy maksymalnym spalaniu.',
                consumption: high,
                enabled: state.fuelSeparators.dynamicEnabled
            }
        ];
    };

    const fuelDrivingStyles = () => allFuelDrivingStyles()
        .filter((style) => style.enabled);

    const fuelCostDrivingStyles = () => allFuelDrivingStyles()
        .filter((style) => style.type === 'economic' || style.type === 'dynamic')
        .map((style) => ({
            ...style,
            enabled: true
        }));

    const createFuelSeparatorsForStyle = (style, tankCapacity, thresholdPercent, legs) => {
        const litersPerKilometer = style.consumption / 100;
        const thresholdFuel = tankCapacity * Math.min(99, Math.max(0, thresholdPercent)) / 100;
        let remainingFuel = tankCapacity * Math.min(100, Math.max(0, state.initialFuelPercent)) / 100;
        const result = [];

        legs.forEach((leg, index) => {
            const distance = Number(leg?.distance);

            if (!Number.isFinite(distance) || distance <= 0 || litersPerKilometer <= 0) {
                return;
            }

            let remainingDistance = distance / 1000;
            let consumedDistance = 0;
            let separatorIndex = 0;

            while (remainingDistance > 0 && separatorIndex < 100) {
                const fuelAfterRemainingDistance = remainingFuel - remainingDistance * litersPerKilometer;

                if (fuelAfterRemainingDistance > thresholdFuel) {
                    remainingFuel = fuelAfterRemainingDistance;
                    break;
                }

                const distanceToThreshold = Math.max(0, (remainingFuel - thresholdFuel) / litersPerKilometer);

                if (distanceToThreshold > remainingDistance) {
                    remainingFuel = fuelAfterRemainingDistance;
                    break;
                }

                result.push({
                    afterPointIndex: index,
                    ...style,
                    remainingFuel: Math.max(0, thresholdFuel),
                    remainingPercent: Math.max(0, thresholdFuel / tankCapacity * 100),
                    distanceFromPoint: consumedDistance + distanceToThreshold,
                    sequence: separatorIndex + 1
                });

                remainingDistance = Math.max(0, remainingDistance - distanceToThreshold);
                consumedDistance += distanceToThreshold;
                remainingFuel = tankCapacity;
                separatorIndex += 1;
            }
        });

        return result;
    };

    const createFuelSeparatorsFromStyles = (styles, options = {}) => {
        const { respectVisibility = true } = options;
        const profile = state.activeCarProfile;
        const tankCapacity = Number(profile?.fuel_tank_capacity);
        const thresholdPercent = Number(state.fuelSeparators.thresholdPercent);
        const legs = state.currentRoute?.legs || [];

        if (
            (respectVisibility && !state.fuelSeparators.enabled)
            || !isCarTransport()
            || !profile
            || !Number.isFinite(tankCapacity)
            || tankCapacity <= 0
            || !Number.isFinite(thresholdPercent)
            || thresholdPercent < 0
            || legs.length < 1
            || !hasFuelRouteParameters()
        ) {
            return [];
        }

        const typeOrder = {
            economic: 1,
            average: 2,
            dynamic: 3
        };

        return styles
            .flatMap((style) => createFuelSeparatorsForStyle(style, tankCapacity, thresholdPercent, legs))
            .sort((left, right) => (
                left.afterPointIndex - right.afterPointIndex
                || left.distanceFromPoint - right.distanceFromPoint
                || (typeOrder[left.type] || 0) - (typeOrder[right.type] || 0)
            ));
    };

    const createFuelSeparators = () => createFuelSeparatorsFromStyles(fuelDrivingStyles());

    const createFuelCostSeparators = () => createFuelSeparatorsFromStyles(
        fuelCostDrivingStyles(),
        { respectVisibility: false }
    );

    const separatorKey = (separator) => [
        separator.type,
        separator.afterPointIndex,
        separator.sequence,
        Math.round(separator.distanceFromPoint * 1000)
    ].join(':');

    const distanceBetween = (left, right) => {
        const lat1 = Number(left?.[1]);
        const lon1 = Number(left?.[0]);
        const lat2 = Number(right?.[1]);
        const lon2 = Number(right?.[0]);

        if (![lat1, lon1, lat2, lon2].every(Number.isFinite)) {
            return 0;
        }

        const radius = 6371000;
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat / 2) ** 2
            + Math.cos(lat1 * Math.PI / 180)
            * Math.cos(lat2 * Math.PI / 180)
            * Math.sin(dLon / 2) ** 2;

        return 2 * radius * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    };

    const coordinateAtDistance = (meters) => {
        const coordinates = state.currentRoute?.geometry?.coordinates || [];

        if (!coordinates.length) {
            return null;
        }

        let remaining = Math.max(0, Number(meters) || 0);

        for (let index = 1; index < coordinates.length; index += 1) {
            const previous = coordinates[index - 1];
            const current = coordinates[index];
            const segment = distanceBetween(previous, current);

            if (remaining <= segment || index === coordinates.length - 1) {
                const ratio = segment > 0 ? Math.min(1, Math.max(0, remaining / segment)) : 0;
                const lon = Number(previous[0]) + (Number(current[0]) - Number(previous[0])) * ratio;
                const lat = Number(previous[1]) + (Number(current[1]) - Number(previous[1])) * ratio;

                return Number.isFinite(lat) && Number.isFinite(lon)
                    ? { latitude: lat, longitude: lon }
                    : null;
            }

            remaining -= segment;
        }

        const last = coordinates[coordinates.length - 1];
        return { latitude: Number(last[1]), longitude: Number(last[0]) };
    };

    const separatorAbsoluteDistance = (separator) => {
        const legs = state.currentRoute?.legs || [];
        const before = legs.slice(0, separator.afterPointIndex).reduce((sum, leg) => (
            sum + (Number(leg?.distance) || 0)
        ), 0);

        return before + separator.distanceFromPoint * 1000;
    };

    const countryFromReverseData = (data) => (
        data?.place?.selected?.address?.country_code
        || data?.place?.selected?.raw_data?.address?.country_code
        || null
    );

    const countryForCoordinate = async (coordinate) => {
        if (!coordinate) {
            return null;
        }

        const cacheKey = `${coordinate.latitude.toFixed(3)},${coordinate.longitude.toFixed(3)}`;

        if (state.countryCache.has(cacheKey)) {
            return state.countryCache.get(cacheKey);
        }

        try {
            const params = new URLSearchParams({
                lat: String(coordinate.latitude),
                lon: String(coordinate.longitude)
            });
            const response = await fetch(`/api/map/reverse?${params.toString()}`, {
                headers: { 'Accept': 'application/json' }
            });
            const data = await response.json();
            const countryCode = countryFromReverseData(data);

            if (countryCode) {
                const normalized = normalizeCountryCode(countryCode);
                state.countryCache.set(cacheKey, normalized);
                return normalized;
            }
        } catch (error) {
            // Fallback below keeps the route panel responsive without location details.
        }

        return null;
    };

    const countryFromSeparatorLeg = (separator) => {
        const startCountry = pointCountryCode(state.points[separator.afterPointIndex]);
        const endCountry = pointCountryCode(state.points[separator.afterPointIndex + 1]);

        if (startCountry && startCountry === endCountry) {
            return startCountry;
        }

        return null;
    };

    const nearestRoutePointCountry = (coordinate) => {
        if (!coordinate) {
            return null;
        }

        const nearest = state.points
            .map((point) => ({
                country: pointCountryCode(point),
                distance: distanceBetween(
                    [coordinate.longitude, coordinate.latitude],
                    [Number(point.longitude), Number(point.latitude)]
                )
            }))
            .filter((entry) => entry.country && Number.isFinite(entry.distance))
            .sort((left, right) => left.distance - right.distance)[0];

        return nearest?.country || null;
    };

    const countryForSeparator = async (separator, coordinate) => {
        const legCountry = countryFromSeparatorLeg(separator);

        if (legCountry) {
            return legCountry;
        }

        const coordinateCountry = await countryForCoordinate(coordinate);

        return coordinateCountry || nearestRoutePointCountry(coordinate);
    };

    const enrichFuelSeparators = async () => {
        const separatorMap = new Map();

        [...createFuelSeparators(), ...createFuelCostSeparators()].forEach((separator) => {
            separatorMap.set(separatorKey(separator), separator);
        });

        const separators = Array.from(separatorMap.values());

        for (const separator of separators) {
            const coordinate = coordinateAtDistance(separatorAbsoluteDistance(separator));
            const countryCode = await countryForSeparator(separator, coordinate);
            const price = fuelPriceForCountry(countryCode);

            if (!price) {
                continue;
            }

            const liters = Math.max(0, Number(state.activeCarProfile?.fuel_tank_capacity || 0) - separator.remainingFuel);
            const displayComponent = moneyComponent(liters, price, price.displayCurrency);
            const summaryComponent = moneyComponent(liters, price, routeCostCurrency());

            state.fuelSeparatorDetails.set(separatorKey(separator), {
                type: separator.type,
                countryCode: price.isFallback ? null : price.countryCode,
                country: price.isFallback ? null : price.country,
                currency: routeCostCurrency(),
                displayCurrency: displayComponent?.currency || price.displayCurrency,
                liters,
                cost: summaryComponent?.amount ?? null,
                displayCost: displayComponent?.amount ?? null
            });
        }
    };

    const fuelSeparatorText = (separator) => (
        (() => {
            const details = state.fuelSeparatorDetails.get(separatorKey(separator));
            const costText = (() => {
                if (!details || !Number.isFinite(details.displayCost)) {
                    return '';
                }

                const countryText = details.country && state.travelCostCurrency === 'country'
                    ? ` (${details.country})`
                    : '';
                return ` Do pełna: ${details.liters.toFixed(1)} l, około ${formatMoney(details.displayCost, details.displayCurrency)}${countryText}.`;
            })();

            return `${separator.description} ${separator.sequence > 1 ? `Tankowanie ${separator.sequence}. ` : ''}Po około ${separator.distanceFromPoint.toFixed(1)} km od punktu zostaje ${separator.remainingFuel.toFixed(1)} l (${separator.remainingPercent.toFixed(0)}%), spalanie ${separator.consumption.toFixed(2)} l/100 km.${costText}`;
        })()
    );

    const maneuverIcon = (maneuver = {}) => {
        const modifier = maneuver.modifier || '';
        const type = maneuver.type || '';

        if (type === 'depart') {
            return '●';
        }

        if (type === 'arrive') {
            return '■';
        }

        if (modifier.includes('left')) {
            return '↰';
        }

        if (modifier.includes('right')) {
            return '↱';
        }

        if (modifier === 'straight') {
            return '↑';
        }

        if (type === 'roundabout' || type === 'rotary') {
            return '⟳';
        }

        if (type === 'merge') {
            return '⇡';
        }

        return '•';
    };

    const maneuverText = (step = {}, index = 0) => {
        if (step.instruction) {
            return step.instruction;
        }

        const maneuver = step.maneuver || {};
        const type = maneuver.type || '';
        const modifier = maneuver.modifier || '';
        const road = step.name ? ` w ${step.name}` : '';

        if (type === 'depart') {
            return `Rusz${road || ''}`;
        }

        if (type === 'arrive') {
            return 'Dotrzyj do celu';
        }

        if (type === 'roundabout' || type === 'rotary') {
            const exit = maneuver.exit ? ` i zjedź ${maneuver.exit}. zjazdem` : '';
            return `Wjedź na rondo${exit}${road}`;
        }

        if (type === 'merge') {
            return `Włącz się do ruchu${road}`;
        }

        if (type === 'fork') {
            return modifier.includes('left') ? `Trzymaj się lewej${road}` : `Trzymaj się prawej${road}`;
        }

        if (modifier.includes('left')) {
            return `Skręć w lewo${road}`;
        }

        if (modifier.includes('right')) {
            return `Skręć w prawo${road}`;
        }

        if (modifier === 'straight') {
            return `Jedź prosto${road}`;
        }

        return index === 0 ? `Rusz${road}` : `Kontynuuj${road}`;
    };

    const routeSteps = (route = state.currentRoute) => (
        (route?.legs || [])
            .flatMap((leg, legIndex) => (leg.steps || []).map((step) => ({
                ...step,
                legIndex
            })))
            .filter((step) => Number(step?.distance) > 0 || step?.maneuver?.type === 'arrive')
    );

    const renderInstructions = (route = state.currentRoute) => {
        instructionsList.replaceChildren();

        if (!route) {
            const empty = document.createElement('li');
            empty.className = 'route-details-panel__empty';
            empty.textContent = 'Instrukcje pojawią się po obliczeniu trasy.';
            instructionsList.append(empty);
            return;
        }

        const steps = routeSteps(route);

        if (!steps.length) {
            const empty = document.createElement('li');
            empty.className = 'route-details-panel__empty';
            empty.textContent = 'Brak instrukcji nawigacji dla tej trasy.';
            instructionsList.append(empty);
            return;
        }

        steps.forEach((step, index) => {
            const item = document.createElement('li');
            item.className = 'route-details-panel__instruction';

            const icon = document.createElement('span');
            icon.className = 'route-details-panel__instruction-icon';
            icon.textContent = maneuverIcon(step.maneuver);
            icon.setAttribute('aria-hidden', 'true');

            const content = document.createElement('span');
            content.className = 'route-details-panel__instruction-content';

            const title = document.createElement('strong');
            title.textContent = maneuverText(step, index);

            const hint = document.createElement('small');
            hint.textContent = step.name ? step.name : 'Droga bez nazwy';

            const meta = document.createElement('span');
            meta.className = 'route-details-panel__instruction-meta';
            meta.textContent = `${formatDistance(step.distance)} · ${formatDuration(step.duration)}`;

            content.append(title, hint);
            item.append(icon, content, meta);
            instructionsList.append(item);
        });
    };

    const routeSummaryHtml = (route) => {
        const distance = Number(route?.distance);
        const kilometers = Number.isFinite(distance) ? distance / 1000 : 0;
        const minFuel = kilometers * state.travelCosts.minConsumption / 100;
        const maxFuel = kilometers * state.travelCosts.maxConsumption / 100;
        const hasCarProfile = Boolean(state.activeCarProfile);
        const hasFuel = isCarTransport() && hasCarProfile && state.travelCosts.minConsumption > 0 && state.travelCosts.maxConsumption > 0;
        const costCurrency = routeCostCurrency();
        const startFuelCost = (() => {
            if (!hasFuel) {
                return null;
            }

            const tankCapacity = Number(state.activeCarProfile?.fuel_tank_capacity);
            const startFuel = tankCapacity * Math.min(100, Math.max(0, state.initialFuelPercent)) / 100;
            const component = moneyComponent(startFuel, routeFuelPrice(), costCurrency);

            return component?.amount ?? null;
        })();
        const refuelCostForStyle = (style) => Array.from(state.fuelSeparatorDetails.values())
            .filter((details) => details?.type === style && Number.isFinite(details.cost))
            .reduce((sum, details) => sum + details.cost, 0);
        const requiredRefuels = createFuelCostSeparators();
        const pendingRefuelCosts = requiredRefuels.some((separator) => {
            const details = state.fuelSeparatorDetails.get(separatorKey(separator));
            return !details || !Number.isFinite(details.cost);
        });
        const economicTripCost = Number.isFinite(startFuelCost)
            ? startFuelCost + refuelCostForStyle('economic')
            : null;
        const dynamicTripCost = Number.isFinite(startFuelCost)
            ? startFuelCost + refuelCostForStyle('dynamic')
            : null;
        const hasTripCost = hasFuel
            && !pendingRefuelCosts
            && Number.isFinite(economicTripCost)
            && Number.isFinite(dynamicTripCost);
        const tripCostText = pendingRefuelCosts
            ? 'Przeliczanie...'
            : hasTripCost
                ? rangeText(economicTripCost, dynamicTripCost, (value) => formatMoney(value, costCurrency))
                : '-';

        return `
            <div class="route-details-panel__summary-grid">
                <span>Dystans</span><strong>${formatDistance(route?.distance)}</strong>
                <span>Czas</span><strong>${formatDuration(route?.duration)}</strong>
                ${isCarTransport() ? `
                    <span>Zużycie paliwa</span><strong>${hasFuel ? rangeText(minFuel, maxFuel, formatFuel) : '-'}</strong>
                    <span>Koszt podróży</span><strong>${tripCostText}</strong>
                ` : ''}
            </div>
        `;
    };

    const refreshFuelSeparatorDetails = async (route = state.currentRoute) => {
        if (!route) {
            return;
        }

        await enrichFuelSeparators();

        if (state.currentRoute !== route) {
            return;
        }

        renderPoints();
        summary.innerHTML = routeSummaryHtml(route);
    };

    const dispatchRoute = (route = null) => {
        document.dispatchEvent(new CustomEvent('travel-manager:route-updated', {
            detail: {
                route,
                transport: state.transportMode,
                points: state.points.map((point) => ({ ...point }))
            }
        }));
    };

    const dispatchSession = () => {
        document.dispatchEvent(new CustomEvent('travel-manager:route-session-changed', {
            detail: { active: state.points.length > 0 }
        }));
    };

    const calculateRoute = async () => {
        const requestId = ++state.routeRequestId;

        if (state.points.length < 2) {
            state.currentRoute = null;
            summary.textContent = 'Dodaj punkt początkowy.';
            status.textContent = 'Trasa wymaga co najmniej dwóch punktów.';
            renderInstructions(null);
            dispatchRoute();
            return null;
        }

        summary.textContent = 'Obliczanie trasy...';
        status.textContent = 'Obliczanie trasy...';
        renderInstructions(null);

        try {
            const response = await fetch('/api/map/route', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    transport: state.transportMode,
                    include_toll_roads: state.tollRoads.roadsEnabled !== false,
                    points: state.points.map(({ latitude, longitude }) => ({ latitude, longitude }))
                })
            });
            const data = await response.json();

            if (requestId !== state.routeRequestId) {
                return null;
            }

            if (!response.ok || data?.status !== 'ok') {
                throw new Error(data?.message || 'Nie znaleziono trasy.');
            }

            const route = data.route;
            state.currentRoute = route;
            state.fuelSeparatorDetails.clear();
            summary.innerHTML = routeSummaryHtml(route);
            status.textContent = route.toll_exclusion_warning
                || (route.toll_exclusion_applied
                    ? 'Trasa została obliczona z omijaniem płatnych dróg.'
                    : 'Przeciągnij punkty, aby zmienić ich kolejność.');
            renderInstructions(route);
            renderPoints();
            refreshFuelSeparatorDetails(route);
            dispatchRoute(route);
            return route;
        } catch (error) {
            if (requestId !== state.routeRequestId) {
                return null;
            }

            summary.textContent = error.message || 'Nie udało się obliczyć trasy.';
            status.textContent = summary.textContent;
            state.currentRoute = null;
            renderInstructions(null);
            renderPoints();
            dispatchRoute();
            return null;
        }
    };

    const ensureCurrentRoute = async () => {
        if (state.currentRoute && state.points.length >= 2) {
            return state.currentRoute;
        }

        return calculateRoute();
    };

    const saveRoutePayload = async (payload) => {
        const saved = await window.travelManagerRoutes?.save(payload);

        if (saved) {
            state.savedRoute = saved;
            updateSavedControls();
            summary.innerHTML = routeSummaryHtml(state.currentRoute || saved);
        }

        return saved;
    };

    const saveNewRoute = async () => {
        if (state.points.length < 2) {
            status.textContent = 'Dodaj co najmniej dwa punkty przed zapisem trasy.';
            return;
        }

        const route = await ensureCurrentRoute();

        if (!route) {
            status.textContent = 'Najpierw musi udać się obliczyć trasę.';
            return;
        }

        const result = await window.travelManagerRouteEditor?.show({
            name: '',
            icon: '🚗',
            editing: false
        });

        if (result?.action !== 'save') {
            return;
        }

        await saveRoutePayload(routePayload({
            name: result.name,
            icon: result.icon || '🚗'
        }));
    };

    const saveRouteChanges = async () => {
        if (!state.savedRoute?.id) {
            await saveNewRoute();
            return;
        }

        if (state.points.length < 2) {
            status.textContent = 'Zapisana trasa wymaga co najmniej dwóch punktów.';
            return;
        }

        const route = await ensureCurrentRoute();

        if (!route) {
            status.textContent = 'Najpierw musi udać się obliczyć trasę.';
            return;
        }

        await saveRoutePayload(routePayload(state.savedRoute));
    };

    const saveRoute = async () => {
        if (state.savedRoute?.id) {
            await saveRouteChanges();
            return;
        }

        await saveNewRoute();
    };

    const editSavedRoute = async () => {
        if (!state.savedRoute?.id) {
            return;
        }

        const result = await window.travelManagerRouteEditor?.show({
            name: routeName(state.savedRoute),
            icon: state.savedRoute.icon || '🚗',
            editing: true,
            allowDelete: true
        });

        if (result?.action === 'delete') {
            const accepted = await window.travelManagerDialogs?.yesNo({
                title: 'Usunąć trasę?',
                description: `Trasa „${routeName(state.savedRoute)}” zostanie usunięta.`,
                icon: 'warning'
            });

            if (accepted) {
                await window.travelManagerRoutes?.remove(state.savedRoute.id);
                await close({ confirm: false });
            }
            return;
        }

        if (result?.action !== 'save') {
            return;
        }

        await saveRoutePayload(routePayload({
            ...state.savedRoute,
            name: result.name,
            icon: result.icon || '🚗'
        }));
    };

    const hideMenu = () => {
        menu.classList.remove('route-details-panel__menu--open');
        menu.setAttribute('aria-hidden', 'true');
        state.menuPointId = null;
    };

    const movePoint = (pointId, targetIndex) => {
        const currentIndex = state.points.findIndex((point) => point.id === pointId);

        if (currentIndex < 0) {
            return;
        }

        const [point] = state.points.splice(currentIndex, 1);
        const nextIndex = Math.min(Math.max(targetIndex, 0), state.points.length);
        state.points.splice(nextIndex, 0, point);
        state.currentRoute = null;
        updateInitialFuelControls();
        renderPoints();
        renderInstructions(null);
        calculateRoute();
    };

    const removePoint = (pointId) => {
        state.points = state.points.filter((point) => point.id !== pointId);
        state.currentRoute = null;
        updateInitialFuelControls();
        renderPoints();
        renderInstructions(null);
        setSelecting(false);
        calculateRoute();
        dispatchSession();
    };

    const reverseRoute = () => {
        if (state.points.length < 2) {
            return;
        }

        hideMenu();
        state.points.reverse();
        state.currentRoute = null;
        updateInitialFuelControls();
        renderPoints();
        renderInstructions(null);
        setSelecting(false);
        calculateRoute();
        dispatchSession();
    };

    const menuAction = (label, action, danger = false) => {
        const button = document.createElement('button');
        button.className = 'route-details-panel__menu-button';
        button.classList.toggle('route-details-panel__menu-button--danger', danger);
        button.type = 'button';
        button.role = 'menuitem';
        button.textContent = label;
        button.addEventListener('click', () => {
            const pointId = state.menuPointId;
            hideMenu();

            if (pointId) {
                action(pointId);
            }
        });

        return button;
    };

    const separator = () => {
        const element = document.createElement('div');
        element.className = 'route-details-panel__menu-separator';
        element.role = 'separator';
        return element;
    };

    const showMenu = (pointId, anchor) => {
        if (
            state.menuPointId === pointId
            && menu.classList.contains('route-details-panel__menu--open')
        ) {
            hideMenu();
            return;
        }

        state.menuPointId = pointId;
        menu.replaceChildren(
            menuAction('Przesuń na górę', (id) => movePoint(id, 0)),
            menuAction('Przesuń na dół', (id) => movePoint(id, state.points.length)),
            separator(),
            menuAction('Przesuń wyżej', (id) => {
                const index = state.points.findIndex((point) => point.id === id);
                movePoint(id, index - 1);
            }),
            menuAction('Przesuń niżej', (id) => {
                const index = state.points.findIndex((point) => point.id === id);
                movePoint(id, index + 1);
            }),
            separator(),
            menuAction('Usuń', removePoint, true)
        );

        menu.classList.add('route-details-panel__menu--open');
        menu.setAttribute('aria-hidden', 'false');

        const rect = anchor.getBoundingClientRect();
        const menuRect = menu.getBoundingClientRect();
        const left = Math.min(rect.right - menuRect.width, window.innerWidth - menuRect.width - 10);
        const spaceBelow = window.innerHeight - rect.bottom;
        const top = spaceBelow >= menuRect.height + 6
            ? rect.bottom + 6
            : rect.top - menuRect.height - 6;

        menu.style.left = `${Math.max(10, left)}px`;
        menu.style.top = `${Math.max(10, top)}px`;
        menu.querySelector('[role="menuitem"]')?.focus();
    };

    function renderPoints() {
        pointsList.replaceChildren();
        updateSavedControls();
        reverseButton.disabled = state.selecting || state.points.length < 2;
        const separatorsByPoint = new Map();

        createFuelSeparators().forEach((separator) => {
            const items = separatorsByPoint.get(separator.afterPointIndex) || [];
            items.push(separator);
            separatorsByPoint.set(separator.afterPointIndex, items);
        });

        state.points.forEach((point, index) => {
            const item = document.createElement('li');
            item.className = 'route-details-panel__point';
            item.dataset.pointId = point.id;
            item.draggable = true;

            const drag = document.createElement('button');
            drag.className = 'route-details-panel__drag';
            drag.type = 'button';
            drag.setAttribute('aria-label', `Przenieś punkt ${index + 1}`);

            const number = document.createElement('span');
            number.className = 'route-details-panel__point-number';
            number.textContent = String(index + 1);
            number.setAttribute('aria-hidden', 'true');

            const name = document.createElement('span');
            name.className = 'route-details-panel__point-name';
            name.textContent = point.title;
            name.title = point.title;

            const more = document.createElement('button');
            more.className = 'route-details-panel__more';
            more.type = 'button';
            more.setAttribute('aria-label', `Opcje punktu ${point.title}`);
            more.addEventListener('click', (event) => {
                event.stopPropagation();
                showMenu(point.id, more);
            });

            item.addEventListener('dragstart', (event) => {
                state.draggedId = point.id;
                item.classList.add('route-details-panel__point--dragging');
                event.dataTransfer.effectAllowed = 'move';
            });
            item.addEventListener('dragover', (event) => {
                event.preventDefault();
                item.classList.add('route-details-panel__point--drag-over');
            });
            item.addEventListener('dragleave', () => {
                item.classList.remove('route-details-panel__point--drag-over');
            });
            item.addEventListener('drop', (event) => {
                event.preventDefault();
                item.classList.remove('route-details-panel__point--drag-over');
                const targetIndex = state.points.findIndex((entry) => entry.id === point.id);
                if (state.draggedId && state.draggedId !== point.id) {
                    movePoint(state.draggedId, targetIndex);
                }
            });
            item.addEventListener('dragend', () => {
                state.draggedId = null;
                item.classList.remove('route-details-panel__point--dragging');
                document.querySelectorAll('.route-details-panel__point--drag-over').forEach((element) => {
                    element.classList.remove('route-details-panel__point--drag-over');
                });
            });

            item.append(drag, number, name, more);
            pointsList.append(item);

            (separatorsByPoint.get(index) || []).forEach((separator) => {
                const item = document.createElement('li');
                item.className = `route-details-panel__separator route-details-panel__separator--${separator.type}`;
                const separatorText = fuelSeparatorText(separator);
                item.setAttribute('aria-label', `${separator.title}. ${separatorText}`);

                const marker = document.createElement('span');
                marker.className = 'route-details-panel__separator-marker';
                marker.setAttribute('aria-hidden', 'true');

                const content = document.createElement('span');
                content.className = 'route-details-panel__separator-content';

                const title = document.createElement('strong');
                title.textContent = separator.sequence > 1
                    ? `${separator.title} (${separator.sequence})`
                    : separator.title;

                const description = document.createElement('small');
                description.textContent = separatorText;

                content.append(title, description);
                item.append(marker, content);
                pointsList.append(item);
            });
        });
    }

    const consumeElement = (title, element) => {
        if (!state.selecting) {
            return false;
        }

        const point = pointFromElement(title, element);

        if (!point) {
            status.textContent = 'Wybrane miejsce nie ma prawidłowych współrzędnych.';
            return true;
        }

        const firstPoint = state.points.length === 0;
        state.points.push(point);

        state.currentRoute = null;
        if (firstPoint) {
            resetRouteFuelSettings();
        }
        updateInitialFuelControls();
        setSelecting(false);
        renderPoints();
        renderInstructions(null);
        calculateRoute();
        dispatchSession();

        return true;
    };

    const addElement = (title, element) => {
        const point = pointFromElement(title, element);

        if (!point) {
            return false;
        }

        const firstPoint = state.points.length === 0;
        state.points.push(point);
        state.currentRoute = null;
        if (firstPoint) {
            resetRouteFuelSettings();
        }
        updateInitialFuelControls();
        setSelecting(false);
        renderPoints();
        renderInstructions(null);
        calculateRoute();
        dispatchSession();
        open();

        return true;
    };

    const open = () => {
        panel.classList.add('route-details-panel--open');
        panel.setAttribute('aria-hidden', 'false');
        window.travelManagerLegendDetailsPanel?.close();
        window.travelManagerLayerDetailsPanel?.close();
        window.travelManagerPlaceDetailsPanel?.close(false);
    };

    const openWithDestination = (title, element) => {
        const startPoint = pointFromElement(title, element);

        if (!startPoint) {
            return;
        }

        state.points = [startPoint];
        state.savedRoute = null;
        state.routeRequestId += 1;
        state.currentRoute = null;
        resetRouteFuelSettings();
        updateInitialFuelControls();
        renderPoints();
        renderInstructions(null);
        summary.textContent = 'Dodaj kolejny punkt.';
        dispatchRoute();
        dispatchSession();
        open();
        setSelecting(true, 'append');
    };

    const clearRoute = () => {
        state.routeRequestId += 1;
        state.currentRoute = null;
        state.savedRoute = null;
        state.points = [];
        resetRouteFuelSettings();
        updateInitialFuelControls();
        renderPoints();
        renderInstructions(null);
        summary.textContent = 'Dodaj punkt początkowy.';
        dispatchRoute();
        dispatchSession();
    };

    const openSavedRoute = async (route) => {
        if (!route?.points?.length) {
            return false;
        }

        hideMenu();
        setSelecting(false);
        state.routeRequestId += 1;
        state.savedRoute = {
            ...route,
            points: (route.points || []).map(clonePoint)
        };
        state.points = state.savedRoute.points.map(clonePoint);
        state.currentRoute = null;
        resetRouteFuelSettings();
        updateInitialFuelControls();
        renderPoints();
        renderInstructions(null);
        summary.innerHTML = routeSummaryHtml(route);
        dispatchRoute();
        dispatchSession();
        open();
        await calculateRoute();
        return true;
    };

    const startNewRoute = async () => {
        if (panel.classList.contains('route-details-panel--open')) {
            const accepted = await window.travelManagerDialogs?.yesNo({
                title: 'Utworzyć nową trasę?',
                description: 'Obecna trasa zostanie usunięta. Tej operacji nie można cofnąć.',
                icon: 'warning'
            });

            if (!accepted) {
                return false;
            }
        }

        hideMenu();
        setSelecting(false);
        clearRoute();
        open();
        setSelecting(true, 'append');
        return true;
    };

    const close = async ({ confirm = true } = {}) => {
        if (confirm && state.points.length && !isSavedRouteUnchanged()) {
            const accepted = await window.travelManagerDialogs?.yesNo({
                title: 'Zamknąć trasę?',
                description: 'Wszystkie wybrane punkty i obliczona trasa zostaną usunięte.',
                icon: 'warning'
            });

            if (!accepted) {
                return false;
            }
        }

        hideMenu();
        setSelecting(false);
        clearRoute();
        panel.classList.remove('route-details-panel--open');
        panel.setAttribute('aria-hidden', 'true');
        return true;
    };

    const refreshRouteFuelPresentation = () => {
        updateFuelSeparatorControls();
        updateTollControls();
        updateInitialFuelControls();

        if (state.currentRoute) {
            state.fuelSeparatorDetails.clear();
            renderPoints();
            summary.innerHTML = routeSummaryHtml(state.currentRoute);
            refreshFuelSeparatorDetails(state.currentRoute);
            return;
        }

        renderPoints();
    };

    const refreshRouteTollPresentation = () => {
        updateTollControls();

        renderPoints();
    };

    tabs.forEach((button) => {
        button.addEventListener('click', () => setActiveTab(button.dataset.routeTab || 'points'));
    });
    addButton.addEventListener('click', () => setSelecting(true, 'append'));
    reverseButton.addEventListener('click', reverseRoute);
    saveButton.addEventListener('click', saveRoute);
    editNameButton.addEventListener('click', editSavedRoute);
    separatorsEnabledInput.addEventListener('change', () => {
        state.fuelSeparators.enabled = separatorsEnabledInput.checked;
        refreshRouteFuelPresentation();
    });
    separatorEconomicInput.addEventListener('change', () => {
        state.fuelSeparators.economicEnabled = separatorEconomicInput.checked;
        refreshRouteFuelPresentation();
    });
    separatorAverageInput.addEventListener('change', () => {
        state.fuelSeparators.averageEnabled = separatorAverageInput.checked;
        refreshRouteFuelPresentation();
    });
    separatorDynamicInput.addEventListener('change', () => {
        state.fuelSeparators.dynamicEnabled = separatorDynamicInput.checked;
        refreshRouteFuelPresentation();
    });
    tollRoadsEnabledInput.addEventListener('change', () => {
        state.tollRoads.roadsEnabled = tollRoadsEnabledInput.checked;

        if (state.points.length >= 2) {
            state.currentRoute = null;
            renderPoints();
            renderInstructions(null);
            calculateRoute();
            return;
        }

        refreshRouteTollPresentation();
    });
    transportButtons.forEach((button) => {
        button.addEventListener('click', () => {
            if (button.disabled || state.transportMode === button.dataset.routeTransport) {
                return;
            }

            state.transportMode = button.dataset.routeTransport || 'car';
            updateTransportControls();
            updateInitialFuelControls();
            updateFuelSeparatorControls();
            updateTollControls();

            if (state.points.length >= 2) {
                state.currentRoute = null;
                renderPoints();
                renderInstructions(null);
                calculateRoute();
            } else {
                renderPoints();
            }
        });
    });
    fuelSlider.addEventListener('input', () => {
        state.initialFuelPercent = Math.min(100, Math.max(0, Number(fuelSlider.value) || 0));
        updateInitialFuelControls();

        if (state.currentRoute) {
            state.fuelSeparatorDetails.clear();
            renderPoints();
            summary.innerHTML = routeSummaryHtml(state.currentRoute);
            refreshFuelSeparatorDetails(state.currentRoute);
        }
    });
    closeButton.addEventListener('click', () => close());
    document.addEventListener('click', (event) => {
        if (!menu.contains(event.target)) {
            hideMenu();
        }
    });
    document.addEventListener('travel-manager:app-view-changed', (event) => {
        if (event.detail?.view !== 'map') {
            hideMenu();
        }
    });
    document.addEventListener('travel-manager:ui-settings-changed', (event) => {
        const detail = event.detail || {};
        applyTravelCosts(detail, state.activeCarProfile);

        if (state.currentRoute) {
            state.fuelSeparatorDetails.clear();
            summary.innerHTML = routeSummaryHtml(state.currentRoute);
            renderPoints();
            refreshFuelSeparatorDetails(state.currentRoute);

            if (Object.prototype.hasOwnProperty.call(detail, 'route_toll_roads_enabled')) {
                state.currentRoute = null;
                renderPoints();
                renderInstructions(null);
                calculateRoute();
            }
        }
    });
    document.addEventListener('travel-manager:car-profiles-changed', (event) => {
        state.activeCarProfile = event.detail?.activeCarProfile || null;
        applyTravelCosts({}, state.activeCarProfile);

        if (state.currentRoute) {
            state.fuelSeparatorDetails.clear();
            summary.innerHTML = routeSummaryHtml(state.currentRoute);
            renderPoints();
            refreshFuelSeparatorDetails(state.currentRoute);
        }
    });
    document.addEventListener('travel-manager:fuel-costs-changed', async (event) => {
        if (Array.isArray(event.detail?.rows)) {
            state.fuelCostRows = event.detail.rows;
            state.fuelCostRates = event.detail.rates || {};
        } else {
            await loadFuelCostData();
        }

        state.countryCache.clear();
        updateInitialFuelControls();

        if (state.currentRoute) {
            state.fuelSeparatorDetails.clear();
            summary.innerHTML = routeSummaryHtml(state.currentRoute);
            renderPoints();
            refreshFuelSeparatorDetails(state.currentRoute);
        }
    });
    document.addEventListener('travel-manager:routes-changed', (event) => {
        if (!state.savedRoute?.id) {
            return;
        }

        const route = (event.detail?.routes || []).find((item) => item.id === state.savedRoute.id);

        if (!route) {
            state.savedRoute = null;
            updateSavedControls();
            return;
        }

        state.savedRoute = {
            ...route,
            points: (route.points || []).map(clonePoint)
        };
        updateSavedControls();
    });

    const resize = { startX: 0, startWidth: 0 };
    const onPointerMove = (event) => {
        const computed = window.getComputedStyle(panel);
        const min = Number.parseFloat(computed.minWidth) || 300;
        const max = Number.parseFloat(computed.maxWidth) || 680;
        const width = Math.min(Math.max(resize.startWidth + resize.startX - event.clientX, min), max);
        panel.style.setProperty('--route-details-panel-width', `${width}px`);
    };
    const stopResize = () => {
        panel.classList.remove('route-details-panel--resizing');
        document.removeEventListener('pointermove', onPointerMove);
        document.removeEventListener('pointerup', stopResize);
        patchUiSettings({
            route_details_panel_width: Math.round(panel.getBoundingClientRect().width)
        });
    };

    grabber?.addEventListener('pointerdown', (event) => {
        event.preventDefault();
        resize.startX = event.clientX;
        resize.startWidth = panel.getBoundingClientRect().width;
        panel.classList.add('route-details-panel--resizing');
        document.addEventListener('pointermove', onPointerMove);
        document.addEventListener('pointerup', stopResize);
    });

    loadFuelCostData().then(() => {
        updateInitialFuelControls();

        if (state.currentRoute) {
            summary.innerHTML = routeSummaryHtml(state.currentRoute);
            renderPoints();
            refreshFuelSeparatorDetails(state.currentRoute);
        }
    });
    loadUiSettings();
    setSelecting(false);
    setActiveTab('points');
    renderInstructions(null);
    updateSavedControls();
    updateTransportControls();
    updateFuelSeparatorControls();
    updateInitialFuelControls();

    window.travelManagerRouteDetailsPanel = {
        addElement,
        close,
        consumeElement,
        isActive: () => state.points.length > 0,
        isSelectingPoint: () => state.selecting,
        open,
        openWithStart: openWithDestination,
        openSavedRoute,
        openWithDestination,
        startNewRoute
    };
});
