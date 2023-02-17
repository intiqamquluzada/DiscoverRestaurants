jQuery(function ($) {

    'use strict';

    // Mean menu
    jQuery('.mean-menu').meanmenu({
        meanScreenWidth: "1199"
    });

    // Header parallax
    function scrollParallax() {
        var opThresh = 350;
        var opFactor = 750;
    
        $(window).on("scroll", function() {
            var top = this.pageYOffset;
            var layers = $(".parallax");
            var layer, speed, yPos;
            for (var i = 0; i < layers.length; i++) {
                layer = layers[i];
                speed = layer.getAttribute('data-speed');
                var yPos = -(top * speed / 100);
                layer.setAttribute('style', 'transform: translate3d(0px, ' + yPos + 'px, 0px)');
            }
        })
    }
    $(window).on("load", function() {
        scrollParallax()
    })

    // Selectize
    $(".location").selectize({
        maxItems: 1
    });
    $(".travelType").selectize({
        create: true,
        sortField: 'text'
    });
    $(".datepicker").datepicker();

    $(".booking-input").on("click", function() {
        $("input", this).focus();
        $(this).find(".guest-popup").addClass("active")
    })

    $(".guest-input").on("click", function() {
        $(this).siblings(".guest-popup").addClass("active");
    })

    // Preloader
    $("body").addClass("pre-loaded");

    // Scrolltop
    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 50) {
            $('.navbar-area').addClass('is-sticky');
            $(".fixed-top").addClass("non-fixed");
        } else {
            $('.navbar-area').removeClass('is-sticky');
            $(".fixed-top").removeClass("non-fixed");
        }
        // scrolltop
        if( $(this).scrollTop() > 300 ) {
            $("#scrolltop").addClass("scrolltopactive");
        }
        else {
            $("#scrolltop").removeClass("scrolltopactive");
        }
    });
    // animation triggers
    $(window).scroll();
    $("#scrolltop").on('click', function () {
        $("html").animate({
            scrollTop: 0
        }, 2000);
        return false;
    });

    // Language-switcher
    $(".language-option").each(function() {
        var each = $(this)
        each.find(".lang-name").html(each.find(".language-dropdown-menu a:nth-child(1)").text());
        var allOptions = $(".language-dropdown-menu").children('a');
        each.find(".language-dropdown-menu").on("click", "a", function() {
             allOptions.removeClass('selected');
             $(this).addClass('selected');
             $(this).closest(".language-option").find(".lang-name").html($(this).text());
        });
    })

    // Featured-product
    $(".feature-product-filter-list li").on("click", function() {
        var tab_modal = $(this).attr("data-feature-filter-list");
        $(this).addClass("active").siblings().removeClass("active");
        $(".feature-product-filter-item[data-feature-filter-item=" +tab_modal+ "]").addClass("active").siblings().removeClass("active");
    })

    // Mobile Booking Search
    $(".mobile-search-collapse").on("click", function() {
        $(".mobile-search-wrapper").toggleClass("active");
        $(".mobile-booking-search").toggleClass("active");
        $("body").toggleClass("mobile-booking-search-body");
    })

    // Mobile-option-dot
    $(".mobile-option-dot").on("click", function(e) {
        e.preventDefault()
        $(this).siblings(".mobile-option-dropdown").toggleClass("show");
    })
    $("body").on('click',function(e){
        if(!$(".mobile-option-dot").is(e.target) && $(".mobile-option-dot").has(e.target).length===0 && $('.show').has(e.target).length===0){
            $(".mobile-option-dropdown").removeClass('show');
        }
        if((!$(".booking-input").is(e.target) && $(".booking-input").has(e.target).length===0) && (!$(".mobile-search-item").is(e.target) && $(".mobile-search-item").has(e.target).length===0)){
            $(".guest-popup").removeClass("active")
        }
    })

    // Top-sidebar-action
    $(".top-sidebar-action").on("click", function(e) {
        e.preventDefault()
        $(".top-sidebar-wrapper").addClass("active");
    })
    $(".topbar-sidebar-close").on("click", function() {
        $(".top-sidebar-wrapper").removeClass("active");
    })

    // Guest buttons
    $(".counter-btn").on("click", function(e) {
        e.preventDefault();
        var btn = $(this),
        inp = btn.siblings(".counter-input").val(), i=0;
        if(btn.hasClass("counter-inc")){
            i = parseFloat(inp) + 1;
        }
        else {
            if (inp > 1) (i = parseFloat(inp) - 1) < 2 && $(".counter-dec").addClass("deact");
            else i = 0;
        }
        btn.addClass("deact").siblings("input").val(i)
        var selfInput = $(".guest");
        let newVal = i;
        if (newVal == 1) {
            selfInput.val(newVal+ " Guest")
        }
        else if (newVal > 1) {
            selfInput.val(newVal+ " Guests")
        }
        else if (newVal < 1) {
            selfInput.val("Select Number Of Guest")
        }
    })

    // Popular package carousel
    var popularCarousel = $(".popular-package-carousel");
    popularCarousel.owlCarousel({
        loop: true,
        nav: false,
        dots: false,
        margin: 20,
        smartSpeed: 1500,
        autoHeight: true,
        responsive:{
            0: {
                items: 1,
                stagePadding: 0
            },
            576: {
                items: 1,
                stagePadding: 100
            },
            768: {
                items: 2,
                stagePadding: 50
            },
            960: {
                items: 2,
                stagePadding: 100
            },
            1200: {
                items: 2,
                stagePadding: 240
            },
            1700: {
                items: 3,
                stagePadding: 240
            }
        }
    });
    popularCarousel.on('mousewheel', '.owl-stage', function (e) {
        if (e.originalEvent.wheelDelta>0) {
            popularCarousel.trigger('next.owl');
        } else {
            popularCarousel.trigger('prev.owl');
        }
        e.preventDefault();
    });

    // Testimonial carousel
    $(".testimonial-carousel").owlCarousel({
        center: true,
        items: 3,
        loop: true,
        dots: true,
        smartSpeed: 1500,
        responsive:{
            0: {
                items: 1,
                margin: 20
            },
            576: {
                items: 2,
                margin: 20
            },
            992: {
                items: 3,
                margin: 90
            },
            1200: {
                items: 3,
                margin: 120
            },
        }
    });

    // Partner carousel
    $(".partner-carousel").owlCarousel({
        items: 8,
        loop: true,
        dots: false,
        nav: false,
        margin: 20,
        smartSpeed: 1500,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true,
        responsive:{
            0: {
                items: 3,
            },
            576: {
                items: 5,
            },
            992: {
                items: 6,
            },
            1200: {
                items: 8
            }
        }
    });

    // Holiday carousel
    $(".holiday-carousel").owlCarousel({
        items: 4,
        loop: true,
        dots: true,
        dotsEach: 3,
        nav: false,
        margin: 20,
        smartSpeed: 1500,
        responsive:{
            0: {
                items: 1,
                nav: true,
                navText: [
                    "<i class='flaticon-left-arrow'></i>",
                    "<i class='flaticon-right-arrow-angle'></i>"
                ]
            },
            576: {
                items: 2,
            },
            992: {
                items: 3,
                nav: false
            },
            1200: {
                items: 4
            }
        }
    });

    // Gallery carousel
    $(".gallery-carousel").owlCarousel({
        items: 4,
        loop: true,
        dots: true,
        nav: false,
        margin: 20,
        stagePadding: 150,
        smartSpeed: 1500,
        responsive:{
            0: {
                items: 2,
                stagePadding: 0,
                nav: true,
                navText: [
                    "<i class='flaticon-left-arrow'></i>",
                    "<i class='flaticon-right-arrow-angle'></i>"
                ]
            },
            576: {
                items: 3,
                stagePadding: 100
            },
            991: {
                nav: false
            },
            1200: {
                stagePadding: 150
            }
        }
    });

    // More blogs
    $(".more-col-item").slice(0, 6).show();
    $(".product-more-item").slice(0, 8).show();
    $(".hotel-more-item").slice(0, 6).show();
    $(".load-more-btn").on("click", function(e) {
        e.preventDefault();
        $(this).parent(".load-more").siblings(".load-more-gallery").find(".more-col-item:hidden").slice(0, 2).slideDown();
        $(this).parent(".load-more").siblings(".load-more-gallery").find(".product-more-item:hidden").slice(0, 4).slideDown();
        $(this).parent(".load-more").siblings(".load-more-gallery").find(".hotel-more-item:hidden").slice(0, 3).slideDown();
    })

    // Details-card-image-carousel
    $(".details-card-image-carousel").owlCarousel({
        items: 1,
        loop: true,
        dots: false,
        nav: true,
        navText: [
            "<i class='flaticon-left-arrow'></i>",
             "<i class='flaticon-right-arrow-angle'></i>"
        ],
        margin: 0,
        smartSpeed: 1500
    });

    // Product-details-carousel
    $(".product-details-carousel").owlCarousel({
        items: 1,
        loop: false,
        dots: false,
        nav: true,
        navText: [
            "<i class='flaticon-left-arrow'></i>",
            "<i class='flaticon-right-arrow-angle'></i>"
        ],
        margin: 0,
        smartSpeed: 1500
    });

    // Product sort
    $(".product-filter").selectize({
        create: true,
        sortField: 'text'
    });

    // Product-gallery-grid
    $(".product-gallery-grid").magnificPopup({
        delegate: 'a',
        type: 'image',
        tLoading: 'Loading image #%curr%...',
        mainClass: 'mfp-img-mobile',
        gallery: {
        enabled: true,
        navigateByImgClick: true,
        preload: [0,1]
        },
        image: {
            tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
        },
    });

    // Product +/- button
    $(".qu-btn").on("click", function(e) {
        var btn = $(this),
        inp = btn.siblings(".qu-input").val();
        if(btn.hasClass("inc")){
            var i = parseFloat(inp) + 1;
        }
        else {
            if (inp > 1) (i = parseFloat(inp) - 1) < 2 && $(".dec").addClass("deact");
            else i = 1;
        }
        btn.addClass("deact").siblings("input").val(i)
    })

    // Product-tab-list
    $(".product-tab-list li").on("click", function() {
        var tab_modal = $(this).attr("data-product-tab");
        $(this).addClass("active").siblings().removeClass("active");
        $(".product-tab-information-item[data-product-details-tab=" +tab_modal+ "]").addClass("active").siblings().removeClass("active");
    })

    // Recent-product-carousel
    $(".recent-product-carousel").owlCarousel({
        items: 4,
        loop: true,
        dots: false,
        nav: true,
        navText: [
            "<i class='flaticon-left-arrow'></i>",
            "<i class='flaticon-right-arrow-angle'></i>"
        ],
        margin: 20,
        smartSpeed: 1500,
        responsive: {
            0: {
                items: 1,
                stagePadding: 50
            },
            576: {
                items: 2,
                stagePadding: 0
            },
            768: {
                items: 3
            },
            992: {
                items: 4
            }
        }
    });

    // About-selection-content
    $(".about-selection-list li").on("click", function() {
        var tab_modal = $(this).attr("data-about-list");
        $(this).addClass("active").siblings().removeClass("active");
        $(".about-selection-details-item[data-about-details=" +tab_modal+ "]").addClass("active").siblings().removeClass("active");
    })

    // Coupon modal
    $(".coupon-btn").on("click", function(e) {
        e.preventDefault;
        $(".coupon-popup-wrapepr").addClass("active")
    });
    $(".coupon-modal-close").on("click", function() {
        $(".coupon-popup-wrapepr").removeClass("active")
    })

    // Billing-address-input
    $(".billing-title p").on("click", function() {
        $(".billing-address").addClass("none");
        $(".billing-address-input").addClass("active");
    })

    // Authentication tab
    $(".authentication-header ul li").on("click", function() {
        var tab_modal = $(this).attr("data-authentication-list");
        $(this).addClass("active").siblings().removeClass("active");
        $(".authentication-form-box-item[data-authentication-item=" +tab_modal+ "]").addClass("active").siblings().removeClass("active");
    })

    // Magnific-popup
    $(".video-popup").magnificPopup({
        disableOn: 0,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false
    });

    // Coming-soon counter
    function newCounter2() {
        var countDate = new Date("15 October 2025 9:56:00");
        var sec = 1000;
        var min = sec * 60;
        var hr = min * 60;
        var day = hr * 24;
        var today = new Date();
        var distance = countDate - today;
        var days = Math.floor(distance / day);
        var hours = Math.floor((distance % day) / hr);
        var mins = Math.floor((distance % hr) / min);
        var secs = Math.floor((distance % min) / sec);
        $(".day1").html(days + "<span>Days</span>")
        $(".hr1").html(hours + "<span>Hrs</span>")
        $(".min1").html(mins + "<span>Mins</span>")
        $(".sec1").html(secs + "<span>Sec</span>")
        if(distance < 0) {
            clearInterval(dealCounter1);
            $(".new-counter-2").html("Session Expired");
        }
    }
    setInterval(function() {
        newCounter2();
    }, 1000);

    // Split nav
    $(".split-navbar-fixed .main-nav .navbar-nav").clone().appendTo(".split-screen-nav-menu");
    $(".split-screen-nav-menu .navbar-nav li a.dropdown-toggle").on("click", function() {
        $(this).siblings(".dropdown-menu").slideToggle();
    })
    $(".split-collapse-button").on("click", function() {
        $(".split-screen-nav-wrapper").addClass("active");
    })
    $(".split-nav-close i").on("click", function() {
        $(".split-screen-nav-wrapper").removeClass("active");
    })

    // Page search
    $(".page-search-btn").on("click", function(e) {
        e.preventDefault();
        $(".searchbar-wrapper").addClass("active");
    })
    $(".page-searchbar-close").on("click", function() {
        $(".searchbar-wrapper").removeClass("active");
    })

    // Subscribe form
    $("#contactForm, .newsletter-form").validator().on("submit", function(event) {
        if (event.isDefaultPrevented()) {
            // handle the invalid form...
            formErrorSub();
            submitMSGSub(false, "Please enter your email correctly.");
        } else {
            // everything looks good!
            event.preventDefault();
        }
    });
    function callbackFunction(resp) {
        if (resp.result === "success") {
            formSuccessSub();
        } else {
            formErrorSub();
        }
    }
    function formSuccessSub() {
        $(".newsletter-form")[0].reset();
        submitMSGSub(true, "Thank you for subscribing!");
        setTimeout(function() {
            $("#validator-newsletter").addClass('hide');
        }, 4000)
    }
    function formErrorSub() {
        $(".newsletter-form").addClass("animate__animated animate__shakeX");
        setTimeout(function() {
            $(".newsletter-form").removeClass("animate__animated animate__shakeX");
        }, 1000)
    }
    function submitMSGSub(valid, msg) {
        if (valid) {
            var msgClasses = "validation-success submit-post-info";
        } else {
            var msgClasses = "validation-danger submit-post-info";
        }
        $("#validator-newsletter").removeClass().addClass(msgClasses).text(msg);
    }

    // ajax mailchimp
    $(".newsletter-form").ajaxChimp({
        url: "https://hibootstrap.us20.list-manage.com/subscribe/post?u=60e1ffe2e8a68ce1204cd39a5&amp;id=42d6d188d9", // Your url MailChimp
        callback: callbackFunction
    });
});