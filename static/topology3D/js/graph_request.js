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

    GraphRequests.prototype.addNode = function(args, choice, success, error) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
        data.append('group_id', args.info.group[0]);
        data.append('element_id', args.id);
        data.append('element_type', args.info.type);
        if(args.info.desc_id)
            data.append('element_desc_id', args.info.desc_id || '');
        //FIXME questo metodo dovrebbere essere generico
        if(args.existing_vnf)
            data.append('existing_vnf', args.existing_vnf ? args.existing_vnf : false)
        if (choice)
            data.append('choice', choice);
        $.ajax({
            url: "addelement",
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(result) {
                if (success)
                    success();
            },
            error: function(result) {
                if (error)
                    error();
                log("some error: " + result);
            }
        });
    };

    GraphRequests.prototype.removeNode = function(args, choice, success, error) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
        data.append('group_id', args.info.group[0]);
        data.append('element_id', args.id);
        data.append('element_type', args.info.type);
        if (choice)
            data.append('choice', choice);
        $.ajax({
            url: "removeelement",
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(result) {
                if (success)
                    success();
            },
            error: function(result) {
                if (error)
                    error();
            }
        });
    };



    GraphRequests.prototype.addLink = function(link, choice, success, error) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
        data.append('link', JSON.stringify(link));

        //data.append('destination', JSON.stringify(destination));
        if (choice)
            data.append('choice', choice);
        $.ajax({
            url: "addlink",
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(result) {
                if (success)
                    success();
            },
            error: function(result) {
                if (error)
                    error();
                log("some error: " + result);
            }
        });
    };

    GraphRequests.prototype.removeLink = function(link, success, error) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
        data.append('link', JSON.stringify(link));
        $.ajax({
            url: "removelink",
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(result) {
                if (success)
                    success();
            },
            error: function(result) {
                if (error)
                    error();
                log("some error: " + result);
            }
        });
    };

    //
    GraphRequests.prototype.getAvailableNodes = function(args, success, error){
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
        $.ajax({
            url: "availablenodes?layer="+args.layer,
            type: 'GET',
            success: function(result) {

                if (success)
                    success(result);
            },
            error: function(result) {
                if (error)
                    error();
                log("some error: " + result);
            }
        });
    }

    GraphRequests.prototype.savePositions = function(positions, success, error) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
        data.append('positions', JSON.stringify(positions));
        $.ajax({
            url: "positions",
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(result) {
                if (success)
                    success();
            },
            error: function(result) {
                if (error)
                    error();
                log("some error: " + result);
            }
        });
    };

    /*  START ETSI methods  */
    GraphRequests.prototype.addVnffg = function(args, success, error) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
        data.append('group_id', args.info.group[0]);
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
                if (success)
                    success(result);
            },
            error: function(result) {
                if (error)
                    error();
                log("some error: " + result);
            }
        });
    };

    GraphRequests.prototype.addNodeToVnffg = function(args, success, error) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
        data.append('group_id', args.info.group[0]);
        data.append('element_id', args.id);
        data.append('element_type', args.info.type);
        data.append('vnffg_id', args.vnffgId);
        $.ajax({
            url: "addnodetovnffg",
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(result) {
                if (success)
                    success(result);
            },
            error: function(result) {
                if (error)
                    error();
                log("some error: " + result);
            }
        });
    };

    GraphRequests.prototype.getUnusedVnf = function(nsd_id, success, error) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
        $.ajax({
            url: "unusedvnf/" + nsd_id,
            type: 'GET',
            success: function(result) {
                if (success)
                    success(result);
            },
            error: function(result) {
                if (error)
                    error();
                log("some error: " + result);
            }
        });

    };
    /*  END ETSI methods  */

    GraphRequests.prototype.getCookie = function(name) {
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


    /**
     * Log utility
     */
    function log(text) {
        if (DEBUG)
            console.log("::GraphRequests::", text);
    }

    return GraphRequests;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.GraphRequests;
}