//GraphEditor instance
var graph_editor = new dreamer.ModelGraphEditor();
var selected_vnffgId = null;
var show_all = null;

// Enable Drop Action on the Graph
initDropOnGraph();


$(document).ready(function () {
    var descriptor_type = getUrlParameter('type') === 'ns' || getUrlParameter('type') === 'nsd' ? 'ns' : 'vnf';
    descriptor_type = getUrlParameter('type') === 'click' ? ['click'] : descriptor_type;
    var params = {}
    if (descriptor_type === 'click') {
        allowed_types = ['element', 'compound_element', 'class_element'];
        params = {
            node: {
                type: allowed_types,
                group: [getUrlParameter('id')]
            },
            link: {
                group: [getUrlParameter('id')],
                view: ['compact']
            }
        };
    } else {
        var allowed_types = descriptor_type === 'ns' ? ['vnf', 'ns_cp', 'ns_vl'] : ['vnf_vl', 'vnf_ext_cp', 'vnf_vdu_cp', 'vnf_vdu', 'vnf_click_vdu', 'vnf_k8s_vdu', 'vnf_docker_vdu', 'vnf_ansibledocker_vdu', 'k8s_service_cp'];
        params = {
            node: {
                type: allowed_types,
                group: [getUrlParameter('id')]
            },
            link: {
                group: [getUrlParameter('id')],
                view: [descriptor_type]
            }
        };

    }

    graph_editor.addListener("refresh_graph_parameters", refreshGraphParameters);


    // graph_editor initialization
    graph_editor.init({
        width: $('#graph_ed_container').width(),
        height: $('#graph_ed_container').height(),
        gui_properties: example_gui_properties,
        filter_base: params,
        behaviorsOnEvents: {
            viewBased: false,
            behaviors: buildBehaviorsOnEvents()
        }
    });

    // this will filter in the different views, excluding the node types that are not listed in params
    graph_editor.handleFiltersParams(params);
    graph_editor.addListener("filters_changed", changeFilter);
    graph_editor.addListener("edit_descriptor", openEditorEvent);

});


