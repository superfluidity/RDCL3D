
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
/*
function InvalidGitUrl(textbox) {
    console.log('InvalidGitUrl', textbox,textbox.value == '' ,textbox.validity.typeMismatch)
    if (textbox.value === '') {
        textbox.setCustomValidity('Required git URL');
    }
    else if (textbox.validity.typeMismatch){
        textbox.setCustomValidity('please enter a valid git URL');

    }
    else {
        textbox.setCustomValidity('please enter a valid git URL');
    }
    return true;
}
*/
function startFromRepo(start) {


    if (start == 'exist'){
        $('#div_new_repo').hide();
        $('#div_available_repo').show();
    }
    else if (start == 'new'){
        $('#div_available_repo').hide();
        $('#div_new_repo').show();
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
    $("#push_start_buttons_select :input").change(function () {
        console.log("select")
        startFromRepo(this.value);
    });

    // Bind events
    $("form").submit(function(e) {
        console.log("on submit form")
        $("#start_new_deployment").button('loading');
    });

});