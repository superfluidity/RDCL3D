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

    /**
     * Add a new node to the graph.
     * @param {Object} Required. An object that specifies tha data of the new node.
     * @returns {boolean}
     */
    GraphRequests.prototype.addNode = function(args) {
        switch(args.info.type){
            case 'ns_cp':
                this.add_sapd(args.info.group, args.id)
                break;
        }
    };

    GraphRequests.prototype.add_sapd= function(ns_id, sap_id){
        console.log('ajax add sap')
        var data = new FormData();
        data.append('csrfmiddlewaretoken', getCookie('csrftoken'));
        data.append('ns_id', ns_id);
        data.append('sap_id', sap_id);
        $.ajax({
            url: "sap",
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