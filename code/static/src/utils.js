function generateUID() {
    return ("0000" + (Math.random() * Math.pow(36, 4) << 0).toString(36)).slice(-4)
}

function openProject(pId){
    window.location.href='/projects/' + pId;
}

function openDeployment(expId){
    window.location.href='/deployments/' + expId;
}

function cloneDescriptor(project_id, descriptor_type, descriptor_id) {
    $("#input_choose_new_descriptor_name").val(descriptor_id + "_" + generateUID());
    $('#save_new_descriptor_name').off('click').on('click', function () {
        var new_descriptor_id = $("#input_choose_new_descriptor_name").val();
        console.log(descriptor_id);
        window.location.href = "/projects/" + project_id + "/descriptors/" + descriptor_type + "/" + descriptor_id + "/clone?newid=" + new_descriptor_id;
    });
    $('#modal_new_descriptor_name').modal('show');

}

function openDescriptorView(project_id, descriptor_type, descriptor_id) {
    console.log("openDescriptorView", project_id, descriptor_type, descriptor_id);
    window.location.href = '/projects/' + project_id + '/descriptors/' + descriptor_type + '/' + descriptor_id;

}

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

function createNewDescriptor(project_id, descriptor_type) {
    var type_capitalized = toTitleCase(descriptor_type)

    $("#modal_chooser_new_descriptor_name").text("New " + type_capitalized + " Descriptor");
    $("#input_choose_new_descriptor_name").val(descriptor_type + "_" + generateUID());


    $('#save_new_descriptor_name').off('click').on('click', function () {
        var descriptor_id = $("#input_choose_new_descriptor_name").val();
        window.location.href = '/projects/' + project_id + '/descriptors/' + descriptor_type + '/new?id=' + descriptor_id;
    });
    $('#modal_new_descriptor_name').modal('show');

}

function buildPalette(args) {
    //
    $("#paletteContainer").empty();
    var type_property = graph_editor.getTypeProperty();
    if (args.length > 0) {
        args.forEach(function (category) {
            var category_id = "category_" + category.category_name.replace(/[.*+?^${}()|[\]\\]/g, "_");//.replace(/\s/g, '');
            var content_id = "palette-content-" + category.category_name.replace(/[.*+?^${}()|[\]\\]/g, "_");//.replace(/\s/g, '');
            $("#paletteContainer").append('<div id="' + category_id + '" class="palette-category" ><div class="palette-header" onClick="handlePaletteCat(this);" category_id="' + category_id + '"> ' +
                '<i class="fa fa-chevron-right fa-rotate-90"></i>' +
                '<span>  ' + category.category_name + '</span>' +
                '</div>' +
                '<div id="' + content_id + '" class="palette-content">' +

                '</div>' +
                '</div>');
            category.types.forEach(function (type) {
                var type_id = type.id.replace(/[.*+?^${}()|[\]\\]/g, "_");
                var palette_node_icon = (type_property[category.id].image) ? '<div class="palette-node-icon" style="background-image: url(' + (type_property[category.id].image || "") + ')"></div>' :
                    '<div class="palette-node-icon" style="background-color:' + type_property[category.id].color + '"></div>'
                var html_to_append = '<div class="palette-node ui-draggable" draggable="true" id="' + type_id + '" ondragstart="nodeDragStart(event)">' +
                    '<div class="palette-node-label">' + type.name + '</div>' +
                    '<div class="palette-node-icon-container">' +
                    palette_node_icon +
                    '</div>' +
                    '</div>'
                $("#" + content_id).append(html_to_append);
            });

        });
    }
    togglePaletteSpinner();


}

function handlePaletteCat(item) {
    console.log("handlePaletteContainer")
    var category_id = $(item).attr("category_id")
    $('#' + category_id).toggleClass("palette-open");

}

function togglePaletteSpinner() {
    $('#palette').toggleClass("palette-status-hidden");
}

function showAlert(msg) {
    // modal_alert_text
    $('#modal_alert_text').text(msg);
    $('#modal_alert').modal('show');
}

function getUrlParameter(par_name) {
    var results = new RegExp('[\?&]' + par_name + '=([^&#]*)').exec(window.location.href);
    if (results == null) {
        return null;
    } else {
        return results[1] || 0;
    }
}

if (!String.format) {
    String.format = function (format) {
        var args = Array.prototype.slice.call(arguments, 1);
        return format.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined' ?
                args[number] :
                match;
        });
    };
}