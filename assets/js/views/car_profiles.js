document.addEventListener('travel-manager:views-ready', () => {
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

    const name = (profile) => profile.name || [profile.brand, profile.model].filter(Boolean).join(' ') || 'Samochód';
    const meta = (profile) => [
        profile.brand,
        profile.model,
        profile.version,
        profile.generation,
        profile.production_year
    ].filter(Boolean).join(' · ');
    const spec = (profile) => [
        profile.registration_number,
        profile.fuel_type,
        profile.power_hp ? `${profile.power_hp} KM` : null,
        profile.power_kw ? `${profile.power_kw} kW` : null,
        profile.min_consumption && profile.max_consumption
            ? `${profile.min_consumption}-${profile.max_consumption} L/100km`
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
            const result = name(left).localeCompare(name(right), 'pl', { sensitivity: 'base' });
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
            title: 'Usunąć samochód?',
            description: `Profil „${name(profile)}” zostanie usunięty.`,
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

    const createButton = (label, icon, handler) => {
        const button = document.createElement('button');
        button.className = 'car-profiles-view__button';
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
            empty.textContent = state.query ? 'Nie znaleziono samochodów.' : 'Brak profili samochodów.';
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
            title.textContent = `${name(profile)}${profile.id === state.activeCarProfileId ? ' · aktywny' : ''}`;

            const metaLine = document.createElement('div');
            metaLine.className = 'car-profiles-view__meta';
            metaLine.textContent = meta(profile) || 'Brak danych podstawowych';

            const specLine = document.createElement('div');
            specLine.className = 'car-profiles-view__spec';
            specLine.textContent = spec(profile) || 'Brak danych technicznych';

            const actions = document.createElement('div');
            actions.className = 'car-profiles-view__actions';
            actions.append(
                createButton('Pokaż', 'eye', () => openDetails(profile)),
                createButton('Edytuj', 'pencil', () => editProfile(profile)),
                createButton('Usuń', 'trash-2', () => deleteProfile(profile))
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
