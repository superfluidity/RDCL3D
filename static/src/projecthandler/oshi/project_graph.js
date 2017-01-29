//GraphEditor instance
var graph_editor = new dreamer.ModelGraphEditor();
var selected_vnffgId = null;
var show_all = null;

// Enable Drop Action on the Graph
initDropOnGraph();

// get Url parameters
$.urlParam = function(name) {
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results == null) {
        return null;
    } else {
        return results[1] || 0;
    }
}



$(document).ready(function() {
    var params = {
        node: {
            type: [],
            group: []
        },
        link: {
            group: [],
            view: ['Data']
        }
    }
    graph_editor.addListener("filters_changed", changeFilter);
    graph_editor.addListener("refresh_graph_parameters", refreshGraphParameters);

    console.log(example_gui_properties)
    // graph_editor initialization
    graph_editor.init({
        width: $('#graph_ed_container').width(),
        height: $('#graph_ed_container').height(),
        data_url: "graph_data/"+$.urlParam('id'),
        gui_properties: example_gui_properties
    });
    // this will filter in the different views, excluding the node types that are not listed in params
    graph_editor.handleFiltersParams(params);

});

var filters = function(e, params) {
    graph_editor.handleFiltersParams(params);
    $('#' + e).nextAll('li').remove();
}


function initDropOnGraph() {

    var dropZone = document.getElementById('graph_ed_container');
    dropZone.ondrop = function(e) {
        var group = graph_editor.getCurrentGroup()
        e.preventDefault();
        var nodetype = e.dataTransfer.getData("text/plain");
        if (nodetype) {
            var type_name = graph_editor.getTypeProperty()[nodetype].name;
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

        $("#title_header").text("OSHI Graph Editor");
        $("#vnffg_box").hide();
        $("#vnffg_options").prop("disabled", true);

}

function openEditor(project_id) {
    window.location.href = '/projects/' + project_id + '/descriptors/'+$.urlParam('type')+'/' + $.urlParam('id');
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

}