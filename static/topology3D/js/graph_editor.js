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



    /**
     * Constructor
     */
    function GraphEditor(args) {
        log("Constructor");
        this.eventHandler = new EventHandler();
        this.lastKeyDown = -1;
        this._selected_node = undefined;
        this.filter_parameters = {
            node: {
                type : [],
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
            links: []
        };


    }



    GraphEditor.prototype.init = function(args){
        args = args || {}
        var self = this;
        this.width = args.width || 500;
        this.height = args.height || 500;
        this.forceSimulationActive = false;

        //FixMe
        this.width = this.width -this.width*0.007;
        this.height =  this.height - this.height*0.07;

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
            .force("charge", d3.forceManyBody().strength(-10))
            .force("link", d3.forceLink().distance(100).iterations(3).id(function(d) { return d.id; }))
            .force("center", d3.forceCenter(this.width / 2, this.height / 2));

        var zoom = d3.zoom().scaleExtent([min_zoom, max_zoom])

        var size = d3.scalePow().exponent(2)
            .domain([1, 100])
            .range([8, 24]);

        this.svg = d3.select("#graph_ed_container").append("svg")
            .attr("id", "graph_svg")
            .attr("width", this.width)
            .attr("height", this.height);

        d3.select(window)
            .on('keydown', function() {
                log('keydown ' + d3.event.keyCode);
                //d3.event.preventDefault();
                if (self.lastKeyDown !== -1) return;
                self.lastKeyDown = d3.event.keyCode;
                if(self.lastKeyDown === CANC_BUTTON && self._selected_node != undefined){
                    self.removeNode(self._selected_node);
                }

            })
            .on('keyup', function() {
                log('keyup'+ self.lastKeyDown);
                self.lastKeyDown = -1;
            });


        d3.json("graph_data", function(error, data) {
            console.log(data)
            self.d3_graph.nodes = data.vertices;
            self.d3_graph.links = data.edges;
            self.refresh();
            self.startForce();
            setTimeout(function(){ self.handleForce(self.forceSimulationActive); }, 500);


        });

    }

    /**
     * Start or Stop force layout
     * @param {boolean} Required. Value true: start, false: stop
     * @returns {boolean}
     */
    GraphEditor.prototype.handleForce = function(start) {
        if(start)
            this.force.stop();
        this.forceSimulationActive = start;
        this.node.each(function(d) {
                d.fx = (start) ? null : d.x;
                d.fy = (start) ? null : d.y;
        });

        if(start)
            this.force.restart();

        this.eventHandler.fire("force_status_changed_on", start);
    };

    /**
     * Handle the parameters of basic filters: node type, view, group
     * @param {Object} Required.
     *
     */
    GraphEditor.prototype.handleFiltersParams = function(filtersParams) {
        this.filter_parameters = filtersParams;
        this.current_view_id = (this.filter_parameters.link.view[0] != undefined) ? this.filter_parameters.link.view[0] : current_view_id
        this.cleanAll();
        this.refresh();
        this.startForce();
        this.force.restart();
        this._deselectAllNodes();
        this.handleForce(this.forceSimulationActive);
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
            .selectAll(".line")
            .data(self.d3_graph.links
                .filter(this.link_filter_cb)
            )
            .enter().append("line")
            .attr("class", "link")
            .attr("class", "cleanable")
            .style("stroke-width", nominal_stroke)
            .style("stroke", function(d) {
                return default_link_color;
            });

        this.node = this.svg
            .selectAll(".node")
            .data(self.d3_graph.nodes
                .filter(this.node_filter_cb))
            .enter()
            .append("g")
            .attr("class", "node")
            .attr("class", "cleanable")
            .append("svg:path")
            .attr("class", "node_path")

        .attr("id", function(d) {
                return "path_" + d.id;
            })
            .attr("d", d3.symbol()
                .size(function(d) {
                    return Math.PI * Math.pow(self._node_property_by_type(d.info.type, 'size'), 2.2);
                })
                .type(function(d) {
                    return self._node_property_by_type(d.info.type, 'shape');
                })
            )
            .style("fill", function(d) {
                return self._node_property_by_type(d.info.type, 'color');
            })
            .attr("transform", function() {
                return "rotate(-45)";

            })
            .attr("stroke-width", 2.4)
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        this.node.on("contextmenu", self.behavioursOnEvents.nodes["contextmenu"])
            .on("mouseover",  self.behavioursOnEvents.nodes["mouseover"])
            .on("mouseout", self.behavioursOnEvents.nodes["mouseout"])
            .on('click', self.behavioursOnEvents.nodes["click"])
            .on('dblclick',self.behavioursOnEvents.nodes["dblclick"] );

        this.link
            .on("contextmenu", self.behavioursOnEvents.links["contextmenu"])
            .on("mouseover", self.behavioursOnEvents.links["mouseover"])
            .on("mouseout", self.behavioursOnEvents.links["mouseout"]);

        this.text = this.svg.selectAll(".text")
            .data(self.d3_graph.nodes
                .filter(this.node_filter_cb))
            .enter().append("text")
            .attr("class", "nodetext")
            .attr("class", "cleanable")
            .attr("dy", ".35em")
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
             if(self.forceSimulationActive){
                d.fx = null;
                d.fy = null;
            }else{
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

            self.link.attr("x1", function(d) {
                    return d.source.x;
                })
                .attr("y1", function(d) {
                    return d.source.y;
                })
                .attr("x2", function(d) {
                    return d.target.x;
                })
                .attr("y2", function(d) {
                    return d.target.y;
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
     *  Export Graph data.
     *  @returns {Object} Graph object.
     */
    GraphEditor.prototype.exportJSONGraph = function() {

    };

    /**
     *  Get the data tree of availables views
     *  @returns {Object} object.
     */
    GraphEditor.prototype.getTreeViews = function() {

    };

    /**
     *  Get the the type of Availables Nodes Of View
     *  @returns {Object} object.
     */
    GraphEditor.prototype.getAvailablesNodesOfView = function() {

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

    /**
     *  Remove all the graph objects from the view
     */
    GraphEditor.prototype.cleanAll = function() {
        this.svg.selectAll('.cleanable').remove();

    };

    /**
     *  Internal functions
     */

     GraphEditor.prototype._node_property_by_type = function(type, property){
        if(this.type_property[type] != undefined && this.type_property[type][property] != undefined)
            return this.type_property[type][property];
        else
            return this.type_property['unrecognized'][property];
     }

     /**
     *
     *
     *
     */
     GraphEditor.prototype._setupFiltersBehaviors = function(args) {

        var self = this;

        this.node_filter_cb = args.node_filter_cb || function(d) {
            var result = true;

            // check filter by node type
            if(self.filter_parameters.node.type.length > 0){
                if (self.filter_parameters.node.type.indexOf(d.info.type) < 0)
                    result = false;
            }

            // check filter by group
            if(self.filter_parameters.node.group.length > 0){
                if(self.filter_parameters.node.group.indexOf(d.info.group) < 0)
                    result = false;
            }

            return result;
        };

        this.link_filter_cb = args.link_filter_cb || function(d) {
            var result = true;
            // check filter by view
            if(self.filter_parameters.link.view.length > 0){
                if (self.filter_parameters.link.view.indexOf(d.view) < 0)
                    result = false;
            }

            // check filter by group
            if(self.filter_parameters.link.group.length > 0){
                if(self.filter_parameters.link.group.indexOf(d.group) < 0)
                    result = false;
            }

            return result;
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
                'dblclick': function(d) {
                    d3.event.preventDefault();
                    log('dblclick');
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

    /**
     *  Select node in exclusive mode
     *  @param {Object} Required. Element selected on click event
     */
    GraphEditor.prototype._selectNodeExclusive = function(node_instance, node_id) {
        log("_selectNodeExclusive " );
        var activeClass = "node_selected";
        var alreadyIsActive = d3.select(node_instance).classed(activeClass);
        this._deselectAllNodes();
        d3.select(node_instance).classed(activeClass, !alreadyIsActive);
        this._selected_node = (alreadyIsActive) ? undefined : node_instance.__data__;
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