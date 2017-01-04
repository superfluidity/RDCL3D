if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.EtsiController = (function(global) {
    'use strict';

    var DEBUG = true;

    EtsiController.prototype.constructor = EtsiController;

    /**
     * Constructor
     */
    function EtsiController(args) {


    }

   EtsiController.prototype.chooseId= function(self, args, success, error){

            new dreamer.GraphRequests().addNode(args, null, function() {
                    self.parent.addNode.call(self, args);
                    if (success)
                        success();
                });
    };



    return EtsiController;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.EtsiController;
}