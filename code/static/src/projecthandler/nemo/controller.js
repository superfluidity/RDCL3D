if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.NemoController = (function(global) {
    'use strict';

    var DEBUG = true;

    NemoController.prototype.constructor = NemoController;

    /**
     * Constructor
     */
    function NemoController() {


    }

    NemoController.prototype.addNodemodel = function(self, node, success, error) {
        if (node.existing_vnf) {
            new dreamer.GraphRequests().addNode(node, null, function() {
                if (success)
                    success();
            });

        } else {
            new dreamer.GraphRequests().addNode(node, null, function() {
                var vnf_ext_cp = {
                    'id': 'vnf_ext_cp' + "_" + node.id,
                    'info': {
                        'type': 'vnf_ext_cp',
                        'group': [node.id]
                    },
                    'x': node.x,
                    'y': node.y
                }
                new dreamer.GraphRequests().addNode(vnf_ext_cp, null, function() {
                    self.parent.addNode.call(self, vnf_ext_cp);
                    if (success)
                        success();
                });
            });
        }

    };

    NemoController.prototype.addNode = function(self, node, success, error) {
        console.log("addNode")
        console.log(node, success, error)
        new dreamer.GraphRequests().addNode(node, null, function() {
            if (success)
                success();
        });
    };




    NemoController.prototype.linkNode2Node = function(self, link, success, error) {
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var vnf_ext_cp_id = source_type == 'vnf_ext_cp' ? source_id : target_id;
        var old_link = $.grep(self.d3_graph.links, function(e) {
            return (e.source.id == vnf_ext_cp_id || e.target.id == vnf_ext_cp_id);
        });
        new dreamer.GraphRequests().addLink(link,  null, function() {
            self._deselectAllNodes();
            if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                self.parent.removeLink.call(self, old_link[0].index);
            }
            if (success) {
                success();
            }
        });
    };
    NemoController.prototype.removeNode = function(self, node, success, error) {
        new dreamer.GraphRequests().removeNode(node, null, function() {
            if (success) {
                success();
            }
        });
    };

    NemoController.prototype.removeLink = function(self, link, success, error) {
        log("removeLink " + JSON.stringify(link))

        new dreamer.GraphRequests().removeLink(link, success, error);
    };



    /**
     * Log utility
     */
    function log(text) {
        if (DEBUG)
            console.log("::EtsiController::", text);
    }

    return NemoController;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.NemoController;
}
