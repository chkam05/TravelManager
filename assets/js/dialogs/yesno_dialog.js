document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#yesno-dialog');
    const title = document.querySelector('#yesno-dialog-title');
    const description = document.querySelector('#yesno-dialog-description');
    const icon = document.querySelector('#yesno-dialog-icon');
    const yesButton = dialog?.querySelector('[data-dialog-result="yes"]');
    const noButton = dialog?.querySelector('[data-dialog-result="no"]');
    const cancelButton = dialog?.querySelector('[data-dialog-result="cancel"]');
    let resolveResult = null;
    let unsaved = false;
    let choiceInput = null;

    if (
        !layer ||
        !dialog ||
        !title ||
        !description ||
        !icon ||
        !yesButton ||
        !noButton ||
        !cancelButton
    ) {
        return;
    }

    const finish = (result) => {
        dialog.setAttribute('aria-hidden', 'true');
        layer.classList.remove('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'true');
        const resolve = resolveResult;
        resolveResult = null;
        const choice = choiceInput;
        choiceInput = null;
        resolve?.(choice ? (result === true ? choice.value : null) : result);
    };

    const show = ({
        title: nextTitle,
        description: nextDescription,
        icon: nextIcon = 'warning',
        saveDiscardCancel = false,
        yesLabel = null,
        noLabel = null,
        information = false,
        choices = null,
    }) => {
        if (resolveResult) {
            resolveResult(unsaved ? 'cancel' : false);
        }

        unsaved = saveDiscardCancel;
        yesButton.textContent =
            yesLabel || window.i18n.t(unsaved ? 'COMMON.SAVE' : 'COMMON.YES');
        noButton.textContent =
            noLabel ||
            window.i18n.t(unsaved ? 'LAYER_EDITOR.DISCARD' : 'COMMON.NO');
        cancelButton.hidden = !unsaved;
        noButton.hidden = information;
        title.textContent =
            nextTitle || window.i18n.t('DIALOG_YES_NO.CONFIRMATION');
        description.textContent = nextDescription || '';
        choiceInput = null;
        if (choices) {
            choiceInput = document.createElement('select');
            choiceInput.className = 'yesno-dialog__choice';
            choiceInput.setAttribute(
                'aria-label',
                nextDescription || nextTitle
            );
            choices.forEach(([value, label]) => {
                const option = document.createElement('option');
                option.value = value;
                option.textContent = label;
                choiceInput.append(option);
            });
            choiceInput.value = choices[0][0];
            description.append(choiceInput);
        }
        icon.className = `yesno-dialog__icon yesno-dialog__icon--${nextIcon}`;
        dialog.setAttribute('aria-hidden', 'false');
        layer.classList.add('dialog-layer--open');
        layer.setAttribute('aria-hidden', 'false');

        return new Promise((resolve) => {
            resolveResult = resolve;
            window.requestAnimationFrame(() =>
                (information
                    ? yesButton
                    : unsaved
                      ? cancelButton
                      : noButton
                ).focus()
            );
        });
    };

    yesButton.addEventListener('click', () => finish(unsaved ? 'save' : true));
    noButton.addEventListener('click', () =>
        finish(unsaved ? 'discard' : false)
    );
    cancelButton.addEventListener('click', () => finish('cancel'));
    layer.addEventListener('click', (event) => {
        if (event.target === layer && resolveResult) {
            event.preventDefault();
            event.stopImmediatePropagation();
            finish(unsaved ? 'cancel' : false);
        }
    });
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && resolveResult) {
            event.preventDefault();
            event.stopImmediatePropagation();
            finish(unsaved ? 'cancel' : false);
        }
    });

    window.travelManagerDialogs = {
        ...(window.travelManagerDialogs || {}),
        yesNo: show,
        choose: show,
        saveDiscardCancel: (options) =>
            show({ ...options, saveDiscardCancel: true }),
    };
});
