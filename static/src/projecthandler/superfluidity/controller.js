if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.SuperfluidityController = (function(global) {
    'use strict';

    var DEBUG = true;

    SuperfluidityController.prototype.constructor = SuperfluidityController;

    /**
     * Constructor
     */
    function SuperfluidityController() {


    }

    SuperfluidityController.prototype.addVnf = function(self, node, success, error) {
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


    SuperfluidityController.prototype.addNode = function(self, node, success, error) {

        new dreamer.GraphRequests().addNode(node, null, function() {
            if (success)
                success();
        });
    };



    SuperfluidityController.prototype.removeNode = function(self, node, success, error) {
        new dreamer.GraphRequests().removeNode(node, null, function() {
            if (success) {
                success();
            }
        });
    };

    SuperfluidityController.prototype.removeLink = function(self, link, success, error) {

        new dreamer.GraphRequests().removeLink(link, success,error);
    };


    return SuperfluidityController;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.SuperfluidityController;
}