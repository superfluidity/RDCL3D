if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.GraphRequests = (function(global) {
    'use strict';

    var DEBUG = true;

    GraphRequests.prototype.constructor = GraphRequests;

    /**
     * Constructor
     */
    function GraphRequests(args) {


    }

   GraphRequests.prototype.addNode= function(args){
        var data = new FormData();
        data.append('csrfmiddlewaretoken', getCookie('csrftoken'));
        data.append('group_id', args.info.group);
        data.append('element_id', args.id);
        data.append('element_type', args.info.type);
        $.ajax({
            url: "addelement",
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(result) {
            },
            error: function(result) {
                alert("some error");
            }
        });
    };

   GraphRequests.prototype.removeNode= function(args){
        var data = new FormData();
        data.append('csrfmiddlewaretoken', getCookie('csrftoken'));
        data.append('group_id', args.info.group);
        data.append('element_id', args.id);
        data.append('element_type', args.info.type);
        $.ajax({
            url: "removeelement",
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(result) {
            },
            error: function(result) {
                alert("some error");
            }
        });
    };

   GraphRequests.prototype.addLink= function(source, destination){
        var data = new FormData();
        data.append('csrfmiddlewaretoken', getCookie('csrftoken'));
        data.append('source', JSON.stringify(source));
        data.append('destination', JSON.stringify(destination));
        $.ajax({
            url: "addlink",
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(result) {
            },
            error: function(result) {
                alert("some error");
            }
        });
    };

    GraphRequests.prototype.getCookie =  function (name) {
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
    };



    return GraphRequests;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.GraphRequests;
}