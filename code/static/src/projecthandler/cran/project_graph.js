
//GraphEditor instance
var graph_editor = new dreamer.ModelGraphEditor();
var selected_vnffgId = null;
var show_all = null;

// Enable Drop Action on the Graph
initDropOnGraph();



$(document).ready(function() {
    var descriptor_type = getUrlParameter('type');
    // should init the correct parameters
    var type = [];
    var params = {
        node: {
            type: [],
            group: []
        },
        link: {
            group: [],
            view: ['full']
        }
    }



    // graph_editor initialization
    graph_editor.init({
        width: $('#graph_ed_container').width(),
        height: $('#graph_ed_container').height(),
        gui_properties: example_gui_properties,
        desc_id: getUrlParameter('id'),
        data_url: "graph_data/"+getUrlParameter('id'),
        filter_base: params
    });
    //console.log(graph_editor.getCurrentView())
    graph_editor.handleFiltersParams(params, false);
    graph_editor.addListener("filters_changed", changeFilter);

});

var filters = function(e, params) {
    graph_editor.handleFiltersParams(params);
    $('#' + e).nextAll('li').remove();
}



function initDropOnGraph(){
var dropZone = document.getElementById('graph_ed_container');
dropZone.ondrop = function(e) {
    var group = graph_editor.getCurrentGroup()
    e.preventDefault();
    var nodetype = e.dataTransfer.getData("text/plain");
    if (nodetype) {
        //nodetype = nodetype.replace(/_/g, ".")
        //console.log(graph_editor.getTypeProperty())
        var type_name = graph_editor.getTypeProperty()[nodetype].name;
        $('#div_chose_id').show();
                $('#div_chose_vnf').hide();
                $('#input_choose_node_id').val(nodetype.substring(nodetype.lastIndexOf(".")+1) + "_" + generateUID());
                $('#modal_chooser_title_add_node').text('Add ' + type_name);
                $('#save_choose_node_id').off('click').on('click', function() {
                    var name = $('#input_choose_node_id').val();
                    var node_information = {
                        'id': name,
                        'info': {
                            'type': nodetype,
                            //'group': [group]
                            'rfb-level': (nodetype != 'functional_block' ) ? 'leaf' : 'rfb/1',
                            'desc_id': getUrlParameter('id'),
                        },
                        'x': e.layerX,
                        'y': e.layerY
                    }
                    graph_editor.addNode(node_information, function() {
                        $('#modal_choose_node_id').modal('hide');
                    }, function(error){
                        showAlert(error)
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
    console.log("changeFilter", JSON.stringify(c));
    var type_property = graph_editor.getTypeProperty();
    $("#title_header").text("Cran NFV Graph Editor");

        view = (c.link && c.link.view && c.link.view[0] ) ? c.link.view[0]: 'full';
    new dreamer.GraphRequests().getAvailableNodes({layer: c.link.view[0]}, buildPalette, showAlert);
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

function nodeDragStart(event){
    event.dataTransfer.setData("Text", event.target.id);
}

function openEditor(project_id){
    window.location.href='/projects/'+project_id+'/descriptors/'+getUrlParameter('type')+'/'+getUrlParameter('id');
}

