"""Navigation contract for municipal and railway transport entry points."""
import unittest
from pathlib import Path

from resources.menu import Menu


class MenuTransportNavigationTests(unittest.TestCase):
    def test_transport_has_a_separate_menu_section_after_favourites(self):
        sections = [
            [item.url for item in section['items']]
            for section in Menu.menu_sections()
        ]
        self.assertEqual(
            sections[2],
            ['transport:city', 'transport:rail']
        )
        self.assertEqual(sections[1][-1], 'view:favourites')
        self.assertEqual(sections[3][0], 'view:fuel-cost')

    def test_home_transport_group_contains_city_and_train_tiles(self):
        transport = [
            item
            for section in Menu.home_sections()
            for item in section['items']
            if item.url.startswith('transport:')
        ]
        self.assertEqual(
            [item.url for item in transport],
            ['transport:city', 'transport:rail']
        )
        self.assertEqual(transport[1].icon, 'train-front')

    def test_menu_separators_cannot_collapse_when_menu_gets_taller(self):
        stylesheet = (
            Path(__file__).resolve().parents[1] / 'assets/css/index.css'
        ).read_text(encoding='utf-8')
        self.assertRegex(
            stylesheet,
            r'\.side-menu__separator\s*\{[^}]*flex:\s*0 0 1px;'
        )
        self.assertRegex(
            stylesheet,
            r'\.side-menu__navigation\s*\{[^}]*overflow-y:\s*auto;'
        )


if __name__ == '__main__':
    unittest.main()
