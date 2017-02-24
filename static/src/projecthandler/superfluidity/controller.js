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
         var vnf_id = node.info.group[0];
        var vnf_vdus = $.grep(self.d3_graph.nodes, function(e) {
            return (e.info.group.indexOf(vnf_id) >= 0 && (e.info.type == 'vnf_vdu' || e.info.type == 'vnf_click_vdu'));
        });
        if (success)
            success();
        if (typeof vnf_vdus == 'undefined' || vnf_vdus.length <= 0) {
            alert('You should add a VDU')
        } else {
            console.log(vnf_vdus)
            showChooserModal('Select the VDU to link', vnf_vdus, function(choice) {
                var target = choice;
                choice = $.grep(vnf_vdus, function(e){ return e.id == choice; });
                console.log(choice)
                choice = vnf_vdus[0].info.type == 'vnf_vdu' ? choice : vnf_vdus[0].vduId;

                new dreamer.GraphRequests().addNode(node, choice, function() {
                    var link = {
                        source: node.id,
                        target: target,
                        view: self.filter_parameters.link.view[0],
                        group: [node.info.group[0]],
                    };

                    self.parent.addLink.call(self, link);

                    $('#modal_create_link_chooser').modal('hide');
                });
            });
        }
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
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var vnf_vdu_cp_id = source_type == 'vnf_vdu_cp' ? source_id : target_id;
        var vdu_links = $.grep(self.d3_graph.links, function(e) {
            return (e.source.id == vnf_vdu_cp_id || e.target.id == vnf_vdu_cp_id) && (e.source.info.type == 'vnf_vdu' || e.target.info.type == 'vnf_vdu'
            || e.source.info.type == 'vnf_click_vdu' || e.target.info.type == 'vnf_click_vdu')
        });
        var vdu_id = vdu_links[0].source.info.type == 'vnf_vdu' ? vdu_links[0].source.id : vdu_links[0].target.id;
        if(vdu_links[0].source.info.type == 'vnf_vdu'){
            vdu_id = vdu_links[0].source.id;
        }else if (vdu_links[0].target.info.type == 'vnf_vdu'){
            vdu_id = vdu_links[0].target.id;
        } else if(vdu_links[0].source.info.type == 'vnf_click_vdu'){
          var vnf_vdus = $.grep(self.d3_graph.nodes, function(e) {
            return (e.id == vdu_links[0].source.id) && (e.info.type == 'vnf_click_vdu')
          });
          vdu_id = vnf_vdus[0].vduId;
        }else{
            var vnf_vdus = $.grep(self.d3_graph.nodes, function(e) {
            return (e.id == vdu_links[0].target.id) && (e.info.type == 'vnf_click_vdu')
          });
          vdu_id = vnf_vdus[0].vduId;
        }
        var old_link = $.grep(self.d3_graph.links, function(e) {
            return (e.source.id == vnf_vdu_cp_id || e.target.id == vnf_vdu_cp_id) && (e.source.info.type == 'vnf_vl' || e.target.info.type == 'vnf_vl')
        });
        new dreamer.GraphRequests().addLink(link,  vdu_id, function() {
            self._deselectAllNodes();
            if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                self.parent.removeLink.call(self, old_link[0].index);
            }
            if (success) {
                success();
            }
        });
    }

   SuperfluidityController.prototype.linkVnfVltoExpCp = function(self, link, success, error) {
        SuperfluidityController.etsiController.linkVnfVltoExpCp(self, link, success, error);
   }

   SuperfluidityController.prototype.removeVnfVdu = function(self, node, success, error) {
        SuperfluidityController.etsiController.removeVnfVdu(self, node, success, error);
   }

    SuperfluidityController.prototype.removeVnfVduCp = function(self, node, success, error) {
        var vdu_links = $.grep(self.d3_graph.links, function(e) {
            return (e.source.id == node.id || e.target.id == node.id) && (e.source.info.type == 'vnf_vdu' || e.target.info.type == 'vnf_vdu'
            || e.source.info.type == 'vnf_click_vdu' || e.target.info.type == 'vnf_click_vdu')
        });
        var vdu_id;
        if(vdu_links[0].source.info.type == 'vnf_vdu'){
            vdu_id = vdu_links[0].source.id;
        }else if(vdu_links[0].target.info.type == 'vnf_vdu' ){
            vdu_id = vdu_links[0].target.id;
        }else if(vdu_links[0].source.info.type == 'vnf_click_vdu' ){
            vdu_id = vdu_links[0].source.vduId;
        }else{
            vdu_id = vdu_links[0].target.vduId;
        }
        console.log(vdu_id)
        new dreamer.GraphRequests().removeNode(node, vdu_id, function() {
            if (success) {
                success();
            }
        });
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