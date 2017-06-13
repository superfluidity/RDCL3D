
function startFromAgent(start) {


    if (start == 'exist'){
        $('#div_new_agent').hide();
        $('#div_available_agent').show();
    }
    else if (start == 'new'){
        $('#div_available_agent').hide();
        $('#div_new_agent').show();
    }

    $('.required').prop('required', function(){
        return  $(this).is(':visible');
    });

}

$(document).ready(function () {
    $("#startButtonsSelect :input").change(function () {
        console.log("select")
        startFromAgent(this.value);
    });
    // Bind events
    $("form").submit(function(e) {
        $("#start_new_deployment").button('loading');
    });

});