function initDropOnGraph() {

    var dropZone = document.getElementById('graph_ed_container');
    dropZone.ondrop = function (e) {
        e.preventDefault();
        var group = graph_editor.getCurrentGroup();
        var nodetype = e.dataTransfer.getData("text/plain");
        var onLoadModal, retriveDataToSend;
        if (nodetype) {
            var node_information = {
                'id': '',
                'info': {
                    'type': nodetype,
                    'group': [group],
                    'desc_id': graph_editor.getCurrentView(),
                },
                'x': e.layerX,
                'y': e.layerY
            };
            var vdu_opt_params = {
                'nested_desc': {
                    'id': '',
                    'vduNestedDescriptorType': '',
                    'vduNestedDescriptor': ''
                },
                "vdu_param": {
                    'vduParent': null,
                    'vduParentBareMetal': null,
                    'vduParentMandatory': null,
                    'envVars': ''
                }
            };

            if (nodetype == 'vnf') {
                onLoadModal = new dreamer.GraphRequests().getUnusedVnf(group, function (vnfs) {

                    $('#selection_chooser_vnf').empty();
                    $('#selection_chooser_vnf').append('<option >None</option>');
                    for (var i in vnfs) {
                        $('#selection_chooser_vnf').append('<option id="' + vnfs[i] + '">' + vnfs[i] + '</option>');
                    }

                });

                retriveDataToSend = function () {
                    var choice = $("#selection_chooser_vnf option:selected").text();
                    var vdu_id = $('#input_choose_node_id').val();
                    if (choice == 'None')
                        node_information['id'] = vdu_id;
                    else {
                        node_information['existing_element'] = true;
                        node_information['id'] = choice;
                    }
                    return node_information;
                }

            }
            else if (graph_editor.getCurrentView() == 'compact' || graph_editor.getCurrentView() == 'expandable') {
                onLoadModal = null;
                retriveDataToSend = function () {
                    var vdu_id = $('#input_choose_node_id').val();

                    node_information['id'] = vdu_id;
                    node_information['desc_id'] = group;
                    return node_information;
                };

            }
            else if (nodetype == 'vnf_docker_vdu') {
                onLoadModal = null;
                retriveDataToSend = function () {
                    var vdu_id = $('#input_choose_node_id').val();
                    var docker_image = $('#input_choose_vnf_docker_vdu_image').val();
                    var envVars = $('#input_choose_vnf_vdu_envVars').val();
                    //var choice = $("#selection_chooser_vnf_vduNestedDesc option:selected").text();
                    node_information['id'] = vdu_id;
                    node_information['opt_params'] = {};
                    node_information['opt_params']['docker_image_name'] = docker_image;
                    node_information['opt_params']['envVars'] = envVars;

                    node_information['opt_params'] = JSON.stringify(node_information['opt_params']);
                    return node_information;
                };
            }
            else if(nodetype == 'vnf_ansibledocker_vdu'){
                onLoadModal = null;
                retriveDataToSend = function () {
                    var vdu_id = $('#input_choose_node_id').val();
                    var vduNestedDesc_id = $('#input_choose_vnf_ansibledocker_vdu_role').val();
                    var envVars = $('#input_choose_vnf_ansibledocker_vdu_envVars').val();
                    node_information['id'] = vdu_id;
                    node_information['opt_params'] = vdu_opt_params;
                    node_information['opt_params']['nested_desc']['vduNestedDescriptorType'] = 'ansibledocker'
                    node_information['opt_params']['nested_desc']['id'] = vduNestedDesc_id;
                    node_information['opt_params']['nested_desc']['vduNestedDescriptor'] = vduNestedDesc_id;
                    node_information['opt_params']['vdu_param']['envVars'] = envVars;
                    node_information['opt_params'] = JSON.stringify(node_information['opt_params']);
                    return node_information;
                };
            }
            else if (nodetype == 'vnf_k8s_vdu') {
                onLoadModal = null;
                retriveDataToSend = function () {
                    var vdu_id = $('#input_choose_node_id').val();
                    var vduNestedDesc_id = $('#input_choose_vnf_vduK8sDesc_id').val();
                    var choice = $("#selection_chooser_vnf_vduNestedDesc option:selected").text();
                    node_information['id'] = vdu_id;
                    node_information['opt_params'] = vdu_opt_params;
                    node_information['opt_params']['nested_desc']['vduNestedDescriptorType'] = 'kubernetes'
                    /*
                    if (choice == 'None'){*/
                        node_information['opt_params']['nested_desc']['id'] = vduNestedDesc_id;
                        node_information['opt_params']['nested_desc']['vduNestedDescriptor'] = vduNestedDesc_id;
                    /*
                    }
                    else {

                    }*/
                    node_information['opt_params'] = JSON.stringify(node_information['opt_params']);
                    return node_information;
                };
            }
            else if (nodetype == 'vnf_click_vdu') {
                onLoadModal = null;/* new dreamer.GraphRequests().getUnusedVnf(group, function (vduNestedDescs) {

                    $('#selection_chooser_vnf_vduNestedDesc').empty();
                    $('#selection_chooser_vnf_vduNestedDesc').append('<option >None</option>');
                    for (var i in vduNestedDescs) {
                        $('#selection_chooser_vnf_vduNestedDesc').append('<option id="' + vduNestedDescs[i] + '">' + vduNestedDescs[i] + '</option>');
                    }

                });*/
                retriveDataToSend = function () {
                    var vdu_id = $('#input_choose_node_id').val();
                    var vduNestedDesc_id = $('#input_choose_vnf_vduClickDesc_id').val();
                    var choice = $("#selection_chooser_vnf_vduNestedDesc option:selected").text();
                    node_information['id'] = vdu_id;
                    node_information['opt_params'] = vdu_opt_params;
                    node_information['opt_params']['nested_desc']['vduNestedDescriptorType'] = 'click'
                    /*
                    if (choice == 'None'){*/
                        node_information['opt_params']['nested_desc']['id'] = vduNestedDesc_id;
                        node_information['opt_params']['nested_desc']['vduNestedDescriptor'] = vduNestedDesc_id;
                    /*
                    }
                    else {

                    }*/
                    node_information['opt_params'] = JSON.stringify(node_information['opt_params']);
                    return node_information;
                };
            }
            else if (nodetype == 'k8s_service_cp') {
                onLoadModal = null;
                retriveDataToSend = function () {
                    var node_id = $('#input_choose_node_id').val();
                    var k8ss = $('#input_choose_k8s_service_cpd_id').val();
                    node_information['id'] = node_id;
                    node_information['opt_params'] = {
                        'k8s_service_cpd': {
                            'cpdId': node_id,
                            'serviceDescriptor': k8ss
                        }

                    };
                    node_information['opt_params'] = JSON.stringify(node_information['opt_params']);
                    return node_information;
                };
            }
            else if (nodetype == 'vnf_vdu_cp'){
                onLoadModal = null;
                    var vnf_vdus = $.grep(graph_editor.d3_graph.nodes, function (e) {

                        return (e.info.group.indexOf(group) >= 0 && ['vnf_vdu', 'vnf_click_vdu', 'vnf_k8s_vdu', 'vnf_docker_vdu', 'vnf_ansibledocker_vdu'].indexOf( e.info.type) >= 0);
                    });
                    $('#selection_chooser_vdu').empty();
                    for (var i in vnf_vdus) {
                        $('#selection_chooser_vdu').append('<option id="' + vnf_vdus[i].id + '">' + vnf_vdus[i].id + '</option>');
                    }

                retriveDataToSend = function () {
                    var name = $('#input_choose_node_id').val();
                    var vdu = $("#selection_chooser_vdu option:selected").text();
                    node_information['id'] = name;
                    node_information['opt_params'] = {
                        'vdu': vdu
                    };
                    return node_information;
                };
            }
            else {
                onLoadModal = null;
                retriveDataToSend = function () {
                    var name = $('#input_choose_node_id').val();
                    node_information['id'] = name;
                    return node_information;
                };

            }
            newNodeModalFromType(e, onLoadModal, retriveDataToSend);
        }

    };

    dropZone.ondragover = function (ev) {
        console.log("ondragover");
        return false;
    };

    dropZone.ondragleave = function () {
        console.log("ondragleave");
        return false;
    }
}

