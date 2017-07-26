function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}


$(document).ready(function () {

    //event section

    // save if sidebar is collapsed or not
    $('.sidebar-toggle').click(function (event) {
        event.preventDefault();
        var cookie = getCookie("collapsed_sidebar");
        if (cookie != "") {
            setCookie("collapsed_sidebar", "")
        } else {
            setCookie("collapsed_sidebar", "1")
        }
    });

});