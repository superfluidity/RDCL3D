/*
   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni

   Licensed under the Apache License, Version 2.0 (the );
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an  BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.ModelGraphEditor = (function(global) {
    'use strict';

    var DEBUG = true;
    var SHIFT_BUTTON = 16;
    var IMAGE_PATH = "/static/assets/img/";
    var GUI_VERSION = "v1";


    ModelGraphEditor.prototype = new dreamer.GraphEditor();
    ModelGraphEditor.prototype.constructor = ModelGraphEditor;
    ModelGraphEditor.prototype.parent = dreamer.GraphEditor.prototype;

    /**
     * Constructor
     */
    function ModelGraphEditor(args) {

        log("Constructor");

    }


    ModelGraphEditor.prototype.init = function(args) {
        this.parent.init.call(this, args);

        if (args.gui_properties[GUI_VERSION] != undefined) {
            args.gui_properties = args.gui_properties[GUI_VERSION];
        }

        this.desc_id = args.desc_id || undefined;
        this.type_property = {};
        this.type_property["unrecognized"] = args.gui_properties["default"];
        this.type_property["unrecognized"]["default_node_label_color"] = args.gui_properties["default"]["label_color"];
        //this.type_property["unrecognized"]["shape"] = d3.symbolCross;

        Object.keys(args.gui_properties["nodes"]).forEach(function(key, index) {
            this.type_property[key] = args.gui_properties["nodes"][key];
            this.type_property[key]["shape"] = this.parent.get_d3_symbol(this.type_property[key]["shape"]);
            if (this.type_property[key]["image"] != undefined) {
                this.type_property[key]["image"] = IMAGE_PATH + this.type_property[key]["image"];
            }


        }, this);
        var self = this;
        var data_url = (args.data_url) ? args.data_url : "graph_data/";
        d3.json(data_url, function(error, data) {
            log('data from remote')
            console.log(data)
            self.d3_graph.nodes = data.vertices;
            self.d3_graph.links = data.edges;
            self.d3_graph.graph_parameters = data.graph_parameters;
            self.model = data.model;

            self.refreshGraphParameters(self.d3_graph.graph_parameters);
            self.refresh();
            self.startForce();
             //if(args.filter_base != undefined)

            setTimeout(function() {
                //self.handleForce(self.forceSimulationActive);
                self.handleFiltersParams(args.filter_base);
            }, 500);

        });
    }

    /**
     * Add a new node to the graph.
     * @param {Object} Required. An object that specifies tha data of the new node.
     * @returns {boolean}
     */
    ModelGraphEditor.prototype.addNode = function(node, success, error) {
        var self = this;
        var current_layer = self.getCurrentView()
        var node_type = node.info.type;

        if (self.model.layer[current_layer] && self.model.layer[current_layer].nodes[node_type] && self.model.layer[current_layer].nodes[node_type].addable) {
            if (self.model.layer[current_layer].nodes[node_type].addable.callback) {
                var c = self.model.callback[self.model.layer[current_layer].nodes[node_type].addable.callback].class;
                var controller = new dreamer[c]();
                controller[self.model.layer[current_layer].nodes[node_type].addable.callback](self, node, function() {
                    self.parent.addNode.call(self, node);
                    success && success();
                }, error);

            } else {

                log('addNode: callback undefined in model spec.');
                error && error("You can't add a " + node.info.type + ", callback undefined.");
            }
        }
        else{
            //FIXME Error handling????
            log("You can't add a " + node.info.type + " in a current layer " + current_layer);
            error && error("You can't add a " + node.info.type + " in a current layer " + current_layer);
        }
    };



    /**
     * Update the data properties of the node
     * @param {Object} Required. An object that specifies tha data of the node.
     * @returns {boolean}
     */
    ModelGraphEditor.prototype.updateDataNode = function(args) {
        //FIXME updating a node properties need commit to server side!
        this.parent.updateDataNode.call(this, args);
    };

    /**
     * Remove a node from graph and related links.
     * @param {String} Required. Id of node to remove.
     * @returns {boolean}
     */
    ModelGraphEditor.prototype.removeNode = function(node, success, error) {
        var self = this;
        var current_layer = self.getCurrentView();
        var node_type = node.info.type;
        if (self.model.layer[current_layer] && self.model.layer[current_layer].nodes[node_type] && self.model.layer[current_layer].nodes[node_type].removable) {
            if (self.model.layer[current_layer].nodes[node_type].removable.callback) {
                var c = self.model.callback[self.model.layer[current_layer].nodes[node_type].removable.callback].class;
                var controller = new dreamer[c]();
                controller[self.model.layer[current_layer].nodes[node_type].removable.callback](self, node, function() {
                    self.parent.removeNode.call(self, node);
                    success && success();
                }, error);
            } else {

                log('removeNode: callback undefined in model spec.');
                error && error("You can't remove a " + node.info.type + ", callback undefined.");
            }
        } else {
            //FIXME we need to manage alert in a different way: FAILBACK
            log("You can't remove a " + node.info.type);
            error && error("You can't remove a " + node.info.type);
        }
    };

    /**
     * Add a new link to graph.
     * @param {Object} Required. An object that specifies tha data of the new Link.
     * @returns {boolean}
     */
    ModelGraphEditor.prototype.addLink = function(s, d, success, error) {
        var self = this;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var link = {
            source: s,
            target: d,
            view: this.filter_parameters.link.view[0],
            group: this.filter_parameters.link.group,
            desc_id: this.desc_id
        };
        log("addLink: " + JSON.stringify(link))
        var current_layer = self.getCurrentView()
        if (self.model.layer[current_layer].allowed_edges && self.model.layer[current_layer].allowed_edges[source_type] && self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type]) {

            if (self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type].callback) {
                var callback = self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type].callback;
                var c = self.model.callback[callback].class;
                var controller = new dreamer[c]();
                controller[callback](self, link, function() {
                    self._deselectAllNodes();
                    self.parent.addLink.call(self, link);
                    if (success)
                        success();
                }, error);
            } else {
                log('addLink: callback undefined in model spec.');
                error && error("You can't add a link, callback undefined.");
            }

        } else {
            //FIXME we need to manage alert in a different way: FAILBACK
            log("You can't link a " + source_type + " with a " + destination_type);

            error && error("You can't link a " + source_type + " with a " + destination_type);
        }
    };

    /**
     * Remove a link from graph.
     * @param {String} Required. The identifier of link to remove.
     * @returns {boolean}
     */
    ModelGraphEditor.prototype.removeLink = function(link, success, error) {
        var self = this;
        var s = link.source;
        var d = link.target;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var current_layer = self.getCurrentView()
        if (self.model.layer[current_layer].allowed_edges && self.model.layer[current_layer].allowed_edges[source_type] && self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type] &&
            self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type].removable
        ) {
            if (self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type].removable.callback) {
                var callback = self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type].removable.callback;
                var c = self.model.callback[callback].class;
                var controller = new dreamer[c]();
                controller[callback](self, link, function() {
                    self._deselectAllNodes();
                    self._deselectAllLinks();
                    self.parent.removeLink.call(self, link.index);
                    success && success();
                }, error);
            } else {
                log('removeLink: callback undefined in model spec.');
                error && error("You can't remove a link, callback undefined.");
            }

        } else {
            //FIXME we need to manage alert in a different way: FAILBACK
            log("You can't delete the link");
            error && error("You can't delete the link");
        }


    };


    ModelGraphEditor.prototype.savePositions = function(data) {
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
    ModelGraphEditor.prototype._setupBehaviorsOnEvents = function(layer) {
        log("_setupBehaviorsOnEvents");
        var self = this;
        var contextmenuNodesAction = [{
            title: 'Show graph',
            action: function(elm, c_node, i) {
                if (c_node.info.type != undefined) {
                    var current_layer_nodes = Object.keys(self.model.layer[self.getCurrentView()].nodes);
                    if (current_layer_nodes.indexOf(c_node.info.type) >= 0) {
                        if (self.model.layer[self.getCurrentView()].nodes[c_node.info.type].expands) {
                            var new_layer = self.model.layer[self.getCurrentView()].nodes[c_node.info.type].expands;
                            self.handleFiltersParams({
                                node: {
                                    type: Object.keys(self.model.layer[new_layer].nodes),
                                    group: [c_node.id]
                                },
                                link: {
                                    group: [c_node.id],
                                    view: [new_layer]
                                }
                            });

                        }
                    }
                }
            }
        }, {
            title: 'Edit',
            action: function(elm, d, i) {
                if (d.info.type != undefined) {

                    //FIXME non va bene :)
                    window.location.href = '/projects/' + self.project_id + '/descriptors/' + graph_editor.getCurrentView() + 'd/' + graph_editor.getCurrentGroup();
                }
            }

        }, {
            title: 'Delete',
            action: function(elm, d, i) {
                self.removeNode(d, null, showAlert);
            }

        }];
        if (self.model && self.model.layer && self.model.layer[layer] && self.model.layer[layer].action && self.model.layer[layer].action.node) {
            for (var i in self.model.layer[layer].action.node) {
                var action = self.model.layer[layer].action.node[i]
                contextmenuNodesAction.push({
                    title: action.title,
                    action: function(elm, d, i) {
                        var callback = action.callback;
                        var c = self.model.callback[callback].class;
                        var controller = new dreamer[c]();
                        var args = {
                            elm: elm,
                            d: d,
                            i: i
                        }

                        controller[callback](self, args);
                    }
                });
            }
        }
        var contextmenuLinksAction = [{
            title: 'Delete Link',
            action: function(elm, link, i) {
                self.removeLink(link);
            }

        }];
        if (self.model && self.model.layer && self.model.layer[layer] && self.model.layer[layer].action && self.model.layer[layer].action.link) {
            for (var i in self.model.layer[layer].action.link) {
                var action = self.model.layer[layer].action.link[i];
                contextmenuLinksAction.push({
                    title: action.title,
                    action: function(elm, link, i) {
                        var callback = action.callback;
                        var c = self.model.callback[callback].class;
                        var controller = new dreamer[c]();
                        var args = {
                            elm: elm,
                            link: link,
                            i: i
                        }

                        controller[callback](self, args);
                    }
                });
            }
        }

        this.behavioursOnEvents = {
            'nodes': {
                'click': function(d) {

                    d3.event.preventDefault();

                    if (self.lastKeyDown == SHIFT_BUTTON && self._selected_node != undefined) {
                        self.addLink(self._selected_node, d, null,showAlert);
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
                    log('dblclick');
                    if (c_node.info.type != undefined) {
                        var current_layer_nodes = Object.keys(self.model.layer[self.getCurrentView()].nodes);
                        if (current_layer_nodes.indexOf(c_node.info.type) >= 0) {
                            if (self.model.layer[self.getCurrentView()].nodes[c_node.info.type].expands) {
                                var new_layer = self.model.layer[self.getCurrentView()].nodes[c_node.info.type].expands;
                                self.handleFiltersParams({
                                    node: {
                                        type: Object.keys(self.model.layer[new_layer].nodes),
                                        group: [c_node.id]
                                    },
                                    link: {
                                        group: [c_node.id],
                                        view: [new_layer]
                                    }
                                });

                            }
                        }
                    }

                },
                'contextmenu': d3.contextMenu(contextmenuNodesAction)
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
                'contextmenu': d3.contextMenu(contextmenuLinksAction)
            }
        };

    };

    ModelGraphEditor.prototype.handleFiltersParams = function(filtersParams, notFireEvent) {
        this._setupBehaviorsOnEvents(filtersParams.link.view[0]);
        this.parent.handleFiltersParams.call(this, filtersParams, notFireEvent);
    };

    ModelGraphEditor.prototype.getAvailableNodes = function (){
        log('getAvailableNodes');
        log(this.model)
        if(this.model && this.model.layer[this.getCurrentView()] != undefined)
            return this.model.layer[this.getCurrentView()].nodes;
        return [];
    }


    ModelGraphEditor.prototype.exploreLayer = function(args) {

    };

    ModelGraphEditor.prototype.getTypeProperty = function() {
        return this.type_property;
    };

    ModelGraphEditor.prototype.getCurrentGroup = function() {
        return this.filter_parameters.node.group[0];

    }

    ModelGraphEditor.prototype.getCurrentView = function() {
        return this.filter_parameters.link.view[0];

    }
    /**
     * Log utility
     */
    function log(text) {
        if (DEBUG)
            console.log("::ModelGraphEditor::", text);
    }



    return ModelGraphEditor;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.ModelGraphEditor;
}
