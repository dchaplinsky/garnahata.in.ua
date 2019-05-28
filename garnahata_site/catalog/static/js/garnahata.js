(function($) {
    "use strict"; // Start of use strict

    var $d = $('header').height() - 160,
        $w = $(window),
        $b = $("body");

    $(".search-form-q").typeahead({
        minLength: 2,
        items: 100,
        autoSelect: false,
        source: function(query, process) {
            $.get($(".search-form-q").data("endpoint"), {
                    "q": query
                })
                .done(function(data) {
                    process(data);
                })
        },
        matcher: function() {
            return true;
        },
        highlighter: function(instance) {
            return instance;
        },
        updater: function(instance) {
            return $(instance).data("sugg_text")
        },
        sorter: function(items) {
            return items
        },
        afterSelect: function(item) {
            var form = $(".search-form-q").closest("form");
            form.find("input[name=is_exact]").val("on");

            form.submit();
        }
    });

    // jQuery for page scrolling feature - requires jQuery Easing plugin
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top - 50)
        }, 1250, 'easeInOutExpo');
        event.preventDefault();
    });

    function adjust_margin() {
        $('.homepage .first-after-intro').css('margin-top', $('header').height());
    }

    function toggle_header() {
        $b.toggleClass('fixed-header', $w.scrollTop() >= $d);
        $b.toggleClass('not-fixed-header', $w.scrollTop() < $d);
    }
    
    function bigMap() {
        $(".bigMapPage #bigMap, .bigMapPage .pre-scrollable").height($(window).height()-360);
    }
    
    $w.on("scroll", function() {
        toggle_header();
    });

    $w.on("resize", function() {
        toggle_header();
        adjust_margin();
        bigMap();
    });
    
    $( document ).ready(function() {
        $(".overInfo h3").fitText(
        1.4, {
            minFontSize: '30px',
            maxFontSize: '65px'
        }
    );

        $(".overInfo h4, .overInfo h1").fitText(
            1.4, {
                minFontSize: '18px',
                maxFontSize: '24px'
            }
        );
    });

    adjust_margin();
    bigMap();

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a').click(function() {
        $('.navbar-toggle:visible').click();
    });
    
    $('.btn.mortgage_registered').on('click', function(e) {
            $(this).closest('tr').next('tr').find('.mortgage-cell').toggleClass("show");
        e.preventDefault();
    });
    
    $('#navbar-collapse-1').on('show.bs.collapse', function () {
       $('#navbar-collapse-1').addClass("show");
    })
    $('#navbar-collapse-1').on('hide.bs.collapse', function () {
       $('#navbar-collapse-1').removeClass("show");
    })

    // Fit Text Plugin for Main Header
    

    $(window).on('map:init', function (e) {
        var detail = e.originalEvent ?
                     e.originalEvent.detail : e.detail,
            data = $(".geojson-container").data("geojson"),
            markers = new L.MarkerClusterGroup(),
            mapbox = new L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
                maxZoom: 18,
                id: 'mapbox.streets',
                accessToken: 'pk.eyJ1IjoiZGNoYXBsaW5za3kiLCJhIjoiY2p3N3Z0dnozMGUzdDQ2bzdrMm5vZXJmdSJ9.rc9StX2ALGB5TR2e6FGEjA'
            }),

            mapbox_sat = new L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
                maxZoom: 18,
                id: 'mapbox.streets-satellite',
                accessToken: 'pk.eyJ1IjoiZGNoYXBsaW5za3kiLCJhIjoiY2p3N3Z0dnozMGUzdDQ2bzdrMm5vZXJmdSJ9.rc9StX2ALGB5TR2e6FGEjA'
            }),

            cadastre = new L.tileLayer.wms('https://map.land.gov.ua/geowebcache/service/wms', {
                maxZoom: 22,
                layers: 'kadastr',
                format: 'image/png',
                transparent: true,
                hash: "cadastre",
                overlay: true
            });

        for (var i = data.length - 1; i >= 0; i--) {
            markers.addLayer(
                new L.Marker(data[i].coords, {
                    "title": data[i].title
                }
            ).bindPopup([
                    '<strong>',
                    data[i].title,
                    '</strong><br />',
                    data[i].commercial_name,
                    '<br />',
                    '<a href="',
                    data[i].href,
                    '">Посилання</a>'
                ].join("")
            ));
        };

        detail.map.addLayer(markers);
        detail.map.addLayer(mapbox);

        detail.map.layerscontrol.addBaseLayer(mapbox, "Карта");
        detail.map.layerscontrol.addBaseLayer(mapbox_sat, "Супутник");
        detail.map.layerscontrol.addOverlay(cadastre, "Кадастр");

        detail.map.fitBounds(markers)
    });
})(jQuery); // End of use strict
