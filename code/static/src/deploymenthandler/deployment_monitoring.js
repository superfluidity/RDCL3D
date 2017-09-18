function closeTab(closeButton){
    var tabContentId = $(closeButton).parent().parent().attr("href");
    $(closeButton).parent().parent().parent().remove(); //remove li of tab
    $('#deploymentTab a:last').tab('show'); // Select first tab
    $(tabContentId).remove(); //remove respective tab content
}

function getNodeShell(args){

    getDeploymentNodeConsole({
        'nodeId': args['node']['id']
    }, function(result){
        //console.log(result);
        args['console_info'] = result['console_info']
        openShellTab(args)
    }, function(error){
        showAlert("Error opening shell.")
    })
}


function getNodeInfo(args){

    getDeploymentNodeInfo({
        'nodeId': args['node']['id']
    }, function(result){
        //console.log("getNodeInfo")
        //console.log(result);
        //args['console_info'] = result['console_info']
        //openShellTab(args)
        openNodeModalInfo(result);
    }, function(error){
        showAlert("Error opening info node.")
    })
}
function openShellTab(shellData){
    var name = generateUID();
    var html_tab = '<li><a href="#tab_pane_' + shellData['node']['id'] +'_'+name+'" data-toggle="tab"><i class="fa fa-terminal"></i> ' + shellData['node']['label'] +' <span><i class="fa fa-times closeTab" onClick="closeTab(this)" style="cursor: pointer; padding-left: 10px;"></i></span></a></li>';
    var html_tab_iframe = '<iframe name='+name+' src="'+ shellData['console_info']['url'] +'" class="shellIframe"></iframe>';
    var html_tab_content = '<div class="tab-pane" id="tab_pane_' + shellData['node']['id'] +'_'+name+'">' + html_tab_iframe + '</div>';
    //console.log(html_tab)
    //console.log(html_tab_content)
    $('#deploymentTab').append(html_tab);
    $('#tab_pane_container').append(html_tab_content);
}




function buildBehaviorsOnEvents(){
    var contextmenuNodesAction = [{
            title: 'Show info',
            action: function(elm, d, i) {
                //console.log('Show NodeInfo', elm, d, i);
                var nodeData = {
                    "node": {
                        "id": d.id
                    }
                };
                getNodeInfo(nodeData);
            },
            edit_mode: false

        },{
            title: 'Open Console',
            action: function(elm, d, i) {
                //console.log('Open Console from menu', elm, d, i);
                var shellData = {
                    "node": {
                        "id": d.id,
                        "label": d.id
                    }
                };
                getNodeShell(shellData);
            },
            edit_mode: false

        }];
    var behavioursOnEvents = {
            'nodes': contextmenuNodesAction,

        };

    return behavioursOnEvents;
}