document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#favourites-editor');
    const title = document.querySelector('#favourites-editor-title');
    const nameInput = document.querySelector('#favourites-editor-name');
    const tagSelect = document.querySelector('#favourites-editor-tag');
    const iconInput = document.querySelector('#favourites-editor-icon');
    const selectedIcon = document.querySelector('#favourites-editor-selected-icon');
    const selectedName = document.querySelector('#favourites-editor-selected-name');
    const toggleIconsButton = document.querySelector('#favourites-editor-toggle-icons');
    const removeIconButton = document.querySelector('#favourites-editor-remove-icon');
    const emojiPicker = document.querySelector('#favourites-editor-emoji-picker');
    const tabs = document.querySelector('#favourites-editor-tabs');
    const presets = document.querySelector('#favourites-editor-presets');
    const cancelButtons = dialog?.querySelectorAll('[data-favourites-editor-cancel]');
    let resolveResult = null;
    const state = {
        groups: [],
        activeGroup: null
    };

    if (
        !layer
        || !dialog
        || !title
        || !nameInput
        || !tagSelect
        || !iconInput
        || !selectedIcon
        || !selectedName
        || !toggleIconsButton
        || !removeIconButton
        || !emojiPicker
        || !tabs
        || !presets
        || !cancelButtons?.length
    ) {
        return;
    }

    const renderTags = (tags, selectedTagId) => {
        tagSelect.replaceChildren();

        (tags || []).forEach((tag) => {
            const option = document.createElement('option');
            option.value = tag.id;
            option.textContent = `${tag.icon || '⭐'} ${tag.name}`;
            tagSelect.append(option);
        });

        if (selectedTagId && [...tagSelect.options].some((option) => option.value === selectedTagId)) {
            tagSelect.value = selectedTagId;
        } else if (tagSelect.options.length) {
            tagSelect.selectedIndex = 0;
        }
    };

    const setIcon = (icon, label = '') => {
        const value = icon || '';
        iconInput.value = value;
        selectedIcon.textContent = value || '-';
        selectedName.textContent = value ? (label || 'Własna ikona miejsca') : 'Brak własnej ikony';
        removeIconButton.hidden = !value;
    };

    const setEmojiPickerOpen = (open) => {
        emojiPicker.hidden = !open;
        toggleIconsButton.textContent = open ? 'Ukryj ikony' : 'Wybierz ikonę';
    };

    const fetchJson = async (url) => {
        const response = await fetch(url, {
            cache: 'no-store',
            headers: { 'Accept': 'application/json' }
        });

        if (!response.ok) {
            throw new Error(`Emoji request failed: ${response.status}`);
        }

        return response.json();
    };

    const renderTabs = () => {
        tabs.replaceChildren();
        state.groups.forEach((group) => {
            const button = document.createElement('button');
            const active = group.key === state.activeGroup;
            button.className = 'favourites-editor__tab';
            button.classList.toggle('favourites-editor__tab--active', active);
            button.type = 'button';
            button.setAttribute('role', 'tab');
            button.setAttribute('aria-selected', String(active));
            button.textContent = [group.emoji, group.label || group.name].filter(Boolean).join(' ');
            button.addEventListener('click', () => loadGroup(group.key));
            tabs.append(button);
        });
    };

    const renderPresets = (items) => {
        presets.replaceChildren();

        if (!items.length) {
            const empty = document.createElement('p');
            empty.className = 'favourites-editor__empty';
            empty.textContent = 'Brak emoji w tej kategorii.';
            presets.append(empty);
            return;
        }

        items.forEach((item) => {
            const label = item.label || item.name || item.emoji || '';
            const button = document.createElement('button');
            button.className = 'favourites-editor__preset';
            button.type = 'button';
            button.title = label;
            button.setAttribute('aria-label', label);
            button.textContent = item.emoji;
            button.addEventListener('click', () => {
                setIcon(item.emoji, label);
                setEmojiPickerOpen(false);
            });
            presets.append(button);
        });
    };

    const loadGroup = async (groupKey) => {
        state.activeGroup = groupKey;
        renderTabs();
        presets.textContent = 'Ładowanie...';
        const data = await fetchJson(`/api/emojis?group=${encodeURIComponent(groupKey)}`);
        renderPresets(data.emojis || []);
    };

    const loadGroups = async () => {
        if (state.groups.length) {
            return;
        }

        const data = await fetchJson('/api/emojis/groups');
        state.groups = data.groups || [];
        state.activeGroup = state.groups[0]?.key || null;
        renderTabs();

        if (state.activeGroup) {
            await loadGroup(state.activeGroup);
        }
    };

    const finish = (result) => {
        dialog.setAttribute('aria-hidden', 'true');
        layer.classList.remove('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'true');
        const resolve = resolveResult;
        resolveResult = null;
        resolve?.(result);
    };

    const show = async ({ name = '', tagId = '', icon = null, editing = false } = {}) => {
        if (resolveResult) {
            resolveResult(null);
        }

        title.textContent = editing ? 'Edytuj ulubione miejsce' : 'Dodaj do ulubionych';
        nameInput.value = name;
        setIcon(icon || null, icon ? 'Aktualnie wybrana ikona' : '');
        setEmojiPickerOpen(false);
        try {
            renderTags(await window.travelManagerFavourites?.listTags(), tagId);
        } catch (error) {
            renderTags([], tagId);
        }
        dialog.setAttribute('aria-hidden', 'false');
        layer.classList.add('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'false');

        return new Promise((resolve) => {
            resolveResult = resolve;
            window.requestAnimationFrame(() => {
                nameInput.focus();
                nameInput.select();
            });
        });
    };

    dialog.addEventListener('submit', (event) => {
        event.preventDefault();
        const name = nameInput.value.trim();
        const tagId = tagSelect.value;
        const icon = iconInput.value.trim() || null;

        if (name && tagId) {
            finish({ name, tagId, icon });
        }
    });
    toggleIconsButton.addEventListener('click', async () => {
        const shouldOpen = emojiPicker.hidden;
        setEmojiPickerOpen(shouldOpen);

        if (shouldOpen) {
            try {
                await loadGroups();
            } catch (error) {
                presets.textContent = 'Nie udało się wczytać emoji.';
            }
        }
    });
    removeIconButton.addEventListener('click', () => {
        setIcon(null);
        setEmojiPickerOpen(false);
    });
    cancelButtons.forEach((button) => button.addEventListener('click', () => finish(null)));
    layer.addEventListener('click', (event) => {
        if (event.target === layer && resolveResult) {
            finish(null);
        }
    });
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && resolveResult) {
            finish(null);
        }
    });

    window.travelManagerFavouritesEditor = { show };
});
