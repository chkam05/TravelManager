import json
import unittest
from services.layer_transfer import export_layer, import_layer
import test_custom_layers as fixtures
payload = fixtures.payload


class TransferTests(unittest.TestCase):
    def test_native_round_trip_preserves_every_field_but_replaces_ids(self):
        data = payload()
        data.update(icon='🗺️', show_title=True)
        data['elements'][0].update(hidden=True, locked=True)
        restored = import_layer(export_layer(data, 'json'))
        self.assertNotEqual(restored['id'], data['id'])
        self.assertNotEqual(restored['elements'][0]['id'], data['elements'][0]['id'])
        restored['id'] = data['id']
        restored['elements'][0]['id'] = data['elements'][0]['id']
        from models.settings.custom_layer import CustomLayer
        self.assertEqual(restored, CustomLayer.from_payload(data).to_dict())

    def test_geojson_samples_curves_and_uses_longitude_first(self):
        exported = json.loads(export_layer(payload(), 'geojson'))
        coords = exported['features'][0]['geometry']['coordinates']
        self.assertEqual(coords[0], [20, 50])
        self.assertEqual(coords[-1], [21, 51])
        self.assertEqual(len(coords), 25)
        imported = import_layer(json.dumps(exported))
        self.assertEqual(imported['elements'][0]['points'][0], [50, 20])
        self.assertTrue(all(e['type'] == 'line' for e in imported['elements'][0]['segments']))

    def test_area_exports_as_polygon_and_closed_gpx_outline(self):
        data = payload()
        data['elements'][0].update(type='area', points=[[50,20],[51,20],[50,21]], segments=[])
        geo = json.loads(export_layer(data, 'geojson'))
        ring = geo['features'][0]['geometry']['coordinates'][0]
        self.assertEqual(ring[0], ring[-1])
        self.assertEqual(import_layer(json.dumps(geo))['elements'][0]['type'], 'area')
        gpx = export_layer(data, 'gpx')
        outline = import_layer(gpx)['elements'][0]
        self.assertEqual(outline['points'][0], outline['points'][-1])
        self.assertEqual(outline['type'], 'route')

    def test_gpx_track_segments_and_routes_share_one_layer(self):
        text = '<gpx xmlns="http://www.topografix.com/GPX/1/1"><metadata><name>A &amp; B</name></metadata><trk><trkseg><trkpt lat="50" lon="20"/><trkpt lat="51" lon="21"/></trkseg><trkseg><trkpt lat="52" lon="22"/><trkpt lat="53" lon="23"/></trkseg></trk><rte><rtept lat="54" lon="24"/><rtept lat="55" lon="25"/></rte></gpx>'
        layer = import_layer(text)
        self.assertEqual(layer['name'], 'A & B')
        self.assertEqual(len(layer['elements']), 3)

    def test_rejects_holes_points_entities_and_invalid_coordinates(self):
        for text in [
            '<!DOCTYPE gpx [<!ENTITY x "test">]><gpx/>',
            '<gpx><wpt lat="95" lon="20"/></gpx>',
            json.dumps({'type':'Point','coordinates':[20,95]}),
            json.dumps({'type':'Polygon','coordinates': [[[20,50],[21,50],[20,51],[20,50]]]*2}),
            json.dumps({'type':'LineString','coordinates':[[20,95],[21,50]]}),
        ]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                import_layer(text)

    def test_multigeometries_become_shapes_in_one_layer(self):
        data = {'type':'FeatureCollection','features':[{'type':'Feature','properties':{'name':'Two'},'geometry':{'type':'MultiLineString','coordinates':[[[20,50],[21,51]],[[22,52],[23,53]]]}}]}
        layer = import_layer(json.dumps(data))
        self.assertEqual(len(layer['elements']), 2)
        self.assertEqual([e['name'] for e in layer['elements']], ['Two','Two'])


class TransferApiTests(unittest.TestCase):
    setUp = fixtures.LayerTests.setUp
    def test_preview_is_read_only_and_import_preserves_existing_layer(self):
        data = payload()
        self.client.post('/api/custom-layers', json=data)
        response = self.client.get('/api/custom-layers/layer-1/export/json')
        self.assertEqual(response.status_code, 200)
        exported = response.json
        preview = self.client.post('/api/custom-layers/parse', json=exported)
        self.assertEqual(preview.status_code, 200)
        self.assertEqual(len(self.client.get('/api/custom-layers').json['layers']),1)
        self.client.post('/api/custom-layers', json=preview.json['layer'])
        self.assertEqual(len(self.client.get('/api/custom-layers').json['layers']),2)

    def test_invalid_input_never_changes_saved_layers(self):
        self.client.post('/api/custom-layers', json=payload())
        for text in ['<gpx>', '{', '{"type":"LineString","coordinates":null}', '<gpx><trk><trkseg><trkpt/></trkseg></trk></gpx>']:
            response = self.client.post('/api/custom-layers/parse', json={'text':text})
            self.assertEqual(response.status_code,400)
        self.assertEqual(len(self.client.get('/api/custom-layers').json['layers']),1)
        self.assertEqual(self.client.get('/api/custom-layers/layer-1/export/invalid').status_code,400)

class PointTransferTests(unittest.TestCase):
    def test_point_note_round_trip_in_all_three_formats(self):
        data = {'id':'points','name':'Stops','elements':[{'id':'point','name':'Parking & entrance','type':'point','points':[[50,20]],'icon':'🚗','note':'First line\n<second>'}]}
        for format in ('json','geojson','gpx'):
            with self.subTest(format=format):
                result = import_layer(export_layer(data,format))['elements'][0]
                for key in ('name','type','points','icon','note'):
                    self.assertEqual(result[key],data['elements'][0][key])

    def test_point_requires_exactly_one_position_and_bounded_note(self):
        from models.settings.custom_layer import CustomLayer
        data = {'id':'points','name':'Stops','elements':[{'id':'point','type':'point','points':[[50,20],[51,21]]}]}
        with self.assertRaises(ValueError):
            CustomLayer.from_payload(data)
        data['elements'][0].update(points=[[50,20]],note='x'*4001)
        with self.assertRaises(ValueError):
            CustomLayer.from_payload(data)
