/*
   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an  BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

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

        data = args_to_formdata(args, data);

        //FIXME questo metodo dovrebbere essere generico
        if(args.existing_element)
            data.append('existing_element', args.existing_element ? args.existing_element : false)
        //if (choice)
        //    data.append('choice', choice);
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
                    error(result);
                log("some error: " + result);
            }
        });
    };

    GraphRequests.prototype.removeNode = function(args, choice, success, error) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));

        data = args_to_formdata(args, data);

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
                    error(result);
            }
        });
    };

    GraphRequests.prototype.getNodeOverview = function(args, success, error) {

        var params = jQuery.param(args)
        console.log("params", params)
        $.ajax({
            url: "overviewelement?"+params,
            type: 'GET',
            success: function(result) {
                if (success)
                    success(result);
            },
            error: function(result) {
                if (error)
                    error(result);
            }
        });
    };

    GraphRequests.prototype.addLink = function(args, choice, success, error) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
        data = args_to_formdata(args, data);

        //data.append('destination', JSON.stringify(destination));
        if (choice)
            data.append('choice', choice);
        //if(link.desc_id)
        //    data.append('element_desc_id', link.desc_id || '');
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
                    error(result);
                log("some error: " + result);
            }
        });
    };

    GraphRequests.prototype.removeLink = function(args, success, error) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
        data = args_to_formdata(args, data);

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
                    error(result);
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
                    error(result);
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
                    error(result);
                log("some error: " + result);
            }
        });
    };

    /*  START ETSI methods  */
    GraphRequests.prototype.addVnffg = function(args, success, error) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
       /* data.append('group_id', args.info.group[0]);
        data.append('element_id', args.id);
        data.append('element_type', args.info.type);*/
        data = args_to_formdata(args, data);
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
                    error(result);
                log("some error: " + result);
            }
        });
    };

    GraphRequests.prototype.addNodeToVnffg = function(args, success, error) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
       /* data.append('group_id', args.info.group[0]);
        data.append('element_id', args.id);
        data.append('element_type', args.info.type);
        data.append('vnffg_id', args.vnffgId);*/
        data = args_to_formdata(args, data);

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
                    error(result);
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
                    error(result);
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

    function args_to_formdata(args, form_data){
        for ( var key in args ) {
            form_data.append(key, args[key]);
        }
        return form_data;
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
