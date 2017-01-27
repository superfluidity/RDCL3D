if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.OshiController = (function(global) {
    'use strict';

    var DEBUG = true;

    OshiController.prototype.constructor = OshiController;

    /**
     * Constructor
     */
    function OshiController() {


    }

    OshiController.prototype.addNode = function(self, node, success, error) {
        new dreamer.GraphRequests().addNode(node, null, function() {
            if (success)
                success();
        });
    };

    OshiController.prototype.addLink = function(self, s, d, success, error) {

        new dreamer.GraphRequests().addLink(s, d, null, function() {
            self._deselectAllNodes();
            if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                self.parent.removeLink.call(self, old_link[0].index);
            }
            if (success) {
                success();
            }
        });
    };

    OshiController.prototype.removeNode = function(self, node, success, error) {
        new dreamer.GraphRequests().removeNode(node, null, function() {
            if (success) {
                success();
            }
        });
    };

    OshiController.prototype.removeLink = function(self, link, success, error) {
        var s = link.source;
        var d = link.target;
        new dreamer.GraphRequests().removeLink(s, d, function() {
            if (success) {
                success();
            }
        });
    };

    return OshiController;
}(this));

if (typeof module === 'object') {
    module.exports = dreamer.OshiController;
}