if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.ClickController = (function(global) {
    'use strict';

    var DEBUG = true;

    ClickController.prototype.constructor = ClickController;

    /**
     * Constructor
     */
    function ClickController() {


    }


    ClickController.prototype.addNode = function(self, node, success, error) {
        console.log("addNode");
        console.log(JSON.stringify(node), success, error);

        var data_to_send = {
            'group_id': node.info.group[0],
            'element_id': node.id,
            'element_type': node.info.type,
            'element_desc_id': node.info.desc_id,
            'x': node.x,
            'y': node.y
        };
        console.log(data_to_send)
        new dreamer.GraphRequests().addNode(data_to_send, null, function() {
            if (success)
                success();
        });
    };



    ClickController.prototype.removeNode = function(self, node, success, error) {
        node.info.desc_id = getUrlParameter('id');
        if(node.id.indexOf('@') !== -1){
            error && error('To delete this type of node you must edit the configuration file')
        }else{
            new dreamer.GraphRequests().removeNode(node, null, function() {
                if (success) {
                    success();
                }
            });
        }
    };

    ClickController.prototype.removeLink = function(self, link, success, error) {
        var s = link.source;
        var d = link.target;
        link.desc_id = getUrlParameter('id');
        if(s.id.indexOf('@') !== -1 || d.id.indexOf('@') !== -1){
            error && error('To delete this link you must edit the configuration file')
        }else{
            new dreamer.GraphRequests().removeLink(link, success,error);
        }
    };

    ClickController.prototype.addLink = function(self, link, success, error) {
        var s = link.source;
        var d = link.target;
        link.desc_id = getUrlParameter('id');
        console.log(link.desc_id )
        if(s.id.indexOf('@') !== -1 || d.id.indexOf('@') !== -1){
            console.log('To link this types of nodes you must edit the configuration file');
            error && error('To link this types of nodes you must edit the configuration file');
        }else{
            new dreamer.GraphRequests().addLink(link, null, success,error);
        }
    };


    return ClickController;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.ClickController;
}