document.addEventListener('travel-manager:views-ready', () => {
    const t = window.i18n.t;
    const locale = window.i18n.locale.replace('_', '-');
    const view = document.querySelector('[data-app-view="car-profiles"]');
    const form = document.querySelector('#car-profiles-search');
    const searchInput = document.querySelector('#car-profiles-search-input');
    const sortButton = document.querySelector('#car-profiles-sort-button');
    const sortMenu = document.querySelector('#car-profiles-sort-menu');
    const list = document.querySelector('#car-profiles-list');
    const addButton = document.querySelector('#car-profiles-add');

    if (!view || !form || !searchInput || !sortButton || !sortMenu || !list || !addButton) {
        return;
    }

    const state = {
        query: '',
        sortDirection: 'asc',
        profiles: [],
        activeCarProfileId: null
    };

    const name = (profile) => profile.name
        || [profile.brand, profile.model].filter(Boolean).join(' ')
        || t('CAR_PROFILES_VIEW.DEFAULT_CAR');
    const selectValueLabel = (fieldName, value) => {
        const options = document.querySelector(`[name="${fieldName}"]`)?.options || [];
        return Array.from(options).find((option) => option.value === value)?.textContent || value;
    };
    const meta = (profile) => [
        profile.brand,
        profile.model,
        profile.version,
        profile.generation,
        profile.production_year
    ].filter(Boolean).join(' · ');
    const spec = (profile) => [
        profile.registration_number,
        selectValueLabel('fuel_type', profile.fuel_type),
        profile.power_hp
            ? t('PANEL_CAR_DETAILS.POWER_HP_VALUE', { value: profile.power_hp })
            : null,
        profile.power_kw
            ? t('PANEL_CAR_DETAILS.POWER_KW_VALUE', { value: profile.power_kw })
            : null,
        profile.min_consumption && profile.max_consumption
            ? t('PANEL_CAR_DETAILS.CONSUMPTION_RANGE_VALUE', {
                minimum: profile.min_consumption,
                maximum: profile.max_consumption
            })
            : null
    ].filter(Boolean).join(' · ');

    const setSortOpen = (open) => {
        sortMenu.setAttribute('aria-hidden', String(!open));
        sortButton.setAttribute('aria-expanded', String(open));
    };

    const filtered = () => {
        const query = state.query.trim().toLocaleLowerCase();
        const items = query
            ? state.profiles.filter((profile) => [
                name(profile), meta(profile), spec(profile)
            ].join(' ').toLocaleLowerCase().includes(query))
            : [...state.profiles];

        return items.sort((left, right) => {
            const result = name(left).localeCompare(name(right), locale, { sensitivity: 'base' });
            return state.sortDirection === 'asc' ? result : -result;
        });
    };

    const editProfile = async (profile = null) => {
        const result = await window.travelManagerCarProfileEditor?.show(profile);

        if (result) {
            await window.travelManagerCarProfiles?.save(result);
        }
    };

    const deleteProfile = async (profile) => {
        const accepted = await window.travelManagerDialogs?.yesNo({
            title: t('CAR_PROFILES_VIEW.DELETE_TITLE'),
            description: t('CAR_PROFILES_VIEW.DELETE_DESCRIPTION', { name: name(profile) }),
            icon: 'warning'
        });

        if (accepted) {
            await window.travelManagerCarProfiles?.remove(profile.id);
        }
    };

    const openDetails = (profile) => {
        window.travelManagerCarDetailsPanel?.open(profile);
    };

    const renderImage = (profile) => {
        const image = document.createElement('div');
        image.className = 'car-profiles-view__image';

        if (profile.image) {
            const img = document.createElement('img');
            img.alt = '';
            img.src = profile.image;
            image.append(img);
        } else {
            image.innerHTML = '<i data-lucide="car" aria-hidden="true"></i>';
        }

        return image;
    };

    const createButton = (label, icon, handler, danger = false) => {
        const button = document.createElement('button');
        button.className = `car-profiles-view__button${danger ? ' car-profiles-view__button--danger' : ''}`;
        button.type = 'button';
        button.innerHTML = `<i data-lucide="${icon}" aria-hidden="true"></i><span>${label}</span>`;
        button.addEventListener('click', handler);
        return button;
    };

    const render = () => {
        list.replaceChildren();
        const items = filtered();

        if (!items.length) {
            const empty = document.createElement('p');
            empty.className = 'car-profiles-view__empty';
            empty.textContent = state.query
                ? t('CAR_PROFILES_VIEW.NO_SEARCH_RESULTS')
                : t('CAR_PROFILES_VIEW.NO_PROFILES');
            list.append(empty);
            return;
        }

        items.forEach((profile) => {
            const item = document.createElement('article');
            item.className = 'car-profiles-view__item';

            const details = document.createElement('div');
            details.className = 'car-profiles-view__details';

            const title = document.createElement('div');
            title.className = 'car-profiles-view__name';
            title.textContent = profile.id === state.activeCarProfileId
                ? `${name(profile)} · ${t('CAR_PROFILES_VIEW.ACTIVE')}`
                : name(profile);

            const metaLine = document.createElement('div');
            metaLine.className = 'car-profiles-view__meta';
            metaLine.textContent = meta(profile) || t('CAR_PROFILES_VIEW.NO_BASIC_DATA');

            const specLine = document.createElement('div');
            specLine.className = 'car-profiles-view__spec';
            specLine.textContent = spec(profile) || t('CAR_PROFILES_VIEW.NO_TECHNICAL_DATA');

            const actions = document.createElement('div');
            actions.className = 'car-profiles-view__actions';
            actions.append(
                createButton(t('COMMON.SHOW'), 'eye', () => openDetails(profile)),
                createButton(t('COMMON.EDIT'), 'pencil', () => editProfile(profile)),
                createButton(t('COMMON.DELETE'), 'trash-2', () => deleteProfile(profile), true)
            );

            details.append(title, metaLine, specLine);
            item.append(renderImage(profile), details, actions);
            list.append(item);
        });

        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
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
    addButton.addEventListener('click', () => editProfile(null));
    document.addEventListener('travel-manager:car-profiles-changed', (event) => {
        state.profiles = event.detail?.profiles || [];
        state.activeCarProfileId = event.detail?.activeCarProfileId || null;
        render();
    });
    window.travelManagerCarProfiles?.list().then((profiles) => {
        state.profiles = profiles;
        state.activeCarProfileId = window.travelManagerCarProfiles?.active()?.id || null;
        render();
    }).catch(() => render());
});
