(function($) {
    "use strict"; // Start of use strict

    var $d = $('header').height() - 160,
        $w = $(window),
        $b = $("body");

    $("#search-form").typeahead({
        minLength: 2, 
        autoSelect: false,
        source: function(query, process) {
            $.get('/ajax/suggest', {"q": query})
                .success(function(data){
                    process(data);
                })
        },
        matcher: function() {
            // Big guys are playing here
            return true;
        }
    })

    $('.massonry').imagesLoaded(function() {
        $('.massonry').masonry({
            itemSelector: '.item',
            columnWidth: '.grid-sizer',
            percentPosition: true,
            singleMode: false,
            isResizable: true,
            isAnimated: true,
            animationOptions: {
                queue: false,
                duration: 500
            }
        });
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

    adjust_margin();
    bigMap();

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a').click(function() {
        $('.navbar-toggle:visible').click();
    });

    // Fit Text Plugin for Main Header
    $(".overInfo h3").fitText(
        1.2, {
            minFontSize: '35px',
            maxFontSize: '65px'
        }
    );

    $(".overInfo h4").fitText(
        1.2, {
            minFontSize: '18px',
            maxFontSize: '24px'
        }
    );

    $(window).on('map:init', function (e) {
        var detail = e.originalEvent ?
                     e.originalEvent.detail : e.detail,
            data = $(".geojson-container").data("geojson"),
            markers = new L.MarkerClusterGroup();

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
        detail.map.fitBounds(markers)
    });    
    
    $(document).ready(function () {

        $('.objectAdressTable').each(function () {
            var Column_number_to_Merge = 1;
 
            // Previous_TD holds the first instance of same td. Initially first TD=null.
            var Previous_TD = null;
            var i = 1;
            $("tbody",this).find('tr').each(function () {
                // find the correct td of the correct column
                // we are considering the table column 1, You can apply on any table column
                var Current_td = $(this).find('td:nth-child(' + Column_number_to_Merge + ')');
                 
                if (Previous_TD == null) {
                    // for first row
                    Previous_TD = Current_td;
                    i = 1;
                } 
                else if (Current_td.text() == Previous_TD.text()) {
                    // the current td is identical to the previous row td
                    // remove the current td
                    Current_td.remove();
                    // increment the rowspan attribute of the first row td instance
                    Previous_TD.attr('rowspan', i + 1);
                    i = i + 1;
                } 
                else {
                    // means new value found in current td. So initialize counter variable i
                    Previous_TD = Current_td;
                    i = 1;
                }
            });
              
              $('.ownershipAsset').each(function () {
                    if($(this).text().length === 0) {
                        $(this).parent("td").addClass("emptyTd");
                    }
              });
        });
    });
    
})(jQuery); // End of use strict
