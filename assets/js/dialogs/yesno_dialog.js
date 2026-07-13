document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#yesno-dialog');
    const title = document.querySelector('#yesno-dialog-title');
    const description = document.querySelector('#yesno-dialog-description');
    const icon = document.querySelector('#yesno-dialog-icon');
    const yesButton = dialog?.querySelector('[data-dialog-result="yes"]');
    const noButton = dialog?.querySelector('[data-dialog-result="no"]');
    let resolveResult = null;

    if (!layer || !dialog || !title || !description || !icon || !yesButton || !noButton) {
        return;
    }

    const finish = (result) => {
        dialog.setAttribute('aria-hidden', 'true');
        layer.classList.remove('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'true');
        const resolve = resolveResult;
        resolveResult = null;
        resolve?.(result);
    };

    const show = ({ title: nextTitle, description: nextDescription, icon: nextIcon = 'warning' }) => {
        if (resolveResult) {
            resolveResult(false);
        }

        title.textContent = nextTitle || 'Potwierdzenie';
        description.textContent = nextDescription || '';
        icon.className = `yesno-dialog__icon yesno-dialog__icon--${nextIcon}`;
        dialog.setAttribute('aria-hidden', 'false');
        layer.classList.add('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'false');

        return new Promise((resolve) => {
            resolveResult = resolve;
            window.requestAnimationFrame(() => noButton.focus());
        });
    };

    yesButton.addEventListener('click', () => finish(true));
    noButton.addEventListener('click', () => finish(false));
    layer.addEventListener('click', (event) => {
        if (event.target === layer && resolveResult) {
            finish(false);
        }
    });
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && resolveResult) {
            finish(false);
        }
    });

    window.travelManagerDialogs = { yesNo: show };
});
