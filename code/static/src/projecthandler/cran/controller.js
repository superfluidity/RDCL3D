if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.CranController = (function(global) {
    'use strict';

    var DEBUG = true;

    CranController.prototype.constructor = CranController;

    /**
     * Constructor
     */
    function CranController() {


    }


    CranController.prototype.addNode = function(graph_editor, node, success, error) {
        log('addNode');
        var data_to_send = {
                'group_id': node.info.group &&  node.info.group.length > 0 ? node.info.group[0] : undefined,
                'element_id': node.id,
                'element_type': node.info.type,
                'element_desc_id': node.info.desc_id,
                'element_rfb_level': node.info.element_rfb_level,
                'x': node.x,
                'y': node.y
         };
        new dreamer.GraphRequests().addNode(data_to_send, null, function() {
            if (success)
                success();
        },error);
    };

    CranController.prototype.addLink = function(graph_editor, link, success, error) {
        log('addLink');
        var data_to_send = {
            'element_desc_id': getUrlParameter('id'),
            'source': link.source.id,
            'target': link.target.id,
            //'rfb_level': link.rfb_level
        };
        new dreamer.GraphRequests().addLink(data_to_send, null, function() {
            graph_editor._deselectAllNodes();
            if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                graph_editor.parent.removeLink.call(graph_editor, old_link[0].index);
            }
            if (success) {
                success();
            }
        },error);
    };

    CranController.prototype.removeNode = function(graph_editor, node, success, error) {
        log('removeNode');
        new dreamer.GraphRequests().removeNode(node, null, function() {
            if (success) {
                success();
            }
        },error);
    };

    CranController.prototype.removeLink = function(graph_editor, link, success, error) {
        log('removeLink');
        var s = link.source;
        var d = link.target;
        new dreamer.GraphRequests().removeLink(link, function() {
            if (success) {
                success();
            }
        },error);
    };

    /**
     * Log utility
     */
    function log(text) {
        if (DEBUG)
            console.log("::CranController::", text);
    }

    return CranController;
}(this));

if (typeof module === 'object') {
    module.exports = dreamer.CranController;
}