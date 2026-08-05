from typing import ClassVar

from models.menu.menu_group import MenuGroup
from models.menu.menu_item import MenuItem


class Menu:
    """Central navigation definitions used by the menu and home view."""

    def __new__(cls, *args, **kwargs):
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    GROUPS: ClassVar[list[MenuGroup]] = [
        MenuGroup(0, 'Strona główna', '', -1, 0),
        MenuGroup(1, 'Mapa', 'Mapa oraz zapisane miejsca.', 0, -1),
        MenuGroup(2, 'Podróże', 'Planowanie tras, samochody i koszty podróży.', 1, -1),
        MenuGroup(3, 'Komunikacja miejska', 'Linie, przystanki i rozkłady jazdy.', 2, -1),
        MenuGroup(4, 'Ustawienia i informacje', 'Konfiguracja i informacje o aplikacji.', 3, -1),
        MenuGroup(10, 'Główne funkcje', '', -1, 1),
        MenuGroup(11, 'Dane podróży', '', -1, 2),
        MenuGroup(12, 'Aplikacja', '', -1, 3)
    ]

    ITEMS: ClassVar[list[MenuItem]] = [
        MenuItem('house', 'Strona Główna', 'Przejdź do strony głównej.', 'view:home', -1, 0),
        MenuItem('map', 'Mapa', 'Przeglądaj mapę i wybrane miejsca.', 'view:map', 1, 10),
        MenuItem('bus-front', 'Komunikacja miejska', 'Przeglądaj linie, przystanki i rozkłady jazdy.', 'view:public-transport', 3, 10),
        MenuItem('route', 'Moje Trasy', 'Otwieraj i edytuj zapisane trasy.', 'view:my-routes', 2, 10),
        MenuItem('navigation', 'Tworzenie trasy', 'Zaplanuj nową trasę i oblicz jej koszty.', 'action:new-route', 2, 10),
        MenuItem('star', 'Ulubione', 'Przeglądaj zapisane miejsca.', 'view:favourites', 1, 10),
        MenuItem('fuel', 'Ceny paliw', 'Sprawdzaj i aktualizuj ceny paliw w krajach.', 'view:fuel-cost', 2, 11),
        MenuItem('car', 'Samochody', 'Zarządzaj profilami samochodów i ich spalaniem.', 'view:car-profiles', 2, 11),
        MenuItem('tags', 'Tagi ulubionych', 'Porządkuj ulubione miejsca za pomocą tagów.', 'view:favourites-tags', 1, 11),
        MenuItem('settings', 'Ustawienia', 'Dostosuj działanie i dane aplikacji.', 'view:settings', 4, 12),
        MenuItem('info', 'Informacje', 'Sprawdź wersję i informacje o aplikacji.', 'view:information', 4, 12)
    ]

    HOME_ITEM_ORDER: ClassVar[tuple[str, ...]] = (
        'view:map', 'view:favourites', 'view:favourites-tags',
        'action:new-route', 'view:my-routes', 'view:car-profiles', 'view:fuel-cost',
        'view:public-transport', 'view:settings', 'view:information'
    )

    MENU_ITEM_ORDER: ClassVar[tuple[str, ...]] = (
        'view:home', 'view:map', 'view:public-transport', 'view:my-routes',
        'action:new-route', 'view:favourites', 'view:fuel-cost', 'view:car-profiles',
        'view:favourites-tags', 'view:settings', 'view:information'
    )

    @classmethod
    def _sections(
        cls,
        group_field: str,
        index_field: str,
        item_order: tuple[str, ...]
    ) -> list[dict]:
        sections = []
        order = {url: index for index, url in enumerate(item_order)}

        for group in sorted(cls.GROUPS, key=lambda item: getattr(item, index_field)):
            items = [
                item for item in cls.ITEMS
                if getattr(item, group_field) == group.id
            ]
            items.sort(key=lambda item: order.get(item.url, len(order)))

            if items:
                sections.append({'group': group, 'items': items})

        return sections

    @classmethod
    def menu_sections(cls) -> list[dict]:
        return cls._sections('menu_group_id', 'menu_index', cls.MENU_ITEM_ORDER)

    @classmethod
    def home_sections(cls) -> list[dict]:
        return cls._sections('home_group_id', 'home_index', cls.HOME_ITEM_ORDER)
