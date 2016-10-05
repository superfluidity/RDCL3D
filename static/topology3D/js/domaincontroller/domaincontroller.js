if (typeof dreamer === 'undefined') {
    var dreamer = {};
}

dreamer.DomainController = (function() {

    var config = new dreamer.Config();


    var tsv_host = config.top_ser_validator.host_name;
    var tsv_port = config.top_ser_validator.host_port;
    var tsv_base = tsv_host + ":" + tsv_port;

    var vmmcontroller;

    function DomainController() {
        //console.log("DomainController");
        vmmcontroller = new dreamer.VmmController();
    }

    DomainController.prototype.loadSpec = function(modelname, callback) {



        var self = this;
        $.ajax({
            url: "/mpv/" + modelname,


            success: function(result) {
                ////console.log(JSON.stringify(result));
                var response = {};
                //response['error'] = false;
                if (!result.error) {
                    self.spec = result;
                }
                callback(result);
            },
            error: function(xhr, status, errore) {
                var response = {};
                console.log("loadSpec", errore);
                console.log(status)
                console.log(JSON.stringify(xhr))
                response['error'] = {
                    "message": "Unable to contact the server, please refresh the page and try again"
                };
                callback(response);
            }

        });


    };

    DomainController.prototype.validateTopology = function(graph, callback) {
        var modelname = this.spec["model_name"];
        var topology = this.exportJson(graph);
        var self = this;
        $.ajax({
            url: "/validateTopology",
            type: "POST",
            dataType: "json",
            //contentType: 'application/json; charset=utf-8;',
            data: {
                "topology": this.exportJson(graph),
                "modelname": this.spec["model_name"]
            },
            success: function(result) {
                var response = {};
                //response['error'] = false;
                response = result;
                ////console.log(response);
                callback(response);
            },
            error: function(xhr, status, errore) {
                var response = {};
                response['error'] = {
                    "message": errore
                };
                console.log("validate error", errore);
                callback(response);
            }

        });


    };

    DomainController.prototype.getRandomTopology = function(n, p, callback) {

        $.ajax({
            url: "/getRandom/?n=" + n + "&p=" + p,

            beforeSend: function() {
                $('#randomprogbar').show();
            },
            success: function(result) {

                var response = {};
                response['error'] = false;
                response['topology'] = result;
                callback(response);
            },
            error: function(xhr, status, errore) {
                var response = {};
                response['error'] = true;
                callback(response);

            }

        });
    };


    DomainController.prototype.newExp = function(graph, callback) {
        //console.log("newExp");
        //var modelname = this.spec["model_name"];
        var topology = this.exportJson(graph);
        var self = this;
        var addr = config.experiment_handler.host_name + ":" + config.experiment_handler.host_port;
        $.ajax({
            url: "/newExp",
            type: "POST",
            dataType: "json",
            //contentType: 'application/json; charset=utf-8;',
            data: {
                "expid": graph.exp_id,
                "topology": this.exportJson(graph),
                //"modelname": this.spec["model_name"]
            },
            success: function(result) {
                var response = {};
                //response['error'] = false;
                response = result;
                //console.log(response);
                callback(response);
            },
            error: function(xhr, status, errore) {
                //console.log("error", "newExp")
                var response = {};
                response['error'] = {
                    "message": errore
                };
                //console.log(xhr, status , errore);
                callback(response);
            }

        });


    };

    DomainController.prototype.isVisible = function(element, layername) {
        if (element instanceof dreamer.Vertex) {
            //console.log(element.getType(), layername)
            return this.isVisibleVertex(element.getType(), layername);

        } else if (element instanceof dreamer.Edge) {
            //var layername = layer.getCurLayer();
            for (l in element.links) {
                if (element.links[l].layer == layername) {
                    return true;
                }
            }
        }
        return false;

    };

    DomainController.prototype.isVisibleVertex = function(ntype, layername) {
        // var layername = layer.getCurLayer();
        var layer_constraints = this.spec['layer_constraints'];
        if (this.spec['list_of_all_layer'].indexOf(layername) > -1 && (ntype == undefined || layer_constraints[layername]['list_of_nodes_layer'] === undefined || layer_constraints[layername]['list_of_nodes_layer'].indexOf(ntype) > -1)) {
            return true;
        }
        return false;
    };

    DomainController.prototype.isSelectableEdge = function(from_, to_node, edges, layername){

        var selectable_edges = this.spec['layer_constraints'][layername]['selectable_edges'];

        var res = {
            "error": false
        };

        for(s in selectable_edges){
            for(var pro in selectable_edges[s]){
                var upperCaseNames = selectable_edges[s][pro].map(function(value) {
                    return value.toUpperCase();
                });
                console.log("..",from_.info['property'][pro], upperCaseNames, to_node.info['property'][pro]);
                if((from_.info['property'][pro] != null &&  upperCaseNames.indexOf(from_.info['property'][pro].toUpperCase()) > -1)
                    && (to_node.info['property'][pro] != null && upperCaseNames.indexOf(to_node.info['property'][pro].toUpperCase()) > -1)
                    && (from_.info['property'][pro] != to_node.info['property'][pro])){
                    res = {
                        "error": false
                    };
                }
                else{
                    res = {
                        "error": true
                    };
                }
            }
        }

        return res;
    };

    DomainController.prototype.isValidEdge = function(from_, to_node, edges, layername) {
        var lnae = this.spec['layer_constraints'][layername]['not_allowed_edge'];
        var res = {
            "error": false
        };
        var from_type = from_.getType();
        var to_type = to_node.getType();
        //console.log(from_type, to_type);

        for (i in lnae) {

            if (lnae[i].source == from_type) {
                if (lnae[i].not_allowed_des.indexOf(to_type) > -1) {

                    res["error"] = true;
                }

            }

        }
        //controllo multilink non abilitato "peo6&&cro3"
        if (this.spec['layer_constraints'][layername]['multilink'] != undefined) {
            //console.log("multilink");
            var name_a = from_.label + "&&" + to_node.label;
            var name_b = to_node.label + "&&" + from_.label;
            //console.log(name_a, name_b);

            for (i = edges.length - 1; i > -1; i -= 1) {

                edge = edges[i];
                // edge.existBetween(node1, node2, curLayer.getCurLayer());
                if (edge.existBetween(from_, to_node) && edge.hasLink(layername)) {
                    res["error"] = true;
                    return res;

                }
            }

        }

        //
        //console.log("Layer constr " + JSON.stringify(this.spec['layer_constraints'][layername]))
        if (this.spec['layer_constraints'][layername]['multihoming'] != undefined && this.spec['layer_constraints'][layername]['multihoming'] == false) {
            //console.log("Controllo multihoming")
        }

        return res;

    };

    DomainController.prototype.isNewVertexAllowed = function(type, curlayer) {

        var res = {};

        if (!this.isInsertEnabled(curlayer)) {
            res["error"] = {
                'message': "inserting a node not allowed in this view"
            };
            return res;
        }

        if (this.spec['layer_constraints'][curlayer]['list_of_nodes_layer'] != undefined && this.spec['layer_constraints'][curlayer]['list_of_nodes_layer'].indexOf(type) < 0) {
            res["error"] = {
                'message': "inserting a new node of type " + type + " not allowed in this view"
            };
            return res;
        }

        return res;

    };

    DomainController.prototype.getNodeCurrentLayer = function(layer, nodes) {
        var available = [];
        for (i in nodes) {
            if (this.isVisible(nodes[i], layer.getCurLayer()))
                available.push(nodes[i]);
        }
        return available;
    };


    DomainController.prototype.getEdgeCurrentLayer = function(layer, edges) {
        var available = [];
        for (i in edges) {
            if (this.isVisible(edges[i], layer.getCurLayer()))
                available.push(edges[i]);
        }
        return available;
    };

    DomainController.prototype.getNodeTypes = function() {
        //console.log("getNodeTypes");
        //console.log(JSON.stringify(this.spec))
        //return ["OSHI-CR", "OSHI-PE", "CE", "OF Controller"];
        if (this.spec)
            return this.spec['list_of_all_node_types'];
        return [];
    };

    DomainController.prototype.getAllLayers = function() {
        return this.spec['list_of_all_layer'];
    };

    DomainController.prototype.isValidLayers = function(layer) {
        if (this.spec['list_of_all_layer'].indexOf(layer) > -1) {
            return true;
        }
        return false;
    };


    DomainController.prototype.isInsertEnabled = function(layername) {

        if (this.spec['layer_constraints'][layername]['insert_new_node'] == undefined || this.spec['layer_constraints'][layername]['insert_new_node'] == true)
            return true;

        return false;
    };

    DomainController.prototype.getNotSelectedMgtIp = function(nodetype) {
        return vmmcontroller.getNotSelectedMgtIp(nodetype);
    }

    DomainController.prototype.getNodeProperties = function(node, nodes) {
        var vertype = node.info["type"] || "";
        var info_data = {
            selected: "Vertex",
            base_info: {

                pos: {
                    x: node.get_pos().x.toFixed(1),
                    y: node.get_pos().y.toFixed(1)
                },
                index: nodes.indexOf(node),
                node_type: vertype,
                label: node.label,
            },
            custom_info: (node.info.property["custom_info"]) ? node.info.property["custom_info"] : undefined,
        };

        return info_data;
    };

    DomainController.prototype.getGraphSpecDomine = function() {
        return this.spec['graph_parameters'];
    };


    DomainController.prototype.getEdgeDataView = function(edg, layer){
       // console.log("EDGE", JSON.stringify(edg));
        var selected_color = "#CC0000";
        var closest_color = "#CCC000";
        var from_node_selected_color = "#0000C0";
        var default_color = "#000000";

        var color  = default_color;

        if (edg.selected) {
            color = selected_color;
        } else if (edg.closest) {
            color = closest_color;
        } else if (edg.node1.selected || edg.node2.selected) {
            color = from_node_selected_color;
        } else {
            color = default_color;
        }

        return {
            color: color
        };

    };

    DomainController.prototype.getNodeDataView = function(node, is_closest, layer) {
        var empty_color = "#FFFFFF";
        var img = '/static/assets/img/punto.png';
        var bgcolor;
        var b_color = "#FFFFFF";
        var h_color = "#A8A8A8";

        if (is_closest)
            bgcolor = h_color;
        else
            bgcolor = b_color;

        if (this.getNodeTypes().indexOf(node.getType()) > -1) {
            var name = node.getType().replace(/ /g, '');
            name = name.toLowerCase();
            img = '/static/assets/img/' + name + '.png'
        }

        return {
            icon: img,
            bgcolor: bgcolor
        };
    };

    DomainController.prototype.getNodeLabel = function(nodetype) {
        var result;
        try {
            result = this.spec['nodes'][nodetype]['node_label'];
        } catch (err) {
            //console.log("getNodeLabel Exception: " + err);
            result = nodetype;
        }

        return result;


    };

    DomainController.prototype.setProperties = function(graph, args, layername) {
        var result = {};

        if (args.node) {
            var node_index = objectFindIdByKey(graph.vertices, args.node.index_key, args.node.index)
            console.log(args.node.index_key, args.node.index);
            console.log("node_index", node_index);
            if (args.node.properties.type) {
                if (this.spec['layer_constraints'][layername].changing_nodes_type == undefined || this.spec['layer_constraints'][layername].changing_nodes_type == true) {

                    var new_node_label = this.getNodeLabel(args.node.properties.type);
                    console.log(new_node_label);

                    graph.vertices[args.node.index].label = new_node_label + (parseInt(args.node.index) + 1);

                    graph.vertices[args.node.index].info["type"] = args.node.properties.type
                    var newp = this.buildNodeProperties(args.node.properties.type);
                    delete graph.vertices[args.node.index].info['property'];
                    graph.vertices[args.node.index].info['property'] = {}
                    for (p in newp) {
                        graph.vertices[args.node.index].info['property'][p] = newp[p];
                    }
                } else {
                    result['error'] = "Changing nodes type not allowed in " + layername;
                }
            }
            else if (args.node.properties.vm) {
                var mgtip = args.node.properties.vm.mgt_ip;
                var interfaces = args.node.properties.vm.interfaces;
                var type = graph.vertices[node_index].info["type"];

                var curnmgtip = graph.vertices[node_index].info['property']["vm"]["mgt_ip"];
                if (curnmgtip != "") {
                    vmmcontroller.deselectMgtIP(type, curnmgtip);
                    graph.vertices[0]['info']['property']["vm"]["mgt_ip"] = ""
                }

                if (mgtip) {
                    if (mgtip != "") {
                        var res = vmmcontroller.selectMgtIP(type, mgtip);
                        if (res.error) {
                            //console.log("@@" + res.error)
                            result['error'] = res.error;
                        } else {

                            graph.vertices[node_index].info['property']["vm"]["mgt_ip"] = mgtip;
                            if (interfaces) {
                                var vint = vmmcontroller.isValidInterfaces(type, mgtip, interfaces);
                                if (vint.error) {
                                    result['error'] = vint.error;
                                } else {
                                    graph.vertices[node_index].info['property']["vm"]["interfaces"] = interfaces;
                                }
                            }

                        }
                    }

                } else {
                    if (mgtip != "") {
                        result['error'] = "MgtIp not defined!";
                    }

                }
            }

            else {
                var keys = Object.keys(args.node.properties);

                for (k in keys) {

                    if (keys[k].indexOf("domain-") < 0) { // prendo solo quelli base
                        graph.vertices[node_index].info['property'][keys[k]] = args.node.properties[keys[k]];
                    }
                }

            }

        } else if (args.edge) {

        } else if (args.graph_parameters) {
            if (args.graph_parameters.tunneling) {
                if (graph.graph_parameters instanceof dreamer.GraphParameters) {
                    graph.graph_parameters.setTunneling(args.graph_parameters.tunneling);
                } else {

                    graph.graph_parameters = new dreamer.GraphParameters({
                        tunneling: args.graph_parameters.tunneling
                    });
                }

            } else if (args.graph_parameters.testbed) {
                if (graph.graph_parameters instanceof dreamer.GraphParameters) {
                    graph.graph_parameters.setTestBed(args.graph_parameters.testbed);
                } else {

                    graph.graph_parameters = new dreamer.GraphParameters({
                        testbed: args.graph_parameters.testbed
                    });
                }
            }

        }

        return result;
    };

    DomainController.prototype.buildNodeProperties = function(ntype) {
        var property = {};
        return property;
    };


    DomainController.prototype.getNodesProperty = function(property, nodes) {
        var dict = {};
        var props = property.split('.');
        //console.log(JSON.stringify(props));
        for (n in nodes) {
            //console.log("n: " + n+ " label"+nodes[n].label +" "+ JSON.stringify(nodes[n].info.property));
            var curNprps = nodes[n].info.property;
            //console.log("curNprps :"+JSON.stringify(curNprps));
            for (p in props) {
                //console.log("chiave: " + props[p]);
                curNprps = hasProperty(props[p], curNprps);
                if (curNprps == null) {
                    //console.log("NON HA property");
                    break;
                }

            }

            if (curNprps != null)
                dict[nodes[n].label] = curNprps;
        }

        return JSON.stringify(dict, null, "\t");
    };

    DomainController.prototype.getNodeLabel = function(nodetype) {
        return this.spec['nodes'][nodetype]['node_label'];
    };

    DomainController.prototype.getDomainData = function() {
        var domaindata = {};

        return domaindata;

    };

    DomainController.prototype.getInterfacesMgtIp = function(type, mgtip) {

        return vmmcontroller.getInterfacesMgtIp(type, mgtip);

    };

    DomainController.prototype.exportJson = function(graph, pure) {

        var jsongraph = {};
        jsongraph['vertices'] = {};
        jsongraph['edges'] = {};
        var edges = graph.edges;
        var vertices = graph.vertices;

        for (v in vertices) {
            var curvert = vertices[v];
            jsongraph['vertices'][curvert.label] = {};
            jsongraph['vertices'][curvert.label]['pos'] = curvert.pos;
            jsongraph['vertices'][curvert.label]['v'] = curvert.v;
            jsongraph['vertices'][curvert.label]['info'] = curvert.info;

        }

        for (e in edges) {

            var label = edges[e].node1.label + "&&" + edges[e].node2.label;
            jsongraph['edges'][label] = {};
            jsongraph['edges'][label]['links'] = [];
            for (index in edges[e].links) {
                var tmplink = {};
                tmplink['id'] = edges[e].links[index].edge_label;
                tmplink['view'] = edges[e].links[index]['layer'];
                tmplink['IP-RHS'] = edges[e].links[index]['IP-RHS'];
                tmplink['IP-LHS'] = edges[e].links[index]['IP-LHS'];
                //var domainname = 'domain-'+this.spec['model_name'];
                //tmplink[]


                jsongraph['edges'][label]['links'].push(tmplink);
            }


        }
        jsongraph.graph_parameters = graph.graph_parameters;
        ////console.log(JSON.stringify(jsongraph));
        if (pure) {
            return JSON.stringify(jsongraph);
        }
        return JSON.stringify(jsongraph, null, "\t");
    }

    DomainController.prototype.import_from_JSON = function(graph, size) {
        var nodes = [];
        var edges = [];
        var graph_parameters;
        var tmpdict = {};
        var nopos = false;
        var vertnumber = 0;

        var maxx = -Infinity,
            minx = Infinity,
            maxy = -Infinity,
            miny = Infinity,
            newx, newy, dx, dy;
        for (var vertex in graph.vertices) {
            if (graph.vertices[vertex].pos) {
                maxx = Math.max(maxx, graph.vertices[vertex].pos['x']);
                maxy = Math.max(maxy, graph.vertices[vertex].pos['y']);
                minx = Math.min(minx, graph.vertices[vertex].pos['x']);
                miny = Math.min(miny, graph.vertices[vertex].pos['y']);
                console.log(maxx, maxy, minx, miny)
                dx = maxx - minx;
                dy = maxy - miny;
                console.log(dx, dy)
            } else {
                nopos = true;
            }
            vertnumber++;
        }


        for (var vertex in graph.vertices) {


            if (nopos == false) {

                newx = (graph.vertices[vertex].pos['x'] - minx) / dx;

                newx = newx * 8 * size.x / 10 + size.x / 10;

                newy = (graph.vertices[vertex].pos['y'] - miny) / dy;
                newy = newy * 8 * size.y / 10 + size.y / 10;
                console.log(newx, newy)
            } else {
                newx = size.x / 2 + (2 * size.x / 5) * Math.sin(2 * Math.PI * vertex / vertnumber);
                newy = size.y / 2 - (2 * size.y / 5) * Math.cos(2 * Math.PI * vertex / vertnumber);
                console.log("nopos", newx, newy, size.x, size.y);
            }


            var new_v = new dreamer.Vertex(nodes, {
                x: newx,
                y: newy
            }, vertex, graph.vertices[vertex].info);

            nodes.push(new_v);
            tmpdict[vertex] = new_v;
        }

        for (var edge in graph.edges) {
            var n = edge.split("&&");
            var new_e = new dreamer.Edge(tmpdict[n[0]], tmpdict[n[1]]);
            for (link in graph.edges[edge].links) {

                new_e.addLink(graph.edges[edge].links[link].id, graph.edges[edge].links[link]['view'], graph.edges[edge].links[link]);
            }

            edges.push(new_e);

        }

        graph_parameters = new dreamer.GraphParameters(graph.graph_parameters);
        return {
            'vertices': nodes,
            'edges': edges,
            'graph_parameters': graph_parameters
        };
    }

    DomainController.prototype.getNodeDomainLabel = function(node) {
        return null;
    };

    DomainController.prototype.getVmmConfig = function() {
        return vmmcontroller.getVmmConfig();
    };

    DomainController.prototype.setVmmConfig = function(data) {
        return vmmcontroller.load(data);
    };

    function hasProperty(property, obj) {
        //console.log("property: " + property);
        //console.log("obj: " + JSON.stringify(obj));
        if ((typeof obj === "object") && (obj.constructor === Object)) {
            //console.log("QUII" + JSON.stringify(obj["custom_label"]));
            if (obj.hasOwnProperty(property)) {
                //console.log("QUII DENTROOOO" + obj[property.toString()]);
                return obj[property];
            }
        }
        return null;
    }


    function objectFindIdByKey(array, key, value) {
        for (var i = 0; i < array.length; i++) {
            if (array[i][key] === value) {
                return i;
            }
            else if(array[i]['info'][key] === value) {
                return i;
            }
            else if(array[i]['info']['property'][key] === value) {
                return i;
            }
        }
        return null;
    }



    return DomainController;

}(this));

if (typeof module === 'object') {
    module.exports = dreamer.DomainController;
}