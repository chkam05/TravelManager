from typing import ClassVar

from models.menu.menu_group import MenuGroup
from models.menu.menu_item import MenuItem


class Menu:
    """Central navigation definitions used by the menu and home view."""

    def __new__(cls, *args, **kwargs):
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    GROUPS: ClassVar[list[MenuGroup]] = [
        MenuGroup(0, 'MAIN_MENU.GROUP_HOME', '', -1, 0),
        MenuGroup(1, 'HOME_VIEW.GROUP_MAP', 'HOME_VIEW.GROUP_MAP_DESCRIPTION', 0, -1),
        MenuGroup(2, 'HOME_VIEW.GROUP_TRAVEL', 'HOME_VIEW.GROUP_TRAVEL_DESCRIPTION', 1, -1),
        MenuGroup(3, 'HOME_VIEW.GROUP_PUBLIC_TRANSPORT', 'HOME_VIEW.GROUP_PUBLIC_TRANSPORT_DESCRIPTION', 2, -1),
        MenuGroup(4, 'HOME_VIEW.GROUP_APPLICATION', 'HOME_VIEW.GROUP_APPLICATION_DESCRIPTION', 3, -1),
        MenuGroup(10, 'MAIN_MENU.GROUP_MAIN_FEATURES', '', -1, 1),
        MenuGroup(11, 'MAIN_MENU.GROUP_TRAVEL_DATA', '', -1, 2),
        MenuGroup(12, 'MAIN_MENU.GROUP_APPLICATION', '', -1, 3)
    ]

    ITEMS: ClassVar[list[MenuItem]] = [
        MenuItem('house', 'MAIN_MENU.HOME', 'MAIN_MENU.HOME_DESCRIPTION', 'view:home', -1, 0),
        MenuItem('map', 'MAIN_MENU.MAP', 'MAIN_MENU.MAP_DESCRIPTION', 'view:map', 1, 10),
        MenuItem('bus-front', 'MAIN_MENU.PUBLIC_TRANSPORT', 'MAIN_MENU.PUBLIC_TRANSPORT_DESCRIPTION', 'view:public-transport', 3, 10),
        MenuItem('route', 'MAIN_MENU.ROUTES', 'MAIN_MENU.ROUTES_DESCRIPTION', 'view:my-routes', 2, 10),
        MenuItem('navigation', 'MAIN_MENU.NEW_ROUTE', 'MAIN_MENU.NEW_ROUTE_DESCRIPTION', 'action:new-route', 2, 10),
        MenuItem('star', 'MAIN_MENU.FAVOURITES', 'MAIN_MENU.FAVOURITES_DESCRIPTION', 'view:favourites', 1, 10),
        MenuItem('fuel', 'MAIN_MENU.FUEL', 'MAIN_MENU.FUEL_DESCRIPTION', 'view:fuel-cost', 2, 11),
        MenuItem('car', 'MAIN_MENU.CARS', 'MAIN_MENU.CARS_DESCRIPTION', 'view:car-profiles', 2, 11),
        MenuItem('tags', 'MAIN_MENU.TAGS', 'MAIN_MENU.TAGS_DESCRIPTION', 'view:favourites-tags', 1, 11),
        MenuItem('settings', 'MAIN_MENU.SETTINGS', 'MAIN_MENU.SETTINGS_DESCRIPTION', 'view:settings', 4, 12),
        MenuItem('info', 'MAIN_MENU.INFORMATION', 'MAIN_MENU.INFORMATION_DESCRIPTION', 'view:information', 4, 12)
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
