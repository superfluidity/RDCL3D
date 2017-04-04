$(document).ready(function () {

    // init selector



    $("body").bind("ajaxSend", function (elm, xhr, s) {
        if (s.type == "POST") {
            xhr.setRequestHeader('csrftoken', $('#csrfmiddlewaretoken').val());
        }
    });



});
