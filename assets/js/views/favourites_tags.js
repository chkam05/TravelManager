document.addEventListener('travel-manager:views-ready', () => {
    const view = document.querySelector('[data-app-view="favourites-tags"]');
    const form = document.querySelector('#favourites-tags-search');
    const searchInput = document.querySelector('#favourites-tags-search-input');
    const sortButton = document.querySelector('#favourites-tags-sort-button');
    const sortMenu = document.querySelector('#favourites-tags-sort-menu');
    const list = document.querySelector('#favourites-tags-list');
    const addButton = document.querySelector('#favourites-tags-add');

    if (!view || !form || !searchInput || !sortButton || !sortMenu || !list || !addButton) {
        return;
    }

    const state = {
        query: '',
        sortDirection: 'asc',
        tags: []
    };

    const setSortOpen = (open) => {
        sortMenu.setAttribute('aria-hidden', String(!open));
        sortButton.setAttribute('aria-expanded', String(open));
    };

    const filteredTags = () => {
        const query = state.query.trim().toLocaleLowerCase();
        const items = query
            ? state.tags.filter((tag) => (
                tag.name.toLocaleLowerCase().includes(query)
                || (tag.icon || '').includes(query)
            ))
            : [...state.tags];

        return items.sort((left, right) => {
            const result = left.name.localeCompare(right.name, 'pl', { sensitivity: 'base' });
            return state.sortDirection === 'asc' ? result : -result;
        });
    };

    const editTag = async (tag = null) => {
        const result = await window.travelManagerFavouritesTagEditor?.show({
            name: tag?.name || '',
            icon: tag?.icon || '⭐',
            editing: Boolean(tag)
        });

        if (!result) {
            return;
        }

        await window.travelManagerFavourites.saveTag({
            tag,
            name: result.name,
            icon: result.icon
        });
    };

    const removeTag = async (tag) => {
        const accepted = await window.travelManagerDialogs?.yesNo({
            title: 'Usunąć tag?',
            description: `Tag „${tag.name}” zostanie usunięty, a używające go miejsca wrócą do domyślnego tagu.`,
            icon: 'warning'
        });

        if (accepted) {
            await window.travelManagerFavourites.removeTag(tag.id);
        }
    };

    const createButton = (label, icon, handler) => {
        const button = document.createElement('button');
        button.className = 'favourites-tags-view__button';
        button.type = 'button';
        button.innerHTML = `<i data-lucide="${icon}" aria-hidden="true"></i><span>${label}</span>`;
        button.addEventListener('click', handler);
        return button;
    };

    const render = () => {
        list.replaceChildren();
        const items = filteredTags();

        if (!items.length) {
            const empty = document.createElement('p');
            empty.className = 'favourites-tags-view__empty';
            empty.textContent = state.query ? 'Nie znaleziono tagów.' : 'Brak tagów.';
            list.append(empty);
            return;
        }

        items
            .forEach((tag) => {
                const item = document.createElement('article');
                item.className = 'favourites-tags-view__item';

                const icon = document.createElement('div');
                icon.className = 'favourites-tags-view__icon';
                icon.textContent = tag.icon || '⭐';

                const name = document.createElement('div');
                name.className = 'favourites-tags-view__name';
                name.textContent = tag.name;

                item.append(
                    icon,
                    name,
                    createButton('Edytuj', 'pencil', () => editTag(tag))
                );

                if (tag.id !== 'default') {
                    item.append(createButton('Usuń', 'trash-2', () => removeTag(tag)));
                }

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
    addButton.addEventListener('click', () => editTag(null));
    document.addEventListener('travel-manager:favourite-tags-changed', (event) => {
        state.tags = event.detail?.tags || [];
        render();
    });
    window.travelManagerFavourites?.listTags().then((tags) => {
        state.tags = tags;
        render();
    }).catch(() => render());
});
