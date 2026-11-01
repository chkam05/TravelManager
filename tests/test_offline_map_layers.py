from __future__ import annotations

import unittest

from resources.offline_maps import OfflineMapLayers


class OfflineMapLayerDefinitionTests(unittest.TestCase):
    def test_minimal_layer_set_is_complete_and_unique(self):
        expected = {
            'water', 'landuse', 'buildings', 'roads', 'railways',
            'boundaries', 'places', 'pois',
        }
        self.assertEqual(set(OfflineMapLayers.BY_ID), expected)
        self.assertEqual(
            len(OfflineMapLayers.DEFINITIONS), len(OfflineMapLayers.BY_ID)
        )
        priorities = [item.priority for item in OfflineMapLayers.DEFINITIONS]
        self.assertEqual(priorities, sorted(priorities))

    def test_representative_osm_features_match_expected_layers(self):
        cases = (
            ('way', 'polygon', {'natural': 'water'}, {'water'}),
            ('way', 'polygon', {'landuse': 'forest'}, {'landuse'}),
            ('way', 'polygon', {'building': 'apartments'}, {'buildings'}),
            ('way', 'line', {'highway': 'primary'}, {'roads'}),
            ('way', 'line', {'railway': 'rail'}, {'railways'}),
            (
                'relation', 'polygon',
                {'boundary': 'administrative', 'admin_level': '4'},
                {'boundaries'},
            ),
            ('node', 'point', {'place': 'city'}, {'places'}),
            ('node', 'point', {'amenity': 'fuel'}, {'pois'}),
        )
        for source, geometry, tags, expected in cases:
            with self.subTest(tags=tags):
                self.assertEqual(
                    {
                        item.id for item in OfflineMapLayers.matching(
                            source, geometry, tags
                        )
                    },
                    expected,
                )

    def test_unsupported_or_inactive_features_are_filtered_out(self):
        for source, geometry, tags in (
            ('node', 'point', {'amenity': 'bench'}),
            ('way', 'line', {'highway': 'construction'}),
            ('way', 'line', {'railway': 'rail', 'service': 'yard'}),
            ('node', 'point', {'shop': 'clothes'}),
        ):
            with self.subTest(tags=tags):
                self.assertEqual(
                    OfflineMapLayers.matching(source, geometry, tags), ()
                )

    def test_major_features_become_visible_at_lower_zoom(self):
        roads = OfflineMapLayers.BY_ID['roads']
        self.assertEqual(roads.minimum_zoom({'highway': 'motorway'}), 5)
        self.assertEqual(roads.minimum_zoom({'highway': 'primary'}), 7)
        self.assertEqual(roads.minimum_zoom({'highway': 'residential'}), 13)

        places = OfflineMapLayers.BY_ID['places']
        self.assertEqual(places.minimum_zoom({'place': 'country'}), 3)
        self.assertEqual(places.minimum_zoom({'place': 'city'}), 7)
        self.assertEqual(places.minimum_zoom({'place': 'hamlet'}), 12)

    def test_generalisation_decreases_as_zoom_increases(self):
        for definition in OfflineMapLayers.DEFINITIONS:
            values = [
                definition.simplification_for_zoom(zoom)
                for zoom in range(0, 16)
            ]
            self.assertTrue(all(
                current >= following
                for current, following in zip(values, values[1:])
            ), definition.id)

    def test_only_whitelisted_properties_reach_vector_tiles(self):
        roads = OfflineMapLayers.BY_ID['roads']
        result = roads.mvt_properties({
            'name': 'A4', 'highway': 'motorway', 'surface': 'asphalt',
            'phone': '+48 secret', 'note': 'internal', 'empty': '',
        })
        self.assertEqual(result, {
            'name': 'A4', 'highway': 'motorway', 'surface': 'asphalt',
        })

    def test_required_tag_projection_contains_filters_and_output_fields(self):
        required = OfflineMapLayers.required_tags()
        for key in (
            'name', 'name:pl', 'highway', 'building', 'admin_level',
            'amenity', 'tourism', 'place', 'railway',
        ):
            self.assertIn(key, required)
        self.assertNotIn('phone', required)


if __name__ == '__main__':
    unittest.main()
