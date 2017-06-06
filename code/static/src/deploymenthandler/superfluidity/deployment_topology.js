//GraphEditor instance
var graph_editor = new dreamer.ModelGraphEditor();
var show_all = null;


$(document).ready(function() {
    var params = {
        node: {
            type: [],
            group: []
        },
        link: {
            group: [],
            view: []
        }
    }
    graph_editor.addListener("refresh_graph_parameters", refreshGraphParameters);

    console.log(example_gui_properties)
    // graph_editor initialization
    graph_editor.init({
        width: $('#graph_ed_container').width(),
        height: $('#graph_ed_container').height(),
        graph_data: topology_data,
        gui_properties: example_gui_properties,
        edit_mode: false,
        behaviorsOnEvents:{
            viewBased: false,
            behaviors: buildBehaviorsOnEvents()
        }
    });
    // this will filter in the different views, excluding the node types that are not listed in params
    graph_editor.handleFiltersParams(params);
});

var filters = function(e, params) {
    graph_editor.handleFiltersParams(params);
    $('#' + e).nextAll('li').remove();
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



function refreshGraphParameters(e, graphParameters) {

    var self = $(this);
    if (graphParameters == null) return;


}



function clickView(){
    if ($("#view_box").is(':visible'))
        $("#view_box").hide();
    else
        $("#view_box").show();
}

function changeView(e){
    var viewId = e.value;
    console.log("viewId", viewId)
    var params = {
        node: {
            type: [],
            group: []
        },
        link: {
            group: [],
            view: [viewId]
        }
    }
    graph_editor.handleFiltersParams(params);
}