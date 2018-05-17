if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.EtsiController = (function (global) {
    'use strict';

    var DEBUG = true;

    EtsiController.prototype.constructor = EtsiController;

    /**
     * Constructor
     */
    function EtsiController() {


    }

    EtsiController.prototype.addVnf = function (graph_editor, node, success, error) {
        var data_to_send = {
            'group_id': node.info.group[0],
            'element_id': node.id,
            'element_type': node.info.type,
            'element_desc_id': node.info.desc_id,
            'x': node.x,
            'y': node.y
        };
        if (node.existing_element) {
            data_to_send['existing_element'] = true;
            new dreamer.GraphRequests().addNode(data_to_send, null, function () {
                if (success)
                    success();
            });

        } else {
            new dreamer.GraphRequests().addNode(data_to_send, null, function () {
                var vnf_ext_cp = {
                    'group_id': node.id,
                    'element_id': 'vnf_ext_cp' + "_" + node.id,
                    'element_type': 'vnf_ext_cp',
                    'element_desc_id': node.info.desc_id,
                    'x': node.x,
                    'y': node.y
                };

                new dreamer.GraphRequests().addNode(vnf_ext_cp, null, function () {
                    graph_editor.parent.addNode.call(graph_editor, vnf_ext_cp);
                    if (success)
                        success();
                });
            });
        }

    };

    EtsiController.prototype.addNode = function (graph_editor, node, success, error) {
        console.log("addNode");

        var data_to_send = {
            'group_id': node.info.group[0],
            'element_id': node.id,
            'element_type': node.info.type,
            'element_desc_id': node.info.desc_id,
            'opt_params': node.opt_params,
            'x': node.x,
            'y': node.y
        };
        new dreamer.GraphRequests().addNode(data_to_send, null, function () {
            if (success)
                success();
        });
    };


    EtsiController.prototype.addVnfVdu = function (graph_editor, node, success, error) {
        console.log('addVnfVdu', JSON.stringify(node))
        var data_to_send = {
            'group_id': node.info.group[0],
            'element_id': node.id,
            'element_type': node.info.type,
            'element_desc_id': node.info.desc_id,
            'opt_params': node['opt_params'],
            'x': node.x,
            'y': node.y
        };
        console.log("data_to_send", JSON.stringify(data_to_send));
        new dreamer.GraphRequests().addNode(data_to_send, null, function () {
            var vdu_id = node.id;
            var vnf_vdu_cp = {
                'group_id': node.info.group[0],
                'element_id': 'vnf_vdu_cp' + "_" + generateUID(),
                'element_type': 'vnf_vdu_cp',
                'element_desc_id': node.info.desc_id,
                'x': parseFloat(node.x) - (parseFloat(node.x) * 0.1),
                'y': parseFloat(node.y) - (parseFloat(node.y) * 0.1),
                'choice': vdu_id
            };
            console.log("vnf_vdu_cp", JSON.stringify(vnf_vdu_cp));
            if (success)
                success();
            new dreamer.GraphRequests().addNode(vnf_vdu_cp, vdu_id, function () {
                var node_vdu_cp = {
                    'id': vnf_vdu_cp['element_id'],
                    'info': {
                        'type': 'vnf_vdu_cp',
                        'group': [vnf_vdu_cp['group_id']]
                    },

                    'x': vnf_vdu_cp['x'],
                    'y': vnf_vdu_cp['y']
                };

                graph_editor.parent.addNode.call(graph_editor, node_vdu_cp);
                var link = {
                    source: node.id,
                    target: node_vdu_cp.id,
                    view: graph_editor.filter_parameters.link.view[0],
                    group: [node.info.group[0]]
                };
                graph_editor.parent.addLink.call(graph_editor, link);

            });

        });
    };

    EtsiController.prototype.addVnfVduCp = function (graph_editor, node, success, error) {
        var vnf_id = node.info.group[0];
        var vnf_vdus = $.grep(graph_editor.d3_graph.nodes, function (e) {
            return (e.info.group.indexOf(vnf_id) >= 0 && e.info.type == 'vnf_vdu');
        });
        $('#modal_choose_node_id').modal('hide');
        if (typeof vnf_vdus == 'undefined' || vnf_vdus.length <= 0) {
            alert('You should add a VDU')
        } else {
            showChooserModal('Select the VDU to link', vnf_vdus, function (choice) {
                var data_to_send = {
                    'group_id': node.info.group[0],
                    'element_id': node.id,
                    'element_type': node.info.type,
                    'element_desc_id': node.info.desc_id,
                    'x': node.x,
                    'y': node.y,
                    'choice': choice
                };
                new dreamer.GraphRequests().addNode(data_to_send, choice, function () {
                    if (success)
                        success();
                    var link = {
                        source: node.id,
                        target: choice,
                        view: graph_editor.filter_parameters.link.view[0],
                        group: [node.info.group[0]]
                    };

                    graph_editor.parent.addLink.call(graph_editor, link);

                    $('#modal_create_link_chooser').modal('hide');
                });
            });
        }
    };

    EtsiController.prototype.nsCpExclusiveConnection = function (graph_editor, link, success, error) {
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var cp_id = source_type == 'ns_cp' ? source_id : target_id;
        var old_link = $.grep(graph_editor.d3_graph.links, function (e) {
            return (e.source.id == cp_id || e.target.id == cp_id);
        });
        var data_to_send = {
            'group_id': link.source.info.group[0],
            'element_desc_id': getUrlParameter('id'),
            'source': link.source.id,
            'source_type': link.source.info.type,
            'target': link.target.id,
            'target_type': link.target.info.type
        };

        new dreamer.GraphRequests().addLink(data_to_send, null, function () {
            graph_editor._deselectAllNodes();
            if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                graph_editor.parent.removeLink.call(graph_editor, old_link[0].index);
            }
            if (success) {
                success();
            }
        });

    };


    EtsiController.prototype.linkVnftoNsVl = function (graph_editor, link, success, error) {
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var vnf_id = source_type == 'vnf' ? source_id : target_id;
        var vnf_ext_cps = $.grep(graph_editor.d3_graph.nodes, function (e) {
            return (e.info.group == vnf_id && e.info.type == 'vnf_ext_cp');
        });
        showChooserModal('Select the VNF EXT CP of the VNF', vnf_ext_cps, function (choice) {
            var data_to_send = {
                'group_id': link.source.info.group[0],
                'element_desc_id': getUrlParameter('id'),
                'source': link.source.id,
                'source_type': link.source.info.type,
                'target': link.target.id,
                'target_type': link.target.info.type,
                'choice': choice
            };
            new dreamer.GraphRequests().addLink(data_to_send, choice, function () {
                if (success) {
                    success()
                }
                $('#modal_create_link_chooser').modal('hide');
            });
        });
    };

    EtsiController.prototype.linkVnftoNsCp = function (graph_editor, link, success, error) {
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var vnf_id = source_type == 'vnf' ? source_id : target_id;
        var ns_cp_id = source_type == 'ns_cp' ? source_id : target_id;
        var vnf_ext_cps = $.grep(graph_editor.d3_graph.nodes, function (e) {
            return (e.info.group == vnf_id && e.info.type == 'vnf_ext_cp');
        });
        var old_link = $.grep(graph_editor.d3_graph.links, function (e) {
            return (e.source.id == ns_cp_id || e.target.id == ns_cp_id);
        });
        showChooserModal('Select the VNF EXT CP of the VNF', vnf_ext_cps, function (choice) {
            var data_to_send = {
                'group_id': link.source.info.group[0],
                'element_desc_id': getUrlParameter('id'),
                'source': link.source.id,
                'source_type': link.source.info.type,
                'target': link.target.id,
                'target_type': link.target.info.type,
                'choice': choice
            };
            new dreamer.GraphRequests().addLink(data_to_send, choice, function () {
                if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                    graph_editor.parent.removeLink.call(graph_editor, old_link[0].index);
                }
                if (success) {
                    success()
                }
                $('#modal_create_link_chooser').modal('hide');
            });
        });
    };


    EtsiController.prototype.linkVltoVduCp = function (graph_editor, link, success, error) {
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var vnf_vdu_cp_id = source_type == 'vnf_vdu_cp' ? source_id : target_id;
        var vdu_links = $.grep(graph_editor.d3_graph.links, function (e) {
            return (e.source.id == vnf_vdu_cp_id || e.target.id == vnf_vdu_cp_id) && (e.source.info.type == 'vnf_vdu' || e.target.info.type == 'vnf_vdu')
        });
        var vdu_id = vdu_links[0].source.info.type == 'vnf_vdu' ? vdu_links[0].source.id : vdu_links[0].target.id;
        var old_link = $.grep(graph_editor.d3_graph.links, function (e) {
            return (e.source.id == vnf_vdu_cp_id || e.target.id == vnf_vdu_cp_id) && (e.source.info.type == 'vnf_vl' || e.target.info.type == 'vnf_vl')
        });
        var data_to_send = {
            'group_id': link.source.info.group[0],
            'element_desc_id': getUrlParameter('id'),
            'source': link.source.id,
            'source_type': link.source.info.type,
            'target': link.target.id,
            'target_type': link.target.info.type,
            'choice': vdu_id
        };
        new dreamer.GraphRequests().addLink(data_to_send, vdu_id, function () {
            graph_editor._deselectAllNodes();
            if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                graph_editor.parent.removeLink.call(graph_editor, old_link[0].index);
            }
            if (success) {
                success();
            }
        });
    };


    EtsiController.prototype.linkVnfVltoExpCp = function (graph_editor, link, success, error) {
        var s = link.source;
        var d = link.target;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var vnf_ext_cp_id = source_type == 'vnf_ext_cp' ? source_id : target_id;
        var old_link = $.grep(graph_editor.d3_graph.links, function (e) {
            return (e.source.id == vnf_ext_cp_id || e.target.id == vnf_ext_cp_id);
        });
        var data_to_send = {
            'group_id': link.source.info.group[0],
            'element_desc_id': getUrlParameter('id'),
            'source': link.source.id,
            'source_type': link.source.info.type,
            'target': link.target.id,
            'target_type': link.target.info.type
        };
        new dreamer.GraphRequests().addLink(data_to_send, null, function () {
            graph_editor._deselectAllNodes();
            if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                graph_editor.parent.removeLink.call(graph_editor, old_link[0].index);
            }
            if (success) {
                success();
            }
        });
    };

    EtsiController.prototype.removeVnfVdu = function (graph_editor, node, success, error) {
        var vdu_links = $.grep(graph_editor.d3_graph.links, function (e) {
            return (e.source.id == node.id || e.target.id == node.id) && (e.source.info.type == 'vnf_vdu_cp' || e.target.info.type == 'vnf_vdu_cp')
        });
        for (var i in vdu_links) {
            var cp_node = vdu_links[i].source.info.type == 'vnf_vdu_cp' ? vdu_links[i].source : vdu_links[i].target;
            graph_editor.parent.removeNode.call(graph_editor, cp_node);
        }
        console.log("removeVnfVdu", node.vduId)
        var data_to_send = {
            'group_id': node.info.group && node.info.group.length > 0 ? node.info.group[0] : undefined,
            'element_id': (node.vduId != undefined) ? node.vduId : node.id,
            'element_type': node.info.type,
            'element_desc_id': node.info.desc_id
        };
        new dreamer.GraphRequests().removeNode(data_to_send, null, function () {
            if (success) {
                success();
            }
        });
    };


    EtsiController.prototype.removeVnfVduCp = function (graph_editor, node, success, error) {
        var vdu_links = $.grep(graph_editor.d3_graph.links, function (e) {
            return (e.source.id == node.id || e.target.id == node.id) && (e.source.info.type == 'vnf_vdu' || e.target.info.type == 'vnf_vdu')
        });
        var vdu_id = vdu_links[0].source.info.type == 'vnf_vdu' ? vdu_links[0].source.id : vdu_links[0].target.id;
        console.log(vdu_id)
        var data_to_send = {
            'group_id': node.info.group && node.info.group.length > 0 ? node.info.group[0] : undefined,
            'element_id': node.id,
            'element_type': node.info.type,
            'element_desc_id': node.info.desc_id,
            'choice': vdu_id
        };
        console.log(JSON.stringify(data_to_send));
        new dreamer.GraphRequests().removeNode(data_to_send, vdu_id, function () {
            if (success) {
                success();
            }
        });
    };

    EtsiController.prototype.removeNode = function (graph_editor, node, success, error) {
        var data_to_send = {
            'group_id': node.info.group && node.info.group.length > 0 ? node.info.group[0] : undefined,
            'element_id': node.id,
            'element_type': node.info.type,
            'element_desc_id': node.info.desc_id
        };
        new dreamer.GraphRequests().removeNode(data_to_send, null, function () {
            if (success) {
                success();
            }
        });
    };

    EtsiController.prototype.removeLink = function (graph_editor, link, success, error) {
        log("removeLink " + JSON.stringify(link));
        var data_to_send = {
            'group_id': link.source.info.group[0],
            'element_desc_id': getUrlParameter('id'),
            'source': link.source.id,
            'source_type': link.source.info.type,
            'target': link.target.id,
            'target_type': link.target.info.type
        };
        new dreamer.GraphRequests().removeLink(data_to_send, success, error);
    };

    EtsiController.prototype.addToCurrentVNFFG = function (graph_editor, args, error) {
        var d = args.d;
        if (selected_vnffgId && graph_editor.getCurrentView() == 'ns' && d.info.group.indexOf(selected_vnffgId) < 0) {
            d.vnffgId = selected_vnffgId;

            var data_to_send = {
                'group_id': d.info.group[0],
                'element_id': d.id,
                'element_type': d.info.type,
                'vnffg_id': d.vnffgId
            };
            new dreamer.GraphRequests().addNodeToVnffg(data_to_send, function (result) {
                d.info.group.push(selected_vnffgId);
                var links = $.grep(graph_editor.d3_graph.links, function (e) {
                    return (e.source.id == d.id || e.target.id == d.id);
                });
                for (var i in links) {
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