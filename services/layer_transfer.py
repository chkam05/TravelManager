"""Whole-layer interchange. Native JSON is lossless; geographic formats use sampled curves."""
import json
import xml.etree.ElementTree as ET
from uuid import uuid4
from models.settings.custom_layer import CustomLayer

GPX = 'http://www.topografix.com/GPX/1/1'
MAX_BYTES = 10 * 1024 * 1024


def boundary(e):
    points = e['points']
    result = [points[0]]
    for i, segment in enumerate(e['segments']):
        a, b = points[i], points[(i + 1) % len(points)]
        if segment['type'] == 'curve':
            c, d = segment['control1'], segment['control2']
            for step in range(1, 25):
                t = step / 24
                u = 1 - t
                result.append([u**3*a[k]+3*u*u*t*c[k]+3*u*t*t*d[k]+t**3*b[k] for k in (0, 1)])
        else:
            result.append(b)
    return result


def export_layer(data, format):
    layer = CustomLayer.from_payload(data).to_dict()
    if format == 'json':
        return json.dumps({'format': 'travel-manager-layer', 'version': 1, 'layer': layer}, ensure_ascii=False, indent=2)
    if format == 'geojson':
        features = []
        for e in layer['elements']:
            coordinates = [[lng, lat] for lat, lng in boundary(e)]
            if e['type'] == 'area':
                # RFC 7946 exterior rings have counterclockwise winding.
                area = sum(a[0]*b[1]-b[0]*a[1] for a, b in zip(coordinates, coordinates[1:]))
                if area < 0:
                    coordinates.reverse()
            features.append({'type': 'Feature', 'properties': {k: e[k] for k in ('name', 'color', 'width', 'background_color', 'line_style', 'hidden', 'locked', 'note', 'icon')},
                             'geometry': {'type': 'Point' if e['type'] == 'point' else 'Polygon' if e['type'] == 'area' else 'LineString',
                                          'coordinates': coordinates[0] if e['type'] == 'point' else [coordinates] if e['type'] == 'area' else coordinates}})
        return json.dumps({'type': 'FeatureCollection', 'name': layer['name'], 'features': features}, ensure_ascii=False, indent=2)
    if format != 'gpx':
        raise ValueError('Unsupported format')
    ET.register_namespace('', GPX)
    root = ET.Element(f'{{{GPX}}}gpx', version='1.1', creator='TravelManager')
    def child(parent, name, text=None, **attrs):
        element = ET.SubElement(parent, f'{{{GPX}}}{name}', attrs)
        element.text = text
        return element
    child(child(root, 'metadata'), 'name', layer['name'])
    for e in layer['elements']:
        if e['type'] == 'point':
            lat, lng = e['points'][0]
            waypoint = child(root, 'wpt', lat=str(lat), lon=str(lng))
            child(waypoint, 'name', e['name'])
            child(waypoint, 'desc', e['note'])
            child(waypoint, 'sym', e['icon'])
    for e in layer['elements']:
        if e['type'] == 'point':
            continue
        track = child(root, 'trk')
        child(track, 'name', e['name'])
        segment = child(track, 'trkseg')
        for lat, lng in boundary(e):
            child(segment, 'trkpt', lat=str(lat), lon=str(lng))
    return ET.tostring(root, encoding='unicode', xml_declaration=True)


