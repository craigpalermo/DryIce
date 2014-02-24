$(document).ready(function() {
    $countdown = $('#countdown');
    var end = moment($countdown.data('expire_time'));
    var unixtime = new Date(end).getTime() / 1000;
    $('#countdown').scojs_countdown({until:unixtime});


    var url = $("#download-link").attr("href");

    if (checkURL(url)) {
        $("#image").attr('src', url);
    }
});

function checkURL(url) {
    return(url.match(/\.(jpeg|jpg|gif|png)$/) != null);
}
