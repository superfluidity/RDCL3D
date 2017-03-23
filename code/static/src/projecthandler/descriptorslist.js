
function startFromAgent(start) {


    if (start == 'exist'){
        $('#div_new_agent').hide();
        $('#div_available_agent').show();
    }
    else if (start == 'new'){
        $('#div_available_agent').hide();
        $('#div_new_agent').show();
    }


}

$(document).ready(function () {
    $("#startButtonsSelect :input").change(function () {
        console.log("select")
        startFromAgent(this.value);
    });
});