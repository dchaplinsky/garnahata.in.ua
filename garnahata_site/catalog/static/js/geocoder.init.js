django.jQuery(window).on('map:init', function (e) {
    var detail = e.originalEvent ?
                 e.originalEvent.detail : e.detail,
        geocoder = L.Control.geocoder({
            "position": "topleft",
        }).addTo(detail.map);

    yndx = new L.Yandex(),
    yndxs = new L.Yandex('satellite'),
    cadastre = new L.tileLayer.wms('http://212.26.144.110/geowebcache/service/wms', {
        maxZoom: 19,
        layers: 'kadastr',
        format: 'image/png',
        transparent: true,
        hash: "cadastre",
        overlay: true
    });

    detail.map.addLayer(yndx);

    detail.map.layerscontrol.addBaseLayer(yndx, "Яндекс");
    detail.map.layerscontrol.addBaseLayer(yndxs, "Яндекс Супутник");
    detail.map.layerscontrol.addOverlay(cadastre, "Кадастр");
});
