if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.ClickController = (function(global) {
    'use strict';

    var DEBUG = true;

    ClickController.prototype.constructor = ClickController;

    /**
     * Constructor
     */
    function ClickController() {


    }


    ClickController.prototype.addNode = function(self, node, success, error) {
        console.log("addNode")
        console.log(node, success, error)
        new dreamer.GraphRequests().addNode(node, null, function() {
            if (success)
                success();
        });
    };



    ClickController.prototype.removeNode = function(self, node, success, error) {
        new dreamer.GraphRequests().removeNode(node, null, function() {
            if (success) {
                success();
            }
        });
    };

    ClickController.prototype.removeLink = function(self, link, success, error) {
        var s = link.source;
        var d = link.target;
        new dreamer.GraphRequests().removeLink(s, d, function() {
            if (success) {
                success();
            }
        });
    };


    return ClickController;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.ClickController;
}