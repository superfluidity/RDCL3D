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
         SuperfluidityController.etsiController = new dreamer.EtsiController();

    }

    SuperfluidityController.prototype.addVnf = function(self, node, success, error) {
        SuperfluidityController.etsiController.addVnf(self, node, success, error);
    };

    SuperfluidityController.prototype.addVnfVdu = function(self, node, success, error) {
        SuperfluidityController.etsiController.addVnfVdu(self, node, success, error);
    }

    SuperfluidityController.prototype.addVnfVduCp = function(self, node, success, error) {
         SuperfluidityController.etsiController.addVnfVduCp(self, node, success, error);
    }

    SuperfluidityController.prototype.nsCpExclusiveConnection = function(self, link, success, error) {
        SuperfluidityController.etsiController.nsCpExclusiveConnection(self, link, success, error);
    }

    SuperfluidityController.prototype.linkVnftoNsVl = function(self, link, success, error) {
        SuperfluidityController.etsiController.linkVnftoNsVl(self, link, success, error);
    }

    SuperfluidityController.prototype.linkVnftoNsCp = function(self, link, success, error) {
        SuperfluidityController.etsiController.linkVnftoNsCp(self, link, success, error);
    }

    SuperfluidityController.prototype.linkVltoVduCp = function(self, link, success, error) {
        SuperfluidityController.etsiController.linkVltoVduCp(self, link, success, error);
    }

   SuperfluidityController.prototype.linkVnfVltoExpCp = function(self, link, success, error) {
        SuperfluidityController.etsiController.linkVnfVltoExpCp(self, link, success, error);
   }

   SuperfluidityController.prototype.removeVnfVdu = function(self, node, success, error) {
        SuperfluidityController.etsiController.removeVnfVdu(self, node, success, error);
   }

    SuperfluidityController.prototype.removeVnfVduCp = function(self, node, success, error) {
        SuperfluidityController.etsiController.removeVnfVduCp(self, node, success, error);
    }

    SuperfluidityController.prototype.addNode = function(self, node, success, error) {
        if(self.getCurrentView()!= 'click'){
            SuperfluidityController.etsiController.addNode(self, node, success, error);
        }
    };

    SuperfluidityController.prototype.addToCurrentVNFFG = function(self, args, error) {
        if(self.getCurrentView()!= 'click'){
            SuperfluidityController.etsiController.addToCurrentVNFFG(self, args, error);
        }
    }

    SuperfluidityController.prototype.removeNode = function(self, node, success, error) {
        if(self.getCurrentView()!= 'click'){
            new dreamer.GraphRequests().removeNode(node, null, function() {
                if (success) {
                    success();
                }
            });
         }
    };

    SuperfluidityController.prototype.removeLink = function(self, link, success, error) {
        if(self.getCurrentView()!= 'click'){
            new dreamer.GraphRequests().removeLink(link, success,error);
        }
    };


    return SuperfluidityController;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.SuperfluidityController;
}