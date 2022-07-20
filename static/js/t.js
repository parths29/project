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
function Unsubscribe() {
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