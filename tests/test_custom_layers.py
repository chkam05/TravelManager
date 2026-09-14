"""Regression coverage for layer validation, persistence and concurrent writers."""
import json
from concurrent.futures import ThreadPoolExecutor
from tempfile import TemporaryDirectory
import threading
import time
import unittest
from unittest.mock import patch

from flask import Flask
from controllers.settings_controller import SettingsController
from storage.settings_storage import SettingsStorage


def payload(layer_id='layer-1'):
    return {'id': layer_id, 'name': 'Test', 'elements': [{
        'id': 'element-1', 'name': '', 'type': 'line',
        'points': [[50, 20], [51, 21]], 'color': '#123456', 'width': 4,
        'segments': [{'type': 'curve', 'control1': [50.2, 20.2], 'control2': [50.8, 20.8]}],
    }]}


class LayerTests(unittest.TestCase):
    def test_element_visibility_and_lock_flags_round_trip_and_validate(self):
        from models.settings.custom_layer import CustomLayer
        data = payload()
        legacy = CustomLayer.from_payload(data).to_dict()['elements'][0]
        self.assertFalse(legacy['hidden'])
        self.assertFalse(legacy['locked'])
        data['elements'][0].update(hidden=True, locked=True)
        restored = CustomLayer.from_dict(CustomLayer.from_payload(data).to_dict()).to_dict()
        self.assertTrue(restored['elements'][0]['hidden'])
        self.assertTrue(restored['elements'][0]['locked'])
        for flag in ('hidden', 'locked'):
            invalid = payload()
            invalid['elements'][0][flag] = 'false'
            with self.assertRaises(ValueError):
                CustomLayer.from_payload(invalid)

    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        settings_dir = patch('storage.settings_storage.SETTINGS_DIR', self.directory.name)
        settings_dir.start()
        self.addCleanup(settings_dir.stop)
        self.storage = SettingsStorage()
        self.app = Flask(__name__)
        self.app.testing = True
        self.app.register_blueprint(SettingsController(self.storage))
        self.client = self.app.test_client()

    def test_recovery_draft_survives_restart_without_changing_saved_layers(self):
        draft = {'version': 1, 'layer': payload(), 'baseline': payload(),
                 'mode': 'area', 'drawing': [[52, 21]], 'style': {}}
        response = self.client.put('/api/custom-layer-draft', json=draft)
        self.assertEqual(response.status_code, 200)
        from storage.layer_draft_storage import LayerDraftStorage
        restored = LayerDraftStorage(self.directory.name).load()
        self.assertEqual(restored['drawing'], [[52, 21]])
        self.assertEqual(self.storage.load().custom_layers, [])
        self.assertEqual(self.client.delete('/api/custom-layer-draft').status_code, 200)
        self.assertIsNone(self.client.get('/api/custom-layer-draft').json['draft'])

    def test_invalid_recovery_data_does_not_replace_previous_draft(self):
        draft = {'version': 1, 'layer': payload(), 'mode': 'line', 'drawing': [[50, 20]]}
        self.assertEqual(self.client.put('/api/custom-layer-draft', json=draft).status_code, 200)
        for change in ({'version': 2}, {'layer': None}, {'drawing': [[999, 20]]},
                       {'drawing': [None]}, {'mode': 'unknown'}, {'style': {'color': 'bad'}},
                       {'continuationId': 'missing'}):
            self.assertEqual(self.client.put('/api/custom-layer-draft', json={**draft, **change}).status_code, 400)
        self.assertEqual(self.client.get('/api/custom-layer-draft').json['draft']['drawing'], [[50, 20]])

    def test_editor_width_survives_new_storage_instance(self):
        response = self.client.patch('/api/settings/ui', json={'layer_editor_panel_width': 580})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SettingsStorage().load().ui.layer_editor_panel_width, 580)
        self.assertEqual(self.client.get('/api/settings/ui').json['ui']['layer_editor_panel_width'], 580)

    def test_round_trip_and_retry_use_same_id(self):
        for _ in range(2):
            result = self.client.post('/api/custom-layers', json=payload())
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json['layer']['elements'][0]['segments'], payload()['elements'][0]['segments'])
        self.assertEqual(len(self.storage.load().custom_layers), 1)
        exported = self.storage.export_layers()
        self.assertEqual(self.client.delete('/api/custom-layers/layer-1').status_code, 200)
        self.storage.import_layers(exported)
        self.assertEqual(self.storage.load().custom_layers[0].id, 'layer-1')

    def test_valid_area_and_legacy_straight_segments(self):
        data = payload()
        element = data['elements'][0]
        element.update(type='area', points=[[50, 20], [51, 21], [50, 22]])
        del element['segments']
        result = self.client.post('/api/custom-layers', json=data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['layer']['elements'][0]['segments'], [{'type': 'line'}] * 3)

    def test_invalid_payloads_are_rejected_by_api_and_import_without_writes(self):
        self.client.post('/api/custom-layers', json=payload())
        before = self.storage.file_path.read_bytes()
        bad = [None, [], 'layer', {'id': 'x', 'name': None, 'elements': []}]
        for field, value in [('elements', None), ('elements', [None]), ('elements', ['bad']),
                             ('id', '../bad'), ('id', 12), ('show_title', 'false'), ('name', ' ')]:
            data = payload(); data[field] = value; bad.append(data)
        for field, value in [
            ('id', ''), ('id', None), ('type', 'point'), ('points', [[91, 20], [50, 20]]),
            ('points', [[50, 181], [51, 20]]), ('points', [[float('nan'), 20], [51, 20]]),
            ('points', [[float('inf'), 20], [51, 20]]), ('points', [[True, 20], [51, 20]]),
            ('points', [['50', 20], [51, 20]]), ('points', [[50, 20]]),
            ('points', [[50, 20], [50, 20]]), ('type', 'area'), ('width', 21), ('width', 1.5),
            ('width', True), ('color', 'red'), ('background_color', '#bad'),
            ('line_style', 'unknown'), ('segments', None), ('segments', [None]),
            ('segments', [{'type': 'curve'}]), ('segments', [{'type': 'line', 'control1': [50, 20]}]),
            ('segments', [{'type': 'line'}, {'type': 'line'}]),
            ('segments', [{'type': 'curve', 'control1': [50, 20], 'control2': [999, 20]}]),
        ]:
            data = payload(); data['elements'][0][field] = value; bad.append(data)
        duplicate = payload(); duplicate['elements'] *= 2; bad.append(duplicate)
        for data in bad:
            with self.subTest(data=data):
                result = self.client.post('/api/custom-layers', data=json.dumps(data), content_type='application/json')
                self.assertEqual(result.status_code, 400)
                with self.assertRaises(ValueError):
                    self.storage.import_layers(json.dumps({'layers': [data]}))
                self.assertEqual(self.storage.file_path.read_bytes(), before)

    def test_duplicate_import_layer_ids_are_rejected_atomically(self):
        self.client.post('/api/custom-layers', json=payload())
        before = self.storage.file_path.read_bytes()
        with self.assertRaises(ValueError):
            self.storage.import_layers(json.dumps({'layers': [payload(), payload()]}))
        self.assertEqual(self.storage.file_path.read_bytes(), before)

    def test_concurrent_layer_saves_preserve_every_layer(self):
        barrier = threading.Barrier(8)
        def write(index):
            barrier.wait(timeout=5)
            with self.app.test_client() as client:
                return client.post('/api/custom-layers', json=payload(f'layer-{index}')).status_code
        with ThreadPoolExecutor(max_workers=8) as pool:
            self.assertEqual(list(pool.map(write, range(8))), [200] * 8)
        self.assertEqual(len(self.storage.load().custom_layers), 8)

    def test_other_storage_instance_cannot_overwrite_a_concurrent_layer_save(self):
        other = SettingsStorage()
        entered = threading.Event()
        release = threading.Event()
        original_load = self.storage.load
        def slow_load():
            settings = original_load()
            entered.set()
            self.assertTrue(release.wait(timeout=5))
            return settings
        def save_layer():
            with self.app.test_client() as client:
                return client.post('/api/custom-layers', json=payload()).status_code
        def save_other_setting():
            with other.transaction():
                settings = other.load()
                settings.selected_exchange_rate = 'EUR'
                other.save(settings)
        with patch.object(self.storage, 'load', side_effect=slow_load):
            with ThreadPoolExecutor(max_workers=2) as pool:
                first = pool.submit(save_layer)
                self.assertTrue(entered.wait(timeout=5))
                second = pool.submit(save_other_setting)
                try:
                    time.sleep(.05)
                    self.assertFalse(second.done())
                finally:
                    release.set()
                self.assertEqual(first.result(timeout=5), 200)
                second.result(timeout=5)
        result = SettingsStorage().load()
        self.assertEqual(result.custom_layers[0].id, 'layer-1')
        self.assertEqual(result.selected_exchange_rate, 'EUR')


if __name__ == '__main__':
    unittest.main()
