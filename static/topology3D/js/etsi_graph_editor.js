if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.ManoGraphEditor = (function(global) {
    'use strict';

    var DEBUG = true;
    var SHIFT_BUTTON = 16;

    ManoGraphEditor.prototype = new dreamer.GraphEditor();
    ManoGraphEditor.prototype.constructor = ManoGraphEditor;
    ManoGraphEditor.prototype.parent = dreamer.GraphEditor.prototype;

    /**
     * Constructor
     */
    function ManoGraphEditor(args) {

        log("Constructor");

    }

    ManoGraphEditor.prototype.init = function(args){
         this.parent.init.call(this, args);

         this.type_property = {
            "unrecognized": {
                "shape": d3.symbolCircle,
                "color": "white",
                "default_node_label_color": "black",
                "size": 15
            },
            "ns_vl": {
                "shape": d3.symbolCircle,
                "color": "#196B90",
                "size": 15,
                "name": "VL"
            },
            "ns_cp": {
                "shape": d3.symbolCircle,
                "color": "#F27220",
                "size": 15,
                "name": "CP"
            },
            "vnf": {
                "shape": d3.symbolCircle,
                "color": "#54A698",
                "size": 15,
                "name": "VNF"
            },
            "vnf_vl": {
                "shape": d3.symbolCircle,
                "color": "#5FC9DB",
                "size": 15,
                "name": "IntVL"
            },
            "vnf_ext_cp": {
                "shape": d3.symbolCircle,
                "color": "#00CC66",
                "size": 15,
                "name": "ExtCP"
            },
            "vnf_vdu_cp": {
                "shape": d3.symbolCircle,
                "color": "#E74C35",
                "size": 15,
                "name": "VduCP"
            },
            "vnf_vdu": {
                "shape": d3.symbolCircle,
                "color": "#50A7CC",
                "size": 15,
                "name": "VDU"
            }
        }
    }

    /**
     * Add a new node to the graph.
     * @param {Object} Required. An object that specifies tha data of the new node.
     * @returns {boolean}
     */
    ManoGraphEditor.prototype.addNode = function(args) {
        this.parent.addNode.call(this, args);
    };

    /**
     * Update the data properties of the node
     * @param {Object} Required. An object that specifies tha data of the node.
     * @returns {boolean}
     */
    ManoGraphEditor.prototype.updateDataNode = function(args) {
        this.parent.updateDataNode.call(this, args);
    };

    /**
     * Remove a node from graph and related links.
     * @param {String} Required. Id of node to remove.
     * @returns {boolean}
     */
    ManoGraphEditor.prototype.removeNode = function(node) {
        var self = this;
        new dreamer.GraphRequests().removeNode(node, function(){
            self.parent.removeNode.call(self, node);
        });
    };

    /**
     * Add a new link to graph.
     * @param {Object} Required. An object that specifies tha data of the new Link.
     * @returns {boolean}
     */
    ManoGraphEditor.prototype.addLink = function(s, d) {
        var source_id = s.id;
        var target_id = d.id;
        var link = {
            source: source_id,
            target: target_id,
            view: this.filter_parameters.link.view[0],
            group: this.filter_parameters.link.group[0],
        };
        var source_type = s.info.type;
        var destination_type = d.info.type;
        if((source_type == 'ns_vl' && destination_type ==  'ns_cp') || (source_type == 'ns_cp' && destination_type ==  'ns_vl')){
            var cp_id = source_type == 'ns_cp' ? source_id: target_id;
            var old_link = $.grep(this.d3_graph.links, function(e){return (e.source.id == cp_id || e.target.id == cp_id); });
            var self = this;
            new dreamer.GraphRequests().addLink(s, d, function(){
                self._deselectAllNodes();
                if(typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index){
                    self.removeLink(old_link[0].index);
                }
                self.parent.addLink.call(self, link);
            });
        }
        else if((source_type == 'ns_vl' && destination_type ==  'vnf') || (source_type == 'vnf' && destination_type ==  'ns_vl')){
            //Far scegliere a quale vnf_cpexr collegarlo
            var vnf_id = source_type == 'vnf' ? source_id : target_id;
            var vnf_ext_cps = $.grep(this.d3_graph.nodes, function(e){return (e.info.group == vnf_id &&  e.info.type == 'vnf_ext_cp'); });
            console.log(vnf_ext_cps)

            $('#selection_chooser').empty();
            for (var i in vnf_ext_cps){
                $('#selection_chooser').append('<option id="'+vnf_ext_cps[i].id+'"> '+vnf_ext_cps[i].id+'</option>');
            }
            $('#modal_chooser_title').text('Select the VNF EXT CP of the VNF')
            $('#modal_create_link_chooser').modal('show');
            var self = this;
            $('#save_chooser').on('click', function(){
                var vnf_ext_cp = $( "#selection_chooser option:selected" ).text();
                new dreamer.GraphRequests().addLinkVlVnf(s, d, vnf_ext_cp, function(){
                    self.parent.addLink.call(self, link);
                    $('#modal_create_link_chooser').modal('hide');
                });
            });
        }
        else if((source_type == 'vnf_vl' && destination_type ==  'vnf_vdu_cp') || (source_type == 'vnf_vdu_cp' && destination_type ==  'vnf_vl')){
            //bisognerebbe vedere a quale vdu il cp è collegato
        }
        else if((source_type == 'vnf_ext_cp' && destination_type ==  'vnf_vl') || (source_type == 'vnf_vl' && destination_type ==  'vnf_ext_cp')){
            var self = this;
            new dreamer.GraphRequests().addLink(s, d, function(){
                self._deselectAllNodes();
                self.parent.addLink.call(self, link);
            });
        }else{
            alert("You can't link a "+source_type+" with a "+ destination_type);
        }
    };

    /**
     * Remove a link from graph.
     * @param {String} Required. The identifier of link to remove.
     * @returns {boolean}
     */
    ManoGraphEditor.prototype.removeLink = function(link_id) {
        this.parent.removeLink.call(this, link_id);
    };


    ManoGraphEditor.prototype.savePositions = function(data) {
        var vertices = {}
        this.node.each(function(d) {
            vertices[d.id] = {}
            vertices[d.id]['x'] = d.x;
            vertices[d.id]['y'] = d.y;
        });
        new dreamer.GraphRequests().savePositions({'vertices': vertices});

    }

    /**
     *  Internal functions
     */

    /**
     *
     *
     */
    ManoGraphEditor.prototype._setupBehaviorsOnEvents = function() {
        log("_setupBehaviorsOnEvents");
        var self = this;
        this.behavioursOnEvents = {
            'nodes': {
                'click': function(d) {
                    d3.event.preventDefault();

                    if (self.lastKeyDown == SHIFT_BUTTON && self._selected_node != undefined) {
                        self.addLink(self._selected_node, d);
                    } else {
                        self._selectNodeExclusive(this, d);
                    }

                },
                'mouseover': function(d) {
                    self.link.style('stroke-width', function(l) {
                        if (d === l.source || d === l.target)
                            return 4;
                        else
                            return 2;
                    });
                },
                'mouseout': function(d) {
                    self.link.style('stroke-width', 2);
                },
                'dblclick': function(c_node) {
                    d3.event.preventDefault();
                    log('dblclick ');
                    if(c_node.info.type!= undefined){

                        if(c_node.info.type == 'vnf')
                            self.handleFiltersParams({
                                node: {
                                    type : ['vnf_vl', 'vnf_ext_cp', 'vnf_vdu_cp','vnf_vdu'],
                                    group: [c_node.id]
                                },
                                link: {
                                    group: [c_node.id],
                                    view: ['vnf']
                                }
                            });

                    }

                },
                'contextmenu': function(d,i) {
                    d3.event.preventDefault();
                    log("contextmenu node");
                    self.eventHandler.fire("right_click_node", d);
                }
            },
            'links': {
                'click': function(event) {

                },
                'dblclick': function(event) {

                },
                'mouseover': function(d) {
                    d3.select(this).style('stroke-width', 4);
                },
                'mouseout': function(d) {
                    d3.select(this).style('stroke-width', 2);
                },
                'contextmenu': function(d, i) {
                    d3.event.preventDefault();
                    // react on right-clicking
                    log("contextmenu link");
                }
            }
        };
    };

    ManoGraphEditor.prototype.exploreLayer = function(args) {

    };

    ManoGraphEditor.prototype.getTypeProperty = function(){
        return this.type_property;
    };

    ManoGraphEditor.prototype.getCurrentGroup = function(){
        return this.filter_parameters.node.group[0];

    }
     ManoGraphEditor.prototype.getCurrentView = function(){
        return this.filter_parameters.link.view[0];

    }

    /**
     * Log utility
     */
    function log(text) {
        if (DEBUG)
            console.log("::ManoGraphEditor::", text);
    }



    return ManoGraphEditor;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.ManoGraphEditor;
}