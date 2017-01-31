
//GraphEditor instance
var graph_editor = new dreamer.ClickGraphEditor();
var selected_vnffgId = null;
var show_all = null;

// Enable Drop Action on the Graph
initDropOnGraph();



$(document).ready(function() {
    var descriptor_type = getUrlParamater('type');
    var type = descriptor_type == 'click'  ? ['click'] : ['click'];
    var params = {
        node: {
            type: type,
            group: []
        },
        link: {
            group: [type],
            view: []
        }
    }
    graph_editor.addListener("filters_changed", changeFilter);


    // graph_editor initialization
    graph_editor.init({
        width: $('#graph_ed_container').width(),
        height: $('#graph_ed_container').height(),
        gui_properties: example_gui_properties,
        descriptor_id: getUrlParamater('id')
    });
   // graph_editor.handleFiltersParams(params);

    $('#draggable-container').hide();
    $('#vnffg_options').hide();
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
        var type_name = graph_editor.getTypeProperty()[nodetype].name;
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
    console.log("changeFilter");

}

function openEditor(project_id){
    window.location.href='/projects/'+project_id+'/descriptors/'+getUrlParamater('type')+'/'+getUrlParamater('id');
}

