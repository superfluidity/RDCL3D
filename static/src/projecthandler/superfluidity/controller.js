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