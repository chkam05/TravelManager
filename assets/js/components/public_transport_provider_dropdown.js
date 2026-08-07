(() => {
    const instances = new Map();

    const enhance = (select) => {
        instances.get(select)?.destroy();
        const options = Array.from(select.options).map((option) => ({
            value: option.value,
            name: option.textContent.trim(),
            description: option.dataset.description || '',
            icon: option.dataset.icon || 'bus-front',
            route: option.dataset.showRouteMap === 'true',
            vehicles: option.dataset.showVehiclePositions === 'true'
        }));
        select.classList.add('public-transport-provider-dropdown__native');

        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'public-transport-provider-dropdown__button';
        button.setAttribute('aria-haspopup', 'listbox');
        select.after(button);

        const menu = document.createElement('div');
        menu.className = 'public-transport-provider-dropdown__menu';
        menu.setAttribute('role', 'listbox');
        menu.hidden = true;
        document.body.append(menu);

        const capabilities = (item) => {
            const wrapper = document.createElement('span');
            wrapper.className = 'public-transport-provider-dropdown__capabilities';
            const add = (iconName, label) => {
                const badge = document.createElement('span');
                badge.title = label;
                badge.setAttribute('aria-label', label);
                const icon = document.createElement('i');
                icon.dataset.lucide = iconName;
                icon.setAttribute('aria-hidden', 'true');
                badge.append(icon);
                wrapper.append(badge);
            };
            if (item.route) add('route', 'Trasa na mapie');
            if (item.vehicles) add('map-pin', 'Pojazdy na mapie');
            return wrapper;
        };

        const content = (item, includeChevron = false) => {
            const iconWrapper = document.createElement('span');
            iconWrapper.className = 'public-transport-provider-dropdown__icon';
            const icon = document.createElement('i');
            icon.dataset.lucide = item.icon;
            icon.setAttribute('aria-hidden', 'true');
            iconWrapper.append(icon);
            const details = document.createElement('span');
            details.className = 'public-transport-provider-dropdown__details';
            const name = document.createElement('strong');
            name.textContent = item.name;
            const description = document.createElement('small');
            description.textContent = item.description;
            details.append(name, description, capabilities(item));
            const nodes = [iconWrapper, details];
            if (includeChevron) {
                const chevron = document.createElement('i');
                chevron.dataset.lucide = 'chevron-down';
                chevron.setAttribute('aria-hidden', 'true');
                nodes.push(chevron);
            }
            return nodes;
        };

        const close = () => {
            menu.hidden = true;
            button.setAttribute('aria-expanded', 'false');
        };
        const position = () => {
            const rect = button.getBoundingClientRect();
            const below = window.innerHeight - rect.bottom - 8;
            const above = rect.top - 8;
            const openAbove = below < 320 && above > below;
            menu.style.left = `${Math.max(8, Math.min(rect.left, window.innerWidth - rect.width - 8))}px`;
            menu.style.width = `${rect.width}px`;
            menu.style.maxHeight = `${Math.max(160, openAbove ? above : below)}px`;
            menu.style.top = openAbove ? 'auto' : `${rect.bottom + 4}px`;
            menu.style.bottom = openAbove ? `${window.innerHeight - rect.top + 4}px` : 'auto';
        };
        const sync = () => {
            const selected = options.find((item) => item.value === select.value) || options[0];
            if (!selected) return;
            button.replaceChildren(...content(selected, true));
            menu.querySelectorAll('[role="option"]').forEach((option) => {
                option.setAttribute('aria-selected', String(option.dataset.value === selected.value));
            });
            window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
        };

        options.forEach((item) => {
            const option = document.createElement('button');
            option.type = 'button';
            option.className = 'public-transport-provider-dropdown__option';
            option.dataset.value = item.value;
            option.setAttribute('role', 'option');
            option.replaceChildren(...content(item));
            option.addEventListener('click', () => {
                select.value = item.value;
                select.dispatchEvent(new Event('change', { bubbles: true }));
                sync();
                close();
            });
            menu.append(option);
        });

        button.addEventListener('click', () => {
            if (menu.hidden) {
                menu.hidden = false;
                button.setAttribute('aria-expanded', 'true');
                position();
            } else {
                close();
            }
        });
        button.addEventListener('keydown', (event) => {
            if (!['ArrowDown', 'ArrowUp'].includes(event.key)) return;
            event.preventDefault();
            menu.hidden = false;
            button.setAttribute('aria-expanded', 'true');
            position();
            const selected = menu.querySelector('[aria-selected="true"]');
            const target = event.key === 'ArrowUp'
                ? menu.querySelector('[role="option"]:last-of-type')
                : selected || menu.querySelector('[role="option"]');
            target?.focus();
        });
        menu.addEventListener('keydown', (event) => {
            if (!['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) return;
            event.preventDefault();
            const items = Array.from(menu.querySelectorAll('[role="option"]'));
            const current = items.indexOf(document.activeElement);
            const next = event.key === 'Home'
                ? 0
                : event.key === 'End'
                    ? items.length - 1
                    : event.key === 'ArrowDown'
                        ? Math.min(items.length - 1, current + 1)
                        : Math.max(0, current - 1);
            items[next]?.focus();
        });
        const outside = (event) => {
            if (!button.contains(event.target) && !menu.contains(event.target)) close();
        };
        const escape = (event) => {
            if (event.key === 'Escape' && !menu.hidden) {
                close();
                button.focus();
            }
        };
        const closeOnResize = () => close();
        const closeOnOutsideScroll = (event) => {
            if (!menu.contains(event.target)) close();
        };
        document.addEventListener('pointerdown', outside);
        document.addEventListener('keydown', escape);
        window.addEventListener('resize', closeOnResize);
        window.addEventListener('scroll', closeOnOutsideScroll, true);
        select.addEventListener('change', sync);
        sync();

        const instance = {
            sync,
            destroy: () => {
                document.removeEventListener('pointerdown', outside);
                document.removeEventListener('keydown', escape);
                window.removeEventListener('resize', closeOnResize);
                window.removeEventListener('scroll', closeOnOutsideScroll, true);
                select.removeEventListener('change', sync);
                select.classList.remove('public-transport-provider-dropdown__native');
                button.remove();
                menu.remove();
                instances.delete(select);
            }
        };
        instances.set(select, instance);
        return instance;
    };

    window.travelManagerPublicTransportProviderDropdown = { enhance };
})();
