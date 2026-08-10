document.addEventListener('travel-manager:views-ready', () => {
    const t = window.i18n.t;
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
        title: t('PANEL_PLACE_DETAILS.SELECTED_PLACE')
    };

    const osmEnumGroups = Object.freeze({
        abutters: 'RES_ENUM_ABUTTERS',
        access: 'RES_ENUM_ACCESS',
        advertising: 'RES_ENUM_ADVERTISING',
        aerialway: 'RES_ENUM_AERIALWAY',
        aeroway: 'RES_ENUM_AEROWAY',
        alcohol: 'RES_ENUM_ALCOHOL',
        amenity: 'RES_ENUM_AMENITY',
        area: 'RES_ENUM_AREA',
        artwork_type: 'RES_ENUM_ARTWORK_TYPE',
        'artwork:type': 'RES_ENUM_ARTWORK_TYPE',
        attraction: 'RES_ENUM_ATTRACTION',
        barrier: 'RES_ENUM_BARRIER',
        basin: 'RES_ENUM_BASIN',
        bicycle: 'RES_ENUM_BICYCLE',
        bicycle_road: 'RES_ENUM_BICYCLE_ROAD',
        boat: 'RES_ENUM_BOAT',
        boundary: 'RES_ENUM_BOUNDARY',
        bridge: 'RES_ENUM_BRIDGE',
        building: 'RES_ENUM_BUILDING',
        building_material: 'RES_ENUM_BUILDING_MATERIAL',
        'building:material': 'RES_ENUM_BUILDING_MATERIAL',
        building_part: 'RES_ENUM_BUILDING_PART',
        'building:part': 'RES_ENUM_BUILDING_PART',
        bus_bay: 'RES_ENUM_BUS_BAY',
        busway: 'RES_ENUM_BUSWAY',
        castle_type: 'RES_ENUM_CASTLE_TYPE',
        'castle:type': 'RES_ENUM_CASTLE_TYPE',
        change: 'RES_ENUM_CHANGE',
        construction: 'RES_ENUM_CONSTRUCTION',
        covered: 'RES_ENUM_COVERED',
        craft: 'RES_ENUM_CRAFT',
        crossing: 'RES_ENUM_CROSSING',
        'crossing:island': 'RES_ENUM_AREA',
        cycleway: 'RES_ENUM_CYCLEWAY',
        'cycleway:left': 'RES_ENUM_CYCLEWAY',
        'cycleway:right': 'RES_ENUM_CYCLEWAY',
        'cycleway:both': 'RES_ENUM_CYCLEWAY',
        denomination: 'RES_ENUM_DENOMINATION',
        diplomatic: 'RES_ENUM_DIPLOMATIC',
        drinking_water_legal: 'RES_ENUM_DRINKING_WATER_LEGAL',
        'drinking_water:legal': 'RES_ENUM_DRINKING_WATER_LEGAL',
        electrified: 'RES_ENUM_ELECTRIFIED',
        embankment: 'RES_ENUM_EMBANKMENT',
        embedded_rails: 'RES_ENUM_EMBEDDED_RAILS',
        emergency: 'RES_ENUM_EMERGENCY',
        entrance: 'RES_ENUM_ENTRANCE',
        fee: 'RES_ENUM_FEE',
        footway: 'RES_ENUM_FOOTWAY',
        ford: 'RES_ENUM_FORD',
        generator_method: 'RES_ENUM_GENERATOR_METHOD',
        'generator:method': 'RES_ENUM_GENERATOR_METHOD',
        generator_source: 'RES_ENUM_GENERATOR_SOURCE',
        'generator:source': 'RES_ENUM_GENERATOR_SOURCE',
        geological: 'RES_ENUM_GEOLOGICAL',
        golf: 'RES_ENUM_GOLF',
        hazard: 'RES_ENUM_HAZARD',
        healthcare: 'RES_ENUM_HEALTHCARE',
        highway: 'RES_ENUM_HIGHWAY',
        historic: 'RES_ENUM_HISTORIC',
        horse: 'RES_ENUM_HORSE',
        hov: 'RES_ENUM_HOV',
        image_type: 'RES_ENUM_IMAGE_TYPE',
        incline: 'RES_ENUM_INCLINE',
        information: 'RES_ENUM_INFORMATION',
        landuse: 'RES_ENUM_LANDUSE',
        leaf_type: 'RES_ENUM_LEAF_TYPE',
        'leaf:type': 'RES_ENUM_LEAF_TYPE',
        leisure: 'RES_ENUM_LEISURE',
        lifeguard: 'RES_ENUM_LIFEGUARD',
        line: 'RES_ENUM_LINE',
        location: 'RES_ENUM_LOCATION',
        man_made: 'RES_ENUM_MAN_MADE',
        memorial: 'RES_ENUM_MEMORIAL',
        'memorial:type': 'RES_ENUM_MEMORIAL',
        military: 'RES_ENUM_MILITARY',
        motor_vehicle: 'RES_ENUM_MOTOR_VEHICLE',
        mountain_pass: 'RES_ENUM_MOUNTAIN_PASS',
        natural: 'RES_ENUM_NATURAL',
        noexit: 'RES_ENUM_NOEXIT',
        office: 'RES_ENUM_OFFICE',
        oneway: 'RES_ENUM_ONEWAY',
        'oneway:bicycle': 'RES_ENUM_ONEWAY',
        openfire: 'RES_ENUM_OPENFIRE',
        orientation: 'RES_ENUM_ORIENTATION',
        overtaking: 'RES_ENUM_OVERTAKING',
        parking: 'RES_ENUM_PARKING',
        'parking:side': 'RES_ENUM_PARKING',
        parking_condition: 'RES_ENUM_PARKING_CONDITION',
        'parking:condition': 'RES_ENUM_PARKING_CONDITION',
        parking_lane: 'RES_ENUM_PARKING_LANE',
        'parking:lane': 'RES_ENUM_PARKING_LANE',
        passing_places: 'RES_ENUM_PASSING_PLACES',
        place: 'RES_ENUM_PLACE',
        power: 'RES_ENUM_POWER',
        priority: 'RES_ENUM_PRIORITY',
        priority_road: 'RES_ENUM_PRIORITY_ROAD',
        public_transport: 'RES_ENUM_PUBLIC_TRANSPORT',
        railway: 'RES_ENUM_RAILWAY',
        religion: 'RES_ENUM_RELIGION',
        roller_coaster: 'RES_ENUM_ROLLER_COASTER',
        route: 'RES_ENUM_ROUTE',
        sac_scale: 'RES_ENUM_SAC_SCALE',
        sauna: 'RES_ENUM_SAUNA',
        seasonal: 'RES_ENUM_SEASONAL',
        service: 'RES_ENUM_SERVICE',
        shop: 'RES_ENUM_SHOP',
        shower: 'RES_ENUM_SHOWER',
        side: 'RES_ENUM_SIDE',
        sidewalk: 'RES_ENUM_SIDEWALK',
        smoking: 'RES_ENUM_SMOKING',
        smoothness: 'RES_ENUM_SMOOTHNESS',
        source: 'RES_ENUM_SOURCE',
        sport: 'RES_ENUM_SPORT',
        substance: 'RES_ENUM_SUBSTANCE',
        surface: 'RES_ENUM_SURFACE',
        telecom: 'RES_ENUM_TELECOM',
        telescope_type: 'RES_ENUM_TELESCOPE_TYPE',
        'telescope:type': 'RES_ENUM_TELESCOPE_TYPE',
        tidal: 'RES_ENUM_TIDAL',
        tourism: 'RES_ENUM_TOURISM',
        tower_construction: 'RES_ENUM_TOWER_CONSTRUCTION',
        'tower:construction': 'RES_ENUM_TOWER_CONSTRUCTION',
        tower_type: 'RES_ENUM_TOWER_TYPE',
        'tower:type': 'RES_ENUM_TOWER_TYPE',
        tracktype: 'RES_ENUM_TRACKTYPE',
        traffic_calming: 'RES_ENUM_TRAFFIC_CALMING',
        trail_visibility: 'RES_ENUM_TRAIL_VISIBILITY',
        trailblazed: 'RES_ENUM_TRAILBLAZED',
        tunnel: 'RES_ENUM_TUNNEL',
        turn: 'RES_ENUM_TURN',
        usage: 'RES_ENUM_USAGE',
        vending: 'RES_ENUM_VENDING',
        visibility: 'RES_ENUM_VISIBILITY',
        water: 'RES_ENUM_WATER',
        waterway: 'RES_ENUM_WATERWAY',
        wetland: 'RES_ENUM_WETLAND'
    });

    const enumValue = (fieldName, value) => {
        const group = osmEnumGroups[String(fieldName || '').toLocaleLowerCase()];

        if (!group || typeof value !== 'string') {
            return value;
        }

        return value.split(';').map((rawPart) => {
            const part = rawPart.trim();
            let member = part.toLocaleUpperCase().replace(/[^A-Z0-9]+/g, '_');
            if (/^[0-9]/.test(member)) {
                member = `NUMBER_${member}`;
            }
            const key = `${group}.${member}`;
            const translated = t(key);
            return translated === key ? part : translated;
        }).join('; ');
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
            routeButtonLabel.textContent = active
                ? t('PANEL_PLACE_DETAILS.ADD_TO_ROUTE')
                : t('PANEL_PLACE_DETAILS.ROUTE');
        }

        routeButton?.setAttribute('aria-label', active
            ? t('PANEL_PLACE_DETAILS.ADD_PLACE_TO_ROUTE')
            : t('PANEL_PLACE_DETAILS.CREATE_ROUTE_FROM_PLACE'));
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
            title: t('FAVOURITES_VIEW.DELETE_TITLE'),
            description: t('FAVOURITES_VIEW.DELETE_DESCRIPTION', {
                name: state.favourite.name
            }),
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
        state.title = t('PANEL_PLACE_DETAILS.SELECTED_PLACE');
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

    const field = (label, value, enumField = '') => ({
        label,
        value: enumField ? enumValue(enumField, value) : value
    });

    const objectFields = (object, labels = {}) => Object.entries(object || {}).map(([key, value]) => (
        field(labels[key] || key, value, key)
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
                label: t('PANEL_PLACE_DETAILS.BASIC'),
                sections: [
                    {
                        title: t('PANEL_PLACE_DETAILS.IDENTIFICATION'),
                        fields: [
                            field(t('PANEL_PLACE_DETAILS.NAME'), firstValue(names.name, names.official_name, names.short_name)),
                            field(t('PANEL_PLACE_DETAILS.OFFICIAL_NAME'), names.official_name),
                            field(t('PANEL_PLACE_DETAILS.SHORT_NAME'), names.short_name),
                            field(t('PANEL_PLACE_DETAILS.FULL_DESCRIPTION'), element.display_name)
                        ]
                    },
                    {
                        title: t('PANEL_PLACE_DETAILS.NAMES'),
                        fields: objectFields(names)
                    },
                    {
                        title: t('PANEL_PLACE_DETAILS.ADDRESS'),
                        fields: objectFields(address, {
                            'addr:housenumber': t('PANEL_PLACE_DETAILS.NUMBER'),
                            'addr:housename': t('PANEL_PLACE_DETAILS.HOUSE_NAME'),
                            'addr:street': t('PANEL_PLACE_DETAILS.STREET'),
                            'addr:place': t('PANEL_PLACE_DETAILS.PLACE'),
                            'addr:postcode': t('PANEL_PLACE_DETAILS.POSTCODE'),
                            'addr:city': t('PANEL_PLACE_DETAILS.CITY'),
                            'addr:suburb': t('PANEL_PLACE_DETAILS.DISTRICT'),
                            'addr:district': t('PANEL_PLACE_DETAILS.COUNTY_OR_DISTRICT'),
                            'addr:province': t('PANEL_PLACE_DETAILS.PROVINCE'),
                            'addr:state': t('PANEL_PLACE_DETAILS.STATE_OR_REGION'),
                            'addr:country': t('PANEL_PLACE_DETAILS.COUNTRY'),
                            'country_code': t('PANEL_PLACE_DETAILS.COUNTRY_CODE'),
                            'house_number': t('PANEL_PLACE_DETAILS.NUMBER'),
                            'ISO3166-2-lvl4': t('PANEL_PLACE_DETAILS.ISO_LEVEL_4'),
                            'neighbourhood': t('PANEL_PLACE_DETAILS.NEIGHBOURHOOD'),
                            'quarter': t('PANEL_PLACE_DETAILS.QUARTER_OR_AREA'),
                            'road': t('PANEL_PLACE_DETAILS.ROAD_OR_STREET'),
                            'state_district': t('PANEL_PLACE_DETAILS.STATE_DISTRICT')
                        })
                    },
                    {
                        title: t('PANEL_PLACE_DETAILS.LOCATION'),
                        fields: [
                            field(t('PANEL_PLACE_DETAILS.LATITUDE'), coordinates.latitude),
                            field(t('PANEL_PLACE_DETAILS.LONGITUDE'), coordinates.longitude)
                        ]
                    }
                ]
            },
            {
                id: 'type',
                label: t('PANEL_PLACE_DETAILS.TYPE'),
                sections: [
                    {
                        title: t('PANEL_PLACE_DETAILS.CLASSIFICATION'),
                        fields: [
                            field(t('PANEL_PLACE_DETAILS.CATEGORY'), element.category),
                            field(t('PANEL_PLACE_DETAILS.TYPE'), element.type, element.category),
                            field(t('PANEL_PLACE_DETAILS.AMENITY'), primary.amenity, 'amenity'),
                            field(t('PANEL_PLACE_DETAILS.TOURISM'), primary.tourism, 'tourism'),
                            field(t('PANEL_PLACE_DETAILS.SHOP'), primary.shop, 'shop'),
                            field(t('PANEL_PLACE_DETAILS.BUILDING'), primary.building, 'building'),
                            field(t('PANEL_PLACE_DETAILS.HISTORIC'), primary.historic, 'historic'),
                            field(t('PANEL_PLACE_DETAILS.LEISURE'), primary.leisure, 'leisure'),
                            field(t('PANEL_PLACE_DETAILS.OFFICE'), primary.office, 'office'),
                            field(t('PANEL_PLACE_DETAILS.HEALTHCARE'), primary.healthcare, 'healthcare'),
                            field(
                                t('PANEL_PLACE_DETAILS.PUBLIC_TRANSPORT'),
                                primary.public_transport,
                                'public_transport'
                            )
                        ]
                    },
                    {
                        title: t('PANEL_PLACE_DETAILS.OTHER_PRIMARY_FEATURES'),
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
                label: t('PANEL_PLACE_DETAILS.CONTACT'),
                sections: [
                    {
                        title: t('PANEL_PLACE_DETAILS.CONTACT'),
                        fields: [
                            field(t('PANEL_PLACE_DETAILS.PHONE'), firstValue(annotations.phone, annotations['contact:phone'])),
                            field(t('PANEL_PLACE_DETAILS.EMAIL'), firstValue(annotations.email, annotations['contact:email'])),
                            field(t('PANEL_PLACE_DETAILS.FAX'), firstValue(annotations.fax, annotations['contact:fax'])),
                            field(t('PANEL_PLACE_DETAILS.SMS'), annotations['contact:sms']),
                            field(t('PANEL_PLACE_DETAILS.WEBSITE'), firstValue(annotations.website, annotations['contact:website']))
                        ]
                    },
                    { title: t('PANEL_PLACE_DETAILS.TAKEAWAY'), fields: objectFields(annotations.takeaway) },
                    { title: t('PANEL_PLACE_DETAILS.DRIVE_THROUGH'), fields: objectFields(annotations.drive_through) },
                    { title: t('PANEL_PLACE_DETAILS.DELIVERY'), fields: objectFields(annotations.delivery) },
                    {
                        title: t('PANEL_PLACE_DETAILS.OTHER_CONTACT_DETAILS'),
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
                label: t('PANEL_PLACE_DETAILS.SERVICES'),
                sections: [
                    {
                        title: t('PANEL_PLACE_DETAILS.PLACE_OPERATION'),
                        fields: [
                            field(t('PANEL_PLACE_DETAILS.OPENING_HOURS'), properties.opening_hours),
                            field(t('PANEL_PLACE_DETAILS.DRIVE_THROUGH_HOURS'), properties['opening_hours:drive_through']),
                            field(t('PANEL_PLACE_DETAILS.FEE'), properties.fee, 'fee'),
                            field(t('PANEL_PLACE_DETAILS.CHARGE'), properties.charge),
                            field(t('PANEL_PLACE_DETAILS.INTERNET_ACCESS'), properties.internet_access),
                            field(t('PANEL_PLACE_DETAILS.TOILETS'), properties.toilets),
                            field(t('PANEL_PLACE_DETAILS.WHEELCHAIR_TOILETS'), properties['toilets:wheelchair']),
                            field(t('PANEL_PLACE_DETAILS.SHOWER'), properties.shower),
                            field(t('PANEL_PLACE_DETAILS.DRINKING_WATER'), properties.drinking_water),
                            field(t('PANEL_PLACE_DETAILS.ACCESSIBILITY'), properties.wheelchair)
                        ]
                    }
                ]
            },
            {
                id: 'technical',
                label: t('PANEL_PLACE_DETAILS.TECHNICAL'),
                sections: [
                    {
                        title: t('PANEL_PLACE_DETAILS.IDENTIFIERS_AND_METADATA'),
                        fields: [
                            field(t('PANEL_PLACE_DETAILS.PLACE_ID'), element.place_id),
                            field(t('PANEL_PLACE_DETAILS.OSM_TYPE'), element.osm_type),
                            field(t('PANEL_PLACE_DETAILS.OSM_ID'), element.osm_id),
                            field(t('PANEL_PLACE_DETAILS.CATEGORY'), element.category),
                            field(t('PANEL_PLACE_DETAILS.TYPE'), element.type, element.category),
                            field(t('PANEL_PLACE_DETAILS.IMPORTANCE'), element.importance),
                            field(t('PANEL_PLACE_DETAILS.PLACE_RANK'), element.place_rank),
                            field(t('PANEL_PLACE_DETAILS.LICENCE'), element.licence),
                            field(t('PANEL_PLACE_DETAILS.LATITUDE'), coordinates.latitude),
                            field(t('PANEL_PLACE_DETAILS.LONGITUDE'), coordinates.longitude)
                        ]
                    },
                    {
                        title: t('PANEL_PLACE_DETAILS.BOUNDS'),
                        fields: [
                            field(t('PANEL_PLACE_DETAILS.SOUTH'), bounds.south),
                            field(t('PANEL_PLACE_DETAILS.WEST'), bounds.west),
                            field(t('PANEL_PLACE_DETAILS.NORTH'), bounds.north),
                            field(t('PANEL_PLACE_DETAILS.EAST'), bounds.east)
                        ]
                    },
                    { title: t('PANEL_PLACE_DETAILS.BUILDING'), fields: objectFields(primary.building_attributes) },
                    { title: t('PANEL_PLACE_DETAILS.BOUNDARIES'), fields: objectFields(primary.boundary_attributes) },
                    { title: t('PANEL_PLACE_DETAILS.ROAD'), fields: objectFields(primary.highway_attributes) },
                    { title: t('PANEL_PLACE_DETAILS.PLACE'), fields: objectFields(primary.place_attributes) },
                    { title: t('PANEL_PLACE_DETAILS.RAILWAY'), fields: objectFields(primary.railway_attributes) },
                    { title: t('PANEL_PLACE_DETAILS.PROPERTIES'), fields: objectFields(properties) }
                ]
            },
            {
                id: 'access',
                label: t('PANEL_PLACE_DETAILS.ACCESS'),
                sections: [
                    { title: t('PANEL_PLACE_DETAILS.RESTRICTIONS'), fields: objectFields(restrictions) },
                    {
                        title: t('PANEL_PLACE_DETAILS.ACCESSIBILITY'),
                        fields: [
                            field(t('PANEL_PLACE_DETAILS.WHEELCHAIR'), properties.wheelchair),
                            field(t('PANEL_PLACE_DETAILS.TOLL'), restrictions.toll, 'fee'),
                            field(t('PANEL_PLACE_DETAILS.SMOKING'), restrictions.smoking),
                            field(t('PANEL_PLACE_DETAILS.DOG'), restrictions.dog),
                            field(t('PANEL_PLACE_DETAILS.ONE_WAY'), restrictions.oneway),
                            field(t('PANEL_PLACE_DETAILS.NO_EXIT'), restrictions.noexit)
                        ]
                    }
                ]
            },
            {
                id: 'sources',
                label: t('PANEL_PLACE_DETAILS.SOURCES'),
                sections: [
                    { title: t('PANEL_PLACE_DETAILS.REFERENCES'), fields: objectFields(references) },
                    {
                        title: t('PANEL_PLACE_DETAILS.ANNOTATIONS'),
                        fields: [
                            field(t('PANEL_PLACE_DETAILS.WIKIPEDIA'), annotations.wikipedia),
                            field(t('PANEL_PLACE_DETAILS.SOURCE'), annotations.source),
                            field(t('PANEL_PLACE_DETAILS.GEOMETRY_SOURCE'), annotations['source:geometry']),
                            field(t('PANEL_PLACE_DETAILS.NAME_SOURCE'), annotations['source:name']),
                            field(t('PANEL_PLACE_DETAILS.REFERENCE_SOURCE'), annotations['source:ref']),
                            field(t('PANEL_PLACE_DETAILS.IMAGE'), annotations.image),
                            field(t('PANEL_PLACE_DETAILS.DESCRIPTION'), annotations.description),
                            field(t('PANEL_PLACE_DETAILS.COMMENT'), annotations.comment),
                            field(t('PANEL_PLACE_DETAILS.NOTE'), annotations.note),
                            field(t('PANEL_PLACE_DETAILS.FIXME'), annotations.fixme)
                        ]
                    }
                ]
            },
            {
                id: 'raw',
                label: t('PANEL_PLACE_DETAILS.RAW'),
                sections: [
                    {
                        title: t('PANEL_PLACE_DETAILS.MODEL_JSON'),
                        fields: [
                            field(t('PANEL_PLACE_DETAILS.MODEL'), element)
                        ]
                    },
                    {
                        title: t('PANEL_PLACE_DETAILS.RAW_DATA_JSON'),
                        fields: [
                            field(t('PANEL_PLACE_DETAILS.RAW_DATA'), element.raw_data)
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
            setStatus(t('PANEL_PLACE_DETAILS.NO_PLACE_DATA'));
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
            empty.textContent = t('PANEL_PLACE_DETAILS.NO_DATA_IN_SECTION');
            content.append(empty);
        }

        exportButton.disabled = false;
    };

    const render = (title, element, favourite = null) => {
        state.title = title || t('PANEL_PLACE_DETAILS.SELECTED_PLACE');
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
