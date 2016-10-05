if (typeof dreamer === 'undefined') {
    var dreamer = {};
}

dreamer.GraphEditor = (function(global) {
    'use strict';

    var modelToController = {
        "oshi": "Oshi",
        "openflow": "OpenFlow",
        "ciscoapic": "CiscoApic",
        "ciscocucm": "CiscoCucm",
        "ciscocucmone": "CiscoCucmOne",
        "etlunified": "EtlUnified",
        "skypefb": "SkypeFB",
        "etlunifiedreduc": "EtlUnifiedReduc",
        "etsimano": "Etsimano"
    }

    var Vertex = dreamer.Vertex;
    var Edge = dreamer.Edge;
    var GraphParameters = dreamer.GraphParameters;
    var CurLayer = dreamer.CurLayer;

    var default_node_color = "#ccc";
    var default_node_label_color = "white";
    var default_link_color = "#888";
    var nominal_text_size = 15;
    var max_text_size = 24;
    var nominal_stroke = 1.5;
    var max_stroke = 4.5;
    var max_base_node_size = 36;



    // Constructor
    function GraphEditor(args) {
        log(JSON.stringify(args))

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

        this.node_filter_cb = args.node_filter_cb || function(d){
            //console.log(d.info.type, d.info.type in ["vnf", "ns_cp", "ns_vl"], ["vnf", "ns_cp", "ns_vl"])
            if  (["vnf", "ns_cp", "ns_vl"].indexOf(d.info.type) > -1)
                return true
            return false;
        };

        this.link_filter_cb = args.link_filter_cb || function(d){
            return d.view == 'nsd';
        };

        var type_property = {
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
            .attr("width", this.width)
            .attr("height", this.height);
        //this.g = this.svg.append("g");
        var self = this;
        d3.json("graph_data", function(error, data) {
            log(data)
            var _self = self;
            var d3_graph = {
                nodes: [],
                links: []
            };
            for (var e in data.edges) {
                //log(data.edges[e])
                data.edges[e].links.forEach(function(l) {
                    //log(l.id)
                    var a = e.split("&&");
                    // Add the edge to the array
                    d3_graph.links.push({
                        source: a[0],
                        target: a[1],
                        view: l.view
                    });
                })

            };
            //log(d3_graph.links)
            for (var v in data.vertices) {
                //log(data.edges[e])
                data.vertices[v]["id"] = v
                d3_graph.nodes.push(data.vertices[v]);

            };
            //log(JSON.stringify(d3_graph.links))

            var link = self.svg.append("g")
                .attr("class", "links")
                .attr("width", self.width)
                .attr("height", self.height)
                .selectAll("line")
                .data(d3_graph.links
                    .filter(self.link_filter_cb)
                    )
                .enter().append("line")
                .attr("class", "link")
                .style("stroke-width", nominal_stroke)
                .style("stroke", function(d) {
                    return default_link_color;
                });

            var node = self.svg.append("g")
                .attr("class", "nodes")
                .attr("width", self.width)
                .attr("height", self.height)
                .selectAll("node")
                .data(d3_graph.nodes
                    .filter(self.node_filter_cb))
                .enter()
                .append("g")
                .attr("class", "node")
                .append("svg:path")
                .attr("class", "node_path")
                .attr("id", function(d){
                    return "path_"+ d.id;
                })
                .attr("d", d3.symbol()
                    .size(function(d) {
                        return Math.PI * Math.pow(type_property[d.info.type].size, 2.2);
                    })
                    .type(function(d) {
                        return type_property[d.info.type].shape;
                    })
                )
                .style("fill", function(d) {
                    return type_property[d.info.type].color;
                })
                .attr("transform", function() {
                    return "rotate(-45)";

                })
                .attr("stroke-width", 2.4)
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));


            var text = self.svg.selectAll(".text")
                .data(d3_graph.nodes
                    .filter(self.node_filter_cb))
                .enter().append("text")
                .attr("class", "nodetext")
                .attr("dy", ".35em")
                .attr("pointer-events", "none")
                .style("font-size", nominal_text_size + "px")
                .style("fill", default_node_label_color)
	            .style("text-anchor", "middle")
	            .text(function(d) { return d.id; });


            self.force
                .nodes(d3_graph.nodes)
                .on("tick", ticked);


            self.force.force("link")
                .links(d3_graph.links);



            function ticked() {
                link
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

                node.attr("transform", function(d) {
                    return "translate(" + d.x + "," + d.y + ")rotate(-90)";
                });

                text.attr("transform", function(d) {
                    return "translate(" + d.x + "," + d.y + ")";
                });
            }

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
        });



    }

    GraphEditor.prototype.updateData = function(args) {

    };


    GraphEditor.prototype.cleanAll = function() {
        this.svg.selectAll('.cleanable').remove();
    };




    function log(text) {
        console.log("::GraphEditor::", text);
    }


    return GraphEditor;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.GraphEditor;
}
