(() => {
    const instances = new WeakMap();
    const collator = new Intl.Collator(window.i18n.locale.replace('_', '-'), {
        sensitivity: 'base',
        numeric: true
    });
    const options = [
        ['name-asc', 'PUBLIC_TRANSPORT_LINES.SORT_NAME_ASC'],
        ['name-desc', 'PUBLIC_TRANSPORT_LINES.SORT_NAME_DESC'],
        ['number-asc', 'PUBLIC_TRANSPORT_LINES.SORT_NUMBER_ASC'],
        ['number-desc', 'PUBLIC_TRANSPORT_LINES.SORT_NUMBER_DESC']
    ];

    const sort = (root, mode = 'number-asc') => {
        const [field, direction] = mode.split('-');
        const attribute = field === 'name' ? 'lineName' : 'lineNumber';
        root?.querySelectorAll('.public-transport-lines__grid').forEach((grid) => {
            const tiles = Array.from(grid.querySelectorAll(':scope > .public-transport-lines__tile'));
            tiles.sort((left, right) => {
                const leftValue = String(left.dataset[attribute] || '').trim();
                const rightValue = String(right.dataset[attribute] || '').trim();
                if (field === 'name' && Boolean(leftValue) !== Boolean(rightValue)) {
                    return leftValue ? -1 : 1;
                }
                const result = collator.compare(leftValue, rightValue) || collator.compare(
                    left.dataset.lineNumber || '',
                    right.dataset.lineNumber || ''
                );
                return direction === 'desc' ? -result : result;
            });
            grid.append(...tiles);
        });
    };

    const enhance = (button, getRoot) => {
        if (!button || instances.has(button)) return instances.get(button);
        const menu = document.createElement('div');
        menu.className = 'public-transport-line-sort-menu';
        menu.role = 'menu';
        menu.hidden = true;
        document.body.append(menu);
        let selected = 'number-asc';

        const close = () => {
            menu.hidden = true;
            button.setAttribute('aria-expanded', 'false');
        };
        const position = () => {
            const rect = button.getBoundingClientRect();
            const width = menu.getBoundingClientRect().width;
            menu.style.left = `${Math.max(8, Math.min(rect.right - width, window.innerWidth - width - 8))}px`;
            menu.style.top = `${Math.min(rect.bottom + 6, window.innerHeight - menu.offsetHeight - 8)}px`;
        };
        options.forEach(([value, key]) => {
            const item = document.createElement('button');
            item.type = 'button';
            item.role = 'menuitemradio';
            item.dataset.lineSort = value;
            item.textContent = window.i18n.t(key);
            item.addEventListener('click', () => {
                selected = value;
                sort(getRoot(), selected);
                menu.querySelectorAll('[role="menuitemradio"]').forEach((entry) => {
                    entry.setAttribute('aria-checked', String(entry === item));
                });
                close();
                button.focus();
            });
            item.setAttribute('aria-checked', String(value === selected));
            menu.append(item);
        });
        button.addEventListener('click', () => {
            if (!menu.hidden) {
                close();
                return;
            }
            menu.hidden = false;
            button.setAttribute('aria-expanded', 'true');
            position();
            menu.querySelector('[aria-checked="true"]')?.focus();
        });
        document.addEventListener('pointerdown', (event) => {
            if (!button.contains(event.target) && !menu.contains(event.target)) close();
        });
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && !menu.hidden) close();
        });
        const instance = {
            apply: () => sort(getRoot(), selected)
        };
        instances.set(button, instance);
        return instance;
    };

    window.travelManagerPublicTransportLineSort = { enhance, sort };
})();
