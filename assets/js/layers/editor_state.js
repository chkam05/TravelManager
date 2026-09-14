(() => {
    // Only editable/session data lives here; DOM nodes and Leaflet objects stay in the panel.
    const create = () => ({
        layer: null,
        dirty: false,
        mode: null,
        drawing: [],
        selected: null,
        selectedVertex: null,
        selectedSegment: null,
        continuation: null,
        continuationVertex: null,
        renamingId: null,
        saving: null,
        transitioning: false,
        persistedSnapshot: null,
        history: [],
        historyIndex: -1,
        resetHistory() {
            this.history = this.layer ? [JSON.stringify(this.layer)] : [];
            this.historyIndex = this.history.length - 1;
        },
        recordChange() {
            if (!this.layer) return;
            const snapshot = JSON.stringify(this.layer);
            if (this.history[this.historyIndex] !== snapshot) {
                this.history.splice(this.historyIndex + 1);
                this.history.push(snapshot);
                if (this.history.length > 101) this.history.shift();
                this.historyIndex = this.history.length - 1;
            }
            this.dirty = snapshot !== this.persistedSnapshot;
        },
        restoreHistory(direction) {
            const index = this.historyIndex + direction;
            if (index < 0 || index >= this.history.length) return false;
            const selectedId = this.selected?.id;
            this.historyIndex = index;
            this.layer = JSON.parse(this.history[index]);
            this.selected =
                this.layer.elements.find(
                    (element) => element.id === selectedId
                ) || null;
            this.selectedVertex = null;
            this.selectedSegment = null;
            this.dirty = this.history[index] !== this.persistedSnapshot;
            return true;
        },
        hasChanges(hasSketch = false, hasPendingName = false) {
            return Boolean(
                this.layer &&
                (this.dirty ||
                    hasSketch ||
                    hasPendingName ||
                    (this.persistedSnapshot !== null &&
                        JSON.stringify(this.layer) !== this.persistedSnapshot))
            );
        },
        acceptSnapshot(snapshot) {
            this.persistedSnapshot = snapshot;
            this.dirty = JSON.stringify(this.layer) !== snapshot;
        },
    });
    window.travelManagerLayerEditorState = { create };
})();
