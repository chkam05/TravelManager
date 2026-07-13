document.addEventListener('travel-manager:views-ready', () => {
    const view = document.querySelector('[data-app-view="favourites"]');
    const form = document.querySelector('#favourites-search');
    const searchInput = document.querySelector('#favourites-search-input');
    const tagFilterButton = document.querySelector('#favourites-tag-filter-button');
    const tagFilterLabel = document.querySelector('#favourites-tag-filter-label');
    const tagFilterMenu = document.querySelector('#favourites-tag-filter-menu');
    const tagFilterOptions = document.querySelector('#favourites-tag-filter-options');
    const sortButton = document.querySelector('#favourites-sort-button');
    const sortMenu = document.querySelector('#favourites-sort-menu');
    const list = document.querySelector('#favourites-list');

    if (!view || !form || !searchInput || !tagFilterButton || !tagFilterLabel || !tagFilterMenu || !tagFilterOptions || !sortButton || !sortMenu || !list) {
        return;
    }

    const state = {
        query: '',
        sortDirection: 'asc',
        favourites: [],
        tags: [],
        selectedTagIds: null
    };

    const firstValue = (...values) => values.find((value) => value !== null && value !== undefined && value !== '');

    const getAddress = (favourite) => {
        const place = favourite.place_data || {};
        const address = place.address || {};
        const road = firstValue(address.road, address['addr:street']);
        const number = firstValue(address.house_number, address['addr:housenumber']);
        const city = firstValue(address.city, address.town, address.village, address.suburb);
        const postcode = firstValue(address.postcode, address['addr:postcode']);
        const line = [
            [road, number].filter(Boolean).join(' '),
            [postcode, city].filter(Boolean).join(' ')
        ].filter(Boolean).join(', ');

        return line || place.display_name || 'Brak adresu';
    };

    const coordinatesText = (favourite) => {
        const latitude = Number(favourite.latitude);
        const longitude = Number(favourite.longitude);

        if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
            return 'Brak koordynatów';
        }

        return `${latitude.toFixed(6)}, ${longitude.toFixed(6)}`;
    };

    const setSortOpen = (open) => {
        sortMenu.setAttribute('aria-hidden', String(!open));
        sortButton.setAttribute('aria-expanded', String(open));
    };

    const setTagFilterOpen = (open) => {
        tagFilterMenu.setAttribute('aria-hidden', String(!open));
        tagFilterButton.setAttribute('aria-expanded', String(open));
    };

    const selectedTagSet = () => Array.isArray(state.selectedTagIds)
        ? new Set(state.selectedTagIds)
        : null;

    const favouriteIcon = (favourite) => favourite.icon || favourite.tag?.icon || '⭐';

    const updateTagFilterLabel = () => {
        if (!state.tags.length || !Array.isArray(state.selectedTagIds)) {
            tagFilterLabel.textContent = 'Tagi: wszystkie';
            return;
        }

        if (!state.selectedTagIds.length) {
            tagFilterLabel.textContent = 'Tagi: brak';
            return;
        }

        tagFilterLabel.textContent = `Tagi: ${state.selectedTagIds.length}`;
    };

    const getSelectedTagIds = () => Array.from(tagFilterOptions.querySelectorAll('[data-favourites-tag-filter]'))
        .filter((input) => input.checked)
        .map((input) => input.value);

    const renderTagFilter = () => {
        tagFilterOptions.replaceChildren();

        if (!state.tags.length) {
            const empty = document.createElement('p');
            empty.className = 'favourites-view__tag-filter-empty';
            empty.textContent = 'Brak tagów.';
            tagFilterOptions.append(empty);
            updateTagFilterLabel();
            return;
        }

        const selected = selectedTagSet();

        state.tags.forEach((tag) => {
            const label = document.createElement('label');
            label.className = 'favourites-view__tag-filter-option';

            const input = document.createElement('input');
            input.type = 'checkbox';
            input.value = tag.id;
            input.dataset.favouritesTagFilter = 'true';
            input.checked = selected ? selected.has(tag.id) : true;

            const text = document.createElement('span');
            text.textContent = `${tag.icon || '⭐'} ${tag.name}`;

            label.append(input, text);
            tagFilterOptions.append(label);

            input.addEventListener('change', () => {
                state.selectedTagIds = getSelectedTagIds();
                updateTagFilterLabel();
                render();
            });
        });

        updateTagFilterLabel();
    };

    const filteredItems = () => {
        const query = state.query.trim().toLocaleLowerCase();
        const items = query
            ? state.favourites.filter((item) => (
                item.name.toLocaleLowerCase().includes(query)
                || getAddress(item).toLocaleLowerCase().includes(query)
                || (item.tag?.name || '').toLocaleLowerCase().includes(query)
            ))
            : [...state.favourites];
        const selected = selectedTagSet();
        const visibleItems = selected
            ? items.filter((item) => selected.has(item.tag_id))
            : items;

        return visibleItems.sort((left, right) => {
            const result = left.name.localeCompare(right.name, 'pl', { sensitivity: 'base' });
            return state.sortDirection === 'asc' ? result : -result;
        });
    };

    const editFavourite = async (favourite) => {
        const result = await window.travelManagerFavouritesEditor?.show({
            name: favourite.name,
            tagId: favourite.tag_id,
            icon: favourite.icon || null,
            editing: true
        });

        if (!result) {
            return;
        }

        await window.travelManagerFavourites.save({
            favourite,
            element: favourite.place_data,
            name: result.name,
            tagId: result.tagId,
            icon: result.icon
        });
    };

    const removeFavourite = async (favourite) => {
        const accepted = await window.travelManagerDialogs?.yesNo({
            title: 'Usunąć z ulubionych?',
            description: `Miejsce „${favourite.name}” zniknie z ulubionych i z mapy.`,
            icon: 'warning'
        });

        if (accepted) {
            await window.travelManagerFavourites.remove(favourite.id);
        }
    };

    const showFavourite = (favourite) => {
        window.travelManagerNavigation?.showView('map');
        window.setTimeout(() => window.travelManagerMap?.showFavourite?.(favourite), 0);
    };

    const createButton = (label, icon, handler) => {
        const button = document.createElement('button');
        button.className = 'favourites-view__item-button';
        button.type = 'button';
        button.innerHTML = `<i data-lucide="${icon}" aria-hidden="true"></i><span>${label}</span>`;
        button.addEventListener('click', handler);
        return button;
    };

    const render = () => {
        list.replaceChildren();
        const items = filteredItems();

        if (!items.length) {
            const empty = document.createElement('p');
            empty.className = 'favourites-view__empty';
            empty.textContent = 'Brak ulubionych miejsc.';
            list.append(empty);
            return;
        }

        items.forEach((favourite) => {
            const item = document.createElement('article');
            item.className = 'favourites-view__item';

            const icon = document.createElement('div');
            icon.className = 'favourites-view__icon';
            icon.textContent = favouriteIcon(favourite);

            const details = document.createElement('div');
            details.className = 'favourites-view__details';

            const name = document.createElement('div');
            name.className = 'favourites-view__name';
            name.textContent = favourite.name;

            const address = document.createElement('div');
            address.className = 'favourites-view__address';
            address.textContent = getAddress(favourite);

            const coordinates = document.createElement('div');
            coordinates.className = 'favourites-view__coordinates';
            coordinates.textContent = coordinatesText(favourite);

            details.append(name, address, coordinates);
            item.append(
                icon,
                details,
                createButton('Pokaż', 'eye', () => showFavourite(favourite)),
                createButton('Edytuj', 'pencil', () => editFavourite(favourite)),
                createButton('Usuń', 'trash-2', () => removeFavourite(favourite))
            );
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
    tagFilterButton.addEventListener('click', () => {
        setTagFilterOpen(tagFilterMenu.getAttribute('aria-hidden') !== 'false');
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

        if (!tagFilterMenu.contains(event.target) && !tagFilterButton.contains(event.target)) {
            setTagFilterOpen(false);
        }
    });
    document.addEventListener('travel-manager:favourites-changed', (event) => {
        state.favourites = event.detail?.favourites || [];
        render();
    });
    document.addEventListener('travel-manager:favourite-tags-changed', (event) => {
        const previousSelected = selectedTagSet();
        state.tags = event.detail?.tags || [];
        state.selectedTagIds = previousSelected
            ? state.tags.filter((tag) => previousSelected.has(tag.id)).map((tag) => tag.id)
            : null;
        renderTagFilter();
        render();
    });

    window.travelManagerFavourites?.list().then((items) => {
        state.favourites = items;
        render();
    }).catch(() => render());
    window.travelManagerFavourites?.listTags().then((items) => {
        state.tags = items;
        renderTagFilter();
    }).catch(() => renderTagFilter());
});
