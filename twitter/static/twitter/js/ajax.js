function csrf() {
    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
// Setup ajax connections safetly

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
}

function addRemoveBlogLike(){
    $("form.add-remove-like").each((index, el) => {
        $(el).on("submit", (e) => {
            e.preventDefault();

            const post_id = $(el).find("input[name=post_id]").val();
            const user_id = $(el).find("input[name=user_id]").val();
            const post_likes_id = $(el).find("input[name=post_likes_id]").val();

            if ($(e.currentTarget).hasClass('add-post-like')){
                $.ajax({
                    url: "/like/add-ajax/",
                    type: "POST",
                    dataType: "json",
                    data: {
                        post_id: post_id,
                        user_id: user_id,
                    },
                    success: (data) => {
                        console.log(data);
                        if(data['add']){
                            $(el).removeClass('add-post-like').addClass('remove-post-like');
                            $(el).attr('action', '/twitter/like/remove-ajax/');
                            $(el).find('.like-btn-wrap').empty();
                            $(el).find('.like-btn-wrap').html("
                                <button type="submit" class="remove-like-btn btn bnt-danger">
                                <i class="fi-xnluxl-heart"></i>
                                <span class="likes-qty"></span>
                                </button>"");
                            }

                    }
                })
            }
            if ($(e.currentTarget).hasClass('remove-post-like')){
                $.ajax({
                    url: "/like/remove-ajax/",
                    type: "POST",
                    dataType: "json",
                    data: {
                        post_id: post_id,
                        user_id: user_id,
                        post_likes_id: post_likes_id,
                    },
                    success: (data) => {
                        console.log(data);
                        if(data['remove']){
                            $(el).removeClass('remove-post-like').addClass('add-post-like');
                            $(el).attr('action', '/twitter/like/add-ajax/');
                            $(el).find('.like-btn-wrap').empty();
                            $(el).find('.like-btn-wrap').html("
                                <button type="submit" class="remove-like-btn btn bnt-danger">
                                <i class="fi-xnluxl-heart"></i>
                                <span class="likes-qty"></span>
                                </button>"");
                            }

                    }
                })
            }

        })
    )}

}


$document.ready(()=> {
    csrf();
    addRemoveBlogLike();
});