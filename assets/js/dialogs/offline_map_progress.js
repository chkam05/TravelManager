document.addEventListener('travel-manager:views-ready', () => {
    const t = window.i18n.t;
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#offline-map-progress');
    const heading = dialog?.querySelector('[data-offline-map-progress-heading]');
    const bar = dialog?.querySelector('[data-offline-map-progress-bar]');
    const indeterminate = dialog?.querySelector('[data-offline-map-progress-indeterminate]');
    const text = dialog?.querySelector('[data-offline-map-progress-text]');
    const spinner = dialog?.querySelector('.offline-map-progress__spinner');
    const backgroundButton = dialog?.querySelector('[data-offline-map-progress-background]');
    const cancelButton = dialog?.querySelector('[data-offline-map-progress-cancel]');
    const retryButton = dialog?.querySelector('[data-offline-map-progress-retry]');
    const closeButton = dialog?.querySelector('[data-offline-map-progress-close]');
    if (!layer || !dialog || !heading || !bar || !indeterminate || !text || !spinner
        || !backgroundButton || !cancelButton || !retryButton || !closeButton) return;

    const activeStatuses = new Set(['queued', 'running']);
    const stages = {
        preparing: 'PREPARING', downloading: 'DOWNLOADING', analysing: 'ANALYSING',
        building_tiles: 'BUILDING_TILES', optimising: 'OPTIMISING', installing: 'INSTALLING',
        completed: 'COMPLETED', failed: 'FAILED', cancelled: 'CANCELLED'
    };
    let job = null;
    let timer = null;
    let background = false;
    const dismissedFailures = new Set();
    const formatBytes = (value) => {
        const bytes = Math.max(0, Number(value) || 0);
        const gigabytes = bytes >= 1024 ** 3;
        const locale = window.i18n.locale?.replace('_', '-') || undefined;
        const amount = bytes / (gigabytes ? 1024 ** 3 : 1024 ** 2);
        return `${new Intl.NumberFormat(locale, {
            minimumFractionDigits: gigabytes ? 2 : 0,
            maximumFractionDigits: gigabytes ? 2 : 1
        }).format(amount)} ${gigabytes ? 'GB' : 'MB'}`;
    };
    const stopPolling = () => { window.clearTimeout(timer); timer = null; };
    const hide = () => {
        dialog.setAttribute('aria-hidden', 'true');
        layer.classList.remove('dialog-layer--open'); layer.setAttribute('aria-hidden', 'true');
    };
    const render = () => {
        if (!job) return;
        const stageKey = stages[job.stage] || 'PREPARING';
        const phaseKey = job.stage === 'building_tiles' && job.phase === 'assignment'
            ? 'ASSIGNING_TILES' : job.stage === 'building_tiles' && job.phase === 'encoding'
                ? 'ENCODING_TILES' : stageKey;
        heading.textContent = t(`OFFLINE_MAP_PROGRESS.${phaseKey}`);
        const byteStage = job.stage === 'downloading';
        const current = byteStage ? Number(job.downloaded_bytes) : Number(job.current);
        const total = byteStage ? Number(job.total_bytes) : Number(job.total);
        const hasTotal = Number.isFinite(total) && total > 0;
        bar.hidden = !hasTotal;
        indeterminate.hidden = hasTotal;
        if (hasTotal) {
            bar.max = total;
            bar.value = Math.min(total, Math.max(0, current || 0));
        }
        const count = new Intl.NumberFormat(window.i18n.locale?.replace('_', '-') || undefined);
        const percent = hasTotal ? Math.min(100, Math.floor(100 * Math.max(0, current || 0) / total)) : 0;
        text.textContent = hasTotal
            ? (byteStage
                ? t('OFFLINE_MAP_PROGRESS.BYTES', {current: formatBytes(current), total: formatBytes(total), percent})
                : t('OFFLINE_MAP_PROGRESS.ITEMS', {current: count.format(current || 0), total: count.format(total), percent}))
            : (job.stage === 'analysing' && current > 0
                ? t('OFFLINE_MAP_PROGRESS.ANALYSED', {current: count.format(current)})
                : t('OFFLINE_MAP_PROGRESS.WORKING'));
        const active = activeStatuses.has(job.status);
        spinner.hidden = !active; backgroundButton.hidden = !active; cancelButton.hidden = !active;
        retryButton.hidden = !['failed', 'cancelled'].includes(job.status);
        closeButton.hidden = active; cancelButton.disabled = job.cancel_requested === true;
        if (job.error) text.textContent = job.error;
        document.dispatchEvent(new CustomEvent('travel-manager:offline-map-job-updated', {detail: job}));
    };
    const show = (nextJob, inBackground = false) => {
        job = nextJob; background = inBackground; render();
        if (!background) {
            dialog.setAttribute('aria-hidden', 'false'); layer.classList.add('dialog-layer--open');
            layer.setAttribute('aria-hidden', 'false');
            window.lucide?.createIcons({attrs: {'stroke-width': 1.7}});
        }
        stopPolling();
        if (activeStatuses.has(job.status)) poll();
    };
    const poll = async () => {
        if (!job) return;
        try {
            const response = await fetch(`/api/offline-maps/jobs/${encodeURIComponent(job.id)}?t=${Date.now()}`, {
                headers: {'Accept': 'application/json'}
            });
            const data = await response.json();
            if (response.ok && data.job) job = data.job;
        } catch (error) { /* A transient status error does not stop the durable job. */ }
        render();
        if (job && activeStatuses.has(job.status)) {
            timer = window.setTimeout(poll, 500);
        } else if (job) {
            document.dispatchEvent(new CustomEvent('travel-manager:offline-map-job-finished', {detail: job}));
            if (background) hide();
        }
    };
    const restore = async () => {
        try {
            const response = await fetch('/api/offline-maps/jobs', {headers: {'Accept': 'application/json'}});
            const data = await response.json();
            const jobs = (data.jobs || []).slice().sort(
                (a, b) => String(b.updated_at).localeCompare(String(a.updated_at))
            );
            const active = jobs.find((item) => activeStatuses.has(item.status));
            const completedMaps = new Set();
            const failed = jobs.find((item) => {
                if (item.status === 'completed') completedMaps.add(item.map_id);
                return item.status === 'failed'
                    && !completedMaps.has(item.map_id)
                    && !dismissedFailures.has(item.id);
            });
            if (active || failed) show(active || failed, false);
        } catch (error) { /* Settings remain usable when status cannot be restored. */ }
    };
    backgroundButton.addEventListener('click', () => {
        background = true; hide();
        document.dispatchEvent(new CustomEvent('travel-manager:offline-map-job-background', {detail: job}));
    });
    cancelButton.addEventListener('click', async () => {
        if (!job) return;
        cancelButton.disabled = true; text.textContent = t('OFFLINE_MAP_PROGRESS.CANCELLING');
        try {
            const response = await fetch(`/api/offline-maps/jobs/${encodeURIComponent(job.id)}/cancel`, {method: 'POST'});
            const data = await response.json();
            if (response.ok && data.job) job = data.job;
        } finally { render(); }
    });
    retryButton.addEventListener('click', async () => {
        if (!job || !['failed', 'cancelled'].includes(job.status)) return;
        retryButton.disabled = true;
        try {
            const response = await fetch(
                `/api/offline-maps/jobs/${encodeURIComponent(job.id)}/resume`,
                {method: 'POST', headers: {'Accept': 'application/json'}}
            );
            const data = await response.json();
            if (!response.ok || !data.job) {
                throw new Error(data.message || t('OFFLINE_MAP_PROGRESS.RETRY_FAILED'));
            }
            dismissedFailures.delete(job.id);
            show(data.job, false);
        } catch (error) {
            text.textContent = error.message || t('OFFLINE_MAP_PROGRESS.RETRY_FAILED');
        } finally {
            retryButton.disabled = false;
        }
    });
    closeButton.addEventListener('click', () => {
        if (job?.status === 'failed') dismissedFailures.add(job.id);
        job = null; stopPolling(); hide();
    });
    document.addEventListener('travel-manager:offline-map-job-started', (event) => show(event.detail, false));
    document.addEventListener('travel-manager:app-view-changed', (event) => {
        if (event.detail?.view === 'settings') {
            if (job && activeStatuses.has(job.status)) show(job, false); else restore();
        }
    });
    window.travelManagerOfflineMapProgress = {show, restore, isRunning: () => Boolean(job && activeStatuses.has(job.status))};
    if (document.querySelector('.app-shell')?.dataset.currentView === 'settings') restore();
});
