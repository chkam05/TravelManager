document.addEventListener('travel-manager:views-ready', () => {
    const t = window.i18n.t,
        locale = window.i18n.locale.replace('_', '-');
    const form = document.querySelector('#layers-search'),
        input = document.querySelector('#layers-search-input'),
        sortButton = document.querySelector('#layers-sort-button'),
        sortMenu = document.querySelector('#layers-sort-menu'),
        list = document.querySelector('[data-layers-list]');
    if (!form || !input || !sortButton || !sortMenu || !list) return;
    const state = {
        layers: [],
        query: '',
        sortDirection: 'asc',
        error: false,
        requestId: 0,
    };
    const name = (layer) =>
        layer.name || t('LAYER_EDITOR.NEW_LAYER', { number: '' });
    const filtered = () => {
        const query = state.query.trim().toLocaleLowerCase(locale);
        const items = query
            ? state.layers.filter((layer) =>
                  name(layer).toLocaleLowerCase(locale).includes(query)
              )
            : [...state.layers];
        return items.sort((a, b) => {
            const result = name(a).localeCompare(name(b), locale, {
                sensitivity: 'base',
            });
            return state.sortDirection === 'asc' ? result : -result;
        });
    };
    const setSortOpen = (open) => {
        sortMenu.setAttribute('aria-hidden', String(!open));
        sortButton.setAttribute('aria-expanded', String(open));
    };
    const refresh = async () => {
        const requestId = ++state.requestId;
        try {
            const layers = await window.travelManagerCustomLayers.list();
            if (requestId !== state.requestId) return;
            state.layers = layers;
            state.error = false;
        } catch (error) {
            if (requestId !== state.requestId) return;
            state.error = true;
        }
        render();
    };
    const edit = (layer, duplicate = false) => {
        window.travelManagerNavigation?.showView('map') ||
            document.querySelector('[data-navigation-view="map"]')?.click();
        if (duplicate) return window.travelManagerLayerEditor.duplicate(layer);
        return window.travelManagerLayerEditor.open(layer);
    };
    const transferError = () =>
        window.travelManagerAlert?.(t('LAYER_EDITOR.TRANSFER_FAILED'), 'error');
    const importFile = async (file) => {
        const parsed = await window.travelManagerLayerApi.request(
            '/api/custom-layers/parse',
            {
                method: 'POST',
                body: JSON.stringify(file),
            }
        );
        if (
            !(await window.travelManagerDialogs.yesNo({
                title: t('LAYER_EDITOR.IMPORT_ONE'),
                description: t('LAYER_EDITOR.IMPORT_PREVIEW', {
                    name: parsed.layer.name,
                    count: parsed.layer.elements.length,
                }),
            }))
        )
            return;
        await window.travelManagerCustomLayers.save(parsed.layer);
    };
    const exportFile = async (layer, format) => {
        try {
            const data = await window.travelManagerLayerApi.request(
                `/api/custom-layers/${encodeURIComponent(layer.id)}/export/${format}`
            );
            if (window.pywebview?.api?.save_layer_file) {
                const result = await window.pywebview.api.save_layer_file(
                    data.text,
                    data.filename
                );
                if (!['saved', 'cancelled'].includes(result?.status))
                    throw Error('Save failed');
                return;
            }
            const url = URL.createObjectURL(
                new Blob([data.text], {
                    type:
                        format === 'gpx'
                            ? 'application/gpx+xml'
                            : 'application/json',
                })
            );
            const link = document.createElement('a');
            link.href = url;
            link.download = data.filename;
            document.body.append(link);
            link.click();
            link.remove();
            window.setTimeout(() => URL.revokeObjectURL(url), 1000);
        } catch {
            transferError();
        }
    };
    const importButton = document.querySelector('[data-layer-import]');
    if (importButton)
        importButton.onclick = async () => {
            importButton.disabled = true;
            try {
                if (window.pywebview?.api?.read_layer_file) {
                    const file = await window.pywebview.api.read_layer_file();
                    if (file?.status === 'cancelled') return;
                    if (file?.status !== 'ok') throw Error('Read failed');
                    await importFile(file);
                } else {
                    const input = document.createElement('input');
                    input.type = 'file';
                    input.accept = '.json,.geojson,.gpx';
                    input.onchange = async () => {
                        const file = input.files?.[0];
                        if (!file) return;
                        importButton.disabled = true;
                        try {
                            if (file.size > 10 * 1024 * 1024)
                                throw Error('Too large');
                            await importFile({
                                text: await file.text(),
                                filename: file.name,
                            });
                        } catch {
                            transferError();
                        } finally {
                            importButton.disabled = false;
                        }
                    };
                    input.click();
                }
            } catch {
                transferError();
            } finally {
                importButton.disabled = false;
            }
        };
    const rename = async (layer) => {
        const value = await window.travelManagerLayerNameEditor?.show({
            name: name(layer),
            icon: layer.icon || '',
            showTitle: layer.show_title === true,
        });
        if (!value) return;
        await window.travelManagerCustomLayers.save({
            ...layer,
            name: value.name,
            icon: value.icon,
            show_title: value.showTitle,
        });
    };
    const remove = async (layer) => {
        if (
            await window.travelManagerDialogs.yesNo({
                title: t('LAYER_EDITOR.DELETE_TITLE'),
                description: t('LAYER_EDITOR.DELETE_TEXT'),
            })
        ) {
            await window.travelManagerCustomLayers.delete(layer.id);
        }
    };
    const action = (label, icon, handler, danger = false) => {
        const button = document.createElement('button');
        button.className = `layers-view__action${danger ? ' layers-view__action--danger' : ''}`;
        button.type = 'button';
        button.innerHTML = `<i data-lucide="${icon}" aria-hidden="true"></i><span>${label}</span>`;
        button.onclick = handler;
        return button;
    };
    let openedMenu = null,
        menuTrigger = null;
    const closeMenu = (focus = false) => {
        openedMenu?.remove();
        openedMenu = null;
        menuTrigger?.setAttribute('aria-expanded', 'false');
        if (focus) menuTrigger?.focus();
        menuTrigger = null;
    };
    const showLayer = async (layer) => {
        if ((await window.travelManagerLayerEditor?.close()) === false) return;
        window.travelManagerNavigation?.showView('map');
        let stored = {};
        try {
            stored =
                JSON.parse(
                    localStorage.getItem(
                        'travel-manager-custom-layer-visibility'
                    ) || '{}'
                ) || {};
        } catch {}
        const visibility = Object.fromEntries(
            state.layers.map((item) => [item.id, stored[item.id] !== false])
        );
        visibility[layer.id] = true;
        localStorage.setItem(
            'travel-manager-custom-layer-visibility',
            JSON.stringify(visibility)
        );
        document.dispatchEvent(
            new CustomEvent('travel-manager:custom-layer-visibility-changed', {
                detail: {
                    ids: Object.keys(visibility).filter((id) => visibility[id]),
                },
            })
        );
        window.travelManagerLayerRenderer.fit(
            window.travelManagerMap.map,
            layer.elements
        );
    };
    const exportDialog = async (layer) => {
        const format = await window.travelManagerDialogs.choose({
            title: t('LAYER_EDITOR.EXPORT_ONE'),
            description: t('LAYER_EDITOR.EXPORT_FORMAT'),
            yesLabel: t('LAYER_EDITOR.EXPORT_ONE'),
            noLabel: t('COMMON.CANCEL'),
            choices: [
                ['json', 'TravelManager JSON'],
                ['geojson', 'GeoJSON'],
                ['gpx', 'GPX'],
            ],
        });
        if (format) await exportFile(layer, format);
    };
    const showMenu = (layer, trigger) => {
        const wasOpen = menuTrigger === trigger;
        closeMenu();
        if (wasOpen) return;
        menuTrigger = trigger;
        trigger.setAttribute('aria-expanded', 'true');
        const menu = document.createElement('div');
        menu.className = 'layers-view__context-menu';
        menu.setAttribute('role', 'menu');
        const items = [
            [t('LAYER_EDITOR.DUPLICATE'), 'copy', () => edit(layer, true)],
            [t('COMMON.EDIT'), 'square-pen', () => edit(layer)],
            [t('LAYER_EDITOR.RENAME'), 'pencil', () => rename(layer)],
            null,
            [
                t('LAYER_EDITOR.EXPORT_ONE'),
                'download',
                () => exportDialog(layer),
            ],
            null,
            [t('COMMON.DELETE'), 'trash-2', () => remove(layer), true],
        ];
        items.forEach((item) => {
            if (!item) {
                const separator = document.createElement('div');
                separator.className = 'layer-menu-separator';
                separator.setAttribute('role', 'separator');
                menu.append(separator);
                return;
            }
            const button = action(
                item[0],
                item[1],
                async () => {
                    closeMenu(true);
                    try {
                        await item[2]();
                    } catch {
                        transferError();
                    }
                },
                item[3]
            );
            button.setAttribute('role', 'menuitem');
            menu.append(button);
        });
        document.body.append(menu);
        openedMenu = menu;
        const rect = trigger.getBoundingClientRect();
        menu.style.left = `${Math.max(8, Math.min(rect.right - menu.getBoundingClientRect().width, window.innerWidth - menu.getBoundingClientRect().width - 8))}px`;
        menu.style.top = `${Math.max(8, Math.min(rect.bottom + 5, window.innerHeight - menu.getBoundingClientRect().height - 8))}px`;
        menu.querySelector('button')?.focus();
        window.lucide?.createIcons();
    };
    document.addEventListener('click', (event) => {
        if (
            openedMenu &&
            !openedMenu.contains(event.target) &&
            !menuTrigger?.contains(event.target)
        )
            closeMenu();
    });
    document.addEventListener('keydown', (event) => {
        if (!openedMenu) return;
        if (event.key === 'Escape') {
            event.preventDefault();
            closeMenu(true);
        } else if (
            ['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)
        ) {
            event.preventDefault();
            const buttons = Array.from(openedMenu.querySelectorAll('button'));
            const current = buttons.indexOf(document.activeElement);
            buttons[
                event.key === 'Home'
                    ? 0
                    : event.key === 'End'
                      ? buttons.length - 1
                      : (current +
                            (event.key === 'ArrowDown' ? 1 : -1) +
                            buttons.length) %
                        buttons.length
            ]?.focus();
        }
    });
    window.addEventListener('resize', () => closeMenu());
    list.addEventListener('scroll', () => closeMenu());
    function render() {
        closeMenu();
        list.replaceChildren();
        if (state.error) {
            const message = document.createElement('p');
            message.setAttribute('role', 'alert');
            message.textContent = t('LAYER_EDITOR.LOAD_FAILED');
            list.append(
                message,
                action(t('LAYER_EDITOR.RETRY'), 'refresh-cw', () =>
                    window.travelManagerCustomLayers.refresh().catch(() => {})
                )
            );
            return;
        }
        const items = filtered();
        if (!items.length) {
            const empty = document.createElement('p');
            empty.className = 'layers-view__empty';
            empty.textContent = state.query
                ? t('LAYERS_VIEW.NO_RESULTS')
                : t('LAYERS_VIEW.EMPTY');
            list.append(empty);
            return;
        }
        items.forEach((layer) => {
            const row = document.createElement('article');
            row.className = 'layers-view__item';
            const icon = document.createElement('div');
            icon.className = 'layers-view__icon';
            if (layer.icon) icon.textContent = layer.icon;
            else
                icon.innerHTML =
                    '<i data-lucide="layers" aria-hidden="true"></i>';
            const copy = document.createElement('div');
            copy.className = 'layers-view__copy';
            const title = document.createElement('div');
            title.className = 'layers-view__name';
            title.textContent = name(layer);
            title.title = name(layer);
            const count = document.createElement('div');
            count.className = 'layers-view__count';
            count.textContent = t('LAYERS_VIEW.ELEMENT_COUNT', {
                count: (layer.elements || []).length,
            });
            copy.append(title, count);
            const more = action(
                t('LAYER_EDITOR.MORE_ACTIONS'),
                'ellipsis',
                () => showMenu(layer, more)
            );
            more.innerHTML =
                '<i data-lucide="ellipsis" aria-hidden="true"></i>';
            more.setAttribute('aria-label', t('LAYER_EDITOR.MORE_ACTIONS'));
            more.setAttribute('aria-haspopup', 'menu');
            more.setAttribute('aria-expanded', 'false');
            row.append(
                icon,
                copy,
                action(t('LAYER_EDITOR.SHOW_ON_MAP'), 'scan', async () => {
                    try {
                        await showLayer(layer);
                    } catch {
                        transferError();
                    }
                }),
                more
            );
            list.append(row);
        });
        window.lucide?.createIcons({ attrs: { 'stroke-width': 2 } });
    }
    form.onsubmit = (event) => {
        event.preventDefault();
        state.query = input.value;
        render();
    };
    input.oninput = () => {
        state.query = input.value;
        render();
    };
    sortButton.onclick = () =>
        setSortOpen(sortMenu.getAttribute('aria-hidden') !== 'false');
    sortMenu.onclick = (event) => {
        const button = event.target.closest('[data-sort-direction]');
        if (!button) return;
        state.sortDirection = button.dataset.sortDirection;
        setSortOpen(false);
        render();
    };
    document.addEventListener('click', (event) => {
        if (
            !sortMenu.contains(event.target) &&
            !sortButton.contains(event.target)
        )
            setSortOpen(false);
    });
    document
        .querySelector('[data-layer-add]')
        ?.addEventListener('click', () => {
            window.travelManagerNavigation?.showView('map') ||
                document.querySelector('[data-navigation-view="map"]')?.click();
            window.travelManagerLayerEditor.open();
        });
    document.addEventListener('travel-manager:custom-layers-changed', refresh);
    refresh();
});
