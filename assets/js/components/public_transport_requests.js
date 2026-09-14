(() => {
    const active = new Map();
    const foreground = new Set();
    let bubble = null;

    const ensureBubble = () => {
        if (bubble) return bubble;
        bubble = document.createElement('div');
        bubble.className = 'public-transport-background-download';
        bubble.hidden = true;
        bubble.setAttribute('role', 'status');
        bubble.innerHTML = '<span class="public-transport-background-download__icon"><i data-lucide="loader-circle" aria-hidden="true"></i></span><span></span>';
        document.body.append(bubble);
        return bubble;
    };
    const render = () => {
        const element = ensureBubble();
        const backgroundCount = [...active.keys()].filter((key) => !foreground.has(key)).length;
        element.hidden = backgroundCount === 0;
        element.querySelector('span').textContent = window.i18n?.t(
            'PUBLIC_TRANSPORT_VIEW.BACKGROUND_DOWNLOAD', { count: backgroundCount }
        ) || 'Downloading public transport data in the background…';
        if (!element.hidden) window.lucide?.createIcons({ attrs: { 'stroke-width': 1.7 } });
    };
    const key = ({ provider, screen, url = '', refresh = false }) =>
        JSON.stringify([provider, screen, url, Boolean(refresh)]);
    const request = (details) => {
        const requestKey = key(details);
        let promise = active.get(requestKey);
        if (!promise) {
            const params = new URLSearchParams();
            if (details.url) params.set('url', details.url);
            if (details.refresh) params.set('refresh', '1');
            const endpoint = `/api/public-transport/${encodeURIComponent(details.provider)}/${details.screen}`;
            promise = fetch(`${endpoint}${params.size ? `?${params}` : ''}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            }).then(async (response) => {
                const text = await response.text();
                if (!response.ok) {
                    const parsed = new DOMParser().parseFromString(text, 'text/html');
                    const message = parsed.querySelector(
                        '[data-public-transport-error-message], .public-transport-error p'
                    )?.textContent?.trim();
                    throw new Error(message || response.statusText || text);
                }
                return text;
            }).finally(() => {
                active.delete(requestKey);
                foreground.delete(requestKey);
                render();
            });
            active.set(requestKey, promise);
        }
        render();
        return { key: requestKey, promise };
    };
    const setForeground = (requestKey, value) => {
        if (requestKey) value ? foreground.add(requestKey) : foreground.delete(requestKey);
        render();
    };
    const backgroundProvider = (provider) => {
        [...foreground].forEach((requestKey) => {
            try {
                if (JSON.parse(requestKey)[0] === provider) foreground.delete(requestKey);
            } catch (error) { /* Ignore keys from older application versions. */ }
        });
        render();
    };
    window.travelManagerPublicTransportRequests = { request, setForeground, backgroundProvider };

    fetch('/api/public-transport/pending-downloads')
        .then((response) => response.ok ? response.json() : { providers: [] })
        .then((data) => (data.providers || []).forEach((provider) => {
            request({ provider, screen: 'lines', refresh: true }).promise
                .catch(() => { /* The partial file remains available for retry. */ });
        }))
        .catch(() => { /* Resumption will be retried on the next launch. */ });
})();
