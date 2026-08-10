document.addEventListener('travel-manager:views-ready', () => {
    const t = window.i18n.t;
    const locale = window.i18n.locale.replace('_', '-');
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
            return t('PUBLIC_TRANSPORT_VIEW.NO_DATA');
        }

        const parsed = new Date(value);

        if (Number.isNaN(parsed.getTime())) {
            return value;
        }

        return new Intl.DateTimeFormat(locale, {
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
        title.textContent = announcement.description
            || t('PUBLIC_TRANSPORT_ANNOUNCEMENT.ANNOUNCEMENT');
        city.textContent = announcement.city || t('PUBLIC_TRANSPORT_VIEW.TITLE');
        content.textContent = announcement.content
            || t('PUBLIC_TRANSPORT_ANNOUNCEMENT.NO_FULL_CONTENT');

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
