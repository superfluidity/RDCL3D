function generateUID() {
    return ("0000" + (Math.random() * Math.pow(36, 4) << 0).toString(36)).slice(-4)
}

function cloneDescriptor(project_id, descriptor_type, descriptor_id){
     $( "#input_choose_new_descriptor_name" ).val(descriptor_id+"_"+generateUID());
     $('#save_new_descriptor_name').off('click').on('click', function(){
        var new_descriptor_id = $( "#input_choose_new_descriptor_name" ).val();
        console.log(descriptor_id);
        window.location.href="/projects/"+project_id+"/descriptors/"+descriptor_type+"/"+descriptor_id+"/clone?newid="+new_descriptor_id ;
    });
    $('#modal_new_descriptor_name').modal('show');

}

function openDescriptorView(project_id, descriptor_type, descriptor_id){
    console.log("openDescriptorView", project_id, descriptor_type, descriptor_id);
    window.location.href='/projects/' + project_id + '/descriptors/' + descriptor_type + '/' + descriptor_id;

}

function toTitleCase(str){
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

function createNewDescriptor(project_id, descriptor_type){
    var type_capitalized = toTitleCase(descriptor_type)

    $("#modal_chooser_new_descriptor_name").text("New "+type_capitalized+" Descriptor");
    $("#input_choose_new_descriptor_name" ).val(descriptor_type+"_"+generateUID());


    $('#save_new_descriptor_name').off('click').on('click', function(){
        var descriptor_id = $( "#input_choose_new_descriptor_name" ).val();
        window.location.href='/projects/' + project_id + '/descriptors/' + descriptor_type + '/new?id='+descriptor_id ;
    });
    $('#modal_new_descriptor_name').modal('show');

}

function showAlert(msg){
    // modal_alert_text
    $('#modal_alert_text').text(msg);
    $('#modal_alert').modal('show');
}

function getUrlParameter(par_name){
    var results = new RegExp('[\?&]' + par_name + '=([^&#]*)').exec(window.location.href);
    if (results == null) {
        return null;
    } else {
        return results[1] || 0;
    }
}

if (!String.format) {
  String.format = function(format) {
    var args = Array.prototype.slice.call(arguments, 1);
    return format.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}