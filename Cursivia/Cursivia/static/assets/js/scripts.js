/*
Template Name: 69 Studio
Author: TrendyTheme
Version: 2.0
*/

jQuery(function ($) {

    'use strict';

    /* ======= Blank Wrapper ======= */
    (function () {

        // content here...

    }());


    /* ======= Preloader ======= */
    (function () {
        $('#status').fadeOut();
        $('#preloader').delay(200).fadeOut('slow');
    }());





    /* ======= Navbar for Desktop and Mobile Devices ======= */
    (function () {

        var navbar      = $('.navbar-custom'),
            width       = Math.max($(window).width(), window.innerWidth),
            mobileTest;

        if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            mobileTest = true;
        }

        navbarSubmenu(width);
        hoverDropdown(width, mobileTest);

        $(window).resize(function() {
            var width = Math.max($(window).width(), window.innerWidth);
            hoverDropdown(width, mobileTest);
        });

        /* ---------------------------------------------- /*
         * Navbar submenu
        /* ---------------------------------------------- */

        function navbarSubmenu(width) {
            if (width > 767) {
                $('.navbar-custom .navbar-nav > li.dropdown').hover(function() {
                    var MenuLeftOffset  = $('.dropdown-menu', $(this)).offset().left;
                    var Menu1LevelWidth = $('.dropdown-menu', $(this)).width();
                    if (width - MenuLeftOffset > Menu1LevelWidth * 2) {
                        $(this).children('.dropdown-menu').css( {'right': 'auto', 'left': '0'});
                    } else {
                        $(this).children('.dropdown-menu').css( {'right': '0', 'left': 'auto'});
                    }
                    if ($('.dropdown', $(this)).length > 0) {
                        var Menu2LevelWidth = $('.dropdown-menu', $(this)).width();
                        if (width - MenuLeftOffset - Menu1LevelWidth < Menu2LevelWidth) {
                            $(this).children('.dropdown-menu').addClass('left-side');
                        } else {
                            $(this).children('.dropdown-menu').removeClass('left-side');
                        }
                    }
                });
            }
        }


        /* ---------------------------------------------- /*
         * Navbar hover dropdown on desctop
        /* ---------------------------------------------- */

        function hoverDropdown(width, mobileTest) {
            if ((width > 767) && (mobileTest !== true)) {
                $('.navbar-custom .navbar-nav > li.dropdown, .navbar-custom li.dropdown > ul > li.dropdown').removeClass('open');
                var delay = 0;
                var setTimeoutConst;
                $('.navbar-custom .navbar-nav > li.dropdown, .navbar-custom li.dropdown > ul > li.dropdown').hover(function() {
                    var $this = $(this);
                    setTimeoutConst = setTimeout(function() {
                        $this.addClass('open');
                        $this.find('.dropdown-toggle').addClass('disabled');
                    }, delay);
                },
                function() {
                    clearTimeout(setTimeoutConst);
                    $(this).removeClass('open');
                    $(this).find('.dropdown-toggle').removeClass('disabled');
                });
            } else {
                $('.navbar-custom .navbar-nav > li.dropdown, .navbar-custom li.dropdown > ul > li.dropdown').unbind('mouseenter mouseleave');
                $('.navbar-custom [data-toggle=dropdown]').not('.binded').addClass('binded').on('click', function(event) {
                    event.preventDefault();
                    event.stopPropagation();
                    $(this).parent().siblings().removeClass('open');
                    $(this).parent().siblings().find('[data-toggle=dropdown]').parent().removeClass('open');
                    $(this).parent().toggleClass('open');
                });
            }
        }

        /* ---------------------------------------------- /*
         * Navbar collapse on click
        /* ---------------------------------------------- */

        $(document).on('click','.navbar-collapse.in',function(e) {
            if( $(e.target).is('a') && $(e.target).attr('class') != 'dropdown-toggle' ) {
                $(this).collapse('hide');
            }
        });

    }());




    /* ======= Search box ======= */
    $("#search-box").hide();
        var searchIcon = $(".search-icon");
        var searchBox = $("#search-box");
        searchIcon.on('click', function(event) {
        searchIcon.toggleClass("active");
        searchBox.slideToggle();
    });




    /* === jQuery for page scrolling feature - requires jQuery Easing plugin === */

    $('a.page-scroll').on('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top - 60
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });



    /* ======= Sticky Menu  ======= */
    $(window).scroll(function(){
        if ($(window).scrollTop() > 10){
            $('.main-nav, .navbar-fixed-top, .tt-default-nav').addClass("sticky");
        }else{
            $('.main-nav, .navbar-fixed-top, .tt-default-nav').removeClass("sticky");
        }
    });



    /* ======= Full Screen Menu  ======= */
    $('.nav-bars, .tt-nav').on('click', function(){
        $('.nav-bars').toggleClass('navbar-on');
        $('.tt-nav').fadeToggle();
        $('.tt-nav').removeClass('nav-hide');
    });



    /* ======= Full Screen Background ======= */
    
    $(".tt-fullHeight").height($(window).height());
    $(window).resize(function(){
        $(".tt-fullHeight").height($(window).height());
    });



    /* === Youtube Video Script === */
    if ($('.player').length > 0) {

        jQuery(".player").mb_YTPlayer();
        
    }


    /* ======= Textrotator ======= */
    if ($('.rotate').length > 0) {
        $(".rotate").textrotator({
            animation: "dissolve", // You can pick the way it animates when rotating through words. Options are dissolve (default), fade, flip, flipUp, flipCube, flipCubeUp and spin.
            separator: "|", //  You can define a new separator (|, &, * etc.) by yourself using this field.
            speed: 3000 // How many milliseconds until the next word show.
        });
    }


    /* ======= Revolution slider  homepage Creative======= */
    if ($('.tt-banner').length > 0) {
        jQuery(".tt-banner").revolution({
            delay:10000,
            startwidth:1170,
            startheight:500,
            onHoverStop:"off",
            hideThumbs:10,
            hideTimerBar:"on",
            navigationType:"none",
            navigationStyle:"preview1",
            fullWidth:"off",
            fullScreen:"on",
            fullScreenOffsetContainer: ""
        });
    }


    /* ======= Revolution slider  homepage Gallery======= */
    if ($('.tt-banner-gallery').length > 0) {
        jQuery(".tt-banner-gallery").revolution({
            delay:9000,
            startwidth:1170,
            startheight:500,
            onHoverStop:"off",
            hideThumbs:10,
            hideTimerBar:"on",
            navigationType:"none",
            navigationStyle:"preview1",
            fullWidth:"off",
            fullScreen:"on",
            fullScreenOffsetContainer: ""
        });
    }



    /* === Progress Bar === */
    $('.progress').on('inview', function(event, visible, visiblePartX, visiblePartY) {
        if (visible) {
            $.each($('div.progress-bar'),function(){
                $(this).css('width', $(this).attr('aria-valuenow')+'%');
            });
            $(this).off('inview');
        }
    });




    /* === Counter === */
    $('.counter-section').on('inview', function(event, visible, visiblePartX, visiblePartY) {
        if (visible) {
            $(this).find('.timer').each(function () {
                var $this = $(this);
                $({ Counter: 0 }).animate({ Counter: $this.text() }, {
                    duration: 2000,
                    easing: 'swing',
                    step: function () {
                        $this.text(Math.ceil(this.Counter));
                    }
                });
            });
            $(this).off('inview');
        }
    });



    /* === factsTwo CountUp === */
    $('#factsTwo').on('inview', function(event, visible, visiblePartX, visiblePartY) {
        if (visible) {
            $(this).find('.timer').each(function () {
                var $this = $(this);
                $({ Counter: 0 }).animate({ Counter: $this.text() }, {
                    duration: 2000,
                    easing: 'swing',
                    step: function () {
                        $this.text(Math.ceil(this.Counter));
                    }
                });
            });
            $(this).off('inview');
        }
    });



    /* === magnificPopup === */

    $('.tt-lightbox').magnificPopup({
        type: 'image',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        fixedContentPos: false
        // other options
    });


    $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false
    });




    /* === blogGrid === */
    if ($('#blogGrid').length > 0) {

        $('#blogGrid').masonry({
          // options
          itemSelector: '.blog-grid-item',
        });
    }



    /* ======= Recent Project Carousel ======= */
    (function () {

      var owl = $(".recent-project-carousel");
     
      owl.owlCarousel({
          items : 5, //5 items above 1000px browser width
          itemsDesktop : [1024,4], //4 items between 1000px and 901px
          itemsDesktopSmall : [900,3], // betweem 900px and 601px
          itemsTablet: [600,2], //2 items between 600 and 480
          itemsMobile : [479,1], //1 item between 480 and 0
          pagination : false // Show pagination
      });


      // Custom Navigation Events
      $(".btn-next").on('click', function(){
        owl.trigger('owl.next');
      })
      $(".btn-prev").on('click', function(){
        owl.trigger('owl.prev');
      })


    }());


    /* ======= Partner Carousel ======= */
    (function () {

      var owl = $(".partner-carousel");
     
      owl.owlCarousel({
          items : 4, //5 items above 1000px browser width
          itemsDesktop : [1024,4], //4 items between 1000px and 901px
          itemsDesktopSmall : [900,3], // betweem 900px and 601px
          itemsTablet: [600,2], //2 items between 600 and 480
          itemsMobile : [479,1], //1 item between 480 and 0
          pagination : false // Show pagination
      });

    }());




    /* ======= BlackAndWhite Script ======= */
    $('.bwWrapper').BlackAndWhite({
        hoverEffect : true, // default true
        // set the path to BnWWorker.js for a superfast implementation
        webworkerPath : false,
        // to invert the hover effect
        invertHoverEffect: false,
        // this option works only on the modern browsers ( on IE lower than 9 it remains always 1)
        intensity:1,
        speed: { //this property could also be just speed: value for both fadeIn and fadeOut
            fadeIn: 200, // 200ms for fadeIn animations
            fadeOut: 800 // 800ms for fadeOut animations
        },
        onImageReady:function(img) {
            // this callback gets executed anytime an image is converted
        }
    });






    /* ======= gallerySlider on homepage two ======= */

    if ($('#gallerySlider').length > 0) {

        $('#gallerySlider').flexslider({
            animation: "slide",
            controlNav: "thumbnails",
            directionNav: true
        })
    }



    /* ======= client-slider-v3  ======= */

    if ($('.client-slider-v3').length > 0) {

        $('.client-slider-v3').flexslider({
            animation: "slide",
            controlNav: "thumbnails",
            directionNav: true
        })
    }


    /* ======= client-slider-v4  ======= */

    if ($('.client-slider-v4').length > 0) {

        $('.client-slider-v4').flexslider({
            animation: "slide",
            controlNav: "thumbnails",
            directionNav: true
        })
    }



    /* ======= Contact Form ======= */
    $('#contactForm').on('submit',function(e){

        e.preventDefault();

        var $action = $(this).prop('action');
        var $data = $(this).serialize();
        var $this = $(this);

        $this.prevAll('.alert').remove();

        $.post( $action, $data, function( data ) {

            if( data.response=='error' ){

                $this.before( '<div class="alert alert-danger">'+data.message+'</div>' );
            }

            if( data.response=='success' ){

                $this.before( '<div class="alert alert-success">'+data.message+'</div>' );
                $this.find('input, textarea').val('');
            }

        }, "json");

    });



    /* ======= GOOGLE MAP ======= */

    if ($('#myMap').length > 0) {
        //set your google maps parameters
        var $latitude = 40.716304, //If you unable to find latitude and longitude of your address. Please visit http://www.latlong.net/convert-address-to-lat-long.html you can easily generate.
            $longitude = -73.995763,
            $map_zoom = 16 /* ZOOM SETTING */

        //google map custom marker icon 
        var $marker_url = 'assets/images/pin.png';

        //we define here the style of the map
        var style = [{
            "stylers": [{
                "hue": "#000"
            }, {
                "saturation": -70
            }, {
                "gamma": 2.15
            }, {
                "lightness": 12
            }]
        }];

        //set google map options
        var map_options = {
            center: new google.maps.LatLng($latitude, $longitude),
            zoom: $map_zoom,
            panControl: true,
            zoomControl: true,
            mapTypeControl: true,
            streetViewControl: true,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            scrollwheel: false,
            styles: style
        }
        //inizialize the map
        var map = new google.maps.Map(document.getElementById('myMap'), map_options);
        //add a custom marker to the map                
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng($latitude, $longitude),
            map: map,
            visible: true,
            icon: $marker_url
        });

        var contentString = '<div id="mapcontent">' + '<p>69Studio, 795 Folsom Ave, San Francisco.</p></div>';
        var infowindow = new google.maps.InfoWindow({
            maxWidth: 320,
            content: contentString
        });

        google.maps.event.addListener(marker, 'click', function() {
            infowindow.open(map, marker);
        });
       
    }


});




$(window).load(function() {

    "use strict";


    /* ======= Stellar for background scrolling ======= */
    (function () {

        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
         
        } else {
            $(window).stellar({
                horizontalScrolling: false,
                responsive: true
            });
        }

    }());


    /* ======= shuffle js ======= */
    if ($('#portfolio-grid').length > 0) {
        /* initialize shuffle plugin */
        var $grid = $('#portfolio-grid');

        $grid.shuffle({
            itemSelector: '.portfolio-item' // the selector for the items in the grid
        });

        /* reshuffle when user clicks a filter item */
        $('#filter li').on('click', function (e) {
            e.preventDefault();

            // set active class
            $('#filter li').removeClass('active');
            $(this).addClass('active');

            // get group name from clicked item
            var groupName = $(this).attr('data-group');

            // reshuffle grid
            $grid.shuffle('shuffle', groupName );
        });
    }



});