document.addEventListener('travel-manager:views-ready', () => {
    const t = window.i18n.t;
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#favourites-tag-editor');
    const title = document.querySelector('#favourites-tag-editor-title');
    const nameInput = document.querySelector('#favourites-tag-editor-name');
    const iconInput = document.querySelector('#favourites-tag-editor-icon');
    const selectedIcon = document.querySelector('#favourites-tag-editor-selected-icon');
    const selectedName = document.querySelector('#favourites-tag-editor-selected-name');
    const searchInput = document.querySelector('#favourites-tag-editor-emoji-search');
    const tabs = document.querySelector('#favourites-tag-editor-tabs');
    const presets = document.querySelector('#favourites-tag-editor-presets');
    const genderField = document.querySelector('#favourites-tag-editor-gender-field');
    const genderSelect = document.querySelector('#favourites-tag-editor-gender');
    const skinToneField = document.querySelector('#favourites-tag-editor-skin-tone-field');
    const skinToneSelect = document.querySelector('#favourites-tag-editor-skin-tone');
    const modifiers = document.querySelector('#favourites-tag-editor-modifiers');
    const cancelButtons = dialog?.querySelectorAll('[data-favourites-tag-editor-cancel]');
    let resolveResult = null;
    const state = {
        groups: [],
        items: [],
        recent: [],
        activeGroup: null,
        selectedBaseEmoji: '⭐',
        selectedName: t('COMMON.DEFAULT'),
        selectedSupportsGender: false,
        selectedSupportsSkinTone: false
    };

    if (
        !layer
        || !dialog
        || !title
        || !nameInput
        || !iconInput
        || !selectedIcon
        || !selectedName
        || !searchInput
        || !tabs
        || !presets
        || !genderField
        || !genderSelect
        || !skinToneField
        || !skinToneSelect
        || !modifiers
        || !cancelButtons?.length
    ) {
        return;
    }

    const skinToneModifiers = ['🏻', '🏼', '🏽', '🏾', '🏿'];
    const genderVariants = {
        female: '♀️',
        male: '♂️'
    };
    const recentGroupKey = '__recent__';
    const recentStorageKey = 'travel-manager.recent-emojis';

    const readRecent = () => {
        try {
            const value = JSON.parse(window.localStorage.getItem(recentStorageKey) || '[]');
            return Array.isArray(value) ? value.slice(0, 24) : [];
        } catch (error) {
            return [];
        }
    };

    const writeRecent = () => {
        try {
            window.localStorage.setItem(recentStorageKey, JSON.stringify(state.recent));
        } catch (error) {
            // The picker remains usable when browser storage is unavailable.
        }
    };

    const emojiLabel = (item) => {
        let member = String(item.key || '').toLocaleUpperCase().replace(/[^A-Z0-9]+/g, '_');
        if (/^[0-9]/.test(member)) {
            member = `NUMBER_${member}`;
        }
        const key = `RES_EMOJI.${member}`;
        const translated = t(key);
        return translated === key ? item.label || item.name || item.emoji || '' : translated;
    };

    const stripSkinTone = (emoji) => skinToneModifiers.reduce((value, modifier) => (
        value.replaceAll(modifier, '')
    ), emoji);

    const stripGender = (emoji) => emoji
        .replaceAll('‍♀️', '')
        .replaceAll('‍♂️', '')
        .replaceAll('♀️', '')
        .replaceAll('♂️', '');

    const insertSkinTone = (emoji, skinTone) => {
        if (!skinTone) {
            return emoji;
        }

        const chars = [...emoji];
        const variationIndex = chars.findIndex((char) => char === '️');
        const index = variationIndex >= 0 ? variationIndex : 1;
        chars.splice(index, 0, skinTone);

        return chars.join('');
    };

    const applyModifiers = () => {
        let emoji = stripGender(stripSkinTone(state.selectedBaseEmoji));
        const gender = genderSelect.value;

        if (state.selectedSupportsSkinTone) {
            emoji = insertSkinTone(emoji, skinToneSelect.value);
        }

        if (state.selectedSupportsGender && genderVariants[gender]) {
            emoji = `${emoji}‍${genderVariants[gender]}`;
        }

        iconInput.value = emoji;
        selectedIcon.textContent = emoji;
    };

    const updateSelectedEmoji = ({
        emoji,
        name,
        support_sex: supportSex,
        support_color: supportColor,
        supports_gender: supportsGender,
        supports_skin_tone: supportsSkinTone
    }) => {
        state.selectedBaseEmoji = emoji || '⭐';
        state.selectedName = name || t('COMMON.DEFAULT');
        state.selectedSupportsGender = Boolean(supportSex ?? supportsGender);
        state.selectedSupportsSkinTone = Boolean(supportColor ?? supportsSkinTone);
        selectedName.textContent = state.selectedName;
        genderSelect.disabled = !state.selectedSupportsGender;
        skinToneSelect.disabled = !state.selectedSupportsSkinTone;
        genderField.hidden = genderSelect.disabled;
        skinToneField.hidden = skinToneSelect.disabled;
        modifiers.hidden = genderSelect.disabled && skinToneSelect.disabled;
        modifiers.setAttribute('aria-hidden', String(modifiers.hidden));

        if (!state.selectedSupportsGender) {
            genderSelect.value = '';
        }

        if (!state.selectedSupportsSkinTone) {
            skinToneSelect.value = '';
        }

        applyModifiers();
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
        const groups = state.recent.length
            ? [{ key: recentGroupKey, label: t('EMOJI_PICKER.RECENT'), emoji: '🕘' }, ...state.groups]
            : state.groups;
        groups.forEach((group) => {
            const button = document.createElement('button');
            const active = group.key === state.activeGroup;
            button.className = 'favourites-tag-editor__tab';
            button.classList.toggle('favourites-tag-editor__tab--active', active);
            button.type = 'button';
            button.setAttribute('role', 'tab');
            button.setAttribute('aria-selected', String(active));
            button.textContent = [group.emoji, group.label || group.name].filter(Boolean).join(' ');
            button.addEventListener('click', () => loadGroup(group.key));
            tabs.append(button);
        });
    };

    const renderPresets = (items = state.items) => {
        presets.replaceChildren();
        const query = searchInput.value.trim().toLocaleLowerCase();
        const visibleItems = query
            ? items.filter((item) => (
                emojiLabel(item).toLocaleLowerCase().includes(query)
            ))
            : items;

        if (!visibleItems.length) {
            const empty = document.createElement('p');
            empty.className = 'favourites-tag-editor__empty';
            empty.textContent = query
                ? t('EMOJI_PICKER.NO_RESULTS')
                : state.activeGroup === recentGroupKey
                    ? t('EMOJI_PICKER.NO_RECENT')
                    : t('EMOJI_PICKER.NO_EMOJI_IN_CATEGORY');
            presets.append(empty);
            return;
        }

        visibleItems.forEach((item) => {
            const label = emojiLabel(item);
            const button = document.createElement('button');
            button.className = 'favourites-tag-editor__preset';
            button.type = 'button';
            button.title = label;
            button.setAttribute('aria-label', label);
            button.textContent = item.emoji;
            button.addEventListener('click', () => {
                const recentItem = {
                    key: item.key,
                    emoji: item.emoji,
                    support_color: item.support_color,
                    support_sex: item.support_sex,
                    supports_skin_tone: item.supports_skin_tone,
                    supports_gender: item.supports_gender
                };
                state.recent = [recentItem, ...state.recent.filter((recent) => recent.key !== item.key)]
                    .slice(0, 24);
                writeRecent();
                renderTabs();
                updateSelectedEmoji({
                    ...item,
                    name: label
                });
            });
            presets.append(button);
        });
    };

    const loadGroup = async (groupKey) => {
        state.activeGroup = groupKey;
        renderTabs();
        if (groupKey === recentGroupKey) {
            state.items = state.recent;
            renderPresets();
            return;
        }
        presets.textContent = t('EMOJI_PICKER.LOADING');
        const data = await fetchJson(`/api/emojis?group=${encodeURIComponent(groupKey)}`);
        state.items = data.emojis || [];
        renderPresets();
    };

    const loadGroups = async () => {
        if (state.groups.length) {
            return;
        }

        const data = await fetchJson('/api/emojis/groups');
        state.groups = data.groups || [];
        state.recent = readRecent();
        state.activeGroup = state.recent.length ? recentGroupKey : state.groups[0]?.key || null;
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

    const show = async ({ name = '', icon = '⭐', editing = false } = {}) => {
        if (resolveResult) {
            resolveResult(null);
        }

        title.textContent = editing
            ? t('FAVOURITE_TAG_EDITOR.EDIT_TITLE')
            : t('FAVOURITE_TAG_EDITOR.ADD_TITLE');
        nameInput.value = name;
        searchInput.value = '';
        updateSelectedEmoji({
            emoji: icon || '⭐',
            name: t('FAVOURITE_TAG_EDITOR.CURRENT_ICON'),
            supports_gender: false,
            supports_skin_tone: false
        });
        try {
            await loadGroups();
        } catch (error) {
            presets.textContent = t('EMOJI_PICKER.LOAD_FAILED');
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
        const icon = iconInput.value.trim() || '⭐';

        if (name) {
            finish({ name, icon });
        }
    });
    genderSelect.addEventListener('change', applyModifiers);
    skinToneSelect.addEventListener('change', applyModifiers);
    searchInput.addEventListener('input', () => renderPresets());
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

    window.travelManagerFavouritesTagEditor = { show };
});
