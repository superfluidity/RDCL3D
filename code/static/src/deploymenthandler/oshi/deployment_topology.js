//GraphEditor instance
var graph_editor = new dreamer.ModelGraphEditor();
var selected_vnffgId = null;
var show_all = null;


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
    //graph_editor.addListener("filters_changed", changeFilter);
    graph_editor.addListener("refresh_graph_parameters", refreshGraphParameters);

    console.log(example_gui_properties)
    // graph_editor initialization
    graph_editor.init({
        width: $('#graph_ed_container').width(),
        height: $('#graph_ed_container').height(),
        graph_data: topology_data,//{ 'vertices': [], 'edges': []},
        //data_url: "graph_data/"+getUrlParameter('id'),
        desc_id: getUrlParameter('id'),
        gui_properties: example_gui_properties,
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


function changeFilter(e, c) {

    console.log("changeFilter", JSON.stringify(c));
    //$("#title_header").text("OSHI Graph Editor");
    //updateNodeDraggable({type_property: type_property, nodes_layer: graph_editor.getAvailableNodes()})
    if(c)
        new dreamer.GraphRequests().getAvailableNodes({layer: c.link.view[0]}, buildPalette, showAlert);

}

function openEditor(project_id) {
    window.location.href = '/projects/' + project_id + '/descriptors/'+getUrlParameter('type')+'/' + getUrlParameter('id');
}



function nodeDragStart(event){
    event.dataTransfer.setData("Text", event.target.id);
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