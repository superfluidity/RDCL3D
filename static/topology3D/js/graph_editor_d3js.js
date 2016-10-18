if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.GraphEditor = (function(global) {
    'use strict';


    var default_node_color = "#ccc";
    var default_node_label_color = "white";
    var default_link_color = "#888";
    var nominal_text_size = 15;
    var max_text_size = 24;
    var nominal_stroke = 1.5;
    var max_stroke = 4.5;
    var max_base_node_size = 36;



    /**
     * Constructor
     */
    function GraphEditor(args) {
        // log(JSON.stringify(args))

        this.width = args.width || 500;
        this.height = args.height || 500;

        this.focus_node = null;
        this.highlight_node = null;

        this.text_center = false;
        this.outline = false

        this.min_score = 0;
        this.max_score = 1;

        var min_zoom = 0.1;
        var max_zoom = 7;

        this.node_filter_cb = args.node_filter_cb || function(d) {
            //console.log(d.info.type, d.info.type in ["vnf", "ns_cp", "ns_vl"], ["vnf", "ns_cp", "ns_vl"])
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
                "size": 20
            },
            "ns_vl": {
                "shape": d3.symbolDiamond,
                "color": "#196B90",
                "size": 20
            },
            "ns_cp": {
                "shape": d3.symbolCircle,
                "color": "#F27220",
                "size": 20
            },
            "vnf": {
                "shape": d3.symbolSquare,
                "color": "#54A698",
                "size": 28
            },
            "vnf_vl": {
                "shape": d3.symbolDiamond,
                "color": "#313679",
                "size": 18
            },
            "vnfc_cp": {
                "shape": d3.symbolCircle,
                "color": "#343D41",
                "size": 18
            },
            "vnf_cp": {
                "shape": d3.symbolCircle,
                "color": "#4E6293",
                "size": 18
            },
            "vnfc": {
                "shape": d3.symbolSquare,
                "color": "#1D74C2",
                "size": 28
            },
            "vdu": {
                "shape": d3.symbolSquare,
                "color": "#4B7C91",
                "size": 28
            }
        };

        // graoh data initailization
        this.d3_graph = {
            nodes: [],
            links: []
        };

        this.force = d3.forceSimulation()
            .force("link", d3.forceLink().distance(160).strength(3).id(function(d) {
                return d.id;
            }))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(this.width / 2, this.height / 2));

        // this.force.linkStrength(1);

        var zoom = d3.zoom().scaleExtent([min_zoom, max_zoom])

        var size = d3.scalePow().exponent(2)
            .domain([1, 100])
            .range([8, 24]);

        this.svg = d3.select("#graph_ed_container").append("svg")
            .attr("id", "graph_svg")
            .attr("width", this.width)
            .attr("height", this.height);

        var self = this;

        d3.json("graph_data", function(error, data) {
            // if(error == false)

            self.d3_graph.nodes = data.vertices
            self.d3_graph.links = data.edges;
            /*
            for (var e in data.edges) {
                //log(data.edges[e])
                data.edges[e].links.forEach(function(l) {
                    //log(l.id)
                    var a = e.split("&&");
                    // Add the edge to the array
                    self.d3_graph.links.push({
                        source: a[0],
                        target: a[1],
                        view: l.view
                    });
                })

            };
            //log(d3_graph.links)
            for (var v in data.vertices) {

                data.vertices[v]["id"] = v;
                //log(data.vertices[v])
                self.d3_graph.nodes.push(data.vertices[v]);

            };

            */

            self.update();
            self.startForce();
        });

    }

    /**
     * Start or Stop force layout
     * @param {boolean} Required. Value true: start, false: stop
     * @returns {boolean}
     */
    GraphEditor.prototype.handleForce = function(start) {
        if(start){
            this.force.restart();
        }
        else{
            this.force.stop();
        }
    };


    /**
     * Add a new node to the graph.
     * @param {Object} Required. An object that specifies tha data of the new node.
     * @returns {boolean}
     */
    GraphEditor.prototype.addNode = function(args) {

        if(args.id && args.info && args.info.type){
            this.d3_graph.nodes.push(args);
            this.cleanAll();
            this.update();
            this.startForce();
            return true;
        }

        return false;

    };

    /**
     * Remove a node from graph and related links.
     * @param {String} Required. Id of node to remove.
     * @returns {boolean}
     */
    GraphEditor.prototype.removeNode = function(node_id) {

    };

    /**
     * Add a new link to graph.
     * @param {Object} Required. An object that specifies tha data of the new Link.
     * @returns {boolean}
     */
    GraphEditor.prototype.addLink = function(args) {

    };

    /**
     * Remove a link from graph.
     * @param {Object} Required. An object that specifies tha data of link to remove.
     * @returns {boolean}
     */
    GraphEditor.prototype.removeLink = function(args) {

    };


    /**
     * Force a refresh of GraphView
     * @returns {}
     */
    GraphEditor.prototype.refresh = function() {

    };


    /**
     * Update the data of graph.
     * @param {Object} Required. An object that specifies tha data of the graph.
     * @returns {}
     */
    GraphEditor.prototype.update = function() {

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

       // this.text.exit().remove();


        function dragstarted(d) {
            if (!d3.event.active) self.force.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(d) {
            d.fx = d3.event.x;
            d.fy = d3.event.y;
        }

        function dragended(d) {
            if (!d3.event.active) self.force.alphaTarget(0);
            d.fx = null;
            d.fy = null;
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
            console.log("ticked");
            self.node.attr("transform", function(d) {

                return "translate(" + d.x + "," + d.y + ")rotate(-90)";
            });

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
                return "translate(" + d.x + "," + d.y + ")";
            });
        }
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

    /** Get project object descriptor from the graph
    */
    GraphEditor.prototype.getProjectDescriptor = function(){
         var self = this;
         var project = {nsd: {}, vld :{}, vnfd:{}, vnffgd:{}}
         console.log(self.d3_graph.nodes)
         self.d3_graph.nodes.forEach(function(l) {
            switch(l.info.type){
                case 'ns':
                    project.nsd[l.id] = l.descriptor
                    break
                    project.vld[l.descriptor.id] = l.descriptor
                    break
                case 'vnf':
                    project.vnfd[l.descriptor.id] = l.descriptor
                    break
                case 'vnf_vl':
                    project.vld[l.descriptor.id] = l.descriptor
                    break
                 case 'vnffg':
                    project.vnffgd[l.descriptor.id] = l.descriptor
                    break

            }
         });

         //log(self.d3_graph.links);
         log(project)
    };

    /**
     *  Internal function
     */
    function log(text) {
        console.log("::GraphEditor::", text);
    }


    return GraphEditor;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.GraphEditor;
}
