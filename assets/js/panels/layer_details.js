document.addEventListener('travel-manager:views-ready', () => {
    const panel = document.querySelector('#layer-details-panel');
    const closeButton = document.querySelector('[data-layer-details-panel-close]');
    const grabber = document.querySelector('[data-layer-details-panel-grabber]');
    const baseLayerInputs = Array.from(document.querySelectorAll('[data-base-layer]'));
    const overlayInputs = Array.from(document.querySelectorAll('[data-layer-toggle]'));
    const favouriteTagsList = document.querySelector('#layer-details-favourite-tags');

    if (!panel || !closeButton || !baseLayerInputs.length || !overlayInputs.length) {
        return;
    }

    let tags = [];
    let selectedFavouriteTagIds = null;

    const favouritesToggle = overlayInputs.find((input) => input.dataset.layerToggle === 'layer_favourites_enabled');

    const getLayerState = () => overlayInputs.reduce((state, input) => ({
        ...state,
        [input.dataset.layerToggle]: input.checked
    }), {
        layer_favourite_visible_tag_ids: selectedFavouriteTagIds,
        map_base_layer: baseLayerInputs.find((input) => input.checked)?.dataset.baseLayer || 'standard'
    });

    const getSelectedTagIds = () => {
        const inputs = Array.from(favouriteTagsList?.querySelectorAll('[data-favourite-layer-tag]') || []);
        return inputs
            .filter((input) => input.checked)
            .map((input) => input.value);
    };

    const updateFavouriteTagsAvailability = () => {
        const enabled = favouritesToggle?.checked !== false;
        const options = Array.from(favouriteTagsList?.querySelectorAll('.layer-details-panel__option') || []);

        options.forEach((option) => {
            option.classList.toggle('layer-details-panel__option--disabled', !enabled);
        });

        Array.from(favouriteTagsList?.querySelectorAll('[data-favourite-layer-tag]') || []).forEach((input) => {
            input.disabled = !enabled;
        });
    };

    const renderFavouriteTags = () => {
        if (!favouriteTagsList) {
            return;
        }

        favouriteTagsList.replaceChildren();

        if (!tags.length) {
            const empty = document.createElement('p');
            empty.className = 'layer-details-panel__empty';
            empty.textContent = 'Brak zdefiniowanych tagów.';
            favouriteTagsList.append(empty);
            return;
        }

        const selected = Array.isArray(selectedFavouriteTagIds)
            ? new Set(selectedFavouriteTagIds)
            : null;

        tags.forEach((tag) => {
            const label = document.createElement('label');
            label.className = 'layer-details-panel__option layer-details-panel__tag-option';

            const input = document.createElement('input');
            input.type = 'checkbox';
            input.value = tag.id;
            input.dataset.favouriteLayerTag = 'true';
            input.checked = selected ? selected.has(tag.id) : true;

            const text = document.createElement('span');
            const title = document.createElement('strong');
            const subtitle = document.createElement('small');

            title.textContent = `${tag.icon || '⭐'} ${tag.name}`;
            subtitle.textContent = 'Tag ulubionych miejsc';
            text.append(title, subtitle);
            label.append(input, text);
            favouriteTagsList.append(label);

            input.addEventListener('change', () => {
                selectedFavouriteTagIds = getSelectedTagIds();
                const state = getLayerState();
                patchUiSettings(state);
                document.dispatchEvent(new CustomEvent('travel-manager:layers-changed', {
                    detail: state
                }));
            });
        });

        updateFavouriteTagsAvailability();
    };

    const applyLayerState = (state) => {
        baseLayerInputs.forEach((input) => {
            input.checked = input.dataset.baseLayer === (state.map_base_layer || 'standard');
        });

        overlayInputs.forEach((input) => {
            if (input.dataset.layerToggle in state) {
                input.checked = Boolean(state[input.dataset.layerToggle]);
            }
        });

        if ('layer_favourite_visible_tag_ids' in state) {
            selectedFavouriteTagIds = Array.isArray(state.layer_favourite_visible_tag_ids)
                ? state.layer_favourite_visible_tag_ids.map((item) => String(item))
                : null;
            renderFavouriteTags();
        }

        updateFavouriteTagsAvailability();
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
            const ui = data?.ui || {};
            const width = Number(ui.layer_details_panel_width);

            if (Number.isFinite(width) && width > 0) {
                panel.style.setProperty('--layer-details-panel-width', `${width}px`);
            }

            applyLayerState(ui);
            document.dispatchEvent(new CustomEvent('travel-manager:layers-changed', {
                detail: getLayerState()
            }));
        } catch (error) {
            // Default unchecked layer state remains valid when settings are unavailable.
        }
    };

    const open = () => {
        panel.classList.add('layer-details-panel--open');
        panel.setAttribute('aria-hidden', 'false');
        window.travelManagerLegendDetailsPanel?.close();
    };

    const close = () => {
        panel.classList.remove('layer-details-panel--open');
        panel.setAttribute('aria-hidden', 'true');
    };

    baseLayerInputs.forEach((input) => {
        input.addEventListener('change', () => {
            if (!input.checked || input.disabled) {
                return;
            }

            const state = getLayerState();
            patchUiSettings(state);
            document.dispatchEvent(new CustomEvent('travel-manager:layers-changed', {
                detail: state
            }));
        });
    });

    overlayInputs.forEach((input) => {
        input.addEventListener('change', () => {
            if (input === favouritesToggle) {
                updateFavouriteTagsAvailability();
            }

            const state = getLayerState();
            patchUiSettings(state);
            document.dispatchEvent(new CustomEvent('travel-manager:layers-changed', {
                detail: state
            }));
        });
    });

    closeButton.addEventListener('click', close);

    const resize = {
        startX: 0,
        startWidth: 0
    };

    const getPanelBounds = () => {
        const computed = window.getComputedStyle(panel);

        return {
            min: Number.parseFloat(computed.minWidth) || 260,
            max: Number.parseFloat(computed.maxWidth) || 520
        };
    };

    const onPointerMove = (event) => {
        const bounds = getPanelBounds();
        const nextWidth = resize.startWidth + resize.startX - event.clientX;
        const width = Math.min(Math.max(nextWidth, bounds.min), bounds.max);

        panel.style.setProperty('--layer-details-panel-width', `${width}px`);
    };

    const stopResize = () => {
        panel.classList.remove('layer-details-panel--resizing');
        document.removeEventListener('pointermove', onPointerMove);
        document.removeEventListener('pointerup', stopResize);
        patchUiSettings({
            layer_details_panel_width: Math.round(panel.getBoundingClientRect().width)
        });
    };

    if (grabber) {
        grabber.addEventListener('pointerdown', (event) => {
            event.preventDefault();

            resize.startX = event.clientX;
            resize.startWidth = panel.getBoundingClientRect().width;

            panel.classList.add('layer-details-panel--resizing');
            document.addEventListener('pointermove', onPointerMove);
            document.addEventListener('pointerup', stopResize);
        });
    }

    document.addEventListener('travel-manager:favourite-tags-changed', (event) => {
        tags = event.detail?.tags || [];
        renderFavouriteTags();
    });

    loadUiSettings();
    window.travelManagerFavourites?.listTags().then((items) => {
        tags = items;
        renderFavouriteTags();
    }).catch(() => renderFavouriteTags());

    window.travelManagerLayerDetailsPanel = {
        close,
        open
    };
});
