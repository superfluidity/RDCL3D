
//ManoGraphEditor instance
var graph_editor = new dreamer.ManoGraphEditor();


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
    var descriptor_type = $.urlParam('type') == 'ns' || $.urlParam('type') == 'nsd' ? 'ns' : 'vnf'
    var type = descriptor_type == 'ns'  ? ['vnf', 'ns_cp', 'ns_vl'] : ['vnf_vl', 'vnf_ext_cp', 'vnf_vdu_cp', 'vnf_vdu'];
    var params = {
        node: {
            type: type,
            group: [$.urlParam('id')]
        },
        link: {
            group: [$.urlParam('id')],
            view: [descriptor_type]
        }
    }

    graph_editor.addListener("filters_changed", changeFilter);


    graph_editor.addListener("right_click_node", function(a, args) {
        //console.log("node_selected", a, args);
        $('#modal_edit_descriptor').modal('show');
    });

    // graph_editor initialization
graph_editor.init({
    width: $('#graph_ed_container').width(),
    height: $('#graph_ed_container').height()
});

graph_editor.handleFiltersParams(params);

});

var filters = function(e, params) {
    console.log(e)
    graph_editor.handleFiltersParams(params);
    $('#' + e).nextAll('li').remove();
}

function generateUID() {
    return ("0000" + (Math.random() * Math.pow(36, 4) << 0).toString(36)).slice(-4)
}

function initDropOnGraph(){

var dropZone = document.getElementById('graph_ed_container');
dropZone.ondrop = function(e) {
    var group = graph_editor.getCurrentGroup()
    e.preventDefault();
    var nodetype = e.dataTransfer.getData("text/plain");
    if (nodetype) {
        var node_information = {
            'id': nodetype + "_" + generateUID(),
            'info': {
                'type': nodetype,
                'group': group
                },
               'x': e.layerX,
               'y': e.layerY
            }
        new dreamer.GraphRequests().addNode(node_information, function(){
            graph_editor.addNode(node_information);
        });
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
    var data = new FormData();
    data.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    graph_editor.savePositions(data);
}

function changeFilter(e, c) {
    console.log("changeFilter", $("#draggable-container"))
    var type_property = graph_editor.getTypeProperty();
    $("#draggable-container").empty()
    for (var i in c.node.type) {
        console
        var event = 'event.dataTransfer.setData("text/plain","' + c.node.type[i] + '")'
        $("#draggable-container").append('<span type="button" class="btn btn-flat btn-default drag_button" draggable="true" id="' + c.node.type[i] + '"  ondragstart=' + event + ' style="background-color: ' + type_property[c.node.type[i]].color + ' !important;"><p>' + type_property[c.node.type[i]].name + '</p></span>');
    }
    var newLi = $("<li id=" + JSON.stringify(graph_editor.getCurrentGroup()) + "><a href='javascript:filters(" + JSON.stringify(graph_editor.getCurrentGroup()) + "," + JSON.stringify(c) + ")'>" + graph_editor.getCurrentGroup() + "</a></li>");
    $('#breadcrumb').append(newLi);
}

function openEditor(project_id){
    window.location.href='/projects/'+project_id+'/descriptors/'+graph_editor.getCurrentView()+'d/'+graph_editor.getCurrentGroup();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}