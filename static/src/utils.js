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