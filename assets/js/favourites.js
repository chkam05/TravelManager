document.addEventListener('travel-manager:views-ready', () => {
    let favourites = [];
    let tags = [];
    let loaded = false;
    let tagsLoaded = false;

    const sourceKey = (element) => {
        if (element?.osm_type && element?.osm_id !== null && element?.osm_id !== undefined) {
            return `osm:${element.osm_type}:${element.osm_id}`;
        }

        if (element?.place_id !== null && element?.place_id !== undefined) {
            return `place:${element.place_id}`;
        }

        const latitude = Number(element?.coordinates?.latitude);
        const longitude = Number(element?.coordinates?.longitude);

        return Number.isFinite(latitude) && Number.isFinite(longitude)
            ? `coordinates:${latitude.toFixed(6)}:${longitude.toFixed(6)}`
            : '';
    };

    const notify = () => {
        document.dispatchEvent(new CustomEvent('travel-manager:favourites-changed', {
            detail: { favourites: favourites.map((item) => ({ ...item })) }
        }));
    };

    const notifyTags = () => {
        document.dispatchEvent(new CustomEvent('travel-manager:favourite-tags-changed', {
            detail: { tags: tags.map((item) => ({ ...item })) }
        }));
    };

    const enrichFavourite = (favourite) => {
        const tag = favourite?.tag || tags.find((item) => item.id === favourite?.tag_id) || null;

        return {
            ...favourite,
            tag
        };
    };

    const enrichFavourites = () => {
        favourites = favourites.map(enrichFavourite);
    };

    const load = async (force = false) => {
        if (loaded && !force) {
            return favourites;
        }

        const response = await fetch('/api/favourites', {
            headers: { 'Accept': 'application/json' }
        });

        if (!response.ok) {
            throw new Error('Nie udało się wczytać ulubionych miejsc.');
        }

        favourites = (await response.json()).favourites || [];
        if (tagsLoaded) {
            enrichFavourites();
        }
        loaded = true;
        notify();
        return favourites;
    };

    const loadTags = async (force = false) => {
        if (tagsLoaded && !force) {
            return tags;
        }

        const response = await fetch('/api/favourite-tags', {
            headers: { 'Accept': 'application/json' }
        });

        if (!response.ok) {
            throw new Error('Nie udało się wczytać tagów ulubionych.');
        }

        tags = (await response.json()).tags || [];
        tagsLoaded = true;
        enrichFavourites();
        notifyTags();
        notify();
        return tags;
    };

    const findByElement = (element) => {
        const key = sourceKey(element);
        return favourites.find((item) => item.source_key === key) || null;
    };

    const save = async ({ favourite = null, element, name, tagId, icon = null }) => {
        const latitude = Number(element?.coordinates?.latitude);
        const longitude = Number(element?.coordinates?.longitude);
        const payload = {
            id: favourite?.id || null,
            source_key: sourceKey(element),
            name,
            tag_id: tagId,
            icon: icon || null,
            latitude,
            longitude,
            place_data: element
        };
        const response = await fetch('/api/favourites', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data?.message || 'Nie udało się zapisać ulubionego miejsca.');
        }

        const saved = data.favourite;
        favourites = favourites.filter((item) => (
            item.id !== saved.id && item.source_key !== saved.source_key
        ));
        favourites.push(enrichFavourite(saved));
        loaded = true;
        notify();
        return enrichFavourite(saved);
    };

    const saveTag = async ({ tag = null, name, icon }) => {
        const payload = {
            id: tag?.id || null,
            name,
            icon
        };
        const response = await fetch('/api/favourite-tags', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data?.message || 'Nie udało się zapisać tagu.');
        }

        const saved = data.tag;
        tags = tags.filter((item) => item.id !== saved.id);
        tags.push(saved);
        tagsLoaded = true;
        notifyTags();
        await load(true);
        return saved;
    };

    const remove = async (favouriteId) => {
        const response = await fetch(`/api/favourites/${encodeURIComponent(favouriteId)}`, {
            method: 'DELETE',
            headers: { 'Accept': 'application/json' }
        });

        if (!response.ok) {
            throw new Error('Nie udało się usunąć ulubionego miejsca.');
        }

        favourites = favourites.filter((item) => item.id !== favouriteId);
        notify();
    };

    const removeTag = async (tagId) => {
        const response = await fetch(`/api/favourite-tags/${encodeURIComponent(tagId)}`, {
            method: 'DELETE',
            headers: { 'Accept': 'application/json' }
        });

        if (!response.ok) {
            throw new Error('Nie udało się usunąć tagu.');
        }

        tags = tags.filter((item) => item.id !== tagId);
        notifyTags();
        await load(true);
    };

    window.travelManagerFavourites = {
        findByElement,
        list: load,
        listTags: loadTags,
        remove,
        removeTag,
        save,
        saveTag,
        sourceKey
    };

    Promise.all([load(), loadTags()]).catch(() => {});
});
