from typing import ClassVar


class MapSearchConfig:
    """Advanced map search categories, OSM filters and fallback terms."""

    def __new__(cls, *args, **kwargs):
        raise TypeError(f'{cls.__name__} is a static utility class and cannot be instantiated.')

    GROUPS: ClassVar[dict[str, tuple[str, ...]]] = {
        'food': ('bar', 'cafe', 'takeaway', 'restaurant', 'delivery', 'fast_food', 'pub', 'food_court'),
        'attractions': ('attraction', 'library', 'cinema', 'museum', 'live_music', 'park', 'gym', 'art', 'nightlife', 'theatre', 'zoo'),
        'shopping': ('mall', 'garden', 'chemist', 'electronics', 'local', 'sports', 'grocery', 'car_sales', 'clothes', 'books'),
        'services': ('pharmacy', 'car_wash', 'atm', 'hotel', 'parking', 'laundry', 'beauty', 'charging', 'fuel', 'healthcare', 'courier', 'car_rental', 'post_office')
    }
    FILTERS: ClassVar[dict[str, list[dict[str, str | tuple[str, ...] | None]]]] = {
        'bar': [{'amenity': ('bar', 'pub', 'biergarten')}],
        'cafe': [{'amenity': 'cafe'}, {'shop': 'coffee'}],
        'takeaway': [
            {'amenity': ('restaurant', 'fast_food', 'cafe', 'bar', 'pub'), 'takeaway': ('yes', 'only')},
            {'shop': ('food', 'deli', 'bakery', 'confectionery'), 'takeaway': ('yes', 'only')},
            {'amenity': ('fast_food', 'food_court')},
            {'shop': ('bakery', 'confectionery', 'deli')}
        ],
        'restaurant': [{'amenity': 'restaurant'}],
        'delivery': [
            {'amenity': ('restaurant', 'fast_food', 'cafe'), 'delivery': 'yes'},
            {'shop': ('food', 'deli', 'bakery', 'confectionery'), 'delivery': 'yes'},
            {'amenity': ('restaurant', 'fast_food')}
        ],
        'fast_food': [{'amenity': 'fast_food'}],
        'pub': [{'amenity': ('pub', 'bar', 'biergarten')}],
        'food_court': [{'amenity': 'food_court'}],
        'attraction': [{'tourism': 'attraction'}, {'tourism': 'theme_park'}],
        'library': [{'amenity': 'library'}],
        'cinema': [{'amenity': 'cinema'}],
        'museum': [{'tourism': 'museum'}],
        'live_music': [{'amenity': 'music_venue'}, {'live_music': 'yes'}],
        'park': [{'leisure': ('park', 'garden')}, {'boundary': 'national_park'}],
        'gym': [{'leisure': 'fitness_centre'}, {'amenity': 'gym'}, {'sport': 'fitness'}],
        'art': [{'tourism': 'gallery'}, {'amenity': 'arts_centre'}, {'shop': 'art'}],
        'nightlife': [{'amenity': ('nightclub', 'bar', 'pub', 'biergarten')}],
        'theatre': [{'amenity': 'theatre'}],
        'zoo': [{'tourism': 'zoo'}],
        'mall': [{'shop': ('mall', 'department_store')}, {'landuse': 'retail'}],
        'garden': [{'shop': ('garden_centre', 'doityourself', 'hardware', 'houseware', 'furniture', 'interior_decoration')}],
        'chemist': [{'shop': ('chemist', 'cosmetics', 'perfumery', 'beauty')}],
        'electronics': [{'shop': ('electronics', 'computer', 'mobile_phone', 'hifi', 'appliance')}],
        'local': [{'shop': ('convenience', 'kiosk', 'general', 'variety_store')}],
        'sports': [{'shop': ('sports', 'outdoor', 'bicycle', 'fishing', 'hunting')}],
        'grocery': [{'shop': ('supermarket', 'convenience', 'grocery', 'greengrocer', 'bakery', 'butcher', 'deli')}],
        'car_sales': [{'shop': ('car', 'car_repair', 'car_parts', 'tyres')}],
        'clothes': [{'shop': ('clothes', 'shoes', 'fashion', 'boutique', 'jewelry', 'bag')}],
        'books': [{'shop': ('books', 'stationery', 'newsagent')}],
        'pharmacy': [{'amenity': 'pharmacy'}, {'healthcare': 'pharmacy'}],
        'car_wash': [{'amenity': 'car_wash'}],
        'atm': [{'amenity': 'atm'}, {'amenity': 'bank', 'atm': 'yes'}],
        'hotel': [{'tourism': ('hotel', 'motel', 'guest_house', 'hostel', 'apartment')}],
        'parking': [{'amenity': ('parking', 'parking_entrance')}],
        'laundry': [{'shop': ('laundry', 'dry_cleaning')}],
        'beauty': [{'shop': ('beauty', 'hairdresser', 'massage', 'tattoo')}],
        'charging': [{'amenity': 'charging_station'}],
        'fuel': [{'amenity': 'fuel'}],
        'healthcare': [
            {'amenity': ('hospital', 'clinic', 'doctors', 'dentist')},
            {'healthcare': ('hospital', 'clinic', 'doctor', 'dentist', 'centre')}
        ],
        'courier': [
            {'amenity': ('parcel_locker', 'post_office', 'post_depot')},
            {'parcel_pickup': 'yes'},
            {'parcel_dropoff': 'yes'},
            {'office': ('courier', 'logistics')}
        ],
        'car_rental': [{'amenity': ('car_rental', 'car_sharing')}],
        'post_office': [{'amenity': ('post_office', 'post_box', 'post_depot')}]
    }
    FALLBACK_QUERIES: ClassVar[dict[str, tuple[str, ...]]] = {
        'food': ('restaurant', 'cafe', 'fast food', 'bar', 'pub'),
        'bar': ('bar', 'pub'), 'cafe': ('cafe', 'kawiarnia'),
        'takeaway': ('fast food', 'takeaway', 'restaurant'),
        'restaurant': ('restaurant', 'restauracja'),
        'delivery': ('pizza', 'restaurant', 'food delivery'),
        'fast_food': ('fast food', 'kebab', 'burger'), 'pub': ('pub', 'bar'),
        'food_court': ('food court', 'restaurant'),
        'attractions': ('attraction', 'museum', 'park', 'cinema', 'theatre'),
        'attraction': ('attraction',), 'library': ('library', 'biblioteka'),
        'cinema': ('cinema', 'kino'), 'museum': ('museum', 'muzeum'),
        'live_music': ('music venue', 'live music', 'club'), 'park': ('park',),
        'gym': ('gym', 'fitness'), 'art': ('gallery', 'art'),
        'nightlife': ('nightclub', 'club', 'bar'), 'theatre': ('theatre', 'teatr'),
        'zoo': ('zoo',), 'shopping': ('shop', 'mall', 'supermarket'),
        'mall': ('mall', 'shopping centre', 'centrum handlowe'),
        'garden': ('garden centre', 'doityourself', 'hardware'),
        'chemist': ('chemist', 'drogeria', 'cosmetics'),
        'electronics': ('electronics', 'computer', 'mobile phone'),
        'local': ('convenience', 'kiosk'), 'sports': ('sports shop', 'bicycle shop'),
        'grocery': ('supermarket', 'grocery', 'bakery'),
        'car_sales': ('car dealer', 'car sales', 'samochody'),
        'clothes': ('clothes', 'shoes'),
        'books': ('books', 'bookshop', 'newsagent', 'księgarnia'),
        'services': ('pharmacy', 'atm', 'parking', 'hotel', 'fuel'),
        'pharmacy': ('pharmacy', 'apteka'), 'car_wash': ('car wash', 'automyjnia'),
        'atm': ('atm', 'bankomat'), 'hotel': ('hotel',), 'parking': ('parking',),
        'laundry': ('laundry', 'dry cleaning'), 'beauty': ('beauty salon', 'hairdresser'),
        'charging': ('charging station',), 'fuel': ('fuel station', 'petrol station', 'stacja paliw'),
        'healthcare': ('hospital', 'clinic', 'doctors'),
        'courier': ('parcel locker', 'post office', 'courier'),
        'car_rental': ('car rental',), 'post_office': ('post office', 'poczta')
    }
    KEYWORD_ALIASES: ClassVar[dict[str, str]] = {
        'cafe': 'cafe', 'café': 'cafe', 'kawiarnia': 'cafe', 'kawiarnie': 'cafe',
        'restauracja': 'restaurant', 'restauracje': 'restaurant', 'restaurant': 'restaurant',
        'fast food': 'fast_food', 'fastfood': 'fast_food', 'pub': 'pub', 'bar': 'bar',
        'apteka': 'pharmacy', 'apteki': 'pharmacy', 'pharmacy': 'pharmacy',
        'bankomat': 'atm', 'bankomaty': 'atm', 'atm': 'atm'
    }
