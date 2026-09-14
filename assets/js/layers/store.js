(() => {
    const request = async (url, options = {}) => {
        const response = await fetch(url, {
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            ...options,
        });
        if (!response.ok) {
            const error = new Error('Request failed');
            error.status = response.status;
            throw error;
        }
        return response.json();
    };
    let generation = 0;
    let cached = null;
    let pending = null;
    const invalidate = () => {
        generation += 1;
        cached = null;
        pending = null;
    };
    // Registered before consumers, so every handler sees the same fresh generation.
    document.addEventListener(
        'travel-manager:custom-layers-changed',
        invalidate
    );
    const list = async () => {
        if (cached !== null) return structuredClone(cached);
        if (!pending) {
            const version = generation;
            const read = request('/api/custom-layers')
                .then((data) => {
                    if (version !== generation) return list();
                    if (!Array.isArray(data.layers))
                        throw new Error('Invalid layer list');
                    cached = data.layers;
                    return cached;
                })
                .catch((error) => {
                    if (version !== generation) return list();
                    throw error;
                })
                .finally(() => {
                    if (pending === read) pending = null;
                });
            pending = read;
        }
        return structuredClone(await pending);
    };
    const changed = () =>
        document.dispatchEvent(
            new CustomEvent('travel-manager:custom-layers-changed')
        );
    const mutate = async (url, options) => {
        const result = await request(url, options);
        changed();
        return result;
    };
    window.travelManagerLayerApi = { request };
    window.travelManagerCustomLayers = {
        list,
        save: (layer) =>
            mutate('/api/custom-layers', {
                method: 'POST',
                body: JSON.stringify(layer),
            }),
        delete: (id) =>
            mutate(`/api/custom-layers/${encodeURIComponent(id)}`, {
                method: 'DELETE',
            }),
        refresh: () => {
            changed();
            return list();
        },
    };
})();
