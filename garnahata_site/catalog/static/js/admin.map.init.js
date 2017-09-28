django.jQuery(window).on('map:init', function (e) {
    var mapBoxToken = 'pk.eyJ1IjoiZGNoYXBsaW5za3kiLCJhIjoiY2o3d2p1eWdoNXAzMDJxbnV1ZG05YmF6ZiJ9.tXdY9DfXJiR7t0GgYKMiug';
    var detail = e.originalEvent ?
                 e.originalEvent.detail : e.detail,
        geocoder = L.Control.geocoder({
            "position": "topleft",
            "geocoder": L.Control.Geocoder.google("AIzaSyATnqjBGndYfR-XZSJUaJd9T6qXx7-T1s4")
        }).addTo(detail.map),
        mapbox = new L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox.streets',
            accessToken: mapBoxToken
        }),

        mapbox_sat = new L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox.streets-satellite',
            accessToken: mapBoxToken
        }),
        cadastre = new L.tileLayer.wms('http://212.26.144.110/geowebcache/service/wms', {
            maxZoom: 19,
            layers: 'kadastr',
            format: 'image/png',
            transparent: true,
            hash: "cadastre",
            overlay: true
        });

    detail.map.addLayer(mapbox);

    detail.map.layerscontrol.addBaseLayer(mapbox, "Карта");
    detail.map.layerscontrol.addBaseLayer(mapbox_sat, "Супутник");
    detail.map.layerscontrol.addOverlay(cadastre, "Кадастр");
});
