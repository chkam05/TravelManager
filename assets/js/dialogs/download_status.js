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
    let batch = null;

    if (!layer || !dialog || !heading || !progressBar || !text || !footer || !closeButton) return;
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
            const position = data.total > 0 ? ` (${data.current}/${data.total})` : '';
            const retry = data.attempt > 1 ? ` — próba ${data.attempt}/${data.max_attempts}` : '';
            const details = data.item
                ? `Pobieranie „${data.item}”${position}${retry}…`
                : 'Przygotowywanie danych…';
            text.textContent = batch
                ? `Przewoźnik ${batch.current} z ${batch.total} — ${details.toLocaleLowerCase('pl-PL')}`
                : details;
        } catch (error) { /* Request performing the update reports the final error. */ }
        if (active) timer = window.setTimeout(poll, 250);
    };
    const show = (providerId) => {
        provider = providerId;
        batch = null;
        active = true;
        heading.textContent = 'Pobieranie danych…'; text.textContent = 'Przygotowywanie danych…';
        progressBar.hidden = true; footer.hidden = true; spinner.hidden = false;
        dialog.setAttribute('aria-hidden', 'false'); layer.classList.add('dialog-layer--open'); layer.setAttribute('aria-hidden', 'false');
        stopPolling(); poll(); window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };
    const showAll = (total) => {
        provider = '';
        batch = { current: 0, total: Math.max(0, Number(total) || 0) };
        active = true;
        heading.textContent = 'Aktualizowanie wszystkich przewoźników…';
        text.textContent = 'Przygotowywanie danych…';
        progressBar.hidden = false;
        progressBar.max = Math.max(1, batch.total);
        progressBar.value = 0;
        footer.hidden = true;
        spinner.hidden = false;
        dialog.setAttribute('aria-hidden', 'false');
        layer.classList.add('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'false');
        stopPolling();
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };
    const updateAll = (providerId, providerName, current) => {
        if (!batch) return;
        provider = providerId;
        batch.current = Math.max(1, Number(current) || 1);
        progressBar.value = Math.max(0, batch.current - 1);
        heading.textContent = `Aktualizowanie: ${providerName}`;
        text.textContent = `Przewoźnik ${batch.current} z ${batch.total} — przygotowywanie danych…`;
        stopPolling();
        poll();
    };
    const finish = (error = '') => {
        active = false; stopPolling(); spinner.hidden = true; footer.hidden = !error;
        if (batch) progressBar.value = batch.total;
        if (error) {
            heading.textContent = batch
                ? 'Aktualizacja zakończona z błędami'
                : 'Nie udało się pobrać danych';
            text.textContent = error;
        }
        else close();
    };
    const close = () => {
        active = false; stopPolling(); dialog.setAttribute('aria-hidden', 'true'); layer.classList.remove('dialog-layer--open'); layer.setAttribute('aria-hidden', 'true');
    };
    closeButton.addEventListener('click', close);
    window.travelManagerDownloadStatus = { show, showAll, updateAll, finish };
});
