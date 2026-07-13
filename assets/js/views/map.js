document.addEventListener('travel-manager:views-ready', () => {
    const mapElement = document.querySelector('#map');
    const searchForm = document.querySelector('.header__search');
    const searchInput = document.querySelector('.header__search-input');
    const advancedSearchButton = document.querySelector('.header__advanced-search-button');
    const legendButton = document.querySelector('[data-map-tool="legend"]');
    const layersButton = document.querySelector('[data-map-tool="layers"]');
    const locationButton = document.querySelector('[data-map-tool="location"]');
    const placeDetailsPanel = window.travelManagerPlaceDetailsPanel;
    const routeDetailsPanel = window.travelManagerRouteDetailsPanel;
    let selectedMarker = null;
    let locationMarker = null;
    let mapDataLoading = false;
    let mapNotesLoading = false;
    let activeBaseLayer = null;
    let advancedSearchRequestId = 0;
    let favouritePlaces = [];
    let layerState = {
        map_base_layer: 'standard',
        layer_favourites_enabled: true,
        layer_favourite_visible_tag_ids: null,
        layer_map_data_enabled: false,
        layer_map_notes_enabled: false,
        layer_public_gps_traces_enabled: false
    };

    if (!mapElement || !window.L) {
        return;
    }

    const getJson = async (url) => {
        const response = await fetch(url, {
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`Request failed: ${response.status}`);
        }

        return response.json();
    };

    const getSelectedElement = (data) => data?.place?.selected || null;

    const getCoordinates = (element) => element?.coordinates || {};

    const firstValue = (...values) => values.find((value) => value !== null && value !== undefined && value !== '');
    const reverseCoordinateToleranceMeters = 10;

    const distanceMeters = (firstLat, firstLon, secondLat, secondLon) => {
        const earthRadius = 6371000;
        const toRadians = (value) => value * Math.PI / 180;
        const deltaLat = toRadians(secondLat - firstLat);
        const deltaLon = toRadians(secondLon - firstLon);
        const lat1 = toRadians(firstLat);
        const lat2 = toRadians(secondLat);
        const a = Math.sin(deltaLat / 2) ** 2
            + Math.cos(lat1) * Math.cos(lat2) * Math.sin(deltaLon / 2) ** 2;

        return earthRadius * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    };

    const elementWithClickedCoordinates = (element, clickedLat, clickedLon) => {
        if (!element) {
            return null;
        }

        const elementLat = Number(element?.coordinates?.latitude);
        const elementLon = Number(element?.coordinates?.longitude);
        const latitude = Number(clickedLat);
        const longitude = Number(clickedLon);

        if (
            !Number.isFinite(latitude)
            || !Number.isFinite(longitude)
            || !Number.isFinite(elementLat)
            || !Number.isFinite(elementLon)
        ) {
            return element;
        }

        const distance = distanceMeters(latitude, longitude, elementLat, elementLon);

        if (distance <= reverseCoordinateToleranceMeters) {
            return element;
        }

        return {
            ...element,
            coordinates: {
                ...(element.coordinates || {}),
                latitude,
                longitude
            },
            raw_data: {
                ...(element.raw_data || {}),
                clicked_coordinates: {
                    latitude,
                    longitude
                },
                reverse_result_coordinates: {
                    latitude: elementLat,
                    longitude: elementLon
                },
                reverse_result_distance_meters: Math.round(distance * 100) / 100
            }
        };
    };

    const patchUiSettings = (data) => fetch('/api/settings/ui', {
        method: 'PATCH',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).catch(() => {});

    const getUiSettings = async () => {
        try {
            const response = await fetch('/api/settings/ui', {
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                return null;
            }

            return (await response.json())?.ui || null;
        } catch (error) {
            return null;
        }
    };

    const getSavedMapView = (settings) => {
        const lat = Number(settings?.map_latitude);
        const lon = Number(settings?.map_longitude);
        const zoom = Number(settings?.map_zoom);

        if (!Number.isFinite(lat) || !Number.isFinite(lon) || !Number.isFinite(zoom)) {
            return {
                center: [52.2297, 21.0122],
                zoom: 13
            };
        }

        return {
            center: [lat, lon],
            zoom
        };
    };

    const renderPlaceDetails = (element, fallbackTitle = 'Wybrane miejsce') => {
        if (!element) {
            placeDetailsPanel?.setStatus('Nie znaleziono miejsca.');
            return;
        }

        const names = element.name || {};

        placeDetailsPanel?.render(
            firstValue(names.name, names.official_name, names.short_name, element.display_name, fallbackTitle),
            element
        );
    };

    const map = L.map('map', {
        zoomControl: true
    }).setView([52.2297, 21.0122], 13);

    const baseLayers = {
        standard: {
            label: 'Standard',
            layer: L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            })
        },
        cyclosm: {
            label: 'CyclOSM',
            layer: L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {
                maxZoom: 20,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, CyclOSM'
            })
        },
        humanitarian: {
            label: 'Humanitarian',
            layer: L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
                maxZoom: 20,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Humanitarian OpenStreetMap Team'
            })
        }
    };

    const publicGpsTracesLayer = L.tileLayer('https://{s}.gps-tile.openstreetmap.org/lines/{z}/{x}/{y}.png', {
        maxZoom: 19,
        opacity: 0.75,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    const mapNotesLayer = L.layerGroup();
    const mapDataLayer = L.layerGroup();
    const favouritesLayer = L.layerGroup();
    const routePointsLayer = L.layerGroup().addTo(map);
    let routeGeometryLayer = null;

    const routeLineStyle = (transport) => {
        const baseStyle = {
            opacity: 0.92,
            weight: 6,
            lineJoin: 'round'
        };

        if (transport === 'foot') {
            return {
                ...baseStyle,
                color: '#1f6fae',
                dashArray: '1 11',
                lineCap: 'round'
            };
        }

        if (transport === 'bicycle') {
            return {
                ...baseStyle,
                color: '#1f6fae',
                dashArray: '12 10',
                lineCap: 'butt'
            };
        }

        return {
            ...baseStyle,
            color: '#1f6fae',
            lineCap: 'round'
        };
    };

    const setBaseLayer = (id) => {
        const nextLayer = baseLayers[id] ? id : 'standard';

        if (activeBaseLayer && map.hasLayer(baseLayers[activeBaseLayer].layer)) {
            map.removeLayer(baseLayers[activeBaseLayer].layer);
        }

        activeBaseLayer = nextLayer;
        baseLayers[activeBaseLayer].layer.addTo(map);

        document.dispatchEvent(new CustomEvent('travel-manager:base-layer-changed', {
            detail: {
                map_base_layer: activeBaseLayer,
                label: baseLayers[activeBaseLayer].label
            }
        }));
    };

    setBaseLayer('standard');

    getUiSettings().then((settings) => {
        const view = getSavedMapView(settings);
        map.setView(view.center, view.zoom);
        applyLayerState(settings || {});
    });

    const getBounds = () => {
        const bounds = map.getBounds();

        return {
            south: bounds.getSouth(),
            west: bounds.getWest(),
            north: bounds.getNorth(),
            east: bounds.getEast()
        };
    };

    const getSearchContext = () => {
        const center = map.getCenter();

        return {
            bounds: getBounds(),
            center: {
                latitude: center.lat,
                longitude: center.lng
            },
            zoom: map.getZoom()
        };
    };

    const fetchVisibleOpenStreetMapData = async () => {
        const bounds = getBounds();
        const bbox = `${bounds.south},${bounds.west},${bounds.north},${bounds.east}`;
        const query = `
            [out:json][timeout:25];
            (
                node(${bbox});
                way(${bbox});
                relation(${bbox});
            );
            out body geom;
        `;

        const response = await fetch('https://overpass-api.de/api/interpreter', {
            method: 'POST',
            body: new URLSearchParams({ data: query })
        });

        if (!response.ok) {
            throw new Error(`OpenStreetMap data request failed: ${response.status}`);
        }

        return response.json();
    };

    const setLayerEnabled = (layer, enabled) => {
        if (enabled && !map.hasLayer(layer)) {
            layer.addTo(map);
        }

        if (!enabled && map.hasLayer(layer)) {
            layer.remove();
        }
    };

    const escapeHtml = (value) => {
        const element = document.createElement('span');
        element.textContent = String(value ?? '');
        return element.innerHTML;
    };

    const visibleFavourites = () => {
        const visibleTagIds = Array.isArray(layerState.layer_favourite_visible_tag_ids)
            ? new Set(layerState.layer_favourite_visible_tag_ids)
            : null;

        return visibleTagIds
            ? favouritePlaces.filter((favourite) => visibleTagIds.has(favourite.tag_id))
            : favouritePlaces;
    };

    const favouriteIcon = (favourite) => favourite.icon || favourite.tag?.icon || '⭐';

    const consumeFavouriteAsRoutePoint = (favourite) => routeDetailsPanel?.consumeElement(
        favourite.name,
        {
            ...(favourite.place_data || {}),
            display_name: favourite.place_data?.display_name || favourite.name,
            coordinates: {
                ...(favourite.place_data?.coordinates || {}),
                latitude: Number(favourite.latitude),
                longitude: Number(favourite.longitude)
            }
        }
    );

    const renderFavourites = (favourites = null) => {
        if (Array.isArray(favourites)) {
            favouritePlaces = favourites;
        }

        favouritesLayer.clearLayers();

        visibleFavourites().forEach((favourite) => {
            const latitude = Number(favourite.latitude);
            const longitude = Number(favourite.longitude);

            if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
                return;
            }

            const marker = L.marker([latitude, longitude], {
                bubblingMouseEvents: false,
                icon: L.divIcon({
                    className: 'favourite-marker',
                    html: `<span>${escapeHtml(favouriteIcon(favourite))}</span>`,
                    iconSize: [34, 34],
                    iconAnchor: [17, 17]
                }),
                title: favourite.name
            });
            marker.bindTooltip(
                `<strong>${escapeHtml(favourite.name)}</strong><br><em>${escapeHtml(favourite.tag?.name || 'Ulubione')}</em>`,
                { direction: 'top' }
            );
            marker.on('click', () => {
                if (routeDetailsPanel?.isSelectingPoint()) {
                    consumeFavouriteAsRoutePoint(favourite);
                    return;
                }

                setSelectedMarker(latitude, longitude);
                placeDetailsPanel?.render(favourite.name, favourite.place_data, favourite);
            });
            favouritesLayer.addLayer(marker);
        });
    };

    const showFavourite = (favourite) => {
        const latitude = Number(favourite?.latitude);
        const longitude = Number(favourite?.longitude);

        if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
            return;
        }

        setLayerEnabled(favouritesLayer, true);
        map.setView([latitude, longitude], Math.max(map.getZoom(), 17));

        if (routeDetailsPanel?.isSelectingPoint()) {
            consumeFavouriteAsRoutePoint(favourite);
            return;
        }

        setSelectedMarker(latitude, longitude);
        placeDetailsPanel?.render(favourite.name, favourite.place_data, favourite);
    };

    const showElement = (element, title = 'Wybrane miejsce') => {
        const coordinates = getCoordinates(element);
        const latitude = Number(coordinates.latitude);
        const longitude = Number(coordinates.longitude);

        if (Number.isFinite(latitude) && Number.isFinite(longitude)) {
            map.setView([latitude, longitude], Math.max(map.getZoom(), 16));
            setSelectedMarker(latitude, longitude);
        }

        renderPlaceDetails(element, title);
    };

    const searchLocalFavourites = async ({ keyword = '', category, subcategory, radiusKm = 0 }) => {
        const phrase = keyword.trim().toLowerCase();
        const context = getSearchContext();
        const bounds = context.bounds;
        const radius = Number(radiusKm) || 0;
        const favourites = await window.travelManagerFavourites?.list();
        const results = (favourites || [])
            .filter((favourite) => {
                const latitude = Number(favourite.latitude);
                const longitude = Number(favourite.longitude);

                if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
                    return false;
                }

                if (radius > 0) {
                    const meters = distanceMeters(
                        context.center.latitude,
                        context.center.longitude,
                        latitude,
                        longitude
                    );

                    if (meters > radius * 1000) {
                        return false;
                    }
                } else if (
                    latitude < bounds.south
                    || latitude > bounds.north
                    || longitude < bounds.west
                    || longitude > bounds.east
                ) {
                    return false;
                }

                if (!phrase) {
                    return true;
                }

                return [
                    favourite.name,
                    favourite.tag?.name,
                    favourite.place_data?.display_name,
                    favourite.place_data?.address?.city,
                    favourite.place_data?.address?.road,
                    favourite.place_data?.address?.house_number
                ].some((value) => String(value || '').toLowerCase().includes(phrase));
            })
            .map((favourite) => ({
                id: favourite.id,
                type: 'favourite',
                title: favourite.name,
                subtitle: favourite.place_data?.display_name || favourite.tag?.name || '',
                latitude: Number(favourite.latitude),
                longitude: Number(favourite.longitude),
                favourite
            }));

        window.travelManagerSearchResultsPanel?.show({
            title: subcategory?.label || category?.label || 'Ulubione',
            subtitle: phrase ? `Szukane: ${keyword}` : 'Lokalne ulubione miejsca',
            results
        });
    };

    const advancedSearchTitle = (detail) => detail?.subcategory?.label
        || detail?.category?.label
        || 'Wyniki wyszukiwania';

    const advancedSearchSubtitle = (detail) => {
        if (detail?.radiusKm > 0) {
            return `Promień ${detail.radiusKm} km od centrum mapy`;
        }

        return 'W aktualnie widocznym obszarze mapy';
    };

    const fetchJsonWithRetry = async (url, attempts = 2) => {
        let lastError = null;

        for (let attempt = 0; attempt < attempts; attempt += 1) {
            try {
                return await getJson(url);
            } catch (error) {
                lastError = error;

                if (attempt < attempts - 1) {
                    await new Promise((resolve) => window.setTimeout(resolve, 500 + attempt * 650));
                }
            }
        }

        throw lastError || new Error('Request failed.');
    };

    const searchAdvanced = async (detail) => {
        const requestId = ++advancedSearchRequestId;
        const searchDetail = JSON.parse(JSON.stringify(detail || {}));
        const category = detail?.category || null;
        const subcategory = detail?.subcategory || null;
        const title = advancedSearchTitle(detail);
        const subtitle = category?.id === 'favourites'
            ? (detail?.keyword ? `Szukane: ${detail.keyword}` : 'Lokalne ulubione miejsca')
            : advancedSearchSubtitle(detail);

        window.travelManagerSearchResultsPanel?.showLoading({ title, subtitle });

        if (category?.id === 'favourites') {
            try {
                await searchLocalFavourites(detail || {});
            } catch (error) {
                if (requestId !== advancedSearchRequestId) {
                    return;
                }

                window.travelManagerSearchResultsPanel?.showError({
                    title,
                    subtitle: 'Nie udało się wykonać wyszukiwania.',
                    message: 'Nie udało się wczytać ulubionych miejsc.',
                    retry: () => searchAdvanced(searchDetail)
                });
            }
            return;
        }

        const context = getSearchContext();
        const bounds = context.bounds;
        const url = new URL('/api/map/advanced-search', window.location.origin);

        if (detail?.query) {
            url.searchParams.set('q', detail.query);
        }

        if (detail?.keyword) {
            url.searchParams.set('keyword', detail.keyword);
        }

        url.searchParams.set('category_id', category?.id || '');
        url.searchParams.set('subcategory_id', subcategory?.id || '');
        url.searchParams.set('limit', '30');
        url.searchParams.set('west', bounds.west);
        url.searchParams.set('east', bounds.east);
        url.searchParams.set('south', bounds.south);
        url.searchParams.set('north', bounds.north);
        url.searchParams.set('center_lat', context.center.latitude);
        url.searchParams.set('center_lon', context.center.longitude);
        url.searchParams.set('radius_km', detail?.radiusKm || 0);

        try {
            const data = await fetchJsonWithRetry(url);
            if (requestId !== advancedSearchRequestId) {
                return;
            }

            const elements = data?.place?.elements || [];
            const results = elements.map((element) => {
                const coordinates = getCoordinates(element);

                return {
                    id: element.place_id || `${coordinates.latitude}:${coordinates.longitude}:${element.display_name}`,
                    type: 'place',
                    title: firstValue(
                        element.name?.name,
                        element.name?.official_name,
                        element.name?.short_name,
                        element.display_name,
                        detail?.query
                    ),
                    subtitle: element.display_name || '',
                    latitude: Number(coordinates.latitude),
                    longitude: Number(coordinates.longitude),
                    element
                };
            });

            window.travelManagerSearchResultsPanel?.show({
                title,
                subtitle,
                results
            });
        } catch (error) {
            if (requestId !== advancedSearchRequestId) {
                return;
            }

            window.travelManagerSearchResultsPanel?.showError({
                title,
                subtitle: 'Nie udało się wykonać wyszukiwania.',
                message: 'Nie udało się wykonać wyszukiwania.',
                retry: () => searchAdvanced(searchDetail)
            });
        }
    };

    const isAreaElement = (element) => {
        const tags = element.tags || {};
        const geometry = element.geometry || [];
        const first = geometry[0];
        const last = geometry[geometry.length - 1];
        const isClosed = first && last && first.lat === last.lat && first.lon === last.lon;

        if (!isClosed) {
            return false;
        }

        return Boolean(
            tags.area === 'yes'
            || tags.building
            || tags.landuse
            || tags.natural
            || tags.leisure
            || tags.amenity
            || tags.tourism
            || tags.shop
            || tags.boundary
            || tags.water
            || tags.waterway === 'riverbank'
        );
    };

    const getElementTitle = (element) => {
        const tags = element.tags || {};
        const primaryKey = [
            'name',
            'official_name',
            'short_name',
            'amenity',
            'shop',
            'tourism',
            'building',
            'highway',
            'railway',
            'natural',
            'landuse',
            'leisure'
        ].find((key) => tags[key]);

        return primaryKey ? tags[primaryKey] : `${element.type}/${element.id}`;
    };

    const getPrimaryCategory = (tags) => [
        'amenity',
        'shop',
        'tourism',
        'building',
        'highway',
        'railway',
        'natural',
        'landuse',
        'leisure',
        'historic',
        'office',
        'place'
    ].find((key) => tags[key]);

    const getLayerCenter = (layer, element) => {
        if (layer.getBounds) {
            const center = layer.getBounds().getCenter();

            return {
                latitude: center.lat,
                longitude: center.lng
            };
        }

        if (element.lat && element.lon) {
            return {
                latitude: element.lat,
                longitude: element.lon
            };
        }

        return {
            latitude: null,
            longitude: null
        };
    };

    const getLayerBounds = (layer) => {
        if (!layer.getBounds) {
            return {
                south: null,
                west: null,
                north: null,
                east: null
            };
        }

        const bounds = layer.getBounds();

        return {
            south: bounds.getSouth(),
            west: bounds.getWest(),
            north: bounds.getNorth(),
            east: bounds.getEast()
        };
    };

    const getAddressTags = (tags) => Object.entries(tags || {}).reduce((address, [key, value]) => {
        if (key.startsWith('addr:')) {
            address[key] = value;
        }

        return address;
    }, {});

    const createMapDataDetails = (element, layer) => {
        const tags = element.tags || {};
        const category = getPrimaryCategory(tags);
        const coordinates = getLayerCenter(layer, element);

        return {
            place_id: null,
            osm_type: element.type,
            osm_id: element.id,
            category,
            type: category ? tags[category] : null,
            display_name: getElementTitle(element),
            coordinates,
            bounds: getLayerBounds(layer),
            address: getAddressTags(tags),
            annotations: tags,
            name: {
                name: tags.name || null,
                official_name: tags.official_name || null,
                short_name: tags.short_name || null
            },
            properties: tags,
            references: tags,
            restrictions: tags,
            primary_features: tags,
            raw_data: element
        };
    };

    const bindMapDataClick = (layer, element) => {
        layer.on('click', (event) => {
            event.originalEvent?.stopPropagation();
            const details = createMapDataDetails(element, layer);

            placeDetailsPanel?.render(getElementTitle(element), details);
        });

        return layer;
    };

    const createMapDataLayer = (element) => {
        const tags = element.tags || {};
        const geometry = (element.geometry || []).map((point) => [point.lat, point.lon]);
        const title = getElementTitle(element);

        if (element.type === 'node' && Number.isFinite(element.lat) && Number.isFinite(element.lon)) {
            const marker = L.circleMarker([element.lat, element.lon], {
                radius: 4,
                color: '#6a4c93',
                fillColor: '#6a4c93',
                fillOpacity: 0.72,
                opacity: 0.95,
                weight: 1
            });

            marker.bindTooltip(title, {
                direction: 'top',
                sticky: true
            });

            return bindMapDataClick(marker, element);
        }

        if (!geometry.length) {
            return null;
        }

        const options = {
            color: tags.building ? '#c2410c' : '#6a4c93',
            fillColor: tags.building ? '#f97316' : '#8b5cf6',
            fillOpacity: isAreaElement(element) ? 0.16 : 0,
            opacity: 0.92,
            weight: tags.highway || tags.railway ? 3 : 2
        };

        const layer = isAreaElement(element)
            ? L.polygon(geometry, options)
            : L.polyline(geometry, options);

        layer.bindTooltip(title, {
            direction: 'top',
            sticky: true
        });

        return bindMapDataClick(layer, element);
    };

    const createMapNoteMarker = (note) => {
        const firstComment = note.comments?.[0]?.text || 'OpenStreetMap note';
        const marker = L.circleMarker([note.lat, note.lon], {
            radius: 6,
            color: '#d97706',
            fillColor: '#f59e0b',
            fillOpacity: 0.76,
            opacity: 0.98,
            weight: 2
        });

        marker.bindPopup(firstComment);

        return marker;
    };

    const refreshMapNotesLayer = async () => {
        if (!layerState.layer_map_notes_enabled || mapNotesLoading) {
            return;
        }

        mapNotesLoading = true;

        try {
            const bounds = getBounds();
            const url = new URL('https://www.openstreetmap.org/api/0.6/notes.json');

            url.searchParams.set('bbox', `${bounds.west},${bounds.south},${bounds.east},${bounds.north}`);
            url.searchParams.set('limit', '100');

            const data = await getJson(url);
            const notes = data?.features || [];

            mapNotesLayer.clearLayers();
            notes.forEach((feature) => {
                const coordinates = feature.geometry?.coordinates || [];
                const properties = feature.properties || {};

                if (coordinates.length >= 2) {
                    mapNotesLayer.addLayer(createMapNoteMarker({
                        lat: coordinates[1],
                        lon: coordinates[0],
                        comments: properties.comments || []
                    }));
                }
            });
        } catch (error) {
            mapNotesLayer.clearLayers();
        } finally {
            mapNotesLoading = false;
        }
    };

    const refreshMapDataLayer = async () => {
        if (!layerState.layer_map_data_enabled || mapDataLoading) {
            return;
        }

        mapDataLoading = true;

        try {
            const data = await fetchVisibleOpenStreetMapData();
            const elements = (data?.elements || [])
                .filter((element) => (
                    (element.type === 'node' && element.tags && element.lat && element.lon)
                    || (element.type !== 'node' && element.geometry?.length)
                ))
                .slice(0, 900);

            mapDataLayer.clearLayers();
            elements.forEach((element) => {
                const layer = createMapDataLayer(element);

                if (layer) {
                    mapDataLayer.addLayer(layer);
                }
            });
        } catch (error) {
            mapDataLayer.clearLayers();
        } finally {
            mapDataLoading = false;
        }
    };

    function applyLayerState(nextState) {
        layerState = {
            ...layerState,
            map_base_layer: nextState.map_base_layer || layerState.map_base_layer,
            layer_favourites_enabled: nextState.layer_favourites_enabled !== false,
            layer_favourite_visible_tag_ids: Array.isArray(nextState.layer_favourite_visible_tag_ids)
                ? nextState.layer_favourite_visible_tag_ids.map((item) => String(item))
                : null,
            layer_map_data_enabled: Boolean(nextState.layer_map_data_enabled),
            layer_map_notes_enabled: Boolean(nextState.layer_map_notes_enabled),
            layer_public_gps_traces_enabled: Boolean(nextState.layer_public_gps_traces_enabled)
        };

        setBaseLayer(layerState.map_base_layer);
        renderFavourites();
        setLayerEnabled(favouritesLayer, layerState.layer_favourites_enabled);
        setLayerEnabled(mapNotesLayer, layerState.layer_map_notes_enabled);
        setLayerEnabled(publicGpsTracesLayer, layerState.layer_public_gps_traces_enabled);
        setLayerEnabled(mapDataLayer, layerState.layer_map_data_enabled);

        if (layerState.layer_map_notes_enabled) {
            refreshMapNotesLayer();
        } else {
            mapNotesLayer.clearLayers();
        }

        if (layerState.layer_map_data_enabled) {
            refreshMapDataLayer();
        } else {
            mapDataLayer.clearLayers();
        }
    }

    const setSelectedMarker = (lat, lon) => {
        if (selectedMarker) {
            selectedMarker.setLatLng([lat, lon]);
            return;
        }

        selectedMarker = L.marker([lat, lon]).addTo(map);
    };

    const clearSelectedMarker = () => {
        if (!selectedMarker) {
            return;
        }

        selectedMarker.remove();
        selectedMarker = null;
    };

    const showPlaceFromCoordinates = async (lat, lon) => {
        if (routeDetailsPanel?.isSelectingPoint()) {
            try {
                const url = new URL('/api/map/reverse', window.location.origin);
                url.searchParams.set('lat', lat);
                url.searchParams.set('lon', lon);
                const data = await getJson(url);
                const element = elementWithClickedCoordinates(getSelectedElement(data), lat, lon) || {
                    display_name: `${Number(lat).toFixed(6)}, ${Number(lon).toFixed(6)}`,
                    coordinates: { latitude: lat, longitude: lon }
                };

                routeDetailsPanel.consumeElement(element.display_name, element);
            } catch (error) {
                routeDetailsPanel.consumeElement(`${Number(lat).toFixed(6)}, ${Number(lon).toFixed(6)}`, {
                    coordinates: { latitude: lat, longitude: lon }
                });
            }
            return;
        }

        setSelectedMarker(lat, lon);
        placeDetailsPanel?.setStatus('Ladowanie informacji o miejscu...');

        try {
            const url = new URL('/api/map/reverse', window.location.origin);
            url.searchParams.set('lat', lat);
            url.searchParams.set('lon', lon);
            const data = await getJson(url);
            renderPlaceDetails(elementWithClickedCoordinates(getSelectedElement(data), lat, lon));
        } catch (error) {
            placeDetailsPanel?.render('Wybrane miejsce', {
                coordinates: {
                    latitude: Number(lat).toFixed(6),
                    longitude: Number(lon).toFixed(6)
                },
                raw_data: {
                    status: 'Nie udalo sie pobrac szczegolow miejsca.'
                }
            });
        }
    };

    const showCurrentLocation = () => {
        if (!navigator.geolocation) {
            placeDetailsPanel?.setStatus('Geolokalizacja nie jest dostępna w tym środowisku.');
            return;
        }

        navigator.geolocation.getCurrentPosition((position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const accuracy = position.coords.accuracy;

            if (locationMarker) {
                locationMarker.setLatLng([lat, lon]);
            } else {
                locationMarker = L.circleMarker([lat, lon], {
                    radius: 8,
                    color: '#2e7d32',
                    fillColor: '#2e7d32',
                    fillOpacity: 0.68,
                    opacity: 0.96,
                    weight: 2
                }).addTo(map);
            }

            locationMarker.bindPopup(`Moja lokalizacja${Number.isFinite(accuracy) ? `, dokładność około ${Math.round(accuracy)} m` : ''}`);
            map.setView([lat, lon], Math.max(map.getZoom(), 16));
        }, () => {
            placeDetailsPanel?.setStatus('Nie udało się pobrać lokalizacji. Sprawdź uprawnienia lokalizacji w systemie.');
        }, {
            enableHighAccuracy: true,
            maximumAge: 30000,
            timeout: 12000
        });
    };

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let saveMapViewTimeout = null;

    const saveMapView = () => {
        if (saveMapViewTimeout) {
            window.clearTimeout(saveMapViewTimeout);
        }

        saveMapViewTimeout = window.setTimeout(() => {
            const center = map.getCenter();

            patchUiSettings({
                map_latitude: center.lat,
                map_longitude: center.lng,
                map_zoom: map.getZoom()
            });
        }, 350);
    };

    map.on('moveend zoomend', () => {
        saveMapView();
        refreshMapNotesLayer();
        refreshMapDataLayer();
    });

    map.on('click', (event) => {
        showPlaceFromCoordinates(event.latlng.lat, event.latlng.lng);
    });

    legendButton?.addEventListener('click', () => {
        placeDetailsPanel?.close(false);
        window.travelManagerLegendDetailsPanel?.open();
    });

    layersButton?.addEventListener('click', () => {
        placeDetailsPanel?.close(false);
        window.travelManagerLayerDetailsPanel?.open();
    });

    locationButton?.addEventListener('click', showCurrentLocation);
    advancedSearchButton?.addEventListener('click', () => {
        window.travelManagerAdvancedSearch?.open(getSearchContext());
    });

    document.addEventListener('travel-manager:layers-changed', (event) => {
        applyLayerState(event.detail || {});
    });

    document.addEventListener('travel-manager:favourites-changed', (event) => {
        renderFavourites(event.detail?.favourites || []);
    });

    document.addEventListener('travel-manager:advanced-search-requested', (event) => {
        searchAdvanced(event.detail || {});
    });

    document.addEventListener('travel-manager:place-details-closed', clearSelectedMarker);

    document.addEventListener('travel-manager:route-selection-changed', (event) => {
        if (!searchInput) {
            return;
        }

        searchInput.placeholder = event.detail?.selecting
            ? 'Wyszukaj punkt trasy'
            : 'Szukaj miejsca';
    });

    document.addEventListener('travel-manager:route-updated', (event) => {
        const route = event.detail?.route;
        const points = event.detail?.points || [];
        const transport = event.detail?.transport || 'car';

        if (routeGeometryLayer) {
            routeGeometryLayer.remove();
            routeGeometryLayer = null;
        }

        routePointsLayer.clearLayers();
        points.forEach((point, index) => {
            const marker = L.marker([point.latitude, point.longitude], {
                icon: L.divIcon({
                    className: 'route-point-marker',
                    html: `<span>${index + 1}</span>`,
                    iconSize: [28, 28],
                    iconAnchor: [14, 14]
                })
            });
            marker.bindTooltip(point.title, { direction: 'top' });
            routePointsLayer.addLayer(marker);
        });

        if (!route?.geometry) {
            return;
        }

        routeGeometryLayer = L.geoJSON(route.geometry, {
            style: routeLineStyle(transport)
        }).addTo(map);

        const bounds = routeGeometryLayer.getBounds();
        if (bounds.isValid()) {
            map.fitBounds(bounds, { padding: [42, 42] });
        }
    });

    if (searchForm && searchInput) {
        searchForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const query = searchInput.value.trim();

            if (!query) {
                return;
            }

            const selectingRoutePoint = Boolean(routeDetailsPanel?.isSelectingPoint());

            if (!selectingRoutePoint) {
                placeDetailsPanel?.setStatus('Szukanie miejsca...');
            }

            try {
                const url = new URL('/api/map/search', window.location.origin);
                url.searchParams.set('q', query);
                const data = await getJson(url);
                const result = getSelectedElement(data);

                if (!result) {
                    placeDetailsPanel?.setStatus('Nie znaleziono miejsca.');
                    return;
                }

                const coordinates = getCoordinates(result);
                const lat = Number(coordinates.latitude);
                const lon = Number(coordinates.longitude);

                map.setView([lat, lon], 15);

                if (selectingRoutePoint && routeDetailsPanel?.isSelectingPoint()) {
                    routeDetailsPanel.consumeElement(
                        firstValue(
                            result.name?.name,
                            result.name?.official_name,
                            result.display_name,
                            query
                        ),
                        result
                    );
                    searchInput.value = '';
                    return;
                }

                setSelectedMarker(lat, lon);
                renderPlaceDetails(result, query);
            } catch (error) {
                if (!selectingRoutePoint) {
                    placeDetailsPanel?.setStatus('Wyszukiwanie nie powiodlo sie.');
                }
            }
        });
    }

    window.travelManagerMap = {
        map,
        clearSelectedMarker,
        fetchVisibleOpenStreetMapData,
        getBounds,
        getSearchContext,
        searchAdvanced,
        showElement,
        showFavourite
    };

    window.travelManagerFavourites?.list().then(renderFavourites).catch(() => {});
});
