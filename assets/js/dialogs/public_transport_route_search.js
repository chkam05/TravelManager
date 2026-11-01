document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#public-transport-route-search');
    const openButtons = document.querySelectorAll('[data-public-transport-route-search]');
    if (!layer || !dialog || !openButtons.length) return;
    const closeButtons = dialog.querySelectorAll('[data-route-search-close]');
    const providerSelects = [...dialog.querySelectorAll('[data-route-search-provider]')];
    const citySelects = Object.fromEntries([...dialog.querySelectorAll('[data-route-search-city]')].map(item => [item.dataset.routeSearchCity, item]));
    const stopSelects = Object.fromEntries([...dialog.querySelectorAll('[data-route-search-stop]')].map(item => [item.dataset.routeSearchStop, item]));
    const dateTime = dialog.querySelector('[data-route-search-date-time]');
    const dateTimePicker = dialog.querySelector('[data-route-search-date-time-picker]');
    const dateTimeTrigger = dialog.querySelector('[data-route-search-date-time-trigger]');
    const dateTimeValue = dialog.querySelector('[data-route-search-date-time-value]');
    const dateTimePopover = dialog.querySelector('[data-route-search-date-time-popover]');
    const monthLabel = dialog.querySelector('[data-route-search-month-label]');
    const calendarDays = dialog.querySelector('[data-route-search-calendar-days]');
    const hourSelect = dialog.querySelector('[data-route-search-hour]');
    const minuteSelect = dialog.querySelector('[data-route-search-minute]');
    const arriveBy = dialog.querySelector('[data-route-search-arrive-by]');
    const timeLabel = dialog.querySelector('[data-route-search-time-label]');
    const transfer = dialog.querySelector('[data-route-search-transfer]');
    const status = dialog.querySelector('[data-route-search-status]');
    let catalog = { cities: [] };
    let selectedDateTime = null;
    let visibleMonth = null;
    let catalogLoading = Promise.resolve();
    let catalogRequestId = 0;

    const fill = (select, items, value = '') => {
        select.replaceChildren(...items.map(item => {
            const option = document.createElement('option');
            option.value = item.value; option.textContent = item.label; return option;
        }));
        if ([...select.options].some(option => option.value === value)) select.value = value;
    };
    const localDateTime = () => {
        const value = new Date(Date.now() + 5 * 60 * 1000);
        value.setSeconds(0, 0);
        return new Date(value.getTime() - value.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
    };
    const parseLocalDateTime = value => {
        const match = String(value || '').match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/);
        return match ? new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3]), Number(match[4]), Number(match[5])) : new Date();
    };
    const valueFromDate = value => [
        value.getFullYear(), String(value.getMonth() + 1).padStart(2, '0'), String(value.getDate()).padStart(2, '0')
    ].join('-') + `T${String(value.getHours()).padStart(2, '0')}:${String(value.getMinutes()).padStart(2, '0')}`;
    const sameDay = (first, second) => first && second
        && first.getFullYear() === second.getFullYear()
        && first.getMonth() === second.getMonth()
        && first.getDate() === second.getDate();
    const formatDateTime = value => new Intl.DateTimeFormat(window.i18n.locale.replace('_', '-'), {
        weekday: 'short', day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit'
    }).format(value);
    const positionDateTimePopover = () => {
        const bounds = dateTimeTrigger.getBoundingClientRect();
        const width = Math.min(340, window.innerWidth - 32);
        const left = Math.max(16, Math.min(bounds.right - width, window.innerWidth - width - 16));
        const spaceBelow = window.innerHeight - bounds.bottom - 16;
        dateTimePopover.style.left = `${left}px`;
        dateTimePopover.style.top = spaceBelow >= 410
            ? `${bounds.bottom + 8}px`
            : `${Math.max(16, bounds.top - 418)}px`;
    };
    const renderCalendar = () => {
        monthLabel.textContent = new Intl.DateTimeFormat(window.i18n.locale.replace('_', '-'), {
            month: 'long', year: 'numeric'
        }).format(visibleMonth);
        calendarDays.replaceChildren();
        const first = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth(), 1);
        const offset = (first.getDay() + 6) % 7;
        const start = new Date(first.getFullYear(), first.getMonth(), 1 - offset);
        const today = new Date();
        for (let index = 0; index < 42; index += 1) {
            const day = new Date(start.getFullYear(), start.getMonth(), start.getDate() + index);
            const button = document.createElement('button');
            button.type = 'button'; button.textContent = day.getDate();
            button.setAttribute('aria-label', new Intl.DateTimeFormat(window.i18n.locale.replace('_', '-'), { dateStyle: 'full' }).format(day));
            button.setAttribute('aria-selected', String(sameDay(day, selectedDateTime)));
            if (day.getMonth() !== visibleMonth.getMonth()) button.dataset.outsideMonth = '';
            if (sameDay(day, today)) button.dataset.today = '';
            button.addEventListener('click', event => {
                event.preventDefault();
                event.stopPropagation();
                selectedDateTime.setFullYear(day.getFullYear(), day.getMonth(), day.getDate());
                visibleMonth = new Date(day.getFullYear(), day.getMonth(), 1);
                renderCalendar();
            });
            calendarDays.append(button);
        }
    };
    const syncDateTimePicker = () => {
        selectedDateTime = parseLocalDateTime(dateTime.value || localDateTime());
        visibleMonth = new Date(selectedDateTime.getFullYear(), selectedDateTime.getMonth(), 1);
        hourSelect.value = String(selectedDateTime.getHours());
        minuteSelect.value = String(selectedDateTime.getMinutes());
        dateTimeValue.textContent = formatDateTime(selectedDateTime);
        renderCalendar();
    };
    const closeDateTimePicker = () => {
        dateTimePopover.hidden = true;
        dateTimeTrigger.setAttribute('aria-expanded', 'false');
    };
    const openDateTimePicker = () => {
        syncDateTimePicker();
        dateTimePopover.hidden = false;
        dateTimeTrigger.setAttribute('aria-expanded', 'true');
        positionDateTimePopover();
    };
    fill(hourSelect, Array.from({ length: 24 }, (_, hour) => ({ value: String(hour), label: String(hour).padStart(2, '0') })));
    fill(minuteSelect, Array.from({ length: 60 }, (_, minute) => ({ value: String(minute), label: String(minute).padStart(2, '0') })));
    dialog.querySelector('[data-route-search-month-previous]').addEventListener('click', () => { visibleMonth = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth() - 1, 1); renderCalendar(); });
    dialog.querySelector('[data-route-search-month-next]').addEventListener('click', () => { visibleMonth = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth() + 1, 1); renderCalendar(); });
    dialog.querySelector('[data-route-search-date-today]').addEventListener('click', () => { selectedDateTime = new Date(); visibleMonth = new Date(selectedDateTime.getFullYear(), selectedDateTime.getMonth(), 1); hourSelect.value = String(selectedDateTime.getHours()); minuteSelect.value = String(selectedDateTime.getMinutes()); renderCalendar(); });
    dialog.querySelector('[data-route-search-date-apply]').addEventListener('click', () => {
        selectedDateTime.setHours(Number(hourSelect.value), Number(minuteSelect.value), 0, 0);
        const previous = dateTime.value;
        dateTime.value = valueFromDate(selectedDateTime);
        dateTimeValue.textContent = formatDateTime(selectedDateTime);
        closeDateTimePicker();
        if (dateTime.value !== previous) dateTime.dispatchEvent(new Event('change'));
    });
    dateTimeTrigger.addEventListener('click', () => dateTimePopover.hidden ? openDateTimePicker() : closeDateTimePicker());
    document.addEventListener('click', event => { if (!dateTimePicker.contains(event.target)) closeDateTimePicker(); });
    window.addEventListener('resize', () => { if (!dateTimePopover.hidden) positionDateTimePopover(); });
    const fillStops = (side, selectedValue = stopSelects[side].value) => {
        const city = catalog.cities.find(item => item.name === citySelects[side].value);
        fill(
            stopSelects[side],
            (city?.stops || []).map(stop => ({ value: stop.id, label: stop.name })),
            selectedValue
        );
    };
    const fillCatalog = () => {
        ['origin', 'destination'].forEach(side => {
            const previousCity = citySelects[side].value;
            const previousStop = stopSelects[side].value;
            fill(citySelects[side], catalog.cities.map(city => ({ value: city.name, label: city.name })), previousCity);
            fillStops(side, previousStop);
        });
    };
    const requestCatalog = async () => {
        const requestId = ++catalogRequestId;
        const provider = providerSelects[0].value;
        if (!provider) return;
        status.textContent = 'Wczytywanie przystanków…';
        const response = await fetch(`/api/public-transport/${encodeURIComponent(provider)}/route-search/catalog?date=${dateTime.value.slice(0, 10)}`);
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Nie udało się wczytać przystanków.');
        if (requestId !== catalogRequestId) return;
        catalog = data; fillCatalog(); status.textContent = '';
    };
    const loadCatalog = () => {
        catalogLoading = requestCatalog();
        return catalogLoading;
    };
    const close = () => {
        closeDateTimePicker();
        dialog.setAttribute('aria-hidden', 'true'); layer.classList.remove('dialog-layer--open'); layer.setAttribute('aria-hidden', 'true');
    };
    const open = async () => {
        status.textContent = 'Wczytywanie przewoźników…';
        dialog.setAttribute('aria-hidden', 'false'); layer.classList.add('dialog-layer--open'); layer.setAttribute('aria-hidden', 'false');
        if (!dateTime.value) dateTime.value = localDateTime();
        syncDateTimePicker();
        try {
            const response = await fetch('/api/public-transport/route-search/providers');
            const data = await response.json();
            if (!response.ok || !data.providers?.length) throw new Error('Najpierw pobierz dane wybranego przewoźnika.');
            const options = data.providers.map(provider => ({ value: provider.id, label: provider.name }));
            providerSelects.forEach(select => fill(select, options, providerSelects[0].value));
            providerSelects[1].disabled = true;
            await loadCatalog();
        } catch (error) { status.textContent = error.message; }
    };
    openButtons.forEach(button => button.addEventListener('click', open));
    closeButtons.forEach(button => button.addEventListener('click', close));
    providerSelects[0].addEventListener('change', async () => {
        providerSelects[1].value = providerSelects[0].value;
        try { await loadCatalog(); } catch (error) { status.textContent = error.message; }
    });
    Object.entries(citySelects).forEach(([side, select]) => select.addEventListener('change', () => fillStops(side)));
    dateTime.addEventListener('change', async () => { try { await loadCatalog(); } catch (error) { status.textContent = error.message; } });
    arriveBy.addEventListener('change', () => { timeLabel.textContent = arriveBy.checked ? 'Godzina przyjazdu' : 'Godzina odjazdu'; });
    dialog.addEventListener('submit', async event => {
        event.preventDefault(); status.textContent = 'Wyszukiwanie połączeń…';
        try {
            await catalogLoading;
            const provider = providerSelects[0].value;
            const response = await fetch(`/api/public-transport/${encodeURIComponent(provider)}/route-search`, {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({
                    origin: stopSelects.origin.value, destination: stopSelects.destination.value,
                    date_time: dateTime.value, time_mode: arriveBy.checked ? 'arrive_by' : 'depart_at',
                    max_transfer_minutes: Number(transfer.value), max_transfers: 3, limit: 5
                })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Nie udało się znaleźć połączenia.');
            close();
            document.dispatchEvent(new CustomEvent('travel-manager:public-transport-route-results', { detail: data }));
        } catch (error) { status.textContent = error.message; }
    });
    window.travelManagerPublicTransportRouteSearch = { open, close };
});
