(() => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    const textWidth = (element) => {
        if (!context) return element.scrollWidth;
        const style = window.getComputedStyle(element);
        context.font = style.font || [
            style.fontWeight,
            style.fontSize,
            style.fontFamily
        ].join(' ');
        return context.measureText(element.textContent?.trim() || '').width;
    };

    const resize = (root = document) => {
        root.querySelectorAll('.public-transport-lines').forEach((lines) => {
            const labels = Array.from(lines.querySelectorAll('.public-transport-lines__number'));
            const minimum = Number.parseFloat(
                window.getComputedStyle(lines).getPropertyValue(
                    '--public-transport-line-tile-min-width'
                )
            ) || 92;
            const longest = labels.reduce((width, label) => {
                const parts = Array.from(label.querySelectorAll('strong, small'));
                return Math.max(
                    width,
                    ...(parts.length ? parts.map(textWidth) : [textWidth(label)])
                );
            }, 0);
            lines.style.setProperty(
                '--public-transport-line-tile-width',
                `${Math.ceil(Math.max(minimum, longest + 22))}px`
            );
        });

        root.querySelectorAll('.public-transport-stops__lines').forEach((lines) => {
            const identities = Array.from(lines.querySelectorAll(
                '.public-transport-line-pill__identity'
            ));
            const minimum = 104;
            const longest = identities.reduce((width, identity) => {
                const labels = identity.querySelectorAll('strong, small');
                return Math.max(
                    width,
                    ...Array.from(labels, (label) => textWidth(label))
                );
            }, 0);
            lines.style.setProperty(
                '--public-transport-stop-line-width',
                `${Math.ceil(Math.max(minimum, longest + 52))}px`
            );
        });
    };

    window.travelManagerSizePublicTransportLineTiles = resize;
    document.fonts?.ready.then(() => resize()).catch(() => {});
})();
