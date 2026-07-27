document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#public-transport-announcement-dialog');
    const title = dialog?.querySelector('#public-transport-announcement-title');
    const city = dialog?.querySelector('#public-transport-announcement-city');
    const effectiveDate = dialog?.querySelector('#public-transport-announcement-effective-date');
    const updated = dialog?.querySelector('#public-transport-announcement-updated');
    const content = dialog?.querySelector('#public-transport-announcement-content');
    const closeButtons = dialog?.querySelectorAll('[data-public-transport-announcement-close]');

    if (!layer || !dialog || !title || !city || !effectiveDate || !updated || !content || !closeButtons?.length) {
        return;
    }

    const formatDate = (value, includeTime = false) => {
        if (!value) {
            return 'Brak danych';
        }

        const parsed = new Date(value);

        if (Number.isNaN(parsed.getTime())) {
            return value;
        }

        return new Intl.DateTimeFormat('pl-PL', {
            dateStyle: 'long',
            ...(includeTime ? { timeStyle: 'short' } : {})
        }).format(parsed);
    };

    const close = () => {
        dialog.setAttribute('aria-hidden', 'true');
        layer.classList.remove('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'true');
    };

    const render = (announcement) => {
        title.textContent = announcement.description || 'Komunikat';
        city.textContent = announcement.city || 'Komunikacja miejska';
        content.textContent = announcement.content || 'Brak pełnej treści komunikatu.';

        const dateFrom = formatDate(announcement.effective_date_from);
        const dateTo = announcement.effective_date_to
            ? formatDate(announcement.effective_date_to)
            : '';
        effectiveDate.textContent = dateTo ? `${dateFrom} – ${dateTo}` : dateFrom;
        updated.textContent = formatDate(announcement.last_updated_datetime, true);
    };

    const open = (announcement) => {
        render(announcement);

        dialog.setAttribute('aria-hidden', 'false');
        layer.classList.add('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'false');
        window.requestAnimationFrame(() => closeButtons[0].focus());
    };

    const update = (announcement) => {
        if (dialog.getAttribute('aria-hidden') === 'false') {
            render(announcement);
        }
    };

    closeButtons.forEach((button) => button.addEventListener('click', close));
    layer.addEventListener('click', (event) => {
        if (event.target === layer && dialog.getAttribute('aria-hidden') === 'false') {
            close();
        }
    });
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && dialog.getAttribute('aria-hidden') === 'false') {
            close();
        }
    });

    window.travelManagerPublicTransportAnnouncement = { open, update };
});