function newNodeModalFromType(event, onLoadModal, retriveDataToSend) {
    //event.preventDefault();
    var group = graph_editor.getCurrentGroup();
    var nodetype = event.dataTransfer.getData("text/plain");
    $('.new-node-section').hide();
    $('#new_node_section_' + nodetype).show();
    // fill with random nodeId
    $('#input_choose_node_id').val(nodetype + "_" + generateUID());
    // set title based on node type
    $('#modal_chooser_title_add_node').text('Add ' + nodetype);

    // set action on click save button
    $('#save_choose_node_id').off('click').on('click', function () {
        var node_data = retriveDataToSend();
        graph_editor.addNode(node_data, function () {
            $('#modal_choose_node_id').modal('hide');
        }, function (error) {
            showAlert(error)
        });
    });
    $('#modal_choose_node_id').modal('show');
}

function handleForce(el) {
    if (el.id == "topology_play") {
        $("#topology_pause").removeClass('active');
        $("#topology_play").addClass('active');
    } else {
        $("#topology_pause").addClass('active');
        $("#topology_play").removeClass('active');
    }

    graph_editor.handleForce((el.id == "topology_play") ? true : false);

}

function changeFilter(e, c) {
    var type_property = graph_editor.getTypeProperty();
    if (c.link.view == 'ns') {
        $("#title_header").text("NS Graph Editor")
        $("#vnffg_options").prop("disabled", false);
        graph_editor.refreshGraphParameters();
    } else {
        $("#title_header").text("VNF Graph Editor");
        $("#vnffg_box").hide();
        $("#vnffg_options").prop("disabled", true);
    }

    new dreamer.GraphRequests().getAvailableNodes({layer: c.link.view[0]}, buildPalette, showAlert);
    //updateNodeDraggable({type_property: type_property, nodes_layer: graph_editor.getAvailableNodes()})
    updateBredCrumb(c);
}

var filters = function (e, params) {
    graph_editor.handleFiltersParams(params);
    $('#' + e).nextAll('li').remove();
}

function updateBredCrumb(filter_parameters) {
    var newLi = $("<li id=" + JSON.stringify(graph_editor.getCurrentGroup()) + "><a href='javascript:filters(" + JSON.stringify(graph_editor.getCurrentGroup()) + "," + JSON.stringify(filter_parameters) + ")'>" + graph_editor.getCurrentGroup() + "</a></li>");
    $('#breadcrumb').append(newLi);
}


function openEditor(project_id) {
    //FIXME is not a good solution
    var current_view = graph_editor.getCurrentView();
    if (['expandable', 'compact'].indexOf(current_view) > -1)
        current_view = 'click'
    else
        current_view += 'd'
    window.location.href = '/projects/' + project_id + '/descriptors/' + current_view + '/' + graph_editor.getCurrentGroup();

}


function showChooserModal(title, chooses, callback) {
    console.log('showchooser')
    $('#selection_chooser').empty();
    for (var i in chooses) {
        $('#selection_chooser').append('<option id="' + chooses[i].id + '">' + chooses[i].id + '</option>');
    }
    $('#modal_chooser_title').text(title)
    var self = this;
    $('#save_chooser').off('click').on('click', function () {
        var choice = $("#selection_chooser option:selected").text();
        callback(choice);

    });
    $('#modal_create_link_chooser').modal('show');

}

