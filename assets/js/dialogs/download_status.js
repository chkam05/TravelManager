document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#download-status');
    const heading = dialog?.querySelector('[data-download-status-heading]');
    const progressBar = dialog?.querySelector('[data-download-status-progress]');
    const text = dialog?.querySelector('[data-download-status-text]');
    const spinner = dialog?.querySelector('.download-status__spinner');
    const footer = dialog?.querySelector('[data-download-status-footer]');
    const closeButton = dialog?.querySelector('[data-download-status-close]');
    let provider = '';
    let timer = null;
    let active = false;

    if (!layer || !dialog || !heading || !progressBar || !text || !footer || !closeButton) return;
    const stopPolling = () => { window.clearTimeout(timer); timer = null; };
    const poll = async () => {
        try {
            const response = await fetch(`/api/public-transport/${encodeURIComponent(provider)}/progress?t=${Date.now()}`);
            const data = await response.json();
            const multiple = Number(data.total) > 1;
            progressBar.hidden = !multiple;
            if (multiple) {
                progressBar.max = data.total;
                progressBar.value = data.status === 'complete' ? data.total : Math.max(0, data.current - 1);
            }
            const position = data.total > 0 ? ` (${data.current}/${data.total})` : '';
            const retry = data.attempt > 1 ? ` — próba ${data.attempt}/${data.max_attempts}` : '';
            text.textContent = data.item ? `Pobieranie „${data.item}”${position}${retry}…` : 'Przygotowywanie danych…';
        } catch (error) { /* Request performing the update reports the final error. */ }
        if (active) timer = window.setTimeout(poll, 250);
    };
    const show = (providerId) => {
        provider = providerId;
        active = true;
        heading.textContent = 'Pobieranie danych…'; text.textContent = 'Przygotowywanie danych…';
        progressBar.hidden = true; footer.hidden = true; spinner.hidden = false;
        dialog.setAttribute('aria-hidden', 'false'); layer.classList.add('dialog-layer--open'); layer.setAttribute('aria-hidden', 'false');
        stopPolling(); poll(); window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };
    const finish = (error = '') => {
        active = false; stopPolling(); spinner.hidden = true; footer.hidden = !error;
        if (error) { heading.textContent = 'Nie udało się pobrać danych'; text.textContent = error; }
        else close();
    };
    const close = () => {
        active = false; stopPolling(); dialog.setAttribute('aria-hidden', 'true'); layer.classList.remove('dialog-layer--open'); layer.setAttribute('aria-hidden', 'true');
    };
    closeButton.addEventListener('click', close);
    window.travelManagerDownloadStatus = { show, finish };
});
