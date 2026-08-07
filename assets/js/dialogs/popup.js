document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#popup-dialog');
    const title = dialog?.querySelector('#popup-dialog-title');
    const message = dialog?.querySelector('#popup-dialog-message');
    const icon = dialog?.querySelector('#popup-dialog-icon');
    const closeButton = dialog?.querySelector('[data-popup-close]');
    let resolveResult = null;

    if (!layer || !dialog || !title || !message || !icon || !closeButton) return;

    const variants = {
        info: { title: 'Informacja', icon: 'info' },
        success: { title: 'Gotowe', icon: 'circle-check' },
        warning: { title: 'Ostrzeżenie', icon: 'triangle-alert' },
        error: { title: 'Błąd', icon: 'circle-x' }
    };

    const finish = () => {
        dialog.setAttribute('aria-hidden', 'true');
        layer.classList.remove('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'true');
        const resolve = resolveResult;
        resolveResult = null;
        resolve?.();
    };

    const show = ({ type = 'info', title: nextTitle, message: nextMessage } = {}) => {
        if (resolveResult) resolveResult();
        const variant = variants[type] || variants.info;
        title.textContent = nextTitle || variant.title;
        message.textContent = nextMessage || '';
        icon.className = `popup-dialog__icon popup-dialog__icon--${type in variants ? type : 'info'}`;
        icon.innerHTML = `<i data-lucide="${variant.icon}" aria-hidden="true"></i>`;
        dialog.setAttribute('aria-hidden', 'false');
        layer.classList.add('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'false');
        window.lucide?.createIcons({ attrs: { 'stroke-width': 1.8 } });
        return new Promise((resolve) => {
            resolveResult = resolve;
            window.requestAnimationFrame(() => closeButton.focus());
        });
    };

    closeButton.addEventListener('click', finish);
    layer.addEventListener('click', (event) => {
        if (event.target === layer && resolveResult) finish();
    });
    document.addEventListener('keydown', (event) => {
        if ((event.key === 'Escape' || event.key === 'Enter') && resolveResult) finish();
    });

    window.travelManagerDialogs = {
        ...(window.travelManagerDialogs || {}),
        popup: show
    };
    window.travelManagerAlert = (message, type = 'info', title = null) => show({
        type,
        title,
        message: String(message || '')
    });
});
