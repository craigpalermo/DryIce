$(document).ready(function() {
    $countdown = $('#countdown');
    var end = moment($countdown.data('expire_time'));
    var unixtime = new Date(end).getTime() / 1000;
    $('#countdown').scojs_countdown({until:unixtime});


    var url = $("#download-link").attr("href");

    if (checkURL(url)) {
        $("#image").attr('src', url);
    } else if (checkURLCode(url)) {
        $("#code-preview").load(url, function() {
            prettyPrint();
        });
    }
});

function checkURL(url) {
    return(url.match(/\.(jpeg|jpg|gif|png)$/) != null);
}

function checkURLCode(url) {
    return(url.match(/\.(bsh|c|cc|cpp|cs|csh|cyc|cv|htm|html|java|js|m|mxml|perl|pl|pm|py|rb|sh|xhtml|xml|xsl)$/) != null);
}
