
//ManoGraphEditor instance
var graph_editor = new dreamer.ClickGraphEditor();
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
        height: $('#graph_ed_container').height(),
        gui_properties: example_gui_properties,
        descriptor_id: $.urlParam('id')
    });
    graph_editor.handleFiltersParams(params);

    $('#draggable-container').hide()
});

var filters = function(e, params) {
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


}







//***STEFANO
var example_gui_properties = {
  "default": {
    "shape": "circle",
    "color": "#42f44e",
    "label_color": "black",
    "size": 15
  },
  "nodes": {
    "pippo": {
      "image": "image.png",
      "size": 25
    },
    "ns_vl": {
      "shape": "triangle",
      "color": "#196B90",
      "size": 11,
      "name": "VL"
    },
    "ns_cp": {
      "shape": "circle",
      "color": "#F27220",
      "size": 15,
      "name": "CP"
    },
    "vnf": {
      "shape": "square",
      "color": "#54A698",
      "size": 18,
      "name": "VNF"
    },
    "vnf_vl": {
      "shape": "triangle",
      //"color": "#5FC9DB",
      "color": "#196B90",
      "size": 11,
      "name": "IntVL"
    },
    "vnf_ext_cp": {
      "shape": "circle",
      //"#00CC66",
      "color": "#F27220",
      "size": 15,
      "name": "ExtCP"
    },
    "vnf_vdu_cp": {
      "shape": "circle",
      //"color": "#E74C35",
      "color": "#F27220",
      "size": 15,
      "name": "VduCP"
    },
    "vnf_vdu": {
      "shape": "square",
      //"color": "#50A7CC",
      "color": "#54A698",
      "size": 18,
      "name": "VDU"
    }
  },
  "graphs": null
}