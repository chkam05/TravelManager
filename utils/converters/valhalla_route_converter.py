from __future__ import annotations
from typing import Any, Callable


Translator = Callable[..., str]


class ValhallaRouteConverter:
    """Converts Valhalla route responses to the frontend route shape."""

    @classmethod
    def convert(
        cls,
        data: dict[str, Any],
        translator: Translator | None = None
    ) -> dict[str, Any]:
        trip = data.get('trip') if isinstance(data, dict) else None
        if not isinstance(trip, dict):
            message = data.get('error') if isinstance(data, dict) else None
            raise RuntimeError(
                translator('ROUTE_ERROR.INVALID_VALHALLA_RESPONSE')
                if translator
                else message or 'Invalid Valhalla response.'
            )

        summary = trip.get('summary') if isinstance(trip.get('summary'), dict) else {}
        coordinates: list[list[float]] = []
        legs: list[dict[str, Any]] = []

        for leg in trip.get('legs', []):
            if not isinstance(leg, dict):
                continue
            leg_summary = leg.get('summary') if isinstance(leg.get('summary'), dict) else {}
            shape = str(leg.get('shape') or '')
            leg_coordinates = cls.decode_shape(shape) if shape else []
            coordinates.extend(leg_coordinates[1:] if coordinates and leg_coordinates else leg_coordinates)
            maneuvers = leg.get('maneuvers') if isinstance(leg.get('maneuvers'), list) else []
            legs.append({
                'distance': max(0.0, float(leg_summary.get('length') or 0) * 1000),
                'duration': max(0.0, float(leg_summary.get('time') or 0)),
                'steps': [
                    cls.convert_step(item, translator)
                    for item in maneuvers
                    if isinstance(item, dict)
                ]
            })

        return {
            'distance': max(0.0, float(summary.get('length') or 0) * 1000),
            'duration': max(0.0, float(summary.get('time') or 0)),
            'geometry': {'type': 'LineString', 'coordinates': coordinates},
            'legs': legs,
            'waypoints': [],
            'toll_exclusion_requested': True,
            'toll_exclusion_applied': True,
            'toll_exclusion_warning': None if not summary.get('has_toll') else (
                translator('ROUTE_ERROR.TOLL_EXCLUSION_WARNING')
                if translator
                else 'The router found a possible toll section despite the toll avoidance setting.'
            )
        }

    @classmethod
    def convert_step(
        cls,
        maneuver: dict[str, Any],
        translator: Translator | None = None
    ) -> dict[str, Any]:
        try:
            maneuver_type = int(maneuver.get('type'))
        except (TypeError, ValueError):
            maneuver_type = None
        street_names = maneuver.get('street_names') if isinstance(maneuver.get('street_names'), list) else []
        maneuver_data = {
            'type': cls.maneuver_type(maneuver_type),
            'modifier': cls.maneuver_modifier(maneuver),
            'exit': maneuver.get('roundabout_exit_count')
        }
        name = street_names[0] if street_names else ''
        instruction = (
            cls.maneuver_instruction(maneuver_data, name, translator)
            if translator
            else str(maneuver.get('instruction') or '')
        )
        return {
            'distance': max(0.0, float(maneuver.get('length') or 0) * 1000),
            'duration': max(0.0, float(maneuver.get('time') or 0)),
            'name': name,
            'instruction': instruction,
            'maneuver': maneuver_data
        }

    @staticmethod
    def maneuver_instruction(
        maneuver: dict[str, Any],
        road_name: str,
        translator: Translator
    ) -> str:
        """Builds a locale-aware instruction from normalized maneuver data."""
        maneuver_type = str(maneuver.get('type') or '')
        modifier = str(maneuver.get('modifier') or '')
        road = translator('ROUTE_MANEUVER.ROAD_SUFFIX', name=road_name) if road_name else ''

        if maneuver_type == 'depart':
            return translator('ROUTE_MANEUVER.DEPART', road=road)
        if maneuver_type == 'arrive':
            return translator('ROUTE_MANEUVER.ARRIVE')
        if maneuver_type == 'roundabout':
            exit_number = maneuver.get('exit')
            return translator(
                'ROUTE_MANEUVER.ROUNDABOUT_EXIT' if exit_number else 'ROUTE_MANEUVER.ROUNDABOUT',
                exit=exit_number or '',
                road=road
            )
        if maneuver_type == 'merge':
            return translator('ROUTE_MANEUVER.MERGE', road=road)
        if 'left' in modifier:
            return translator('ROUTE_MANEUVER.TURN_LEFT', road=road)
        if 'right' in modifier:
            return translator('ROUTE_MANEUVER.TURN_RIGHT', road=road)
        return translator('ROUTE_MANEUVER.CONTINUE', road=road)

    @staticmethod
    def maneuver_type(value: int | None) -> str:
        if value in (1, 2, 3):
            return 'depart'
        if value in (4, 5, 6):
            return 'arrive'
        if value in (26, 27):
            return 'roundabout'
        if value in (18, 19):
            return 'merge'
        return 'continue'

    @staticmethod
    def maneuver_modifier(maneuver: dict[str, Any]) -> str:
        instruction = str(maneuver.get('instruction') or '').lower()
        if 'left' in instruction:
            return 'left'
        if 'right' in instruction:
            return 'right'
        return 'straight'

    @staticmethod
    def decode_shape(shape: str) -> list[list[float]]:
        coordinates: list[list[float]] = []
        index = latitude = longitude = 0

        while index < len(shape):
            values = []
            for _ in range(2):
                result, shift = 1, 0
                while True:
                    byte = ord(shape[index]) - 64
                    index += 1
                    result += byte << shift
                    shift += 5
                    if byte < 0x1f:
                        break
                values.append(~(result >> 1) if result & 1 else result >> 1)
            latitude += values[0]
            longitude += values[1]
            coordinates.append([longitude / 1e6, latitude / 1e6])

        return coordinates
