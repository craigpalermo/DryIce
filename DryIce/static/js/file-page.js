$(document).ready(function() {
    $countdown = $('#countdown');
    var end = moment($countdown.data('expire_time'));
    var unixtime = new Date(end).getTime() / 1000;
    $('#countdown').scojs_countdown({until:unixtime});
});
