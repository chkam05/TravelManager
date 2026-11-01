(function (window) {
    'use strict';

    const standard = () => ({
        water: {
            color: '#8bbbd2', weight: 1,
            fill: true, fillColor: '#aad3df', fillOpacity: 1
        },
        landuse: (properties, zoom) => ({
            color: '#c8d8b5',
            weight: zoom >= 12 ? 0.7 : 0.35,
            fill: true,
            fillColor: properties?.natural === 'wood'
                || properties?.landuse === 'forest'
                ? '#add19e'
                : properties?.leisure === 'park'
                    ? '#c8e6b8'
                    : '#e3e7d5',
            fillOpacity: 0.78
        }),
        buildings: {
            color: '#b8ada3', weight: 0.8,
            fill: true, fillColor: '#d9d0c9', fillOpacity: 0.9
        },
        roads: (properties, zoom) => {
            const roadClass = properties?.highway || '';
            const major = ['motorway', 'trunk'].includes(roadClass);
            const primary = ['primary', 'secondary'].includes(roadClass);
            return {
                color: major ? '#e8928f' : primary ? '#f5c97d' : '#ffffff',
                weight: major ? 4.2 : primary ? 3.2 : zoom >= 14 ? 2.2 : 1.4,
                opacity: 0.96,
                lineCap: 'round',
                lineJoin: 'round'
            };
        },
        railways: (properties, zoom) => ({
            color: properties?.railway === 'tram' ? '#806b78' : '#686868',
            weight: zoom >= 13 ? 1.8 : 1.2,
            opacity: 0.9,
            dashArray: properties?.railway === 'subway' ? '3,4' : '6,4'
        }),
        boundaries: (properties) => ({
            color: properties?.admin_level === '2' ? '#8f5b93' : '#a67aa8',
            weight: properties?.admin_level === '2' ? 2 : 1.2,
            opacity: 0.82,
            dashArray: '7,5',
            fill: false
        }),
        // The current canvas renderer cannot draw place names. Empty styles
        // suppress point geometries instead of turning them into black dots.
        places: [],
        pois: []
    });

    window.travelManagerOfflineMapStyles = Object.freeze({standard});
})(window);
