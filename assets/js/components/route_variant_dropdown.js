(() => {
    const groupNames = {
        standard: 'Trasy standardowe',
        short: 'Trasy skrócone',
        changed: 'Trasy zmienione',
        from_depot: 'Trasy z zajezdni',
        to_depot: 'Trasy do zajezdni'
    };
    const groupOrder = Object.keys(groupNames);
    const instances = new Map();

    const enhance = (select, items, selectedValue, onChange) => {
        instances.forEach((instance, element) => {
            if (!element.isConnected) instance.destroy();
        });
        instances.get(select)?.destroy();
        select.replaceChildren(...items.map((item) => {
            const option = document.createElement('option');
            option.value = item.value;
            option.textContent = item.label;
            return option;
        }));
        if (items.some((item) => item.value === selectedValue)) select.value = selectedValue;
        select.classList.add('route-variant-dropdown__native');

        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'route-variant-dropdown__button';
        button.setAttribute('aria-haspopup', 'listbox');
        button.innerHTML = '<span></span><i data-lucide="chevron-down" aria-hidden="true"></i>';
        select.after(button);
        const menu = document.createElement('div');
        menu.className = 'route-variant-dropdown__menu';
        menu.setAttribute('role', 'listbox');
        menu.hidden = true;
        document.body.append(menu);

        const updateButton = () => {
            const item = items.find((entry) => entry.value === select.value) || items[0];
            button.querySelector('span').textContent = item?.label || 'Wybierz trasę';
        };
        const close = () => {
            menu.hidden = true;
            button.setAttribute('aria-expanded', 'false');
        };
        const position = () => {
            const rect = button.getBoundingClientRect();
            const availableBelow = window.innerHeight - rect.bottom - 8;
            const availableAbove = rect.top - 8;
            const openAbove = availableBelow < 260 && availableAbove > availableBelow;
            menu.style.left = `${Math.max(8, Math.min(rect.left, window.innerWidth - rect.width - 8))}px`;
            menu.style.width = `${rect.width}px`;
            menu.style.maxHeight = `${Math.max(120, openAbove ? availableAbove : availableBelow)}px`;
            menu.style.top = openAbove ? 'auto' : `${rect.bottom + 4}px`;
            menu.style.bottom = openAbove ? `${window.innerHeight - rect.top + 4}px` : 'auto';
        };
        const open = () => {
            menu.hidden = false;
            button.setAttribute('aria-expanded', 'true');
            position();
        };

        groupOrder.forEach((group) => {
            const groupItems = items.filter((item) => (item.group || 'standard') === group);
            if (!groupItems.length) return;
            const section = document.createElement('section');
            section.className = 'route-variant-dropdown__group';
            const heading = document.createElement('strong');
            heading.textContent = groupNames[group];
            section.append(heading);
            groupItems.forEach((item) => {
                const option = document.createElement('button');
                option.type = 'button';
                option.className = 'route-variant-dropdown__option';
                option.setAttribute('role', 'option');
                option.textContent = item.label;
                option.onclick = () => {
                    select.value = item.value;
                    updateButton();
                    close();
                    onChange(item.value);
                };
                section.append(option);
            });
            menu.append(section);
        });
        button.onclick = () => menu.hidden ? open() : close();
        const outside = (event) => {
            if (!button.contains(event.target) && !menu.contains(event.target)) close();
        };
        const escape = (event) => {
            if (event.key === 'Escape') close();
        };
        const scrollClose = (event) => {
            if (!menu.contains(event.target)) close();
        };
        document.addEventListener('pointerdown', outside);
        document.addEventListener('keydown', escape);
        window.addEventListener('resize', close);
        window.addEventListener('scroll', scrollClose, true);
        updateButton();
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
        instances.set(select, { destroy: () => {
            document.removeEventListener('pointerdown', outside);
            document.removeEventListener('keydown', escape);
            window.removeEventListener('resize', close);
            window.removeEventListener('scroll', scrollClose, true);
            button.remove();
            menu.remove();
            instances.delete(select);
        } });
    };
    window.travelManagerRouteVariantDropdown = { enhance };
})();
