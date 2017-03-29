/*
   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni

   Licensed under the Apache License, Version 2.0 (the "License");
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

dreamer.GraphEditor = (function(global) {
    'use strict';

    var DEBUG = true;
    var SHIFT_BUTTON = 16;
    var CANC_BUTTON = 46;
    var default_link_color = "#888";
    var nominal_text_size = 15;
    var nominal_stroke = 1.5;
    var EventHandler = dreamer.Event;
    //    var IMAGE_PATH = "/static/assets/img/";



    /**
     * Constructor
     */
    function GraphEditor(args) {
        log("Constructor");
        this.eventHandler = new EventHandler();
        this.lastKeyDown = -1;
        this._selected_node = undefined;
        this._selected_link = undefined;
        this._edit_mode = true;
        this.filter_parameters = {
            node: {
                type: [],
                group: [],
            },
            link: {
                group: [],
                view: [],
            }
        };
        this.current_view_id = '';
        // graph data initailization
        this.d3_graph = {
            nodes: [],
            links: [],
            graph_parameters: {}

        };


    }



    GraphEditor.prototype.init = function(args) {
        args = args || {}
        var self = this;
        this.width = args.width || 500;
        this.height = args.height || 500;
        this.forceSimulationActive = false;

        //FixMe
        this.width = this.width - this.width * 0.007;
        this.height = this.height - this.height * 0.07;

        var min_zoom = 0.1;
        var max_zoom = 7;
        this._setupBehaviorsOnEvents();
        this._setupFiltersBehaviors(args);

        this.type_property = {
            "unrecognized": {
                "shape": d3.symbolCircle,
                "color": "white",
                "node_label_color": "black",
                "size": 15
            },
        };

        this.force = d3.forceSimulation()
            .force("collide", d3.forceCollide().radius(40))
            .force("link", d3.forceLink().distance(80).iterations(1).id(function(d) {
                return d.id;
            }))
            .force("center", d3.forceCenter(this.width / 2, this.height / 2));

        var zoom = d3.zoom().scaleExtent([min_zoom, max_zoom])

        var size = d3.scalePow().exponent(2)
            .domain([1, 100])
            .range([8, 24]);

        this.svg = d3.select("#graph_ed_container").append("svg")
            .attr("id", "graph_svg")
            .attr("width", this.width)
            .attr("height", this.height);

        //End Arrow style
        this.svg.append("svg:defs").selectAll("marker")
            .data(["end"])      // Different link/path types can be defined here
            .enter().append("svg:marker")    // This section adds in the arrows
            .attr("id", String)
            .attr("viewBox", "-5 -5 10 10")
            .attr("refX", 13) /*must be smarter way to calculate shift*/
            .attr("refY", 0)
            .attr("markerUnits", "userSpaceOnUse")
            .attr("markerWidth", 12)
            .attr("markerHeight", 12)
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M 0,0 m -5,-5 L 5,0 L -5,5 Z")
            .attr('fill', default_link_color);

        d3.select(window)
            .on('keydown', function() {
                log('keydown ' + d3.event.keyCode);
                //d3.event.preventDefault();
                if (self.lastKeyDown !== -1) return;
                self.lastKeyDown = d3.event.keyCode;
                if (self.lastKeyDown === CANC_BUTTON && self._selected_node != undefined) {
                    self.removeNode(self._selected_node);
                } else if (self.lastKeyDown === CANC_BUTTON && self._selected_link != undefined) {
                    self.removeLink(self._selected_link);
                }

            })
            .on('keyup', function() {
                log('keyup' + self.lastKeyDown);
                self.lastKeyDown = -1;
            });


    }

    GraphEditor.prototype.get_d3_symbol =
        function(myString) {
            log(myString)
            switch (myString) {
                case "circle":
                    return d3.symbolCircle;
                    break;
                case "square":
                    return d3.symbolSquare;
                    break;
                case "diamond":
                    return d3.symbolDiamond;
                    break;
                case "triangle":
                    return d3.symbolTriangle;
                    break;
                case "star":
                    return d3.symbolStar;
                    break;
                case "cross":
                    return d3.symbolCross;
                    break;
                default:
                    // if the string is not recognized
                    return d3.symbolCross;
                    //return d3.symbolCircleUnknown;
            }

        }

    /**
     * Start or Stop force layout
     * @param {boolean} Required. Value true: start, false: stop
     * @returns {boolean}
     */
    GraphEditor.prototype.handleForce = function(start) {
        if (start)
            this.force.stop();
        this.forceSimulationActive = start;
        this.node.each(function(d) {
            d.fx = (start) ? null : d.x;
            d.fy = (start) ? null : d.y;
        });

        if (start)
            this.force.restart();

        this.eventHandler.fire("force_status_changed_on", start);
    };

    /**
     * Handle the parameters of basic filters: node type, view, group
     * @param {Object} Required.
     *
     */
    GraphEditor.prototype.handleFiltersParams = function(filtersParams, notFireEvent) {

        this.filter_parameters = (filtersParams) ? filtersParams : this.filter_parameters;
        this.current_view_id = (this.filter_parameters != undefined && this.filter_parameters.link.view[0] != undefined) ? this.filter_parameters.link.view[0] : this.current_view_id
        this.cleanAll();
        this.refresh();
        this.startForce();
        this.force.restart();
        this._deselectAllNodes();
        this.handleForce(this.forceSimulationActive);
        if (!notFireEvent)
            this.eventHandler.fire("filters_changed", filtersParams);

    };

    /**
     * Add a new node to the graph.
     * @param {Object} Required. An object that specifies tha data of the new node.
     * @returns {boolean}
     */
    GraphEditor.prototype.addNode = function(args) {
        if (args.id && args.info && args.info.type) {
            args.fixed = true;
            this.force.stop();
            this.cleanAll();
            this.d3_graph.nodes.push(args);
            this.refresh();
            this.startForce();
            this.force.restart();
            this.handleForce(this.forceSimulationActive);
            return true;
        }

        return false;

    };

    /**
     * Update the data properties of the node
     * @param {Object} Required. An object that specifies tha data of the node.
     * @returns {boolean}
     */
    GraphEditor.prototype.updateDataNode = function(args) {

    };

    /**
     * Remove a node from graph and related links.
     * @param {String} Required. Id of node to remove.
     * @returns {boolean}
     */
    GraphEditor.prototype.removeNode = function(node) {
        if (node != undefined) {
            var node_id = node.id;
            this.d3_graph['nodes'].forEach(function(n, index, object) {
                if (n.id == node_id) {
                    object.splice(index, 1);

                }

            });
            //TODO trovare una metodo piu efficace
            var self = this;
            var links_to_remove = [];
            this.d3_graph['links'].forEach(function(l, index, object) {
                if (node_id === l.source.id || node_id === l.target.id) {
                    links_to_remove.push(index);
                }

            });
            var links_removed = 0;
            links_to_remove.forEach(function(l_index) {
                self.d3_graph['links'].splice(l_index - links_removed, 1);
                links_removed++;
            });
            this.cleanAll();
            this.refresh();
            this.startForce();
            this.force.restart();

            return true;
        }
        return false;
    };


    /**
     * Add a new link to graph.
     * @param {Object} Required. An object that specifies tha data of the new Link.
     * @returns {boolean}
     */
    GraphEditor.prototype.addLink = function(link) {
        if (link.source && link.target) {
            this.force.stop();
            this.cleanAll();
            this.d3_graph.links.push(link);
            this.refresh();
            this.startForce();
            this.force.restart();
            return true;
        }

        return false;
    };

    /**
     * Remove a link from graph.
     * @param {String} Required. The identifier of link to remove.
     * @returns {boolean}
     */
    GraphEditor.prototype.removeLink = function(link_id) {
        var self = this;
        if (link_id !== 'undefined') {
            this.d3_graph['links'].forEach(function(l, index, object) {
                if (link_id === l.index) {
                    object.splice(index, 1);

                    self.cleanAll();
                    self.refresh();
                    self.startForce();
                    self.force.restart();
                    return true;
                }

            });
        }

        return false;
    };


    /**
     * Force a refresh of GraphView
     * @returns {}
     */
    GraphEditor.prototype.refresh = function() {

        //log(data)
        var self = this;

        this.link = this.svg
            .selectAll()
            .data(self.d3_graph.links
                .filter(this.link_filter_cb)
            )
            .enter().append("g")
            .attr("class", "link cleanable")
            .append("path")
            .attr("class", "link")
            .attr("class", "cleanable")
            .style("stroke-width", nominal_stroke)
            .style("stroke", function(d) {
                return default_link_color;
            })
            .attr("marker-end",function(d) {return (d.directed_edge ? "url(#end)" : ''); });

        this.nodeContainer = this.svg
            .selectAll()
            .data(self.d3_graph.nodes
                .filter(this.node_filter_cb))
            .enter()
            .append("g")
            // .attr("class", "nodosdads")
            .attr("class", "node cleanable");

        this.svg.selectAll('.node')
            .data(self.d3_graph.nodes
                .filter(this.node_filter_cb))

            .filter(function(d) {
                return (d.info.type == undefined) || (self._node_property_by_type(d.info.type, 'image') == undefined)
            })

            .append("svg:path")
            .attr("d", d3.symbol()
                .size(function(d) {
                    return Math.PI * Math.pow(self._node_property_by_type(d.info.type, 'size'), 2) / 4;
                })
                .type(function(d) {
                    return (self._node_property_by_type(d.info.type, 'shape'));
                })
            )
            .style("fill", function(d) {
                return self._node_property_by_type(d.info.type, 'color');
            })
            .attr("transform", function() {
                return "rotate(-45)";

            })
            .attr("stroke-width", 2.4)

            .attr("class", "node_path")
            .attr("id", function(d) {
                return "path_" + d.id;
            })

            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        var figure_node = this.svg.selectAll('.node')
            .data(self.d3_graph.nodes
                .filter(this.node_filter_cb))

            .filter(function(d) {
                return self._node_property_by_type(d.info.type, 'image') != undefined
            });

            figure_node.append("svg:image")
            .attr("xlink:href", function(d) {
                return self._node_property_by_type(d.info.type, 'image')
            })
            .attr("x", function(d) {
                return -self._node_property_by_type(d.info.type, 'size') / 2
            })
            .attr("y", function(d) {
                return -self._node_property_by_type(d.info.type, 'size') / 2
            })
            .attr("width", function(d) {
                return self._node_property_by_type(d.info.type, 'size')
            })
            .attr("height", function(d) {
                return self._node_property_by_type(d.info.type, 'size')
            })
            .style("stroke", "black")
            .style("stroke-width", "1px")

            .attr("class", "node_path")
            .attr("id", function(d) {
                return "path_" + d.id;
            })
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

            figure_node.append("svg:path")
            .attr("d", d3.symbol()
                .size(function(d) {
                    return Math.PI * Math.pow(self._node_property_by_type(d.info.type, 'size') + 7 , 2) / 4;
                })
                .type(function(d) {
                    return (self.get_d3_symbol('circle'));
                })
            )
            .style("fill", 'transparent')
            .attr("transform", function() {
                return "rotate(-45)";

            })
            .attr("stroke-width", 2.4)

            .attr("class", "hidden_circle")
            .attr("id", function(d) {
                return "path_" + d.id;
            })

            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));



        this.node = this.svg.selectAll('.node')
            .data(self.d3_graph.nodes
                .filter(this.node_filter_cb)).selectAll("image, path, circle");



        this.node.on("contextmenu", self.behavioursOnEvents.nodes["contextmenu"])
            .on("mouseover", self.behavioursOnEvents.nodes["mouseover"])
            .on("mouseout", self.behavioursOnEvents.nodes["mouseout"])
            .on('click', self.behavioursOnEvents.nodes["click"])
            .on('dblclick', self.behavioursOnEvents.nodes["dblclick"]);

        this.link
            .on("contextmenu", self.behavioursOnEvents.links["contextmenu"])
            .on("mouseover", self.behavioursOnEvents.links["mouseover"])
            .on('click', self.behavioursOnEvents.links["click"])
            .on("mouseout", self.behavioursOnEvents.links["mouseout"]);



        this.text = this.svg.selectAll(".node")
            .data(self.d3_graph.nodes
                .filter(this.node_filter_cb))
            .append("svg:text")
            .attr("class", "nodetext")
            .attr("class", "cleanable")
            .attr("dy", "-5")
            .attr("pointer-events", "none")
            .style("font-size", nominal_text_size + "px")
            .style("font-family", "Lucida Console")
            .style("fill", function(d) {
                return self._node_property_by_type(d.info.type, 'node_label_color');
            })
            .style("text-anchor", "middle")
            .text(function(d) {
                return d.id;
            });



        function dragstarted(d) {
            d.draggednode = true;
            if (!d3.event.active) self.force.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;

        }

        function dragged(d) {
            d.fx = d3.event.x;
            d.fy = d3.event.y;
        }

        function dragended(d) {
            d.draggednode = false;
            if (!d3.event.active) self.force.alphaTarget(0);
            if (self.forceSimulationActive) {
                d.fx = null;
                d.fy = null;
            } else {
                d.fx = d.x;
                d.fy = d.y;
                self.force.stop();
                self.forceSimulationActive = false;
            }
        }


    };

    /**
     *  Start force layout on Graph.
     *
     */
    GraphEditor.prototype.startForce = function() {
        //this.force.stop();
        var self = this
        this.force
            .nodes(this.d3_graph.nodes)
            .on("tick", ticked);


        this.force
            .force("link")
            .links(this.d3_graph.links);

        function ticked() {
            self.node.attr("cx", function(d) {
                    return d.x = Math.max(self._node_property_by_type(d.info.type, 'size'), Math.min(self.width - self._node_property_by_type(d.info.type, 'size'), d.x));
                })
                .attr("cy", function(d) {
                    return d.y = Math.max(self._node_property_by_type(d.info.type, 'size'), Math.min(self.height - self._node_property_by_type(d.info.type, 'size'), d.y));
                });

            self.link.attr("d", function(d) {
                var dx = d.target.x - d.source.x,
                    dy = d.target.y - d.source.y,
                    dr = Math.sqrt(dx * dx + dy * dy);
                return "M" + d.source.x + "," + d.source.y + "," + d.target.x + "," + d.target.y;
            });

            self.node.attr("transform", function(d) {
                return "translate(" + d.x + "," + d.y + ")";
            });
            self.text.attr("transform", function(d) {
                var label_pos_y = d.y + self._node_property_by_type(d.info.type, 'size') + 10;
                return "translate(" + d.x + "," + label_pos_y + ")";
            });
        };



    };

    /**
     * This method attaches an event handler.
     * @param {String} Required. A String that specifies the name of the event.
     * @param {Function} Required. Specifies the function to run when the event occurs.
     * @returns {}
     */
    GraphEditor.prototype.addListener = function(event_name, cb) {
        this.eventHandler.addL(event_name, cb);
    }

    /**
     * This method removes an event handler that has been attached with the addListener() method.
     * @param {String} Required. A String that specifies the name of the event to remove.
     * @param {Function} Required. Specifies the function to remove.
     * @returns {}
     */
    GraphEditor.prototype.removeListener = function(event_name, cb) {

    }


    GraphEditor.prototype.setNodeClass = function(class_name, filter_cb) {
        log("setNodeClass");
        var self = this;
        this.svg.selectAll('.node').classed(class_name, false);
        this.svg.selectAll('.node')
            .classed(class_name, filter_cb);
    }

    GraphEditor.prototype.setLinkClass = function(class_name, filter_cb) {
        log("setLinkClass");
        var self = this;
        this.svg.selectAll('.link').classed(class_name, false);
        this.svg.selectAll('.link')
            .classed(class_name, filter_cb);
    }

    /**
     *  Remove all the graph objects from the view
     */
    GraphEditor.prototype.cleanAll = function() {
        this.svg.selectAll('.cleanable').remove();

    };

    /**
     *  Internal functions
     */

    GraphEditor.prototype._node_property_by_type = function(type, property) {
        //log(type + "-" + property)
        if (this.type_property[type] != undefined && this.type_property[type][property] != undefined){
            //if(property == "shape")
            //    log("dentro" + this.type_property[type][property])
            return this.type_property[type][property];
            }
        else{
            return this.type_property['unrecognized'][property];
        }

    }

    /**
     *
     *
     *
     */
    GraphEditor.prototype._setupFiltersBehaviors = function(args) {

        var self = this;

        this.node_filter_cb = args.node_filter_cb || function(d) {

            var cond_view = true,
                cond_group = true;
            //log(d.info.type + " " + self.filter_parameters.node.type + " group: " + self.filter_parameters.node.group + "- " + d.info.group)
            // check filter by node type
            if (self.filter_parameters.node.type.length > 0) {

                if (self.filter_parameters.node.type.indexOf(d.info.type) < 0)
                    cond_view = false;
            }

            // check filter by group
            if (self.filter_parameters.node.group.length > 0) {
                self.filter_parameters.node.group.forEach(function(group) {
                    if (d.info.group.indexOf(group) < 0)
                        cond_group = false;
                });


            }


            return cond_view && cond_group;
        };

        this.link_filter_cb = args.link_filter_cb || function(d) {
            var cond_view = true,
                cond_group = true;

            // check filter by view
            if (self.filter_parameters.link.view.length > 0) {
                self.filter_parameters.link.view.forEach(function(view) {
                    if (d.view.indexOf(view) < 0)
                        cond_view = false;
                });
            }

            // check filter by group
            if (self.filter_parameters.link.group.length > 0) {
                self.filter_parameters.link.group.forEach(function(group) {
                    if (d.group.indexOf(group) < 0)
                        cond_group = false;
                });
            }
            return cond_view && cond_group;
        };

    };

    /**
     *
     *
     */
    GraphEditor.prototype._setupBehaviorsOnEvents = function() {
        log("_setupBehaviorsOnEvents");
        var self = this;
        this.behavioursOnEvents = {
            'nodes': {
                'click': function(d) {
                    d3.event.preventDefault();
                    log('click', d);
                    if (self.lastKeyDown == SHIFT_BUTTON && self._selected_node != undefined) {
                        var source_id = self._selected_node.id;
                        var target_id = d.id;
                        log(JSON.stringify(self.filter_parameters.link.view));
                        var new_link = {
                            source: source_id,
                            target: target_id,
                            view: self.filter_parameters.link.view[0],
                            group: self.filter_parameters.link.group[0],
                        };
                        self.addLink(new_link);
                        self._deselectAllNodes();
                    } else {
                        self._selectNodeExclusive(this, d);
                    }

                },
                'mouseover': function(d) {

                },
                'mouseout': function(d) {},
                'dblclick': function(d) {
                    d3.event.preventDefault();
                    log('dblclick');
                },
                'contextmenu': function(d, i) {
                    d3.event.preventDefault();
                    log("contextmenu node");
                    self.eventHandler.fire("right_click_node", d);
                }
            },
            'links': {
                'click': function(event) {

                },
                'dblclick': function(event) {

                }
            }
        };
    };

    /**
     *  Deselect previously selected nodes
     *
     */
    GraphEditor.prototype._deselectAllNodes = function() {
        log("_deselectAllNodes");
        this.node.classed("node_selected", false);
        this._selected_node = undefined;
    };

    GraphEditor.prototype._deselectAllLinks = function() {
        log("_deselectAllLinks");
        this.link.classed("link_selected", false).style('stroke-width', 2);
        this._selected_link = undefined;
    };
    /**
     *  Select node in exclusive mode
     *  @param {Object} Required. Element selected on click event
     */
    GraphEditor.prototype._selectNodeExclusive = function(node_instance, node_id) {
        log("_selectNodeExclusive ");
        var activeClass = "node_selected";
        var alreadyIsActive = d3.select(node_instance).classed(activeClass);
        this._deselectAllNodes();
        this._deselectAllLinks();
        d3.select(node_instance).classed(activeClass, !alreadyIsActive);
        this._selected_node = (alreadyIsActive) ? undefined : node_instance.__data__;
    };

    /**
     *  Select node in exclusive mode
     *  @param {Object} Required. Element selected on click event
     */
    GraphEditor.prototype._selectLinkExclusive = function(link_instance, link_id) {
        log("_selectLinkExclusive ");
        var activeClass = "link_selected";
        var alreadyIsActive = d3.select(link_instance).classed(activeClass);
        this._deselectAllNodes();
        this._deselectAllLinks();
        d3.select(link_instance).classed(activeClass, !alreadyIsActive);
        d3.select(link_instance).style('stroke-width', 4)
        this._selected_link = link_instance.__data__;
    };

    /**
     *  Callback to resize SVG element on window resize
     */
    GraphEditor.prototype.resizeSvg = function(width, height) {
        log("resizeSvg");
        log(event);
        this.width = width || this.width;
        this.height = height || this.height;
        this.svg.attr('width', width);
        this.svg.attr('height', height);

    }

    GraphEditor.prototype.refreshGraphParameters = function(graphParameters) {
        this.eventHandler.fire("refresh_graph_parameters", graphParameters);
    }

    /**
     * Log utility
     */
    function log(text) {
        if (DEBUG)
            console.log("::GraphEditor::", text);
    }



    return GraphEditor;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.GraphEditor;
}
