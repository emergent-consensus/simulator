
$(function(){
    var app = app || {}

    if (!app.socket)
        app.socket = io.connect('http://' + document.domain + ':' + location.port + '/mining');


    function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
    }


    app.socket.on('connect', function() {
        app.socket.emit('identify', {userid: getCookie("userid")});
    });

    app.socket.on('connection', function(data) {
        $("#connected-count").html(data.count + " Connected");
    });
});