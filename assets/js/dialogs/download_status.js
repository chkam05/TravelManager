document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#download-status');
    const heading = dialog?.querySelector('[data-download-status-heading]');
    const progressBar = dialog?.querySelector('[data-download-status-progress]');
    const text = dialog?.querySelector('[data-download-status-text]');
    const spinner = dialog?.querySelector('.download-status__spinner');
    const footer = dialog?.querySelector('[data-download-status-footer]');
    const closeButton = dialog?.querySelector('[data-download-status-close]');
    const backgroundButton = dialog?.querySelector('[data-download-status-background]');
    const cancelButton = dialog?.querySelector('[data-download-status-cancel]');
    let provider = '';
    let timer = null;
    let active = false;
    let running = false;
    let origin = '';
    let batch = null;

    if (!layer || !dialog || !heading || !progressBar || !text || !footer || !closeButton || !backgroundButton || !cancelButton) return;
    const stopPolling = () => { window.clearTimeout(timer); timer = null; };
    const poll = async () => {
        try {
            const response = await fetch(`/api/public-transport/${encodeURIComponent(provider)}/progress?t=${Date.now()}`);
            const data = await response.json();
            const multiple = Number(data.total) > 1;
            progressBar.hidden = batch ? false : !multiple;
            if (!batch && multiple) {
                progressBar.max = data.total;
                progressBar.value = data.status === 'complete' ? data.total : Math.max(0, data.current - 1);
            }
            const byteProgress = data.total > 100000;
            const position = data.total > 0
                ? window.i18n.t('DIALOG_DOWNLOAD_STATUS.ITEM_POSITION', {
                    current: byteProgress ? `${(data.current / 1048576).toFixed(1)} MB` : data.current,
                    total: byteProgress ? `${(data.total / 1048576).toFixed(1)} MB` : data.total
                })
                : '';
            const retry = data.attempt > 1
                ? window.i18n.t('DIALOG_DOWNLOAD_STATUS.RETRY', {
                    attempt: data.attempt,
                    maxAttempts: data.max_attempts
                })
                : '';
            if (batch) {
                const processingPrefix = window.i18n.t('DOWNLOAD_STATUS.PROCESSING_GTFS', { feed: '' });
                text.textContent = data.item
                    ? (data.item.startsWith(processingPrefix)
                        ? `${batch.current}/${batch.total} — ${data.item}${position}${retry}`
                        : window.i18n.t('DIALOG_DOWNLOAD_STATUS.BATCH_DOWNLOADING_ITEM', {
                        current: batch.current,
                        total: batch.total,
                        item: data.item,
                        position,
                        retry
                    }))
                    : window.i18n.t('DIALOG_DOWNLOAD_STATUS.BATCH_PREPARING_DATA', {
                        current: batch.current,
                        total: batch.total
                    });
            } else {
                const processingPrefix = window.i18n.t('DOWNLOAD_STATUS.PROCESSING_GTFS', { feed: '' });
                text.textContent = data.item
                    ? (data.item.startsWith(processingPrefix)
                        ? `${data.item}${position}${retry}`
                        : window.i18n.t('DIALOG_DOWNLOAD_STATUS.DOWNLOADING_ITEM', {
                        item: data.item,
                        position,
                        retry
                    }))
                    : window.i18n.t('DIALOG_DOWNLOAD_STATUS.PREPARING_DATA');
            }
        } catch (error) { /* Request performing the update reports the final error. */ }
        if (active) timer = window.setTimeout(poll, 250);
    };
    const openDialog = () => {
        active = true;
        dialog.setAttribute('aria-hidden', 'false');
        layer.classList.add('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'false');
        stopPolling();
        poll();
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };
    const show = (providerId, source = 'panel') => {
        provider = providerId;
        origin = source;
        batch = null;
        running = true;
        heading.textContent = window.i18n.t('DIALOG_DOWNLOAD_STATUS.DOWNLOADING_DATA');
        text.textContent = window.i18n.t('DIALOG_DOWNLOAD_STATUS.PREPARING_DATA');
        progressBar.hidden = true; footer.hidden = false; spinner.hidden = false;
        backgroundButton.hidden = false; cancelButton.hidden = false; closeButton.hidden = true;
        openDialog();
    };
    const showAll = (total) => {
        provider = '';
        origin = 'view';
        batch = { current: 0, total: Math.max(0, Number(total) || 0) };
        running = true;
        heading.textContent = window.i18n.t('DIALOG_DOWNLOAD_STATUS.UPDATING_ALL_PROVIDERS');
        text.textContent = window.i18n.t('DIALOG_DOWNLOAD_STATUS.PREPARING_DATA');
        progressBar.hidden = false;
        progressBar.max = Math.max(1, batch.total);
        progressBar.value = 0;
        footer.hidden = false;
        backgroundButton.hidden = false; cancelButton.hidden = false; closeButton.hidden = true;
        spinner.hidden = false;
        openDialog();
    };
    const updateAll = (providerId, providerName, current) => {
        if (!batch) return;
        provider = providerId;
        batch.current = Math.max(1, Number(current) || 1);
        progressBar.value = Math.max(0, batch.current - 1);
        heading.textContent = window.i18n.t('DIALOG_DOWNLOAD_STATUS.UPDATING_PROVIDER', {
            provider: providerName
        });
        text.textContent = window.i18n.t('DIALOG_DOWNLOAD_STATUS.BATCH_PREPARING_DATA', {
            current: batch.current,
            total: batch.total
        });
        stopPolling();
        poll();
    };
    const finish = (error = '') => {
        running = false; active = false; stopPolling(); spinner.hidden = true; footer.hidden = !error;
        if (batch) progressBar.value = batch.total;
        if (error) {
            heading.textContent = batch
                ? window.i18n.t('DIALOG_DOWNLOAD_STATUS.FINISHED_WITH_ERRORS')
                : window.i18n.t('DIALOG_DOWNLOAD_STATUS.DOWNLOAD_FAILED');
            text.textContent = error;
            backgroundButton.hidden = true; cancelButton.hidden = true; closeButton.hidden = false;
        }
        else close();
    };
    const close = () => {
        active = false; stopPolling(); dialog.setAttribute('aria-hidden', 'true'); layer.classList.remove('dialog-layer--open'); layer.setAttribute('aria-hidden', 'true');
    };
    const reopen = (source = '') => {
        if (!running) return false;
        if (source) origin = source;
        openDialog();
        return true;
    };
    closeButton.addEventListener('click', close);
    backgroundButton.addEventListener('click', () => {
        window.travelManagerPublicTransportRequests?.backgroundProvider(provider);
        window.dispatchEvent(new CustomEvent('travel-manager:public-transport-download-background', {
            detail: { origin }
        }));
        close();
    });
    cancelButton.addEventListener('click', async () => {
        cancelButton.disabled = true;
        window.dispatchEvent(new CustomEvent('travel-manager:public-transport-download-cancel'));
        text.textContent = window.i18n.t('DIALOG_DOWNLOAD_STATUS.CANCELLING');
        try {
            await fetch(`/api/public-transport/${encodeURIComponent(provider)}/cancel`, { method: 'POST' });
        } finally {
            cancelButton.disabled = false;
            close();
        }
    });
    document.addEventListener('travel-manager:app-view-changed', (event) => {
        if (event.detail?.view === 'public-transport') reopen('view');
    });
    window.travelManagerDownloadStatus = {
        show, showAll, updateAll, finish, reopen,
        isRunning: () => running
    };
});
