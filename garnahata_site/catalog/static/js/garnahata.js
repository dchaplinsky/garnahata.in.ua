(function($) {
    "use strict"; // Start of use strict
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
	

    // jQuery for page scrolling feature - requires jQuery Easing plugin
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top - 50)
        }, 1250, 'easeInOutExpo');
        event.preventDefault();
    });

    $('.first-after-intro').css('margin-top', $('header').height());
    var $d = $('header').height()-160;

    $(window ).scroll(function() {	
        if  ($(window).scrollTop() >= $d){$('body').addClass('fixed-header');} 
        else {$('body').removeClass('fixed-header');}
    });

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

 

})(jQuery); // End of use strict
