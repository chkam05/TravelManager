(() => {
    const create = (capture, onError) => {
        let timer = null,
            queue = Promise.resolve(),
            last = null;
        const write = (value) => {
            const encoded = JSON.stringify(value);
            if (encoded === last) return queue;
            last = encoded;
            queue = queue
                .catch(() => {})
                .then(() =>
                    window.travelManagerLayerApi.request(
                        '/api/custom-layer-draft',
                        {
                            method: value ? 'PUT' : 'DELETE',
                            ...(value ? { body: encoded } : {}),
                        }
                    )
                )
                .catch((error) => {
                    last = null;
                    onError(error);
                    throw error;
                });
            // Scheduled writes report the error in the editor without unhandled rejections.
            queue.catch(() => {});
            return queue;
        };
        const flush = () => {
            window.clearTimeout(timer);
            timer = null;
            return write(capture());
        };
        return {
            schedule() {
                window.clearTimeout(timer);
                timer = window.setTimeout(() => {
                    flush().catch(() => {});
                }, 400);
            },
            flush,
            clear() {
                window.clearTimeout(timer);
                timer = null;
                return write(null);
            },
            async load() {
                await queue.catch(() => {});
                return (
                    (
                        await window.travelManagerLayerApi.request(
                            '/api/custom-layer-draft'
                        )
                    ).draft || null
                );
            },
        };
    };
    window.travelManagerLayerDraft = { create };
})();
