if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.GraphEditor = (function(global) {
    'use strict';

    var DEBUG = true;
    var SHIFT_BUTTON = 16;

    var default_node_label_color = "white";
    var default_link_color = "#888";
    var nominal_text_size = 15;
    var nominal_stroke = 1.5;
    var EventHandler = dreamer.Event;
    /*
    var default_node_properties = {
        "shape": d3.symbolCircle,
        "color": "white",
        "size": 15,
        "label_color": "white",
        "label_text_size": 15
    };*/


    /**
     * Constructor
     */
    function GraphEditor(args) {
        log("Constructor");
        this.eventHandler = new EventHandler();
        this.lastKeyDown = -1;
        this._selected_node = undefined;
        this.current_view_id = 'nsd'; //TODO change value
        // graph data initailization
        this.d3_graph = {
            nodes: [],
            links: []
        };
        /*

        */
    }

    GraphEditor.prototype.init = function(args){
        args = args || {}
        this.width = args.width || 500;
        this.height = args.height || 500;
        this.forceSimulationActive = true;

        var min_zoom = 0.1;
        var max_zoom = 7;


        this.node_filter_cb = args.node_filter_cb || function(d) {
            //log(d.info.type, d.info.type in ["vnf", "ns_cp", "ns_vl"], ["vnf", "ns_cp", "ns_vl"])
            if (["vnf", "ns_cp", "ns_vl"].indexOf(d.info.type) > -1)
                return true
            return false;
        };

        this.link_filter_cb = args.link_filter_cb || function(d) {
            return d.view == 'nsd';
        };

        this.type_property = {
            "unrecognized": {
                "shape": d3.symbolCircle,
                "color": "white",
                "size": 15
            },
            "ns_vl": {
                "shape": d3.symbolCircle,
                "color": "#196B90",
                "size": 15
            },
            "ns_cp": {
                "shape": d3.symbolCircle,
                "color": "#F27220",
                "size": 15
            },
            "vnf": {
                "shape": d3.symbolCircle,
                "color": "#54A698",
                "size": 15
            },
            "vnf_vl": {
                "shape": d3.symbolCircle,
                "color": "#313679",
                "size": 15
            },
            "vnfc_cp": {
                "shape": d3.symbolCircle,
                "color": "#343D41",
                "size": 15
            },
            "vnf_cp": {
                "shape": d3.symbolCircle,
                "color": "#4E6293",
                "size": 15
            },
            "vnfc": {
                "shape": d3.symbolCircle,
                "color": "#1D74C2",
                "size": 15
            },
            "vdu": {
                "shape": d3.symbolCircle,
                "color": "#4B7C91",
                "size": 15
            }
        };



        this.force = d3.forceSimulation()
            .force("link", d3.forceLink().distance(100).strength(3).id(function(d, i) {
                // log(d,i)
                return d.id;
            }))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(this.width / 2, this.height / 2));

        var self = this;
        // this.force.linkStrength(1);

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

            })
            .on('keyup', function() {
                log('keyup');
                self.lastKeyDown = -1;
            });



        d3.json("graph_data", function(error, data) {
            // if(error == false)

            self.d3_graph.nodes = data.vertices
            self.d3_graph.links = data.edges;


            self.refresh();
            self.startForce();
        });
    }

    /**
     * Start or Stop force layout
     * @param {boolean} Required. Value true: start, false: stop
     * @returns {boolean}
     */
    GraphEditor.prototype.handleForce = function(start) {
        if (start) {

            this.node.each(function(d) {
                d.fx= null;
                d.fy= null;
            });
            this.force.restart();
            this.forceSimulationActive = true;

        } else {

            this.force.stop();
            this.forceSimulationActive = false;
            this.node.each(function(d) {
                d.fx= d.x;
                d.fy= d.y;
            });

        }
    };


    /**
     * Add a new node to the graph.
     * @param {Object} Required. An object that specifies tha data of the new node.
     * @returns {boolean}
     */
    GraphEditor.prototype.addNode = function(args) {

        if (args.id && args.info && args.info.type) {
            this.force.stop();
            this.cleanAll();
            this.d3_graph.nodes.push(args);
            this.refresh();
            this.startForce();
            this.force.restart();
            //
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
    GraphEditor.prototype.removeNode = function(node_id) {
        if (node_id != undefined) {
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
        log("addLink")
        if (link.source && link.target) {
            this.d3_graph.links.push(link);

            this.cleanAll();
            this.refresh();
            this.startForce();
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
        if (link_id) {
            this.d3_graph['links'].forEach(function(l, index, object) {
                if (link_id === l.index) {
                    object.splice(index, 1);

                    self.cleanAll();
                    self.refresh();
                    self.startForce();
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
        //this.link.exit().remove();
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
                    return Math.PI * Math.pow(self.type_property[d.info.type].size, 2.2);
                })
                .type(function(d) {
                    return self.type_property[d.info.type].shape;
                })
            )
            .style("fill", function(d) {
                return self.type_property[d.info.type].color;
            })
            .attr("transform", function() {
                return "rotate(-45)";

            })
            .attr("stroke-width", 2.4)
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        this.node.on("contextmenu", function(d, i) {
                d3.event.preventDefault();
                log("contextmenu node");
                self.eventHandler.fire("right_click_node", d);

            })
            .on("mouseover", function(d) {
                self.link.style('stroke-width', function(l) {
                    if (d === l.source || d === l.target)
                        return 4;
                    else
                        return 2;
                });
            })
            .on("mouseout", function(d) {
                self.link.style('stroke-width', 2);
            })
            .on('click', function(d) {
                d3.event.preventDefault();
                console.log('click', d);
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

            })
            .on('dblclick', function(d) {
                d3.event.preventDefault();
                log('dblclick');
            });

        this.link
            .on("contextmenu", function(d, i) {
                d3.event.preventDefault();
                // react on right-clicking
                console.log("contextmenu link", d, i);
                self.removeLink(i);

            })
            .on("mouseover", function(d) {
                d3.select(this).style('stroke-width', 4);
            })
            .on("mouseout", function(d) {
                d3.select(this).style('stroke-width', 2);
            });

        this.text = this.svg.selectAll(".text")
            .data(self.d3_graph.nodes
                .filter(this.node_filter_cb))
            .enter().append("text")
            .attr("class", "nodetext")
            .attr("class", "cleanable")
            .attr("dy", ".35em")
            .attr("pointer-events", "none")
            .style("font-size", nominal_text_size + "px")
            .style("fill", default_node_label_color)
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
            self.node.attr("transform", function(d) {
                return "translate(" + d.x + "," + d.y + ")rotate(-90)";
            });
            var sub_self = self;

            self.link
                .attr("x1", function(d) {
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



            self.text.attr("transform", function(d) {
                //if((d.draggednode == true && self.forceSimulationActive) || self.forceSimulationActive == false)
                return "translate(" + d.x + "," + d.y + ")";

            });

        };
    };

    /**
     *  Export Graph data.
     *  @returns {Object} Graph object.
     */
    GraphEditor.prototype.exportJSON = function() {

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

    /**
     *
     *
     */
    GraphEditor.prototype._setupBehaviorsOnEvents = function() {
        log("_setupBehaviorsOnEvents");
        this.behavioursOnEvents = {
            'nodes': {
                'click': function(event) {

                },
                'dblclick': function(event) {

                },
                'contextmenu': function(event){

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
        log("_selectNodeExclusive ");
        var activeClass = "node_selected";
        var alreadyIsActive = d3.select(node_instance).classed(activeClass);
        this._deselectAllNodes();
        d3.select(node_instance).classed(activeClass, !alreadyIsActive);
        this._selected_node = (alreadyIsActive) ? undefined : node_id;
    };

    GraphEditor.prototype.savePositions = function(data) {
        log("dentro save potitions")
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