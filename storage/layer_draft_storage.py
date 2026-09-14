"""Independent recovery copy; never included in the user's saved layers."""
from math import isfinite
from core.data.base_json_storage import BaseJsonStorage
from models.settings.custom_layer import CustomLayer


class LayerDraftStorage(BaseJsonStorage):
    def __init__(self, directory):
        super().__init__(directory, 'layer_draft.json', cache_enabled=False)

    def _initialize_default_data(self):
        return {}

    def load(self):
        return self._read().get('draft')

    def save(self, data):
        if not isinstance(data, dict) or type(data.get('version')) is not int or data['version'] != 1:
            raise ValueError('Invalid draft version')
        layer = CustomLayer.from_payload(data.get('layer'))
        baseline = data.get('baseline')
        if baseline is not None:
            baseline_layer = CustomLayer.from_payload(baseline)
            if baseline_layer.id != layer.id:
                raise ValueError('Invalid draft baseline')
        mode = data.get('mode')
        if mode not in (None, 'line', 'curve', 'route', 'area', 'point'):
            raise ValueError('Invalid drawing mode')
        drawing = data.get('drawing', [])
        if not isinstance(drawing, list):
            raise ValueError('Invalid drawing')
        for point in drawing:
            if not isinstance(point, list) or len(point) != 2:
                raise ValueError('Invalid drawing point')
            for value, limit in zip(point, (90, 180)):
                if type(value) not in (int, float) or not -limit <= value <= limit or not isfinite(value):
                    raise ValueError('Invalid drawing coordinate')
        if drawing and mode is None:
            raise ValueError('Drawing requires a mode')
        continuation_id = data.get('continuationId')
        if continuation_id is not None:
            element = next((e for e in layer.elements if e.id == continuation_id), None)
            endpoint = data.get('continuationVertex')
            if (element is None or element.type in ('area', 'point') or mode not in ('line', 'curve', 'route')
                    or type(endpoint) is not int or endpoint not in (0, len(element.points) - 1)
                    or not drawing or drawing[0] != element.points[endpoint]):
                raise ValueError('Invalid continuation')
        style = data.get('style', {})
        # Validate drawing defaults through the same schema as saved elements.
        if not isinstance(style, dict):
            raise ValueError('Invalid drawing style')
        CustomLayer.from_payload({'id': 'style', 'name': 'Style', 'elements': [{
            **style, 'id': 'style', 'type': 'line', 'points': [[0, 0], [1, 1]], 'segments': []
        }]})
        self._write({'draft': {
            'version': 1, 'layer': data['layer'], 'baseline': baseline,
            'mode': mode, 'drawing': drawing, 'continuationId': continuation_id,
            'continuationVertex': data.get('continuationVertex'),
            'style': style,
        }})

    def clear(self):
        self._write({})
