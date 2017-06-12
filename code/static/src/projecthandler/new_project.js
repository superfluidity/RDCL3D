/**
 *      New Project page
 **/
function handleTypeChoose(type) {
    resetStartFromInputs()
    $('#projectType').val(type);
    $('#startGroup').show();
    $('input[id="scratch"]').prop('checked', true);
    $('#startButtonsSelect label').removeClass("active");
    $('#s-scratch').addClass("active");
    $('#createButton').prop('disabled', false);
    //$('#projectName').val('New_'+type+'_project')
}

function startFromChoose(start) {
    resetStartFromInputs()
    //resetSelectors();
    var type = $('#select_type').val();

    if (start == 'files')
        $('#div-file-upload-' + type).show();
    else if (start == 'example')
        //document.getElementById['#div-example-' + type].style.display = "block";
       $('#div-example-' + type).css("display", "inline");

}

function resetStartFromInputs() {
    $('div[class="start-selector"]').hide();
    $('input[type="file"]').val('');
    $('select[class="example-selector"]').val(null).trigger("change");
}

$(document).ready(function () {

    // init selector
    $(".start-selector").css("display", "inline");
    $('#select_type').select2({
        placeholder: {
            id: '-1',
            text: 'Select an option'
        },
        data: data_type_selector
    });


    $('#select_type').on("select2:select", function (evt) {
        if (evt) {
            var args = evt.params;
            handleTypeChoose(args.data.value)
        }
    });

    if (type_example_files) {
        for (var key in type_example_files) {
            $('select[id="example-' + key + '"]').select2({
                placeholder: {
                    id: '-1',
                    text: 'Select an option'
                },
                data: type_example_files[key]
            });
        }


    }



    $("#startButtonsSelect :input").change(function () {
        startFromChoose(this.value);
    });



    $("body").bind("ajaxSend", function (elm, xhr, s) {
        if (s.type == "POST") {
            xhr.setRequestHeader('csrftoken', $('#csrfmiddlewaretoken').val());
        }
    });

    $(".start-selector").css("display", "none");

});