
//GraphEditor instance
var graph_editor = new dreamer.ModelGraphEditor();
var selected_vnffgId = null;
var show_all = null;

// Enable Drop Action on the Graph
initDropOnGraph();



$(document).ready(function() {
    var descriptor_type = getUrlParameter('type');
    var type = descriptor_type == 'click'  ? ['click'] : ['click'];
    var params = {
        node: {
            type: ['element', 'compound_element', 'class_element'],
            group: ['click']
        },
        link: {
            group: ['click'],
            view: ['compact']
        }
    }



    // graph_editor initialization
    graph_editor.init({
        width: $('#graph_ed_container').width(),
        height: $('#graph_ed_container').height(),
        gui_properties: example_gui_properties,
        descriptor_id: getUrlParameter('id'),
        data_url: "graph_data/"+getUrlParameter('id'),
        filter_base: params
    });
    //console.log(graph_editor.getCurrentView())
    graph_editor.handleFiltersParams(params);
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
    var type_property = graph_editor.getTypeProperty();
    $("#title_header").text("Click Graph Editor");
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

function openEditor(project_id){
    window.location.href='/projects/'+project_id+'/descriptors/'+getUrlParameter('type')+'/'+getUrlParameter('id');
}