function refreshGraphParameters(e, graphParameters) {

    var self = $(this);
    if (graphParameters == null) return;
    var vnffgIds = graphParameters.vnffgIds;
    if (vnffgIds == null) return;

    $("#selection_vnffg").empty();
    $("#selection_vnffg").append('<option value="Global">Global</option>')
    for (var i in vnffgIds) {
        var vnffgId = vnffgIds[i]
        var child = $('<option value="' + vnffgId + '">' + vnffgId + '</option>');
        $("#selection_vnffg").append(child)
    }
}

function changeVnffg(e) {
    var vnffgId = e.value;
    selected_vnffgId = vnffgId;
    show_all_change();
}

function newVnffg() {
    var group = graph_editor.getCurrentGroup()
    $('#div_chose_id').show();
    //$('#div_chose_vnf').hide();
    $('#input_choose_node_id').val("vnffg_" + generateUID());
    $('#modal_chooser_title_add_node').text('Add VNFFG');
    $('#save_choose_node_id').off('click').on('click', function () {
        var name = $('#input_choose_node_id').val();

        var node_information = {
            'element_id': name,
            'element_type': "vnffg",
            'group_id': group,
        };
        new dreamer.GraphRequests().addVnffg(node_information, function (result) {

            $('#modal_choose_node_id').modal('hide');
            graph_editor.d3_graph.graph_parameters.vnffgIds.push(node_information.id)
            refreshGraphParameters(null, graph_editor.d3_graph.graph_parameters)
        });


    });
    $('#modal_choose_node_id').modal('show');
}

function show_all_change(e) {
    if (!selected_vnffgId) return;
    var vnffgId = selected_vnffgId;
    if (e) show_all = e.checked;
    if (show_all) {
        handleVnffgParameter("Global", "invisible");
        handleVnffgParameter(vnffgId, "matted");
    } else {
        handleVnffgParameter("Global", "matted");
        handleVnffgParameter(vnffgId, "invisible");
    }
}

function clickVnffg() {
    if ($("#vnffg_box").is(':visible'))
        $("#vnffg_box").hide();
    else
        $("#vnffg_box").show();

}

function handleVnffgParameter(vnffgId, class_name) {

    if (vnffgId != "Global") {
        selected_vnffgId = vnffgId;
        graph_editor.setNodeClass(class_name, function (d) {
            var result = false;
            if (d.info.group.indexOf(vnffgId) < 0) {
                result = true;
            }
            //console.log(result);
            return result;
        });

        graph_editor.setLinkClass(class_name, function (d) {
            var result = false;
            if (d.group.indexOf(vnffgId) < 0) {
                result = true;
            }
            //console.log(result);
            return result;
        });

    } else {
        selected_vnffgId = null;
        graph_editor.setNodeClass(class_name, function (d) {
            var result = false;
            return result;
        });

        graph_editor.setLinkClass(class_name, function (d) {
            var result = false;
            return result;
        });
    }


}

function buildBehaviorsOnEvents() {
    var contextmenuNodesAction = [{
        title: 'Show info',
        action: function (elm, d, i) {
           // console.log('Show NodeInfo', elm, d, i);
            var nodeData = {
                "node": {
                    "id": d.id
                }
            };
            new dreamer.SuperfluidityController().getNodeOverview(graph_editor, d, function (result) {
               // console.log(JSON.stringify(result))
                graph_editor.showNodeInfo({'node_info': result['node_overview']})
            }, function (error) {
                showAlert("Error opening info node.")
            });
        },
        edit_mode: false

    },
        {
            title: 'Show graph',
            action: function (elm, c_node, i) {
                if (c_node.info.type != undefined) {
                    var current_layer_nodes = Object.keys(graph_editor.model.layer[graph_editor.getCurrentView()].nodes);
                    if (current_layer_nodes.indexOf(c_node.info.type) >= 0) {
                        if (graph_editor.model.layer[graph_editor.getCurrentView()].nodes[c_node.info.type].expands) {
                            var new_layer = graph_editor.model.layer[graph_editor.getCurrentView()].nodes[c_node.info.type].expands;
                            graph_editor.handleFiltersParams({
                                node: {
                                    type: Object.keys(graph_editor.model.layer[new_layer].nodes),
                                    group: [c_node.id]
                                },
                                link: {
                                    group: [c_node.id],
                                    view: [new_layer]
                                }
                            });

                        }
                        else {
                            showAlert('This is not an explorable node.')
                        }
                    }
                }
            },
            edit_mode: false
        }];
    var behavioursOnEvents = {
        'nodes': contextmenuNodesAction,

    };

    return behavioursOnEvents;
}