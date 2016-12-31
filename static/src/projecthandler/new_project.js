/**
 *      New Project page
 **/

function handleTypeChoose(type){
    $('#startGroup').show();
}


function startFromChoose(start){
    resetStartFromInputs()
    //resetSelectors();
    var type = $('#select_type').val();

    if(start == 'scratch'){

    }
    if ( start == 'files')
        $('#div-file-upload-'+type).show();
    else if ( start == 'example')
        $('#div-example-'+type).show();

}

function resetStartFromInputs(){
    $('input[type="file"]').val('');

}

$(document).ready(function() {

    // init selector

    $('#select_type').select2({
      placeholder: {
        id: '-1',
        text: 'Select an option'
      },
      data: data_type_selector
    });


    $('#select_type').on("select2:select", function(evt) {
            if (evt) {
                var args = evt.params;
                handleTypeChoose(args.data.value)
            }
    });


    $("#startButtonsSelect :input").change(function() {
        startFromChoose(this.value);
    });


    $('div[class="start-selector"]').each(function(index,item){
        console.log($(item).data('name'), $(item))
    });

});