django.jQuery(window).on('map:init', function (e) {
    var detail = e.originalEvent ?
                 e.originalEvent.detail : e.detail,
        geocoder = L.Control.geocoder({
            "position": "topleft",
        }).addTo(detail.map);
});
