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


    ToscaController.prototype.addNode = function(self, node, success, error) {
        log('addNode');
        new dreamer.GraphRequests().addNode(node, null, function() {
            if (success)
                success();
        },error);
    };

    ToscaController.prototype.addLink = function(self, link, success, error) {
        log('addLink');

        new dreamer.GraphRequests().addLink(link, null, function() {
            self._deselectAllNodes();
            if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                self.parent.removeLink.call(self, old_link[0].index);
            }
            if (success) {
                success();
            }
        },error);
    };

    ToscaController.prototype.linkCpToVL = function(self, link, success, error) {
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var vl_type = source_type != 'tosca.nodes.nfv.CP' ? source_type : destination_type;
        var cp_id = source_type == 'tosca.nodes.nfv.CP' ? source_id : target_id;
        var old_link = $.grep(self.d3_graph.links, function(e) {
            return (e.source.id == cp_id || e.target.id == cp_id) && (e.source.info.type == vl_type || e.target.info.type == vl_type);
        });
        console.log(vl_type , cp_id)
        new dreamer.GraphRequests().addLink(link, null, function() {
            self._deselectAllNodes();
            if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                self.parent.removeLink.call(self, old_link[0].index);
            }
            if (success) {
                success();
            }
        },error);
    };

    ToscaController.prototype.removeNode = function(self, node, success, error) {
        log('removeNode');
        new dreamer.GraphRequests().removeNode(node, null, function() {
            if (success) {
                success();
            }
        },error);
    };

    ToscaController.prototype.removeLink = function(self, link, success, error) {
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

    return ToscaController;
}(this));

if (typeof module === 'object') {
    module.exports = dreamer.ToscaController;
}