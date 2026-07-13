document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#advanced-search');
    const queryInput = document.querySelector('#advanced-search-query');
    const categoriesContainer = document.querySelector('#advanced-search-categories');
    const subcategorySection = document.querySelector('#advanced-search-subcategory-section');
    const subcategoriesContainer = document.querySelector('#advanced-search-subcategories');
    const radiusInput = document.querySelector('#advanced-search-radius');
    const radiusLabel = document.querySelector('#advanced-search-radius-label');
    const cancelButtons = dialog?.querySelectorAll('[data-advanced-search-cancel]');

    if (
        !layer
        || !dialog
        || !queryInput
        || !categoriesContainer
        || !subcategorySection
        || !subcategoriesContainer
        || !radiusInput
        || !radiusLabel
        || !cancelButtons?.length
    ) {
        return;
    }

    const categories = [
        {
            id: '',
            label: 'Brak',
            query: '',
            icon: 'circle-slash',
            subcategories: []
        },
        {
            id: 'attractions',
            label: 'Atrakcje',
            query: 'attraction',
            icon: 'landmark',
            subcategories: [
                { id: 'attraction', label: 'Atrakcje', query: 'attraction', icon: 'sparkles' },
                { id: 'library', label: 'Biblioteki', query: 'library', icon: 'library' },
                { id: 'cinema', label: 'Kina', query: 'cinema', icon: 'clapperboard' },
                { id: 'museum', label: 'Muzea', query: 'museum', icon: 'landmark' },
                { id: 'live_music', label: 'Muzyka na żywo', query: 'live music', icon: 'music' },
                { id: 'park', label: 'Parki', query: 'park', icon: 'trees' },
                { id: 'gym', label: 'Siłownie', query: 'gym fitness', icon: 'dumbbell' },
                { id: 'art', label: 'Sztuka', query: 'art gallery', icon: 'palette' },
                { id: 'theatre', label: 'Teatry', query: 'theatre', icon: 'drama' },
                { id: 'nightlife', label: 'Życie nocne', query: 'nightclub', icon: 'moon' },
                { id: 'zoo', label: 'Zoo', query: 'zoo', icon: 'paw-print' }
            ]
        },
        {
            id: 'food',
            label: 'Jedzenie i napoje',
            query: 'food drink',
            icon: 'utensils',
            subcategories: [
                { id: 'bar', label: 'Bary', query: 'bar', icon: 'martini' },
                { id: 'fast_food', label: 'Fast food', query: 'fast food', icon: 'sandwich' },
                { id: 'food_court', label: 'Food courty', query: 'food court', icon: 'store' },
                { id: 'cafe', label: 'Kawiarnie', query: 'cafe', icon: 'coffee' },
                { id: 'takeaway', label: 'Na wynos', query: 'takeaway', icon: 'package' },
                { id: 'pub', label: 'Puby', query: 'pub', icon: 'beer' },
                { id: 'restaurant', label: 'Restauracje', query: 'restaurant', icon: 'utensils' },
                { id: 'delivery', label: 'Z dostawą', query: 'food delivery', icon: 'truck' }
            ]
        },
        {
            id: 'shopping',
            label: 'Zakupy',
            query: 'shop',
            icon: 'shopping-bag',
            subcategories: [
                { id: 'mall', label: 'Centra handlowe', query: 'mall shopping centre', icon: 'building-2' },
                { id: 'garden', label: 'Dom i ogród', query: 'garden centre houseware', icon: 'shovel' },
                { id: 'chemist', label: 'Drogerie', query: 'chemist cosmetics', icon: 'sparkles' },
                { id: 'electronics', label: 'Elektronika', query: 'electronics shop', icon: 'smartphone' },
                { id: 'books', label: 'Książki i prasa', query: 'books newsagent', icon: 'book-open' },
                { id: 'local', label: 'Sklepy lokalne', query: 'convenience shop', icon: 'store' },
                { id: 'sports', label: 'Sportowe', query: 'sports shop', icon: 'dumbbell' },
                { id: 'grocery', label: 'Spożywcze', query: 'supermarket grocery', icon: 'shopping-cart' },
                { id: 'car_sales', label: 'Sprzedaż aut', query: 'car dealer', icon: 'car' },
                { id: 'clothes', label: 'Ubrania', query: 'clothes shop', icon: 'shirt' }
            ]
        },
        {
            id: 'favourites',
            label: 'Ulubione',
            query: '',
            icon: 'star',
            subcategories: []
        },
        {
            id: 'services',
            label: 'Usługi',
            query: 'services',
            icon: 'briefcase',
            subcategories: [
                { id: 'pharmacy', label: 'Apteki', query: 'pharmacy', icon: 'cross' },
                { id: 'car_wash', label: 'Automyjnie', query: 'car wash', icon: 'waves' },
                { id: 'atm', label: 'Bankomaty', query: 'atm', icon: 'banknote' },
                { id: 'hotel', label: 'Hotele', query: 'hotel', icon: 'bed' },
                { id: 'parking', label: 'Parkingi', query: 'parking', icon: 'square-parking' },
                { id: 'post_office', label: 'Poczta', query: 'post office', icon: 'mail' },
                { id: 'laundry', label: 'Pralnie', query: 'laundry', icon: 'shirt' },
                { id: 'beauty', label: 'Salony piękności', query: 'beauty salon', icon: 'scissors' },
                { id: 'charging', label: 'Stacje ładowania', query: 'charging station', icon: 'plug-zap' },
                { id: 'fuel', label: 'Stacje paliw', query: 'fuel station', icon: 'fuel' },
                { id: 'healthcare', label: 'Szpitale i przychodnie', query: 'hospital clinic', icon: 'hospital' },
                { id: 'courier', label: 'Usługi kurierskie', query: 'parcel locker courier', icon: 'package' },
                { id: 'car_rental', label: 'Wynajem aut', query: 'car rental', icon: 'key-round' }
            ]
        }
    ];

    const state = {
        category: categories[0],
        subcategory: null
    };

    const close = () => {
        dialog.setAttribute('aria-hidden', 'true');
        layer.classList.remove('dialog-layer--open');
    };

    const open = () => {
        dialog.setAttribute('aria-hidden', 'false');
        layer.classList.add('dialog-layer--open');
        queryInput.focus();
    };

    const updateRadiusLabel = () => {
        const value = Number(radiusInput.value);
        radiusLabel.textContent = value > 0 ? `${value} km` : 'Widoczny obszar';
    };

    const createChoice = (item, active, onClick) => {
        const button = document.createElement('button');
        button.className = 'advanced-search__choice';
        button.classList.toggle('advanced-search__choice--active', active);
        button.type = 'button';
        button.setAttribute('role', 'radio');
        button.setAttribute('aria-checked', String(active));
        button.setAttribute('aria-label', item.label);
        button.addEventListener('click', onClick);

        const icon = document.createElement('span');
        icon.className = 'advanced-search__choice-icon';
        icon.innerHTML = `<i data-lucide="${item.icon || 'search'}" aria-hidden="true"></i>`;

        const label = document.createElement('span');
        label.className = 'advanced-search__choice-label';
        label.textContent = item.label;

        button.append(icon, label);

        return button;
    };

    const renderSubcategories = () => {
        subcategoriesContainer.replaceChildren();
        const subcategories = state.category?.subcategories || [];
        state.subcategory = subcategories.some((item) => item.id === state.subcategory?.id)
            ? state.subcategory
            : null;

        subcategorySection.hidden = !subcategories.length;

        if (!subcategorySection.hidden) {
            subcategoriesContainer.append(createChoice(
                { id: '', label: 'Brak', query: '', icon: 'circle-slash' },
                !state.subcategory,
                () => {
                    state.subcategory = null;
                    renderSubcategories();
                }
            ));
        }

        subcategories.forEach((subcategory) => {
            subcategoriesContainer.append(createChoice(
                subcategory,
                state.subcategory?.id === subcategory.id,
                () => {
                    state.subcategory = state.subcategory?.id === subcategory.id ? null : subcategory;
                    renderSubcategories();
                }
            ));
        });
        window.lucide?.createIcons({
            attrs: {
                'stroke-width': 1.7
            }
        });
    };

    const renderCategories = () => {
        categoriesContainer.replaceChildren();
        categories.forEach((category) => {
            categoriesContainer.append(createChoice(
                category,
                state.category.id === category.id,
                () => {
                    state.category = state.category.id === category.id ? categories[0] : category;
                    state.subcategory = null;
                    renderCategories();
                    renderSubcategories();
                }
            ));
        });
        window.lucide?.createIcons({
            attrs: {
                'stroke-width': 1.7
            }
        });
    };

    const selectedSearchQuery = () => {
        return queryInput.value.trim();
    };

    dialog.addEventListener('submit', (event) => {
        event.preventDefault();

        const query = selectedSearchQuery();
        const category = state.category?.id ? state.category : null;

        if (!query && !category) {
            queryInput.focus();
            return;
        }

        document.dispatchEvent(new CustomEvent('travel-manager:advanced-search-requested', {
            detail: {
                keyword: queryInput.value.trim(),
                query,
                category: category
                    ? {
                        id: category.id,
                        label: category.label
                    }
                    : null,
                subcategory: state.subcategory
                    ? { id: state.subcategory.id, label: state.subcategory.label }
                    : null,
                radiusKm: Number(radiusInput.value) || 0
            }
        }));
        close();
    });

    cancelButtons.forEach((button) => button.addEventListener('click', close));
    radiusInput.addEventListener('input', updateRadiusLabel);

    renderCategories();
    renderSubcategories();
    updateRadiusLabel();
    window.lucide?.createIcons({
        attrs: {
            'stroke-width': 1.7
        }
    });

    window.travelManagerAdvancedSearch = { open, close };
});
