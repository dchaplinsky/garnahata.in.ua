django.jQuery(window).on('map:init', function (e) {
    var detail = e.originalEvent ?
                 e.originalEvent.detail : e.detail,
        geocoder = L.Control.geocoder({
            "position": "topleft",
        }).addTo(detail.map);

    detail.map.addLayer(
        new L.TileLayer(
            'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}));
});