def import_layer(text, filename='Imported layer'):
    if not isinstance(text, str) or len(text.encode('utf-8')) > MAX_BYTES:
        raise ValueError('File too large (maximum 10 MB)')
    elements = []
    name = filename.rsplit('.', 1)[0] or 'Imported layer'
    def add(points, title='', area=False, properties=None, point=False):
        properties = properties or {}
        if area:
            if len(points) < 4 or points[0] != points[-1]:
                raise ValueError('Polygon ring must be closed')
            points = points[:-1]
        e = {'id': uuid4().hex, 'name': title, 'type': 'point' if point else 'area' if area else 'route', 'points': points}
        for key in ('color', 'width', 'background_color', 'line_style', 'hidden', 'locked', 'note', 'icon'):
            if key in properties:
                e[key] = properties[key]
        elements.append(e)
    if text.lstrip('\ufeff \t\r\n').startswith('<'):
        if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
            raise ValueError('XML declarations are not supported')
        root = ET.fromstring(text)
        if root.tag not in ('gpx', f'{{{GPX}}}gpx', '{http://www.topografix.com/GPX/1/0}gpx'):
            raise ValueError('Expected GPX')
        ns = root.tag.split('}')[0] + '}' if '}' in root.tag else ''
        name = root.findtext(f'{ns}metadata/{ns}name') or root.findtext(f'{ns}name') or name
        for waypoint in root.findall(f'{ns}wpt'):
            add([[float(waypoint.attrib['lat']), float(waypoint.attrib['lon'])]], waypoint.findtext(f'{ns}name') or '',
                properties={'note': waypoint.findtext(f'{ns}desc') or '', 'icon': waypoint.findtext(f'{ns}sym') or ''}, point=True)
        for track in root.findall(f'{ns}trk'):
            for segment in track.findall(f'{ns}trkseg'):
                add([[float(p.attrib['lat']), float(p.attrib['lon'])] for p in segment.findall(f'{ns}trkpt')], track.findtext(f'{ns}name') or '')
        for route in root.findall(f'{ns}rte'):
            add([[float(p.attrib['lat']), float(p.attrib['lon'])] for p in route.findall(f'{ns}rtept')], route.findtext(f'{ns}name') or '')
    else:
        data = json.loads(text.lstrip('\ufeff'))
        if not isinstance(data, dict):
            raise ValueError('Expected one layer')
        if data.get('format') == 'travel-manager-layer':
            if data.get('version') != 1:
                raise ValueError('Unsupported layer version')
            layer = CustomLayer.from_payload(data.get('layer')).to_dict()
            layer['id'] = uuid4().hex
            for e in layer['elements']:
                e['id'] = uuid4().hex
            return layer
        if 'elements' in data:
            return import_layer(json.dumps({'format': 'travel-manager-layer', 'version': 1, 'layer': data}), filename)
        if 'crs' in data:
            raise ValueError('Only WGS84 GeoJSON is supported')
        name = data.get('name') or name
        def geometry(g, props):
            kind, coords = g['type'], g.get('coordinates')
            title = props.get('name', '')
            def line(values, area=False):
                if not isinstance(values, list) or any(not isinstance(p, list) or len(p) < 2 for p in values):
                    raise ValueError('Invalid coordinates')
                add([[p[1], p[0]] for p in values], title, area, props)
            if kind in ('Point', 'MultiPoint'):
                for p in ([coords] if kind == 'Point' else coords):
                    if not isinstance(p, list) or len(p) < 2:
                        raise ValueError('Invalid point')
                    add([[p[1],p[0]]], title, properties=props, point=True)
            elif kind == 'LineString':
                line(coords)
            elif kind == 'MultiLineString':
                for values in coords:
                    line(values)
            elif kind in ('Polygon', 'MultiPolygon'):
                for polygon in ([coords] if kind == 'Polygon' else coords):
                    if len(polygon) != 1:
                        raise ValueError('Polygons with holes are not supported')
                    line(polygon[0], True)
            elif kind == 'GeometryCollection':
                for g in g['geometries']:
                    geometry(g, props)
            else:
                raise ValueError('Unsupported geometry: ' + str(kind))
        features = data['features'] if data.get('type') == 'FeatureCollection' else [data]
        for feature in features:
            if feature.get('type') == 'Feature':
                geometry(feature['geometry'], feature.get('properties') or {})
            else:
                geometry(feature, {})
    return CustomLayer.from_payload({'id': uuid4().hex, 'name': name, 'elements': elements}).to_dict()
