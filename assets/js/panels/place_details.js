document.addEventListener('travel-manager:views-ready', () => {
    const panel = document.querySelector('#place-details-panel');
    const titleElement = document.querySelector('#place-details-panel-title');
    const titleIconElement = document.querySelector('#place-details-panel-title-icon');
    const tagElement = document.querySelector('#place-details-panel-tag');
    const tabs = document.querySelector('#place-details-panel-tabs');
    const content = document.querySelector('#place-details-panel-content');
    const showEmptyInput = document.querySelector('#place-details-panel-show-empty');
    const exportButton = document.querySelector('#place-details-panel-export');
    const routeButton = document.querySelector('#place-details-panel-route');
    const routeButtonLabel = routeButton?.querySelector('[data-place-route-label]');
    const favouriteAddButton = document.querySelector('#place-details-panel-favourite-add');
    const favouriteActions = document.querySelector('#place-details-panel-favourite-actions');
    const favouriteEditButton = document.querySelector('#place-details-panel-favourite-edit');
    const favouriteRemoveButton = document.querySelector('#place-details-panel-favourite-remove');
    const grabber = document.querySelector('[data-place-details-panel-grabber]');
    const closeButton = document.querySelector('[data-place-details-panel-close]');

    if (!panel || !titleElement || !titleIconElement || !tagElement || !tabs || !content || !showEmptyInput || !exportButton) {
        return;
    }

    const state = {
        activeTab: 'basic',
        element: null,
        favourite: null,
        title: 'Wybrane miejsce'
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
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                return;
            }

            const data = await response.json();
            const width = Number(data?.ui?.place_details_panel_width);

            if (Number.isFinite(width) && width > 0) {
                panel.style.setProperty('--place-details-panel-width', `${width}px`);
            }
        } catch (error) {
            // Missing persisted UI settings should not block panel rendering.
        }
    };

    const isEmpty = (value) => (
        value === null
        || value === undefined
        || value === ''
        || (Array.isArray(value) && value.length === 0)
        || (typeof value === 'object' && !Array.isArray(value) && Object.keys(value).length === 0)
    );

    const firstValue = (...values) => values.find((value) => !isEmpty(value));

    const normalizeUrl = (value) => {
        if (typeof value !== 'string') {
            return null;
        }

        const trimmed = value.trim();

        if (/^https?:\/\//i.test(trimmed)) {
            return trimmed;
        }

        if (/^www\.[^\s]+$/i.test(trimmed)) {
            return `https://${trimmed}`;
        }

        return null;
    };

    const openExternalUrl = async (url) => {
        const api = window.pywebview?.api;

        if (api?.open_external_url) {
            try {
                const result = await api.open_external_url(url);

                if (result?.status === 'opened') {
                    return;
                }
            } catch (error) {
                // Browser fallback is used outside the native WebView bridge.
            }
        }

        window.open(url, '_blank', 'noopener,noreferrer');
    };

    const prettyValue = (value) => {
        if (isEmpty(value)) {
            return '-';
        }

        if (typeof value === 'object') {
            return JSON.stringify(value, null, 2);
        }

        return String(value);
    };

    const open = () => {
        panel.classList.add('place-details-panel--open');
        panel.setAttribute('aria-hidden', 'false');
    };

    const updateRouteButton = () => {
        const active = Boolean(window.travelManagerRouteDetailsPanel?.isActive());
        routeButton?.classList.toggle('place-details-panel__route--add', active);

        if (routeButtonLabel) {
            routeButtonLabel.textContent = active ? 'Dodaj do trasy' : 'Trasa';
        }

        routeButton?.setAttribute('aria-label', active ? 'Dodaj miejsce do trasy' : 'Utwórz trasę od miejsca');
    };

    const updateFavouriteButtons = () => {
        const hasFavourite = Boolean(state.favourite);
        const hasCoordinates = Number.isFinite(Number(state.element?.coordinates?.latitude))
            && Number.isFinite(Number(state.element?.coordinates?.longitude));

        favouriteAddButton.hidden = hasFavourite;
        favouriteAddButton.disabled = !hasCoordinates;
        favouriteActions.hidden = !hasFavourite;
    };

    const updateFavouriteHeader = () => {
        const tag = state.favourite?.tag;
        const icon = state.favourite?.icon || tag?.icon || '';
        titleIconElement.hidden = !icon;
        tagElement.hidden = !tag;

        if (icon) {
            titleIconElement.textContent = icon;
        } else {
            titleIconElement.textContent = '';
        }

        if (tag) {
            tagElement.textContent = tag.name || '';
        } else {
            tagElement.textContent = '';
        }
    };

    const refreshFavouriteTag = async () => {
        if (!state.favourite || state.favourite.tag || !state.favourite.tag_id) {
            updateFavouriteHeader();
            return;
        }

        try {
            const tags = await window.travelManagerFavourites?.listTags();
            const tag = tags?.find((item) => item.id === state.favourite?.tag_id) || null;

            if (tag) {
                state.favourite = {
                    ...state.favourite,
                    tag
                };
            }
        } catch (error) {
            // Missing tag metadata should not block place details rendering.
        }

        updateFavouriteHeader();
    };

    const refreshFavourite = async () => {
        try {
            const favourites = await window.travelManagerFavourites?.list();
            state.favourite = favourites?.find((item) => item.id === state.favourite?.id)
                || window.travelManagerFavourites?.findByElement(state.element)
                || null;
        } catch (error) {
            state.favourite = null;
        }

        updateFavouriteButtons();
        updateFavouriteHeader();
        refreshFavouriteTag();
    };

    const editFavourite = async () => {
        if (!state.element) {
            return;
        }

        const result = await window.travelManagerFavouritesEditor?.show({
            name: state.favourite?.name || state.title,
            tagId: state.favourite?.tag_id || '',
            icon: state.favourite?.icon || null,
            editing: Boolean(state.favourite)
        });

        if (!result) {
            return;
        }

        state.favourite = await window.travelManagerFavourites.save({
            favourite: state.favourite,
            element: state.element,
            name: result.name,
            tagId: result.tagId,
            icon: result.icon
        });
        updateFavouriteButtons();
        updateFavouriteHeader();
        refreshFavouriteTag();
    };

    const removeFavourite = async () => {
        if (!state.favourite) {
            return;
        }

        const accepted = await window.travelManagerDialogs?.yesNo({
            title: 'Usunąć z ulubionych?',
            description: `Miejsce „${state.favourite.name}” zniknie z ulubionych i z mapy.`,
            icon: 'warning'
        });

        if (!accepted) {
            return;
        }

        await window.travelManagerFavourites.remove(state.favourite.id);
        state.favourite = null;
        updateFavouriteButtons();
        updateFavouriteHeader();
        refreshFavouriteTag();
    };

    const close = (clearSelection = true) => {
        panel.classList.remove('place-details-panel--open');
        panel.setAttribute('aria-hidden', 'true');

        if (clearSelection) {
            document.dispatchEvent(new CustomEvent('travel-manager:place-details-closed'));
        }
    };

    const setStatus = (message) => {
        tabs.replaceChildren();
        content.replaceChildren();
        exportButton.disabled = true;
        favouriteAddButton.disabled = true;
        state.element = null;
        state.favourite = null;
        state.title = 'Wybrane miejsce';
        titleElement.textContent = state.title;
        updateFavouriteButtons();
        updateFavouriteHeader();

        const status = document.createElement('p');
        status.className = 'place-details-panel__status';
        status.textContent = message;

        content.append(status);
        open();
    };

    const createItem = (label, value) => {
        const wrapper = document.createElement('div');
        wrapper.className = 'place-details-panel__item';

        const term = document.createElement('dt');
        term.textContent = label;

        const description = document.createElement('dd');
        description.classList.toggle(
            'place-details-panel__value--json',
            typeof value === 'object' && value !== null
        );

        const url = normalizeUrl(value);

        if (url) {
            const link = document.createElement('a');
            link.className = 'place-details-panel__link';
            link.href = url;
            link.rel = 'noopener noreferrer';
            link.target = '_blank';
            link.textContent = value;
            link.addEventListener('click', (event) => {
                event.preventDefault();
                openExternalUrl(url);
            });

            description.append(link);
        } else {
            description.textContent = prettyValue(value);
        }

        wrapper.append(term, description);

        return wrapper;
    };

    const createSection = (section, showEmpty) => {
        const visibleFields = section.fields.filter((field) => showEmpty || !isEmpty(field.value));

        if (!visibleFields.length) {
            return null;
        }

        const wrapper = document.createElement('section');
        wrapper.className = 'place-details-panel__section';

        const title = document.createElement('h3');
        title.className = 'place-details-panel__section-title';
        title.textContent = section.title;

        const list = document.createElement('dl');
        list.className = 'place-details-panel__list';

        visibleFields.forEach((field) => {
            list.append(createItem(field.label, field.value));
        });

        wrapper.append(title, list);

        return wrapper;
    };

    const field = (label, value) => ({ label, value });

    const objectFields = (object, labels = {}) => Object.entries(object || {}).map(([key, value]) => (
        field(labels[key] || key, value)
    ));

    const withoutFields = (fields, excludedLabels) => fields.filter((item) => !excludedLabels.includes(item.label));

    const buildTabs = (element) => {
        const address = element.address || {};
        const annotations = element.annotations || {};
        const bounds = element.bounds || {};
        const coordinates = element.coordinates || {};
        const names = element.name || {};
        const primary = element.primary_features || {};
        const properties = element.properties || {};
        const references = element.references || {};
        const restrictions = element.restrictions || {};

        return [
            {
                id: 'basic',
                label: 'Podstawowe',
                sections: [
                    {
                        title: 'Identyfikacja',
                        fields: [
                            field('Nazwa', firstValue(names.name, names.official_name, names.short_name)),
                            field('Nazwa oficjalna', names.official_name),
                            field('Nazwa krótka', names.short_name),
                            field('Pełny opis', element.display_name)
                        ]
                    },
                    {
                        title: 'Nazwy',
                        fields: objectFields(names)
                    },
                    {
                        title: 'Adres',
                        fields: objectFields(address, {
                            'addr:housenumber': 'Numer',
                            'addr:housename': 'Nazwa domu',
                            'addr:street': 'Ulica',
                            'addr:place': 'Miejsce',
                            'addr:postcode': 'Kod pocztowy',
                            'addr:city': 'Miasto',
                            'addr:suburb': 'Dzielnica',
                            'addr:district': 'Powiat / dzielnica',
                            'addr:province': 'Województwo / prowincja',
                            'addr:state': 'Stan / region',
                            'addr:country': 'Państwo',
                            'country_code': 'Kod państwa',
                            'house_number': 'Numer',
                            'ISO3166-2-lvl4': 'ISO3166-2 lvl4',
                            'neighbourhood': 'Sąsiedztwo',
                            'quarter': 'Kwartał / obszar',
                            'road': 'Droga / ulica',
                            'state_district': 'Okręg / metropolia'
                        })
                    },
                    {
                        title: 'Położenie',
                        fields: [
                            field('Szerokość', coordinates.latitude),
                            field('Długość', coordinates.longitude)
                        ]
                    }
                ]
            },
            {
                id: 'type',
                label: 'Typ',
                sections: [
                    {
                        title: 'Klasyfikacja',
                        fields: [
                            field('Kategoria', element.category),
                            field('Typ', element.type),
                            field('Amenity', primary.amenity),
                            field('Tourism', primary.tourism),
                            field('Shop', primary.shop),
                            field('Building', primary.building),
                            field('Historic', primary.historic),
                            field('Leisure', primary.leisure),
                            field('Office', primary.office),
                            field('Healthcare', primary.healthcare),
                            field('Public transport', primary.public_transport)
                        ]
                    },
                    {
                        title: 'Pozostałe cechy główne',
                        fields: objectFields(primary).filter((item) => ![
                            'amenity',
                            'tourism',
                            'shop',
                            'building',
                            'historic',
                            'leisure',
                            'office',
                            'healthcare',
                            'public_transport',
                            'building_attributes',
                            'boundary_attributes',
                            'highway_attributes',
                            'place_attributes',
                            'railway_attributes'
                        ].includes(item.label))
                    }
                ]
            },
            {
                id: 'contact',
                label: 'Kontakt',
                sections: [
                    {
                        title: 'Kontakt',
                        fields: [
                            field('Telefon', firstValue(annotations.phone, annotations['contact:phone'])),
                            field('Email', firstValue(annotations.email, annotations['contact:email'])),
                            field('Fax', firstValue(annotations.fax, annotations['contact:fax'])),
                            field('SMS', annotations['contact:sms']),
                            field('Strona', firstValue(annotations.website, annotations['contact:website']))
                        ]
                    },
                    { title: 'Takeaway', fields: objectFields(annotations.takeaway) },
                    { title: 'Drive-through', fields: objectFields(annotations.drive_through) },
                    { title: 'Delivery', fields: objectFields(annotations.delivery) },
                    {
                        title: 'Pozostałe dane kontaktowe',
                        fields: withoutFields(objectFields(annotations), [
                            'phone',
                            'contact:phone',
                            'email',
                            'contact:email',
                            'fax',
                            'contact:fax',
                            'contact:sms',
                            'website',
                            'contact:website',
                            'takeaway',
                            'drive_through',
                            'delivery',
                            'wikipedia',
                            'source',
                            'source:geometry',
                            'source:name',
                            'source:ref',
                            'image',
                            'description',
                            'comment',
                            'note',
                            'fixme'
                        ])
                    }
                ]
            },
            {
                id: 'service',
                label: 'Obsługa',
                sections: [
                    {
                        title: 'Działanie miejsca',
                        fields: [
                            field('Godziny otwarcia', properties.opening_hours),
                            field('Godziny drive-through', properties['opening_hours:drive_through']),
                            field('Opłata', properties.fee),
                            field('Koszt', properties.charge),
                            field('Internet', properties.internet_access),
                            field('Toalety', properties.toilets),
                            field('Toalety dla wózków', properties['toilets:wheelchair']),
                            field('Prysznic', properties.shower),
                            field('Woda pitna', properties.drinking_water),
                            field('Dostępność', properties.wheelchair)
                        ]
                    }
                ]
            },
            {
                id: 'technical',
                label: 'Techniczne',
                sections: [
                    {
                        title: 'Identyfikatory i metadane',
                        fields: [
                            field('Place ID', element.place_id),
                            field('OSM type', element.osm_type),
                            field('OSM ID', element.osm_id),
                            field('Kategoria', element.category),
                            field('Typ', element.type),
                            field('Importance', element.importance),
                            field('Place rank', element.place_rank),
                            field('Licence', element.licence),
                            field('Szerokość', coordinates.latitude),
                            field('Długość', coordinates.longitude)
                        ]
                    },
                    {
                        title: 'Bounds',
                        fields: [
                            field('Południe', bounds.south),
                            field('Zachód', bounds.west),
                            field('Północ', bounds.north),
                            field('Wschód', bounds.east)
                        ]
                    },
                    { title: 'Budynek', fields: objectFields(primary.building_attributes) },
                    { title: 'Granice', fields: objectFields(primary.boundary_attributes) },
                    { title: 'Droga', fields: objectFields(primary.highway_attributes) },
                    { title: 'Miejsce', fields: objectFields(primary.place_attributes) },
                    { title: 'Kolej', fields: objectFields(primary.railway_attributes) },
                    { title: 'Właściwości', fields: objectFields(properties) }
                ]
            },
            {
                id: 'access',
                label: 'Dostęp',
                sections: [
                    { title: 'Ograniczenia', fields: objectFields(restrictions) },
                    {
                        title: 'Dostępność',
                        fields: [
                            field('Wheelchair', properties.wheelchair),
                            field('Toll', restrictions.toll),
                            field('Smoking', restrictions.smoking),
                            field('Dog', restrictions.dog),
                            field('One-way', restrictions.oneway),
                            field('No exit', restrictions.noexit)
                        ]
                    }
                ]
            },
            {
                id: 'sources',
                label: 'Źródła',
                sections: [
                    { title: 'Referencje', fields: objectFields(references) },
                    {
                        title: 'Adnotacje',
                        fields: [
                            field('Wikipedia', annotations.wikipedia),
                            field('Źródło', annotations.source),
                            field('Źródło geometrii', annotations['source:geometry']),
                            field('Źródło nazwy', annotations['source:name']),
                            field('Źródło ref', annotations['source:ref']),
                            field('Zdjęcie', annotations.image),
                            field('Opis', annotations.description),
                            field('Komentarz', annotations.comment),
                            field('Note', annotations.note),
                            field('Fixme', annotations.fixme)
                        ]
                    }
                ]
            },
            {
                id: 'raw',
                label: 'Surowe',
                sections: [
                    {
                        title: 'Model JSON',
                        fields: [
                            field('Model', element)
                        ]
                    },
                    {
                        title: 'Raw data JSON',
                        fields: [
                            field('Raw data', element.raw_data)
                        ]
                    }
                ]
            }
        ];
    };

    const currentTabs = () => state.element ? buildTabs(state.element) : [];

    const tabHasVisibleData = (tab, showEmpty) => tab.sections.some((section) => (
        section.fields.some((item) => showEmpty || !isEmpty(item.value))
    ));

    const renderTabs = () => {
        const showEmpty = showEmptyInput.checked;
        const visibleTabs = currentTabs().filter((tab) => tabHasVisibleData(tab, showEmpty));

        if (!visibleTabs.some((tab) => tab.id === state.activeTab)) {
            state.activeTab = visibleTabs[0]?.id || 'basic';
        }

        tabs.replaceChildren();
        visibleTabs.forEach((tab) => {
            const button = document.createElement('button');
            button.className = 'place-details-panel__tab';
            button.classList.toggle('place-details-panel__tab--active', tab.id === state.activeTab);
            button.type = 'button';
            button.textContent = tab.label;
            button.setAttribute('role', 'tab');
            button.setAttribute('aria-selected', String(tab.id === state.activeTab));
            button.addEventListener('click', () => {
                state.activeTab = tab.id;
                renderPanel();
            });

            tabs.append(button);
        });
    };

    const renderPanel = () => {
        if (!state.element) {
            setStatus('Brak danych miejsca.');
            return;
        }

        const showEmpty = showEmptyInput.checked;
        const tab = currentTabs().find((item) => item.id === state.activeTab);

        renderTabs();
        content.replaceChildren();
        titleElement.textContent = state.title;
        updateFavouriteHeader();

        let renderedSections = 0;

        (tab?.sections || []).forEach((section) => {
            const sectionElement = createSection(section, showEmpty);
            if (!sectionElement) {
                return;
            }

            renderedSections += 1;
            content.append(sectionElement);
        });

        if (!renderedSections) {
            const empty = document.createElement('p');
            empty.className = 'place-details-panel__empty';
            empty.textContent = 'Brak danych w tej sekcji.';
            content.append(empty);
        }

        exportButton.disabled = false;
    };

    const render = (title, element, favourite = null) => {
        state.title = title || 'Wybrane miejsce';
        state.element = element || null;
        state.activeTab = 'basic';
        state.favourite = favourite;

        renderPanel();
        const latitude = Number(element?.coordinates?.latitude);
        const longitude = Number(element?.coordinates?.longitude);
        routeButton.disabled = !Number.isFinite(latitude) || !Number.isFinite(longitude);
        state.favourite = favourite || window.travelManagerFavourites?.findByElement(state.element) || null;
        updateFavouriteButtons();
        updateFavouriteHeader();
        refreshFavouriteTag();
        if (!favourite) {
            refreshFavourite();
        }
        updateRouteButton();
        open();
    };

    const createExportFilename = () => {
        const safeName = (state.title || 'place-data').replace(/[^a-z0-9_-]+/gi, '_').toLowerCase();

        return `${safeName || 'place-data'}.json`;
    };

    const downloadData = () => {
        if (!state.element) {
            return;
        }

        const blob = new Blob([JSON.stringify(state.element, null, 2)], {
            type: 'application/json'
        });
        const link = document.createElement('a');

        link.href = URL.createObjectURL(blob);
        link.download = createExportFilename();
        link.click();
        URL.revokeObjectURL(link.href);
    };

    const exportData = async () => {
        if (!state.element) {
            return;
        }

        const api = window.pywebview?.api;

        if (api?.save_place_data) {
            exportButton.disabled = true;

            try {
                const result = await api.save_place_data(state.element, createExportFilename());

                if (result?.status === 'saved' || result?.status === 'cancelled') {
                    return;
                }
            } catch (error) {
                // Browser download remains available when the native bridge cannot save.
            } finally {
                exportButton.disabled = false;
            }
        }

        downloadData();
    };

    showEmptyInput.addEventListener('change', renderPanel);
    exportButton.addEventListener('click', exportData);
    favouriteAddButton.addEventListener('click', editFavourite);
    favouriteEditButton.addEventListener('click', editFavourite);
    favouriteRemoveButton.addEventListener('click', removeFavourite);
    routeButton?.addEventListener('click', () => {
        if (!state.element) {
            return;
        }

        const routePanel = window.travelManagerRouteDetailsPanel;

        if (routePanel?.isActive()) {
            routePanel.addElement(state.title, state.element);
        } else {
            routePanel?.openWithDestination(state.title, state.element);
        }
        close(false);
    });
    closeButton?.addEventListener('click', () => close());
    document.addEventListener('travel-manager:route-session-changed', updateRouteButton);
    document.addEventListener('travel-manager:favourites-changed', (event) => {
        const favourites = event.detail?.favourites || [];
        state.favourite = favourites.find((item) => item.id === state.favourite?.id)
            || window.travelManagerFavourites?.findByElement(state.element)
            || null;
        updateFavouriteButtons();
        updateFavouriteHeader();
        refreshFavouriteTag();
    });

    const resize = {
        startX: 0,
        startWidth: 0
    };

    const getPanelBounds = () => {
        const computed = window.getComputedStyle(panel);

        return {
            min: Number.parseFloat(computed.minWidth) || 260,
            max: Number.parseFloat(computed.maxWidth) || 620
        };
    };

    const onPointerMove = (event) => {
        const bounds = getPanelBounds();
        const nextWidth = resize.startWidth + resize.startX - event.clientX;
        const width = Math.min(Math.max(nextWidth, bounds.min), bounds.max);

        panel.style.setProperty('--place-details-panel-width', `${width}px`);
    };

    const stopResize = () => {
        panel.classList.remove('place-details-panel--resizing');
        document.removeEventListener('pointermove', onPointerMove);
        document.removeEventListener('pointerup', stopResize);
        patchUiSettings({
            place_details_panel_width: Math.round(panel.getBoundingClientRect().width)
        });
    };

    if (grabber) {
        grabber.addEventListener('pointerdown', (event) => {
            event.preventDefault();

            resize.startX = event.clientX;
            resize.startWidth = panel.getBoundingClientRect().width;

            panel.classList.add('place-details-panel--resizing');
            document.addEventListener('pointermove', onPointerMove);
            document.addEventListener('pointerup', stopResize);
        });
    }

    exportButton.disabled = true;
    routeButton.disabled = true;
    favouriteAddButton.disabled = true;
    loadUiSettings();

    window.travelManagerPlaceDetailsPanel = {
        close,
        open,
        render,
        setStatus
    };
});
