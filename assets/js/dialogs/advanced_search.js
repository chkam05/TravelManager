document.addEventListener('travel-manager:views-ready', () => {
    const t = window.i18n.t;
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
            label: t('RES_MAP_SEARCH.NONE'),
            query: '',
            icon: 'circle-slash',
            subcategories: []
        },
        {
            id: 'attractions',
            label: t('RES_MAP_SEARCH.ATTRACTIONS'),
            query: 'attraction',
            icon: 'landmark',
            subcategories: [
                { id: 'attraction', label: t('RES_MAP_SEARCH.ATTRACTIONS'), query: 'attraction', icon: 'sparkles' },
                { id: 'library', label: t('RES_MAP_SEARCH.LIBRARIES'), query: 'library', icon: 'library' },
                { id: 'cinema', label: t('RES_MAP_SEARCH.CINEMAS'), query: 'cinema', icon: 'clapperboard' },
                { id: 'museum', label: t('RES_MAP_SEARCH.MUSEUMS'), query: 'museum', icon: 'landmark' },
                { id: 'live_music', label: t('RES_MAP_SEARCH.LIVE_MUSIC'), query: 'live music', icon: 'music' },
                { id: 'park', label: t('RES_MAP_SEARCH.PARKS'), query: 'park', icon: 'trees' },
                { id: 'gym', label: t('RES_MAP_SEARCH.GYMS'), query: 'gym fitness', icon: 'dumbbell' },
                { id: 'art', label: t('RES_MAP_SEARCH.ART'), query: 'art gallery', icon: 'palette' },
                { id: 'theatre', label: t('RES_MAP_SEARCH.THEATRES'), query: 'theatre', icon: 'drama' },
                { id: 'nightlife', label: t('RES_MAP_SEARCH.NIGHTLIFE'), query: 'nightclub', icon: 'moon' },
                { id: 'zoo', label: t('RES_MAP_SEARCH.ZOOS'), query: 'zoo', icon: 'paw-print' }
            ]
        },
        {
            id: 'food',
            label: t('RES_MAP_SEARCH.FOOD_AND_DRINK'),
            query: 'food drink',
            icon: 'utensils',
            subcategories: [
                { id: 'bar', label: t('RES_MAP_SEARCH.BARS'), query: 'bar', icon: 'martini' },
                { id: 'fast_food', label: t('RES_MAP_SEARCH.FAST_FOOD'), query: 'fast food', icon: 'sandwich' },
                { id: 'food_court', label: t('RES_MAP_SEARCH.FOOD_COURTS'), query: 'food court', icon: 'store' },
                { id: 'cafe', label: t('RES_MAP_SEARCH.CAFES'), query: 'cafe', icon: 'coffee' },
                { id: 'takeaway', label: t('RES_MAP_SEARCH.TAKEAWAY'), query: 'takeaway', icon: 'package' },
                { id: 'pub', label: t('RES_MAP_SEARCH.PUBS'), query: 'pub', icon: 'beer' },
                { id: 'restaurant', label: t('RES_MAP_SEARCH.RESTAURANTS'), query: 'restaurant', icon: 'utensils' },
                { id: 'delivery', label: t('RES_MAP_SEARCH.DELIVERY'), query: 'food delivery', icon: 'truck' }
            ]
        },
        {
            id: 'shopping',
            label: t('RES_MAP_SEARCH.SHOPPING'),
            query: 'shop',
            icon: 'shopping-bag',
            subcategories: [
                { id: 'mall', label: t('RES_MAP_SEARCH.SHOPPING_CENTRES'), query: 'mall shopping centre', icon: 'building-2' },
                { id: 'garden', label: t('RES_MAP_SEARCH.HOME_AND_GARDEN'), query: 'garden centre houseware', icon: 'shovel' },
                { id: 'chemist', label: t('RES_MAP_SEARCH.CHEMISTS'), query: 'chemist cosmetics', icon: 'sparkles' },
                { id: 'electronics', label: t('RES_MAP_SEARCH.ELECTRONICS'), query: 'electronics shop', icon: 'smartphone' },
                { id: 'books', label: t('RES_MAP_SEARCH.BOOKS_AND_PRESS'), query: 'books newsagent', icon: 'book-open' },
                { id: 'local', label: t('RES_MAP_SEARCH.LOCAL_SHOPS'), query: 'convenience shop', icon: 'store' },
                { id: 'sports', label: t('RES_MAP_SEARCH.SPORTS_SHOPS'), query: 'sports shop', icon: 'dumbbell' },
                { id: 'grocery', label: t('RES_MAP_SEARCH.GROCERIES'), query: 'supermarket grocery', icon: 'shopping-cart' },
                { id: 'car_sales', label: t('RES_MAP_SEARCH.CAR_SALES'), query: 'car dealer', icon: 'car' },
                { id: 'clothes', label: t('RES_MAP_SEARCH.CLOTHES'), query: 'clothes shop', icon: 'shirt' }
            ]
        },
        {
            id: 'favourites',
            label: t('RES_MAP_SEARCH.FAVOURITES'),
            query: '',
            icon: 'star',
            subcategories: []
        },
        {
            id: 'services',
            label: t('RES_MAP_SEARCH.SERVICES'),
            query: 'services',
            icon: 'briefcase',
            subcategories: [
                { id: 'pharmacy', label: t('RES_MAP_SEARCH.PHARMACIES'), query: 'pharmacy', icon: 'cross' },
                { id: 'car_wash', label: t('RES_MAP_SEARCH.CAR_WASHES'), query: 'car wash', icon: 'waves' },
                { id: 'atm', label: t('RES_MAP_SEARCH.ATMS'), query: 'atm', icon: 'banknote' },
                { id: 'hotel', label: t('RES_MAP_SEARCH.HOTELS'), query: 'hotel', icon: 'bed' },
                { id: 'parking', label: t('RES_MAP_SEARCH.PARKING'), query: 'parking', icon: 'square-parking' },
                { id: 'post_office', label: t('RES_MAP_SEARCH.POST_OFFICES'), query: 'post office', icon: 'mail' },
                { id: 'laundry', label: t('RES_MAP_SEARCH.LAUNDRIES'), query: 'laundry', icon: 'shirt' },
                { id: 'beauty', label: t('RES_MAP_SEARCH.BEAUTY_SALONS'), query: 'beauty salon', icon: 'scissors' },
                { id: 'charging', label: t('RES_MAP_SEARCH.CHARGING_STATIONS'), query: 'charging station', icon: 'plug-zap' },
                { id: 'fuel', label: t('RES_MAP_SEARCH.FUEL_STATIONS'), query: 'fuel station', icon: 'fuel' },
                { id: 'healthcare', label: t('RES_MAP_SEARCH.HOSPITALS_AND_CLINICS'), query: 'hospital clinic', icon: 'hospital' },
                { id: 'courier', label: t('RES_MAP_SEARCH.COURIER_SERVICES'), query: 'parcel locker courier', icon: 'package' },
                { id: 'car_rental', label: t('RES_MAP_SEARCH.CAR_RENTAL'), query: 'car rental', icon: 'key-round' }
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
        radiusLabel.textContent = value > 0
            ? t('ADVANCED_SEARCH.RADIUS_KILOMETRES', { value })
            : t('ADVANCED_SEARCH.VISIBLE_AREA');
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
                { id: '', label: t('RES_MAP_SEARCH.NONE'), query: '', icon: 'circle-slash' },
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
