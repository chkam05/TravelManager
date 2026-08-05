document.addEventListener('travel-manager:views-ready', () => {
    const layer = document.querySelector('#dialog-layer');
    const dialog = document.querySelector('#color-picker-dialog');
    const canvas = dialog?.querySelector('[data-color-picker-canvas]');
    const hueInput = dialog?.querySelector('[data-color-picker-hue]');
    const hexInput = dialog?.querySelector('[data-color-picker-hex]');
    const redInput = dialog?.querySelector('[data-color-picker-r]');
    const greenInput = dialog?.querySelector('[data-color-picker-g]');
    const blueInput = dialog?.querySelector('[data-color-picker-b]');
    const preview = dialog?.querySelector('[data-color-picker-preview]');
    const cancelButtons = dialog?.querySelectorAll('[data-color-picker-cancel]');
    const context = canvas?.getContext('2d');
    let hue = 207;
    let saturation = 0.72;
    let value = 0.68;
    let resolveResult = null;

    if (!layer || !dialog || !canvas || !context || !hueInput || !hexInput || !redInput || !greenInput || !blueInput || !preview || !cancelButtons?.length) return;

    const clamp = (number, min, max) => Math.min(max, Math.max(min, Number(number) || 0));
    const rgbToHex = (red, green, blue) => `#${[red, green, blue].map((item) => clamp(Math.round(item), 0, 255).toString(16).padStart(2, '0')).join('').toUpperCase()}`;
    const hexToRgb = (hex) => {
        const match = /^#?([0-9a-f]{6})$/i.exec(String(hex || '').trim());
        if (!match) return null;
        const valueNumber = Number.parseInt(match[1], 16);
        return { red: valueNumber >> 16, green: (valueNumber >> 8) & 255, blue: valueNumber & 255 };
    };
    const hsvToRgb = (h, s, v) => {
        const chroma = v * s;
        const part = (h / 60) % 6;
        const x = chroma * (1 - Math.abs((part % 2) - 1));
        const offset = v - chroma;
        const values = part < 1 ? [chroma, x, 0] : part < 2 ? [x, chroma, 0] : part < 3 ? [0, chroma, x] : part < 4 ? [0, x, chroma] : part < 5 ? [x, 0, chroma] : [chroma, 0, x];
        return values.map((item) => Math.round((item + offset) * 255));
    };
    const rgbToHsv = (red, green, blue) => {
        const r = red / 255; const g = green / 255; const b = blue / 255;
        const max = Math.max(r, g, b); const min = Math.min(r, g, b); const delta = max - min;
        let nextHue = 0;
        if (delta && max === r) nextHue = 60 * (((g - b) / delta) % 6);
        else if (delta && max === g) nextHue = 60 * (((b - r) / delta) + 2);
        else if (delta) nextHue = 60 * (((r - g) / delta) + 4);
        return { hue: (nextHue + 360) % 360, saturation: max ? delta / max : 0, value: max };
    };
    const drawCanvas = () => {
        const width = canvas.width; const height = canvas.height;
        context.fillStyle = `hsl(${hue}, 100%, 50%)`;
        context.fillRect(0, 0, width, height);
        const white = context.createLinearGradient(0, 0, width, 0);
        white.addColorStop(0, '#fff'); white.addColorStop(1, 'rgba(255,255,255,0)');
        context.fillStyle = white; context.fillRect(0, 0, width, height);
        const black = context.createLinearGradient(0, 0, 0, height);
        black.addColorStop(0, 'rgba(0,0,0,0)'); black.addColorStop(1, '#000');
        context.fillStyle = black; context.fillRect(0, 0, width, height);
        const x = saturation * width; const y = (1 - value) * height;
        context.beginPath(); context.arc(x, y, 7, 0, Math.PI * 2);
        context.lineWidth = 3; context.strokeStyle = '#fff'; context.stroke();
        context.beginPath(); context.arc(x, y, 9, 0, Math.PI * 2);
        context.lineWidth = 1; context.strokeStyle = '#20242a'; context.stroke();
    };
    const syncFromHsv = () => {
        const [red, green, blue] = hsvToRgb(hue, saturation, value);
        const hex = rgbToHex(red, green, blue);
        hexInput.value = hex; redInput.value = red; greenInput.value = green; blueInput.value = blue;
        hueInput.value = String(Math.round(hue)); preview.style.background = hex; drawCanvas();
    };
    const syncFromRgb = () => {
        const red = clamp(redInput.value, 0, 255); const green = clamp(greenInput.value, 0, 255); const blue = clamp(blueInput.value, 0, 255);
        redInput.value = red; greenInput.value = green; blueInput.value = blue;
        const hsv = rgbToHsv(red, green, blue); hue = hsv.hue; saturation = hsv.saturation; value = hsv.value;
        syncFromHsv();
    };
    const setHex = (hex) => {
        const rgb = hexToRgb(hex); if (!rgb) return false;
        redInput.value = rgb.red; greenInput.value = rgb.green; blueInput.value = rgb.blue; syncFromRgb(); return true;
    };
    const pickCanvas = (event) => {
        const bounds = canvas.getBoundingClientRect();
        saturation = clamp((event.clientX - bounds.left) / bounds.width, 0, 1);
        value = 1 - clamp((event.clientY - bounds.top) / bounds.height, 0, 1);
        syncFromHsv();
    };
    const finish = (result) => {
        dialog.setAttribute('aria-hidden', 'true'); layer.classList.remove('dialog-layer--open'); layer.setAttribute('aria-hidden', 'true');
        const resolve = resolveResult; resolveResult = null; resolve?.(result);
    };
    const show = (initialColor = '#1F6FAE') => {
        if (resolveResult) resolveResult(null);
        setHex(initialColor); dialog.setAttribute('aria-hidden', 'false'); layer.classList.add('dialog-layer--open'); layer.setAttribute('aria-hidden', 'false');
        return new Promise((resolve) => { resolveResult = resolve; window.requestAnimationFrame(() => hexInput.focus()); });
    };

    hueInput.addEventListener('input', () => { hue = clamp(hueInput.value, 0, 359); syncFromHsv(); });
    hexInput.addEventListener('input', () => { if (setHex(hexInput.value)) hexInput.setCustomValidity(''); else hexInput.setCustomValidity('Wpisz kolor w formacie #RRGGBB.'); });
    [redInput, greenInput, blueInput].forEach((input) => input.addEventListener('input', syncFromRgb));
    canvas.addEventListener('pointerdown', (event) => { canvas.setPointerCapture(event.pointerId); pickCanvas(event); });
    canvas.addEventListener('pointermove', (event) => { if (canvas.hasPointerCapture(event.pointerId)) pickCanvas(event); });
    dialog.addEventListener('submit', (event) => { event.preventDefault(); if (setHex(hexInput.value)) finish(hexInput.value.toUpperCase()); });
    cancelButtons.forEach((button) => button.addEventListener('click', () => finish(null)));
    layer.addEventListener('click', (event) => { if (event.target === layer && resolveResult) finish(null); });
    window.travelManagerColorPicker = { show };
});
