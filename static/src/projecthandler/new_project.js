/**
 *      New Project page
 **/

function resetSelectors(){
    $('start-selector').hide();
}

function handleTypeChoose(type){


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




});