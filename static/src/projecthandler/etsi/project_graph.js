//GraphEditor instance
var graph_editor = new dreamer.ModelGraphEditor();
var selected_vnffgId = null;
var show_all = null;

// Enable Drop Action on the Graph
initDropOnGraph();



$(document).ready(function() {
    var descriptor_type = getUrlParamater('type') == 'ns' || getUrlParamater('type') == 'nsd' ? 'ns' : 'vnf'
    var allowed_types = descriptor_type == 'ns' ? ['vnf', 'ns_cp', 'ns_vl'] : ['vnf_vl', 'vnf_ext_cp', 'vnf_vdu_cp', 'vnf_vdu'];
    var params = {
        node: {
            type: allowed_types,
            group: [getUrlParamater('id')]
        },
        link: {
            group: [getUrlParamater('id')],
            view: [descriptor_type]
        }
    }

    graph_editor.addListener("refresh_graph_parameters", refreshGraphParameters);


    // graph_editor initialization
    graph_editor.init({
        width: $('#graph_ed_container').width(),
        height: $('#graph_ed_container').height(),
        gui_properties: example_gui_properties,
        filter_base: params
    });

    // this will filter in the different views, excluding the node types that are not listed in params
    graph_editor.handleFiltersParams(params);
    graph_editor.addListener("filters_changed", changeFilter);

});


function initDropOnGraph() {

    var dropZone = document.getElementById('graph_ed_container');
    dropZone.ondrop = function(e) {
        var group = graph_editor.getCurrentGroup()
        e.preventDefault();
        var nodetype = e.dataTransfer.getData("text/plain");
        if (nodetype) {
            var type_name = graph_editor.getTypeProperty()[nodetype].name;
            if (nodetype == 'vnf') {
                new dreamer.GraphRequests().getUnusedVnf(group, function(vnfs) {
                    $('#div_chose_id').hide();
                    $('#div_chose_vnf').show();
                    $('#input_choose_node_vnf').val(nodetype + "_" + generateUID());
                    $('#selection_chooser_vnf').empty();
                    $('#selection_chooser_vnf').append('<option >None</option>');
                    $('#modal_chooser_title_add_node').text('Add ' + type_name);
                    for (var i in vnfs) {
                        $('#selection_chooser_vnf').append('<option id="' + vnfs[i] + '">' + vnfs[i] + '</option>');
                    }
                    $('#save_choose_node_id').off('click').on('click', function() {
                        var choice = $("#selection_chooser_vnf option:selected").text();
                        var name = $('#input_choose_node_vnf').val();
                        if (choice == 'None') {
                            var node_information = {
                                'id': name,
                                'info': {
                                    'type': nodetype,
                                    'group': [group]
                                },
                                'x': e.layerX,
                                'y': e.layerY
                            }
                            graph_editor.addNode(node_information, function() {
                                $('#modal_choose_node_id').modal('hide');
                            });
                        } else {
                            var node_information = {
                                'existing_vnf': true,
                                'id': choice,
                                'info': {
                                    'type': nodetype,
                                    'group': [group]
                                },
                                'x': e.layerX,
                                'y': e.layerY
                            }
                            graph_editor.addNode(node_information, function() {
                                $('#modal_choose_node_id').modal('hide');
                            });
                        }

                    });

                    $('#modal_choose_node_id').modal('show');
                });

            } else {
                $('#div_chose_id').show();
                $('#div_chose_vnf').hide();
                $('#input_choose_node_id').val(nodetype + "_" + generateUID());
                $('#modal_chooser_title_add_node').text('Add ' + type_name);
                $('#save_choose_node_id').off('click').on('click', function() {
                    var name = $('#input_choose_node_id').val();
                    var node_information = {
                        'id': name,
                        'info': {
                            'type': nodetype,
                            'group': [group]
                        },
                        'x': e.layerX,
                        'y': e.layerY
                    }
                    graph_editor.addNode(node_information, function() {
                        $('#modal_choose_node_id').modal('hide');
                    });
                });
                $('#modal_choose_node_id').modal('show');

            }
        }

    }

    dropZone.ondragover = function(ev) {
        console.log("ondragover");
        return false;
    }

    dropZone.ondragleave = function() {
        console.log("ondragleave");
        return false;
    }
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

function savePositions(el) {
    graph_editor.savePositions();
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

    updateNodeDraggable({type_property: type_property, nodes_layer: graph_editor.getAvailableNodes()})
    updateBredCrumb(c);
}

var filters = function(e, params) {
    graph_editor.handleFiltersParams(params);
    $('#' + e).nextAll('li').remove();
}

function updateBredCrumb(filter_parameters){
     var newLi = $("<li id=" + JSON.stringify(graph_editor.getCurrentGroup()) + "><a href='javascript:filters(" + JSON.stringify(graph_editor.getCurrentGroup()) + "," + JSON.stringify(filter_parameters) + ")'>" + graph_editor.getCurrentGroup() + "</a></li>");
     $('#breadcrumb').append(newLi);
}

function updateNodeDraggable(args){

        var type_property = args.type_property;
        $("#draggable-container").empty()
        for (var i in args.nodes_layer) {
            var node = args.nodes_layer[i]
            if (node.addable) {
                var event = 'event.dataTransfer.setData("text/plain","' + i + '")'
                $("#draggable-container").append('<span type="button" class="btn btn-flat btn-default drag_button" draggable="true" id="' + i + '"  ondragstart=' + event + ' style="background-color: ' + type_property[i].color + ' !important;"><p>' + type_property[i].name + '</p></span>');
            }
        }

}

function openEditor(project_id) {
    window.location.href = '/projects/' + project_id + '/descriptors/' + graph_editor.getCurrentView() + 'd/' + graph_editor.getCurrentGroup();
}


function showChooserModal(title, chooses, callback) {
    console.log('showchooser')
    $('#selection_chooser').empty();
    for (var i in chooses) {
        $('#selection_chooser').append('<option id="' + chooses[i].id + '">' + chooses[i].id + '</option>');
    }
    $('#modal_chooser_title').text(title)
    var self = this;
    $('#save_chooser').off('click').on('click', function() {
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
    $('#div_chose_vnf').hide();
    $('#input_choose_node_id').val("vnffg_" + generateUID());
    $('#modal_chooser_title_add_node').text('Add VNFFG');
    $('#save_choose_node_id').off('click').on('click', function() {
        var name = $('#input_choose_node_id').val();
        var node_information = {
            'id': name,
            'info': {
                'type': "vnffg",
                'group': [group]
            }
        }
        new dreamer.GraphRequests().addVnffg(node_information, function(result) {

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
        graph_editor.setNodeClass(class_name, function(d) {
            var result = false;
            if (d.info.group.indexOf(vnffgId) < 0) {
                result = true;
            }
            console.log(result);
            return result;
        });

        graph_editor.setLinkClass(class_name, function(d) {
            var result = false;
            if (d.group.indexOf(vnffgId) < 0) {
                result = true;
            }
            console.log(result);
            return result;
        });

    } else {
        selected_vnffgId = null;
        graph_editor.setNodeClass(class_name, function(d) {
            var result = false;
            return result;
        });

        graph_editor.setLinkClass(class_name, function(d) {
            var result = false;
            return result;
        });
    }
}