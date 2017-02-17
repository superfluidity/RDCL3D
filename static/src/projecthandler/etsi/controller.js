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
    function EtsiController() {


    }

    EtsiController.prototype.addVnf = function(self, node, success, error) {
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

    EtsiController.prototype.addNode = function(self, node, success, error) {
        console.log("addNode")
        console.log(node, success, error)
        new dreamer.GraphRequests().addNode(node, null, function() {
            if (success)
                success();
        });
    };


    EtsiController.prototype.addVnfVdu = function(self, node, success, error) {
        new dreamer.GraphRequests().addNode(node, null, function() {
            var vdu_id = node.id;
            var vnf_vdu_cp = {
                'id': 'vnf_vdu_cp' + "_" + generateUID(),
                'info': {
                    'type': 'vnf_vdu_cp',
                    'group': [node.info.group[0]]
                },
                'x': node.x - (node.x * 0.1),
                'y': node.y - (node.y * 0.1)
            }
            if (success)
                success();
            new dreamer.GraphRequests().addNode(vnf_vdu_cp, vdu_id, function() {
                self.parent.addNode.call(self, vnf_vdu_cp);
                var link = {
                    source: node.id,
                    target: vnf_vdu_cp.id,
                    view: self.filter_parameters.link.view[0],
                    group: [node.info.group[0]],
                };
                self.parent.addLink.call(self, link);

            });

        });
    };

    EtsiController.prototype.addVnfVduCp = function(self, node, success, error) {
        var vnf_id = node.info.group[0];
        var vnf_vdus = $.grep(self.d3_graph.nodes, function(e) {
            return (e.info.group.indexOf(vnf_id) >= 0 && e.info.type == 'vnf_vdu');
        });
        if (success)
            success();
        if (typeof vnf_vdus == 'undefined' || vnf_vdus.length <= 0) {
            alert('You should add a VDU')
        } else {
            showChooserModal('Select the VDU to link', vnf_vdus, function(choice) {
                new dreamer.GraphRequests().addNode(node, choice, function() {
                    var link = {
                        source: node.id,
                        target: choice,
                        view: self.filter_parameters.link.view[0],
                        group: [node.info.group[0]],
                    };

                    self.parent.addLink.call(self, link);

                    $('#modal_create_link_chooser').modal('hide');
                });
            });
        }
    };

    EtsiController.prototype.nsCpExclusiveConnection = function(self, link, success, error) {
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var cp_id = source_type == 'ns_cp' ? source_id : target_id;
        var old_link = $.grep(self.d3_graph.links, function(e) {
            return (e.source.id == cp_id || e.target.id == cp_id);
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


    EtsiController.prototype.linkVnftoNsVl = function(self, link, success, error) {
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var vnf_id = source_type == 'vnf' ? source_id : target_id;
        var vnf_ext_cps = $.grep(self.d3_graph.nodes, function(e) {
            return (e.info.group == vnf_id && e.info.type == 'vnf_ext_cp');
        });
        showChooserModal('Select the VNF EXT CP of the VNF', vnf_ext_cps, function(choice) {
            new dreamer.GraphRequests().addLink(link,  choice, function() {
                if (success) {
                    success()
                }
                $('#modal_create_link_chooser').modal('hide');
            });
        });
    };

    EtsiController.prototype.linkVnftoNsCp = function(self, link, success, error) {
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var vnf_id = source_type == 'vnf' ? source_id : target_id;
        var ns_cp_id = source_type == 'ns_cp' ? source_id : target_id;
        var vnf_ext_cps = $.grep(self.d3_graph.nodes, function(e) {
            return (e.info.group == vnf_id && e.info.type == 'vnf_ext_cp');
        });
        var old_link = $.grep(self.d3_graph.links, function(e) {
            return (e.source.id == ns_cp_id || e.target.id == ns_cp_id);
        });
        showChooserModal('Select the VNF EXT CP of the VNF', vnf_ext_cps, function(choice) {
            new dreamer.GraphRequests().addLink(link,  choice, function() {
                if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                    self.parent.removeLink.call(self, old_link[0].index);
                }
                if (success) {
                    success()
                }
                $('#modal_create_link_chooser').modal('hide');
            });
        });
    };



    EtsiController.prototype.linkVltoVduCp = function(self, link, success, error) {
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var vnf_vdu_cp_id = source_type == 'vnf_vdu_cp' ? source_id : target_id;
        var vdu_links = $.grep(self.d3_graph.links, function(e) {
            return (e.source.id == vnf_vdu_cp_id || e.target.id == vnf_vdu_cp_id) && (e.source.info.type == 'vnf_vdu' || e.target.info.type == 'vnf_vdu')
        });
        var vdu_id = vdu_links[0].source.info.type == 'vnf_vdu' ? vdu_links[0].source.id : vdu_links[0].target.id;
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
    };


    EtsiController.prototype.linkVnfVltoExpCp = function(self, link, success, error) {
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

    EtsiController.prototype.removeVnfVdu = function(self, node, success, error) {
        var vdu_links = $.grep(self.d3_graph.links, function(e) {
            return (e.source.id == node.id || e.target.id == node.id) && (e.source.info.type == 'vnf_vdu_cp' || e.target.info.type == 'vnf_vdu_cp')
        });
        for (var i in vdu_links) {
            var cp_node = vdu_links[i].source.info.type == 'vnf_vdu_cp' ? vdu_links[i].source : vdu_links[i].target;
            self.parent.removeNode.call(self, cp_node);
        }
        new dreamer.GraphRequests().removeNode(node, null, function() {
            if (success) {
                success();
            }
        });
    };


    EtsiController.prototype.removeVnfVduCp = function(self, node, success, error) {
        var vdu_links = $.grep(self.d3_graph.links, function(e) {
            return (e.source.id == node.id || e.target.id == node.id) && (e.source.info.type == 'vnf_vdu' || e.target.info.type == 'vnf_vdu')
        });
        var vdu_id = vdu_links[0].source.info.type == 'vnf_vdu' ? vdu_links[0].source.id : vdu_links[0].target.id;
        console.log(vdu_id)
        new dreamer.GraphRequests().removeNode(node, vdu_id, function() {
            if (success) {
                success();
            }
        });
    };

    EtsiController.prototype.removeNode = function(self, node, success, error) {
        new dreamer.GraphRequests().removeNode(node, null, function() {
            if (success) {
                success();
            }
        });
    };

    EtsiController.prototype.removeLink = function(self, link, success, error) {
        log("removeLink " + JSON.stringify(link))

        new dreamer.GraphRequests().removeLink(link, success, error);
    };

    EtsiController.prototype.addToCurrentVNFFG = function(self, args, error) {
        var d = args.d;
        if (selected_vnffgId && self.getCurrentView() == 'ns' && d.info.group.indexOf(selected_vnffgId) < 0) {
            d.vnffgId = selected_vnffgId;
            new dreamer.GraphRequests().addNodeToVnffg(d, function(result) {
                d.info.group.push(selected_vnffgId)
                var links = $.grep(self.d3_graph.links, function(e) {
                    return (e.source.id == d.id || e.target.id == d.id);
                });
                for (var i in links) {
                    console.log(links[i])
                    if (links[i].source.info.group.indexOf(selected_vnffgId) >= 0 && links[i].target.info.group.indexOf(selected_vnffgId) >= 0) {
                        links[i].group.push(selected_vnffgId)
                    }
                }
                show_all_change();
            });
        }
    };

    /**
     * Log utility
     */
    function log(text) {
        if (DEBUG)
            console.log("::EtsiController::", text);
    }

    return EtsiController;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.EtsiController;
}