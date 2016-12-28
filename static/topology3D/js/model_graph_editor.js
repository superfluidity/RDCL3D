if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.ManoGraphEditor = (function(global) {
    'use strict';

    var DEBUG = true;
    var SHIFT_BUTTON = 16;
    var IMAGE_PATH = "/static/assets/img/";
    var GUI_VERSION = "v1";


    ManoGraphEditor.prototype = new dreamer.GraphEditor();
    ManoGraphEditor.prototype.constructor = ManoGraphEditor;
    ManoGraphEditor.prototype.parent = dreamer.GraphEditor.prototype;

    /**
     * Constructor
     */
    function ManoGraphEditor(args) {

        log("Constructor");

    }


    //TODO this should be moved in graph_editor
    ManoGraphEditor.prototype.init = function(args) {
        this.parent.init.call(this, args);
        this.current_vnffg = null;

        if (args.gui_properties[GUI_VERSION]!= undefined) {
            args.gui_properties = args.gui_properties[GUI_VERSION];
        }

        this.type_property = {};
        this.type_property["unrecognized"] = args.gui_properties["default"];
        this.type_property["unrecognized"]["default_node_label_color"] = args.gui_properties["default"]["label_color"];
        //this.type_property["unrecognized"]["shape"] = d3.symbolCross;

        Object.keys(args.gui_properties["nodes"]).forEach(function(key, index) {
            //console.log(key);
            this.type_property[key] = args.gui_properties["nodes"][key];
            this.type_property[key]["shape"] = this.parent.get_d3_symbol(this.type_property[key]["shape"]);
            if (this.type_property[key]["image"] != undefined ) {
                this.type_property[key]["image"] = IMAGE_PATH + this.type_property[key]["image"];
            }
            

        }, this);
        var self = this;
        d3.json("graph_data/", function(error, data) {
            //console.log(data)
            self.d3_graph.nodes = data.vertices;
            self.d3_graph.links = data.edges;
            self.d3_graph.graph_parameters = data.graph_parameters;
            //console.log(data.graph_parameters)
            self.model = data.model;
            self.refreshGraphParameters();
            self.refresh();
            self.startForce();
            setTimeout(function() {
                self.handleForce(self.forceSimulationActive);
            }, 500);

        });
    }

    /**
     * Add a new node to the graph.
     * @param {Object} Required. An object that specifies tha data of the new node.
     * @returns {boolean}
     */
    ManoGraphEditor.prototype.addNode = function(args, success, error) {
        var self = this;
        if (args.info.type === 'vnf') {
            if (args.existing_vnf) {
                new dreamer.GraphRequests().addNode(args, null, function() {
                    self.parent.addNode.call(self, args);
                    if (success)
                        success();
                });
            } else {
                new dreamer.GraphRequests().addNode(args, null, function() {
                    self.parent.addNode.call(self, args);
                    var vnf_ext_cp = {
                        'id': 'vnf_ext_cp' + "_" + args.id,
                        'info': {
                            'type': 'vnf_ext_cp',
                            'group': [args.id]
                        },
                        'x': args.x,
                        'y': args.y
                    }
                    new dreamer.GraphRequests().addNode(vnf_ext_cp, null, function() {
                        self.parent.addNode.call(self, vnf_ext_cp);
                        if (success)
                            success();
                    });
                });
            }
        } else if (args.info.type === 'vnf_vdu') {
            new dreamer.GraphRequests().addNode(args, null, function() {
                self.parent.addNode.call(self, args);
                var vdu_id = args.id;
                var vnf_vdu_cp = {
                    'id': 'vnf_vdu_cp' + "_" + generateUID(),
                    'info': {
                        'type': 'vnf_vdu_cp',
                        'group': [args.info.group[0]]
                    },
                    'x': args.x - (args.x * 0.1),
                    'y': args.y - (args.y * 0.1)
                }
                new dreamer.GraphRequests().addNode(vnf_vdu_cp, vdu_id, function() {
                    self.parent.addNode.call(self, vnf_vdu_cp);
                    var link = {
                        source: args.id,
                        target: vnf_vdu_cp.id,
                        view: self.filter_parameters.link.view[0],
                        group: [args.info.group[0]],
                    };
                    self.parent.addLink.call(self, link);
                    if (success)
                        success();
                });

            });
        } else if (args.info.type === 'vnf_vdu_cp') {
            var vnf_id = args.info.group[0];
            var vnf_vdus = $.grep(this.d3_graph.nodes, function(e) {
                return (e.info.group.indexOf(vnf_id) >= 0 && e.info.type == 'vnf_vdu');
            });
            var self = this;
            if (success)
                success();
            if (typeof vnf_vdus == 'undefined' || vnf_vdus.length <= 0) {
                alert('You should add a VDU')
            } else {
                showChooserModal('Select the VDU to link', vnf_vdus, function(choice) {
                    new dreamer.GraphRequests().addNode(args, choice, function() {
                        self.parent.addNode.call(self, args);
                        var link = {
                            source: args.id,
                            target: choice,
                            view: self.filter_parameters.link.view[0],
                            group: [args.info.group[0]],
                        };

                        self.parent.addLink.call(self, link);

                        $('#modal_create_link_chooser').modal('hide');
                    });
                });
            }

        } else {
            new dreamer.GraphRequests().addNode(args, null, function() {
                self.parent.addNode.call(self, args);
                if (success)
                    success();
            });
        }
    };

    ManoGraphEditor.prototype.addVnffg = function(node_info, success) {
        var self = this;
        new dreamer.GraphRequests().addVnffg(node_info, function(result) {
            if (success)
                success();
            self.d3_graph.graph_parameters.vnffgIds.push(node_info.id)
            self.refreshGraphParameters();
        });
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
        console.log('REMOVEEEEEEEEEEEEEE NODEEEEEEEEEEE')
        var self = this;
        if (node.info.type === 'vnf_vdu') {
            var vdu_links = $.grep(this.d3_graph.links, function(e) {
                return (e.source.id == node.id || e.target.id == node.id) && (e.source.info.type == 'vnf_vdu_cp' || e.target.info.type == 'vnf_vdu_cp')
            });
            for (var i in vdu_links) {
                var cp_node = vdu_links[i].source.info.type == 'vnf_vdu_cp' ? vdu_links[i].source : vdu_links[i].target;
                self.parent.removeNode.call(self, cp_node);
            }
            new dreamer.GraphRequests().removeNode(node, null, function() {
                self.parent.removeNode.call(self, node);
            });
        } else if (node.info.type === 'vnf_vdu_cp') {
            var vdu_links = $.grep(this.d3_graph.links, function(e) {
                return (e.source.id == node.id || e.target.id == node.id) && (e.source.info.type == 'vnf_vdu' || e.target.info.type == 'vnf_vdu')
            });
            var vdu_id = vdu_links[0].source.info.type == 'vnf_vdu' ? vdu_links[0].source.id : vdu_links[0].target.id;
            console.log(vdu_id)
            new dreamer.GraphRequests().removeNode(node, vdu_id, function() {
                self.parent.removeNode.call(self, node);
            });
        } else {
            new dreamer.GraphRequests().removeNode(node, null, function() {
                self.parent.removeNode.call(self, node);
            });
        }
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
            group: this.filter_parameters.link.group,
        };
        var source_type = s.info.type;
        var destination_type = d.info.type;
        if ((source_type == 'ns_vl' && destination_type == 'ns_cp') || (source_type == 'ns_cp' && destination_type == 'ns_vl')) {
            var cp_id = source_type == 'ns_cp' ? source_id : target_id;
            var old_link = $.grep(this.d3_graph.links, function(e) {
                return (e.source.id == cp_id || e.target.id == cp_id);
            });
            var self = this;
            new dreamer.GraphRequests().addLink(s, d, null, function() {
                self._deselectAllNodes();
                if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                    self.removeLink(old_link[0].index);
                }
                self.parent.addLink.call(self, link);
            });
        } else if ((source_type == 'ns_vl' && destination_type == 'vnf') || (source_type == 'vnf' && destination_type == 'ns_vl')) {
            var vnf_id = source_type == 'vnf' ? source_id : target_id;
            var vnf_ext_cps = $.grep(this.d3_graph.nodes, function(e) {
                return (e.info.group == vnf_id && e.info.type == 'vnf_ext_cp');
            });
            var self = this;
            showChooserModal('Select the VNF EXT CP of the VNF', vnf_ext_cps, function(choice) {
                new dreamer.GraphRequests().addLink(s, d, choice, function() {
                    self._deselectAllNodes();
                    self.parent.addLink.call(self, link);
                    $('#modal_create_link_chooser').modal('hide');
                });
            });

        } else if ((source_type == 'ns_cp' && destination_type == 'vnf') || (source_type == 'vnf' && destination_type == 'ns_cp')) {
            var vnf_id = source_type == 'vnf' ? source_id : target_id;
            var ns_cp_id = source_type == 'ns_cp' ? source_id : target_id;
            var vnf_ext_cps = $.grep(this.d3_graph.nodes, function(e) {
                return (e.info.group == vnf_id && e.info.type == 'vnf_ext_cp');
            });
            var old_link = $.grep(this.d3_graph.links, function(e) {
                return (e.source.id == ns_cp_id || e.target.id == ns_cp_id);
            });
            var self = this;
            showChooserModal('Select the VNF EXT CP of the VNF', vnf_ext_cps, function(choice) {
                new dreamer.GraphRequests().addLink(s, d, choice, function() {
                    if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                        self.removeLink(old_link[0].index);
                    }
                    self._deselectAllNodes();
                    self.parent.addLink.call(self, link);
                    $('#modal_create_link_chooser').modal('hide');
                });
            });

        } else if ((source_type == 'vnf_vl' && destination_type == 'vnf_vdu_cp') || (source_type == 'vnf_vdu_cp' && destination_type == 'vnf_vl')) {
            var vnf_vdu_cp_id = source_type == 'vnf_vdu_cp' ? source_id : target_id;
            var vdu_links = $.grep(this.d3_graph.links, function(e) {
                return (e.source.id == vnf_vdu_cp_id || e.target.id == vnf_vdu_cp_id) && (e.source.info.type == 'vnf_vdu' || e.target.info.type == 'vnf_vdu')
            });
            var vdu_id = vdu_links[0].source.info.type == 'vnf_vdu' ? vdu_links[0].source.id : vdu_links[0].target.id;
            var old_link = $.grep(this.d3_graph.links, function(e) {
                return (e.source.id == vnf_vdu_cp_id || e.target.id == vnf_vdu_cp_id) && (e.source.info.type == 'vnf_vl' || e.target.info.type == 'vnf_vl')
            });

            var self = this;
            new dreamer.GraphRequests().addLink(s, d, vdu_id, function() {
                self._deselectAllNodes();
                if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                    self.removeLink(old_link[0].index);
                }
                self.parent.addLink.call(self, link);
            });
        } else if ((source_type == 'vnf_ext_cp' && destination_type == 'vnf_vl') || (source_type == 'vnf_vl' && destination_type == 'vnf_ext_cp')) {
            var self = this;
            var vnf_ext_cp_id = source_type == 'vnf_ext_cp' ? source_id : target_id;
            var old_link = $.grep(this.d3_graph.links, function(e) {
                return (e.source.id == vnf_ext_cp_id || e.target.id == vnf_ext_cp_id);
            });
            new dreamer.GraphRequests().addLink(s, d, null, function() {
                self._deselectAllNodes();
                if (typeof old_link !== 'undefined' && old_link.length > 0 && old_link[0].index !== 'undefined') {
                    self.removeLink(old_link[0].index);
                }
                self.parent.addLink.call(self, link);
            });
        } else {
            alert("You can't link a " + source_type + " with a " + destination_type);
        }
    };

    /**
     * Remove a link from graph.
     * @param {String} Required. The identifier of link to remove.
     * @returns {boolean}
     */
    ManoGraphEditor.prototype.removeLink = function(link) {
        var s = link.source;
        var d = link.target;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        if ((source_type == 'vnf_vdu' && destination_type == 'vnf_vdu_cp') || (source_type == 'vnf_vdu_cp' && destination_type == 'vnf_vdu')) {
            alert('You should delete the VDU CP')
        } else {
            var self = this;
            new dreamer.GraphRequests().removeLink(s, d, function() {
                self._deselectAllNodes();
                self._deselectAllLinks();
                self.parent.removeLink.call(self, link.index);
            });
        }

    };


    ManoGraphEditor.prototype.savePositions = function(data) {
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
                    if (c_node.info.type != undefined) {
                        var current_layer_nodes = Object.keys(self.model.layer[self.getCurrentView()].nodes);
                        if(current_layer_nodes.indexOf(c_node.info.type) >= 0 ){
                            console.log(self.model.layer[self.getCurrentView()].nodes[c_node.info.type].expands)
                            if(self.model.layer[self.getCurrentView()].nodes[c_node.info.type].expands){
                                var new_layer = self.model.layer[self.getCurrentView()].nodes[c_node.info.type].expands;
                                console.log(Object.keys(self.model.layer[new_layer].nodes))
                                self.handleFiltersParams({
                                node: {
                                    type: Object.keys(self.model.layer[new_layer].nodes),
                                    group: [c_node.id]
                                },
                                link: {
                                    group: [c_node.id],
                                    view: [c_node.info.type ]
                                }
                            });

                            }
                        }
                    }

                },
                'contextmenu': d3.contextMenu([{
                    title: 'Show graph',
                    action: function(elm, d, i) {
                        if (d.info.type != undefined) {
                            if (d.info.type == 'vnf')
                                self.handleFiltersParams({
                                    node: {
                                        type: ['vnf_vl', 'vnf_ext_cp', 'vnf_vdu_cp', 'vnf_vdu'],
                                        group: [d.id]
                                    },
                                    link: {
                                        group: [d.id],
                                        view: ['vnf']
                                    }
                                });

                        }
                    }
                }, {
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

                }, {
                    title: 'Add to current VNFFG',
                    action: function(elm, d, i) {
                        if (self.current_vnffg && self.getCurrentView() == 'ns' && d.info.group.indexOf(self.current_vnffg) < 0) {
                            d.vnffgId = self.current_vnffg;
                            new dreamer.GraphRequests().addNodeToVnffg(d, function(result) {
                                d.info.group.push(self.current_vnffg)
                                var links = $.grep(self.d3_graph.links, function(e) {
                                    return (e.source.id == d.id || e.target.id == d.id);
                                });
                                for (var i in links) {
                                    console.log(links[i])
                                    if (links[i].source.info.group.indexOf(self.current_vnffg) >= 0 && links[i].target.info.group.indexOf(self.current_vnffg) >= 0) {
                                        links[i].group.push(self.current_vnffg)
                                    }
                                }
                                show_all_change();
                            });
                        }
                    }

                }, {
                    title: 'Delete',
                    action: function(elm, d, i) {
                        self.removeNode(d);
                    }

                }])
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

    ManoGraphEditor.prototype.exploreLayer = function(args) {

    };

    ManoGraphEditor.prototype.getTypeProperty = function() {
        return this.type_property;
    };

    ManoGraphEditor.prototype.getCurrentGroup = function() {
        return this.filter_parameters.node.group[0];

    }
    ManoGraphEditor.prototype.getCurrentView = function() {
        return this.filter_parameters.link.view[0];

    }
    ManoGraphEditor.prototype.refreshGraphParameters = function() {
        setVnffgIds(this.d3_graph.graph_parameters.vnffgIds)
    }
    ManoGraphEditor.prototype.getVnffgParameter = function() {
        return this.d3_graph.graph_parameters.vnffgIds;
    }

    ManoGraphEditor.prototype.handleVnffgParameter = function(vnffgId, class_name) {
        /*
        if(this.old_vnffg != null){
            var index = this.filter_parameters.node.group.indexOf(this.old_vnffg);
            if(index >= 0)
                this.filter_parameters.node.group.splice(index, 1);
            index = this.filter_parameters.link.group.indexOf(this.old_vnffg);
            if(index >= 0)
                this.filter_parameters.link.group.splice(index, 1);
        }
        if(vnffgId != "Global"){
            this.old_vnffg = vnffgId;
            this.filter_parameters.node.group.push(vnffgId);
            this.filter_parameters.link.group.push(vnffgId);

        }else{
            this.old_vnffg = null;
        }
        this.handleFiltersParams(this.filter_parameters, true);
        */

        if (vnffgId != "Global") {
            this.current_vnffg = vnffgId;
            this.setNodeClass(class_name, function(d) {
                var result = false;
                if (d.info.group.indexOf(vnffgId) < 0) {
                    result = true;
                }
                console.log(result);
                return result;
            });

            this.setLinkClass(class_name, function(d) {
                var result = false;
                if (d.group.indexOf(vnffgId) < 0) {
                    result = true;
                }
                console.log(result);
                return result;
            });

        } else {
            this.current_vnffg = null;
            this.setNodeClass(class_name, function(d) {
                var result = false;
                return result;
            });

            this.setLinkClass(class_name, function(d) {
                var result = false;
                return result;
            });
        }
    }


    /**
     * Log utility
     */
    function log(text) {
        if (DEBUG)
            console.log("::ModelGraphEditor::", text);
    }



    return ManoGraphEditor;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.ManoGraphEditor;
}