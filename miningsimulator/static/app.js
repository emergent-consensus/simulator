
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

    createNode = function(blockId, minerId, blockHeight) {
        return {innerHTML: "<div>" + blockHeight + "</div>", collapsable: false, HTMLid: blockId}
    }

    app.socket.on('block-found', function(data) {
        $("#block-history").append("<div>" + data.id + " " + data.miner + " " + data.height + "</div>")
        app.network.addNode(data.id, data.miner, data.height, data.parentid)
    });


    app.socket.on('best-nodes', function(data) {
        $("#block-history").html();
        nodes = data.map(function(item) {
            $("#block-history").append("<div>" + item.id + " " + item.miner + " " + item.height + "</div>")
            return createNode(item.id, item.miner, item.height);
        });
        app.network.setInitialState(nodes);
    });


    app.network = app.network || {};


    app.network.init = function() {
        app.network.setInitialState = function(children) {
            var simple_chart_config = {
                chart: {
                    container: "#tree-simple",
                    rootOrientation: "WEST",
                    connectors: {type: "bCurve"},
                    hideRootNode: true,
                },
                nodeStructure: {
                text: { name: "HEAD" },
                HTMLid: "HEADid",
                children:  children
                }
            };
            app.network.my_chart = new Treant(simple_chart_config);
            

                app.network.my_chart.tree.getNodeDb().walk(function (item) {
                           
                $(item.nodeDOM).children().css({padding: "10px"});
            });
        }

        app.network.addNode = function(blockId, minerId, height, parentId)
        {
            var node;
            app.network.my_chart.tree.getNodeDb().walk(function (item) {
                if (item.nodeHTMLid === parentId)
                    node = item;
            });
            var newNode = app.network.my_chart.tree.addNode(node, createNode(blockId, minerId, height));  
            var red =  parseInt(minerId.substr(0, 2), 16);
            var green =  parseInt(minerId.substr(2, 2), 16);
            var cyan = parseInt(minerId.substr(4, 2), 16);      
            var foreground = "#dddddd";
            if (red*0.299 + green*0.587 + cyan*0.114 > 128) {
                foreground = "#000000";
            }
            $(newNode.nodeDOM).css({backgroundColor: "#" + minerId.substr(0, 6)}).children().css({color: foreground, padding: "10px"});
        }
    };

    app.network.init();

});