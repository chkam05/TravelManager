from __future__ import annotations


def matching_geometry(geometry, geometry_type: str):
    """Returns only the MVT-compatible dimension expected by a feature."""
    from shapely.ops import unary_union

    accepted = {
        'point': {'Point', 'MultiPoint'},
        'line': {'LineString', 'MultiLineString'},
        'polygon': {'Polygon', 'MultiPolygon'},
    }.get(geometry_type)
    if accepted is None or geometry is None or geometry.is_empty:
        return None
    if geometry.geom_type in accepted:
        return geometry
    if not hasattr(geometry, 'geoms'):
        return None
    parts = []
    pending = list(geometry.geoms)
    while pending:
        part = pending.pop()
        if part.geom_type in accepted:
            parts.append(part)
        elif hasattr(part, 'geoms'):
            pending.extend(part.geoms)
    if not parts:
        return None
    merged = unary_union(parts)
    return merged if not merged.is_empty and merged.geom_type in accepted else None
