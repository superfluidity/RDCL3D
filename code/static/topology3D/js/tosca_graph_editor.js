if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.ToscaGraphEditor = (function(global) {
    'use strict';

    var DEBUG = true;
    var SHIFT_BUTTON = 16;
    var IMAGE_PATH = "/static/assets/img/";
    var GUI_VERSION = "v1";


    ToscaGraphEditor.prototype = new dreamer.GraphEditor();
    ToscaGraphEditor.prototype.constructor = ToscaGraphEditor;
    ToscaGraphEditor.prototype.parent = dreamer.GraphEditor.prototype;

    /**
     * Constructor
     */
    function ToscaGraphEditor(args) {

        log("Constructor");

    }



    ToscaGraphEditor.prototype.init = function(args) {
        this.parent.init.call(this, args);
        this.current_vnffg = null;

        if (args.gui_properties[GUI_VERSION]!= undefined) {
            args.gui_properties = args.gui_properties[GUI_VERSION];
        }

        this.type_property = {};
        this.type_property["unrecognized"] = args.gui_properties["default"];
        this.type_property["unrecognized"]["default_node_label_color"] = args.gui_properties["default"]["label_color"];
        this.type_property["unrecognized"]["shape"] = this.parent.get_d3_symbol(args.gui_properties["default"]["shape"]);

        Object.keys(args.gui_properties["nodes"]).forEach(function(key, index) {

            this.type_property[key] = args.gui_properties["nodes"][key];
            this.type_property[key]["shape"] = this.parent.get_d3_symbol(this.type_property[key]["shape"]);
            if (this.type_property[key]["image"] != undefined ) {
                this.type_property[key]["image"] = IMAGE_PATH + this.type_property[key]["image"];
            }
            
        }, this);
        var self = this;
        d3.json("graph_data/" + args.descriptor_id, function(error, data) {
            // console.log(data)
            self.d3_graph.nodes = data.vertices;
            self.d3_graph.links = data.edges;
            self.d3_graph.graph_parameters = data.graph_parameters;
            self.refreshGraphParameters();
            self.refresh();
            self.startForce();
            setTimeout(function() {
                self.handleForce(self.forceSimulationActive);
            }, 500);

        });

    }



    /**
     * Update the data properties of the node
     * @param {Object} Required. An object that specifies tha data of the node.
     * @returns {boolean}
     */
    ToscaGraphEditor.prototype.updateDataNode = function(args) {
        this.parent.updateDataNode.call(this, args);
    };




    ToscaGraphEditor.prototype.savePositions = function(data) {
        var vertices = {}
        this.node.each(function(d) {
            vertices[d.id] = {}
            vertices[d.id]['x'] = d.x;
            vertices[d.id]['y'] = d.y;
        });
        new dreamer.GraphRequests().savePositions({
            'vertices': vertices
        });

    }

    /**
     *  Internal functions
     */

    /**
     *
     *
     */
    ToscaGraphEditor.prototype._setupBehaviorsOnEvents = function() {
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
                    if (c_node.info.type != undefined) {



                    }

                },
                'contextmenu': d3.contextMenu([{
                    title: 'Edit',
                    action: function(elm, d, i) {
                        if (d.info.type != undefined) {
                            if (d.info.type == 'vnf') {
                                window.location.href = '/projects/' + self.project_id + '/descriptors/vnfd/' + d.id;

                            } else {
                                window.location.href = '/projects/' + self.project_id + '/descriptors/' + graph_editor.getCurrentView() + 'd/' + graph_editor.getCurrentGroup();

                            }
                        }
                    }

                }, ])
            },
            'links': {
                'click': function(d) {
                    self._selectLinkExclusive(this, d);

                },
                'dblclick': function(event) {

                },
                'mouseover': function(d) {
                    d3.select(this).style('stroke-width', 4);
                },
                'mouseout': function(d) {
                    if (d != self._selected_link)
                        d3.select(this).style('stroke-width', 2);
                },
                'contextmenu': d3.contextMenu([{
                    title: 'Delete Link',
                    action: function(elm, link, i) {
                        self.removeLink(link);
                    }

                }])
            }
        };
    };

    ToscaGraphEditor.prototype.exploreLayer = function(args) {

    };

    ToscaGraphEditor.prototype.getTypeProperty = function() {
        return this.type_property;
    };

    ToscaGraphEditor.prototype.getCurrentGroup = function() {
        return this.filter_parameters.node.group[0];

    }
    ToscaGraphEditor.prototype.getCurrentView = function() {
        return this.filter_parameters.link.view[0];

    }
    ToscaGraphEditor.prototype.refreshGraphParameters = function() {
        //  setVnffgIds(this.d3_graph.graph_parameters.vnffgIds)
    }
    ToscaGraphEditor.prototype.getVnffgParameter = function() {
        return this.d3_graph.graph_parameters.vnffgIds;
    }



    /**
     * Log utility
     */
    function log(text) {
        if (DEBUG)
            console.log("::ToscaGraphEditor::", text);
    }



    return ToscaGraphEditor;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.ToscaGraphEditor;
}