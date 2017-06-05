function updateDeploymentInfo(args){
    console.log('updateDeploymentInfo')
    getDeploymentInfo({'id': args.id}, function(result){
    }, function(e){
        console.log("getDeploymentInfo Error", e);
    })
}

function getDeploymentInfo(args, success, error){
    $.ajax({
            url: "/deployments/"+args.id,
            type: 'GET',
            dataType: "json",
            contentType: "application/json",
            success: function(result) {
                if (success)
                    success(result);
            },
            error: function(result) {
                if (error)
                    error(result);
            }
        });
}

function getDeploymentNodeConsole(args, success, error){
    $.ajax({
            url: "monitoring/node/"+args.nodeId+"/shell",
            type: 'GET',
            dataType: "json",
            contentType: "application/json",
            success: function(result) {
                if (success)
                    success(result);
            },
            error: function(result) {
                if (error)
                    error(result);
            }
        });
}

function appendDescriptorTab(args){

    var html_tab = '<li><a href="#tab_pane_' + args['id'] +'" data-toggle="tab"><i class="fa fa-file-code-o"></i> ' + args['id'] +'</a></li>';
    var html_tab_textarea = '<textarea id="code_editor_' + args['id'] +'"></textarea>';
    var html_tab_content = '<div class="tab-pane" id="tab_pane_' + args['id'] +'">' + html_tab_textarea + '</div>';
    console.log(html_tab)
    console.log(html_tab_content)
    $('#deploymentDescriptorsTab').append(html_tab);
    $('#tab_pane_container').append(html_tab_content);

     var myTextArea = document.getElementById("code_editor_" + args['id']);
    var editorSuperfluidity = CodeMirror(function (elt) {
        myTextArea.parentNode.replaceChild(elt, myTextArea);
    }, args['editor_settings']);

    editorSuperfluidity.setValue(JSON.stringify(args['desc_data']));
    editorSuperfluidity.setOption("autoRefresh", true);
}