if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.ToscanfvController = (function(global) {
    'use strict';

    var DEBUG = true;

    ToscanfvController.prototype.constructor = ToscanfvController;

    /**
     * Constructor
     */
    function ToscanfvController() {


    }


    ToscanfvController.prototype.addNode = function(graph_editor, node, success, error) {
        log('addNode');
        var data_to_send = {
                'group_id': node.info.group[0],
                'element_id': node.id,
                'element_type': node.info.type,
                'element_desc_id': node.info.desc_id,
                'x': node.x,
                'y': node.y
         };
         console.log(JSON.stringify(data_to_send))
        new dreamer.GraphRequests().addNode(data_to_send, null, function() {
            if (success)
                success();
        },error);
    };

    ToscanfvController.prototype.addLink = function(graph_editor, link, success, error) {
        log('addLink');

        new dreamer.GraphRequests().addLink(link, null, function() {
            graph_editor._deselectAllNodes();
            if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                graph_editor.parent.removeLink.call(graph_editor, old_link[0].index);
            }
            if (success) {
                success();
            }
        },error);
    };

    ToscanfvController.prototype.linkCpToVLorVDU = function(graph_editor, link, success, error) {
        var vl_types = ['tosca.nodes.nfv.VL', 'tosca.nodes.nfv.VL.ELine', 'tosca.nodes.nfv.VL.ELAN', 'tosca.nodes.nfv.VL.ETree'];
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var vl_type = source_type != 'tosca.nodes.nfv.CP' ? source_type : destination_type;
        var cp_id = source_type == 'tosca.nodes.nfv.CP' ? source_id : target_id;
        var old_link = $.grep(graph_editor.d3_graph.links, function(e) {
            if (vl_type == 'tosca.nodes.nfv.VDU'){
                return (e.source.id == cp_id || e.target.id == cp_id) && (e.source.info.type=='tosca.nodes.nfv.VDU' || e.target.info.type == 'tosca.nodes.nfv.VDU');

            }else{
                return (e.source.id == cp_id || e.target.id == cp_id) && (vl_types.indexOf(e.source.info.type)>=0 || vl_types.indexOf(e.target.info.type)>=0);
            }
        });
        console.log(vl_type , cp_id)
        new dreamer.GraphRequests().addLink(link, null, function() {
            graph_editor._deselectAllNodes();
            if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                graph_editor.parent.removeLink.call(graph_editor, old_link[0].index);
            }
            if (success) {
                success();
            }
        },error);
    };

    ToscanfvController.prototype.linkVNFtoVL = function(graph_editor, link, success, error) {
        var vl_types = ['tosca.nodes.nfv.VL', 'tosca.nodes.nfv.VL.ELine', 'tosca.nodes.nfv.VL.ELAN', 'tosca.nodes.nfv.VL.ETree'];
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var vl_type = source_type != 'tosca.nodes.nfv.VNF' ? source_type : destination_type;
        var cp_id = source_type == 'tosca.nodes.nfv.VNF' ? source_id : target_id;
        var old_link = $.grep(graph_editor.d3_graph.links, function(e) {
            return (e.source.id == cp_id || e.target.id == cp_id) && (vl_types.indexOf(e.source.info.type)>=0 || vl_types.indexOf(e.target.info.type)>=0);
        });
        console.log(vl_type , cp_id)
        new dreamer.GraphRequests().addLink(link, null, function() {
            graph_editor._deselectAllNodes();
            if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                graph_editor.parent.removeLink.call(graph_editor, old_link[0].index);
            }
            if (success) {
                success();
            }
        },error);
    };

    ToscanfvController.prototype.removeNode = function(graph_editor, node, success, error) {
        log('removeNode');
        /*
        data.append('group_id', args.info.group[0]);
        data.append('element_id', args.id);
        data.append('element_type', args.info.type);*/
        var data_to_send = {
            'group_id': node.info.group[0],
            'element_id': node.id,
            'element_type': node.info.type
        };
        new dreamer.GraphRequests().removeNode(data_to_send, null, function() {
            if (success) {
                success();
            }
        },error);
    };

    ToscanfvController.prototype.removeLink = function(graph_editor, link, success, error) {
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
            console.log("::ToscaController::", text);
    }

    return ToscanfvController;
}(this));

if (typeof module === 'object') {
    module.exports = dreamer.ToscanfvController;
}