(function ($) {
    "use strict";

    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });


    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });


    // Main News carousel
    $(".main-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        items: 1,
        dots: true,
        loop: true,
        center: true,
    });


    // Tranding carousel
    $(".tranding-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 2000,
        items: 1,
        dots: false,
        loop: true,
        nav: true,
        navText: [
            '<i class="fa fa-angle-left"></i>',
            '<i class="fa fa-angle-right"></i>'
        ]
    });


    // Carousel item 1
    $(".carousel-item-1").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        items: 1,
        dots: false,
        loop: true,
        nav: true,
        navText: [
            '<i class="fa fa-angle-left" aria-hidden="true"></i>',
            '<i class="fa fa-angle-right" aria-hidden="true"></i>'
        ]
    });

    // Carousel item 2
    $(".carousel-item-2").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 30,
        dots: false,
        loop: true,
        nav: true,
        navText: [
            '<i class="fa fa-angle-left" aria-hidden="true"></i>',
            '<i class="fa fa-angle-right" aria-hidden="true"></i>'
        ],
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 1
            },
            768: {
                items: 2
            }
        }
    });


    // Carousel item 3
    $(".carousel-item-3").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 30,
        dots: false,
        loop: true,
        nav: true,
        navText: [
            '<i class="fa fa-angle-left" aria-hidden="true"></i>',
            '<i class="fa fa-angle-right" aria-hidden="true"></i>'
        ],
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 1
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            }
        }
    });


    // Carousel item 4
    $(".carousel-item-4").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 30,
        dots: false,
        loop: true,
        nav: true,
        navText: [
            '<i class="fa fa-angle-left" aria-hidden="true"></i>',
            '<i class="fa fa-angle-right" aria-hidden="true"></i>'
        ],
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 1
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    });

})(jQuery);
// comment

$('#postCommentButton').click(function () {
    console.log('post comment button clicked.');
    var comm = $('#comment').val();
    var user_id = $('#user_id').val();
    var post_id = $('#post_id').val();
    var csr = $('input[name=csrfmiddlewaretoken]').val();
    my_data = { comment_text: comm, user_id: user_id, post_id: post_id, csrfmiddlewaretoken: csr };
    $.ajax({
        url: '/postcomment/',
        method: "POST",
        data: my_data,
        success: function (data) {
            $('#comments_count').load(location.href + " #comments_count");
            $('#main-comment-section').load(location.href + " #main-comment-section");
        }
    })
    $("#comment").val('');
});
function comment_reply(cmnt_id) {
    // $('.postReplyButton').click(function () {
    console.log('post reply button clicked.');
    // var comm_id = $('#comm_coll').val();
    var comm_id = cmnt_id;
    var user_id = $('#user_id').val();
    var post_id = $('#post_id').val();
    var reply_text = $('#reply' + cmnt_id).val();
    var csr = $('input[name=csrfmiddlewaretoken]').val();
    my_data = { reply_text: reply_text, user_id: user_id, post_id: post_id, comment_id: comm_id, csrfmiddlewaretoken: csr };
    $.ajax({
        url: '/commentreply/',
        method: "POST",
        data: my_data,
        success: function (data) {
            $('#comments_count').load(location.href + " #comments_count");
            $('#main-comment-section').load(location.href + " #main-comment-section");
        }
    })
    $(".reply").val('');
    // });
}
function subscribe() {
    console.log('subscribe button clicked.');
    var post_id = $('#post_id').val();
    var user_id = $('#user_id').val();
    var author_id = $('#author_id').val();
    var csr = $('input[name=csrfmiddlewaretoken]').val();
    my_data = { user_id: user_id, post_id: post_id, author_id: author_id, csrfmiddlewaretoken: csr };
    $.ajax({
        url: '/subscribe/',
        method: "POST",
        data: my_data,
        success: function (data) {
            $('#newsletter').load(location.href + " #newsletter");
        }
    })
}
function unsubscribe() {
    console.log('unsubscribe button clicked.');
    var post_id = $('#post_id').val();
    var user_id = $('#user_id').val();
    var author_id = $('#author_id').val();
    var csr = $('input[name=csrfmiddlewaretoken]').val();
    my_data = { user_id: user_id, post_id: post_id, author_id: author_id, csrfmiddlewaretoken: csr };
    $.ajax({
        url: '/unsubscribe/',
        method: "POST",
        data: my_data,
        success: function (data) {
            $('#newsletter').load(location.href + " #newsletter");
        }
    })
}
