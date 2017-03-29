if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.ExampletokenController = (function(global) {
    'use strict';

    var DEBUG = true;

    ExampletokenController.prototype.constructor = ExampletokenController;

    /**
     * Constructor
     */
    function ExampletokenController() {


    }


    ExampletokenController.prototype.addNode = function(self, node, success, error) {
        log('addNode');
        new dreamer.GraphRequests().addNode(node, null, function() {
            if (success)
                success();
        },error);
    };

    ExampletokenController.prototype.addLink = function(self, link, success, error) {
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

    ExampletokenController.prototype.removeNode = function(self, node, success, error) {
        log('removeNode');
        new dreamer.GraphRequests().removeNode(node, null, function() {
            if (success) {
                success();
            }
        },error);
    };

    ExampletokenController.prototype.removeLink = function(self, link, success, error) {
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
            console.log("::ExampletokenController::", text);
    }

    return ExampletokenController;
}(this));

if (typeof module === 'object') {
    module.exports = dreamer.ExampletokenController;
}