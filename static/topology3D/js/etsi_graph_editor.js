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
                "color": "#313679",
                "size": 15,
                "name": "IntVL"
            },
            "vnf_ext_cp": {
                "shape": d3.symbolCircle,
                "color": "#1F2B35",
                "size": 15,
                "name": "ExtCP"
            },
            "vnf_vdu_cp": {
                "shape": d3.symbolCircle,
                "color": "#4E6293",
                "size": 15,
                "name": "VduCP"
            },
            "vnfc": {
                "shape": d3.symbolCircle,
                "color": "#1D74C2",
                "size": 15
            },
            "vnf_vdu": {
                "shape": d3.symbolCircle,
                "color": "#4B7C91",
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
    ManoGraphEditor.prototype.removeNode = function(node_id) {
        this.parent.removeNode.call(this, node_id);
    };

    /**
     * Add a new link to graph.
     * @param {Object} Required. An object that specifies tha data of the new Link.
     * @returns {boolean}
     */
    ManoGraphEditor.prototype.addLink = function(link) {
        this.parent.addLink.call(this, link);
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
        data.append('positions', JSON.stringify({'vertices': vertices}) );
        $.ajax({
            url: "positions",
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(result) {
            },
            error: function(result) {
                alert("some error");
            }
        });
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
                        var source_id = self._selected_node;
                        var target_id = d.id;
                        var new_link = {
                            source: source_id,
                            target: target_id,
                            view: self.current_view_id
                        };
                        self.addLink(new_link);
                        self._deselectAllNodes();
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