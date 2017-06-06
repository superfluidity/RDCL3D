if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.ToscaController = (function(global) {
    'use strict';

    var DEBUG = true;

    ToscaController.prototype.constructor = ToscaController;

    /**
     * Constructor
     */
    function ToscaController() {


    }


    ToscaController.prototype.addNode = function(graph_editor, node, success, error) {
        log('addNode');
        var data_to_send = {
                'group_id': node.info.group[0],
                'element_id': node.id,
                'element_type': node.info.type,
                'element_desc_id': node.info.desc_id,
                'x': node.x,
                'y': node.y
         };
        new dreamer.GraphRequests().addNode(data_to_send, null, function() {
            if (success)
                success();
        },error);
    };

    ToscaController.prototype.removeNode = function(graph_editor, node, success, error) {
        log('removeNode');
         var data_to_send = {
            'group_id': node.info.group[0],
            'element_id': node.id,
            'element_type': node.info.type,
            'element_desc_id': node.info.desc_id,
        };
        new dreamer.GraphRequests().removeNode(data_to_send, null, function() {
            if (success) {
                success();
            }
        },error);
    };

    ToscaController.prototype.addLink = function(graph_editor, link, success, error) {
        log('addLink');
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var old_link = $.grep(graph_editor.d3_graph.links, function(e) {
            return ((e.source.id == source_id || e.target.id == source_id) ||(e.source.id == target_id || e.target.id == target_id)) &&
            ((e.source.info.type == source_type && e.target.info.type == destination_type) || (e.source.info.type == destination_type && e.target.info.type == source_type));
        });
        var data_to_send = {
            'desc_id': link.desc_id,
            'source': link.source.id,
            'source_type': link.source.info.type,
            'target': link.target.id,
            'target_type': link.target.info.type,
            'view': link.view,
            'group': link.group
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

    ToscaController.prototype.removeLink = function(graph_editor, link, success, error) {
        log('removeLink');
        var data_to_send = {
            'desc_id': link.desc_id,
            'source': link.source.id,
            'source_type': link.source.info.type,
            'target': link.target.id,
            'target_type': link.target.info.type,
            'view': link.view,
            'group': link.group
        };
        new dreamer.GraphRequests().removeLink(data_to_send, function() {
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
            console.log("::ToscaController::", text);
    }

    return ToscaController;
}(this));

if (typeof module === 'object') {
    module.exports = dreamer.ToscaController;
}