
$(function(){
    var app = app || {}

    if (!app.socket)
        app.socket = io.connect('http://' + document.domain + ':' + location.port + '/mining');

    function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
    }

    var tickCount = 0;

    app.socket.on('connect', function() {
        app.socket.emit('identify', {userid: getCookie("userid")});
    });

    app.socket.on('connection', function(data) {
        $("#connected-count").html(data.count + " Connected");
    });

    app.socket.on('block-found', function(data) {
        $("#block-history").append("<div>" + data.id + " " + data.miner + " " + data.height + "</div>")
    });

});