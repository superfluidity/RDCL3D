$(".closeTab").click(function () {
    console.log("CloseTab click")

    closeTab(this);
    openShellTab({});
});

function closeTab(closeButton){
    var tabContentId = $(closeButton).parent().parent().attr("href");
    $(closeButton).parent().parent().parent().remove(); //remove li of tab
    $('#deploymentTab a:last').tab('show'); // Select first tab
    $(tabContentId).remove(); //remove respective tab content
}

function openShellTab(shellData){
    shellData = {
        "node": {
            "id": "Node-12",
            "label": "Node-12"
        },
        "shellinabox": {
            "endpoint": "http://192.168.100.191:8081/"
        }
    };
    var html_tab = '<li><a href="#tab_pane_' + shellData['node']['id'] +'" data-toggle="tab"><i class="fa fa-terminal"></i> ' + shellData['node']['label'] +' <span><i class="fa fa-times closeTab" style="cursor: pointer; padding-left: 10px;"></i></span></a></li>';
    var html_tab_iframe = '<iframe src="'+ buildShellEndpoint(shellData) +'" class="shellIframe"></iframe>';
    var html_tab_content = '<div class="tab-pane" id="tab_pane_' + shellData['node']['id'] +'">' + html_tab_iframe + '</div>';
    console.log(html_tab)
    console.log(html_tab_content)
    $('#deploymentTab').append(html_tab);
    $('#tab_pane_container').append(html_tab_content);
}

function buildShellEndpoint(shellData){
    var endpoint = shellData['shellinabox']['endpoint'] + "?"
    endpoint+= "nodeid="+shellData['node']['id']
    return endpoint;
}

function buildBehaviorsOnEvents(){
    var contextmenuNodesAction = [{
            title: 'Open Console',
            action: function(elm, d, i) {
                console.log('Open Console from menu');
            }

        }];
    var behavioursOnEvents = {
            'nodes': {
                'contextmenu': d3.contextMenu(contextmenuNodesAction)
            },

        };

    return behavioursOnEvents;
}