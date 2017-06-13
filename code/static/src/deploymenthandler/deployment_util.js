    var json_editor_settings = {
    mode: "application/json",
    showCursorWhenSelecting: true,
    autofocus: true,
    lineNumbers: true,
    lineWrapping: true,
    foldGutter: true,
    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
    autoCloseBrackets: true,
    matchBrackets: true,
    extraKeys: {
        "F11": function (cm) {
            cm.setOption("fullScreen", !cm.getOption("fullScreen"));
        },
        "Esc": function (cm) {
            if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
        },
        "Ctrl-Q": function (cm) {
            cm.foldCode(cm.getCursor());
        }
    },
    theme: "neat",
    keyMap: "sublime",
    readOnly: true,
};


var yaml_editor_settings = {
            mode: "yaml-frontmatter",
            showCursorWhenSelecting: true,
            autofocus: true,
            autoRefresh: true,
            lineNumbers: true,
            lineWrapping: true,
            foldGutter: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
            autoCloseBrackets: true,
            matchBrackets: true,
            extraKeys: {
                "F11": function(cm) {
                    cm.setOption("fullScreen", !cm.getOption("fullScreen"));
                },
                "Esc": function(cm) {
                    if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
                },
                "Ctrl-Q": function(cm) {
                    cm.foldCode(cm.getCursor());
                }
            },
            theme: "neat",
            keyMap: "sublime",
        };

 var click_editor_settings = {
            mode: "text",
            showCursorWhenSelecting: true,
            autofocus: true,
            lineNumbers: true,
            lineWrapping: true,
            foldGutter: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
            autoCloseBrackets: true,
            matchBrackets: true,
            extraKeys: {
                "F11": function(cm) {
                    cm.setOption("fullScreen", !cm.getOption("fullScreen"));
                },
                "Esc": function(cm) {
                    if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
                },
                "Ctrl-Q": function(cm) {
                    cm.foldCode(cm.getCursor());
                }
            },
            theme: "neat",
            keyMap: "sublime",
        };

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

function getDeploymentNodeInfo(args, success, error){
    $.ajax({
            url: "monitoring/node/"+args.nodeId+"/",
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
    var class_li = (args['active'])? 'active': ''
    var html_tab = '<li class="'+ class_li +'" ><a href="#tab_pane_' + args['id'] +'" data-toggle="tab"><i class="fa fa-file-code-o"></i> ' + args['type_dec'] + ':' + args['id'] +'</a></li>';
    var html_tab_textarea = '<textarea id="code_editor_' + args['id'] +'"></textarea>';
    var html_tab_content = '<div class="tab-pane '+class_li+'" id="tab_pane_' + args['id'] +'">' + html_tab_textarea + '</div>';
    console.log(html_tab)
    console.log(html_tab_content)
    $('#deploymentDescriptorsTab').append(html_tab);
    $('#tab_pane_container').append(html_tab_content);

     var myTextArea = document.getElementById("code_editor_" + args['id']);
    var editorSuperfluidity = CodeMirror(function (elt) {
        myTextArea.parentNode.replaceChild(elt, myTextArea);
    }, json_editor_settings);

    console.log(typeof args['desc_data'])
    if (typeof args['desc_data'] != "string"){
        editorSuperfluidity.setValue(JSON.stringify(args['desc_data']));
        CodeMirror.commands["selectAll"](editorSuperfluidity);
        editorSuperfluidity.autoFormatRange(editorSuperfluidity.getCursor(true), editorSuperfluidity.getCursor(false));
        CodeMirror.commands["goLineStart"](editorSuperfluidity);
    }
    else
        editorSuperfluidity.setValue((args['desc_data']));


    editorSuperfluidity.setOption("autoRefresh", true);
}