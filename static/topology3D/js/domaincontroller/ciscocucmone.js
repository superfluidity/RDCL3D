if (typeof dreamer === 'undefined') {
    var dreamer = {};
}

dreamer.CiscoCucmOne = (function() {


    CiscoCucmOne.prototype = new dreamer.DomainController();
    CiscoCucmOne.prototype.constructor = CiscoCucmOne;
    CiscoCucmOne.prototype.parent = dreamer.DomainController.prototype;

    function CiscoCucmOne() {
        console.log("CiscoCucmOne-Constructor");
    }


    CiscoCucmOne.prototype.setProperties = function(graph, args, layername) {

        var result = this.parent.setProperties.call(this, graph, args, layername);
        console.log("CiscoCucmOne-setProperties", JSON.stringify(args));

        if (result.error) {
            return result;
        }

        if (args.node) {

        }
        //console.log(JSON.stringify(graph));
        return result;
    }

    CiscoCucmOne.prototype.buildNodeProperties = function(ntype) { //TODO eliminare param inutili
        //console.log("CiscoCucmOne:buildNodeProperties");

        var property = this.parent.buildNodeProperties.call(this, ntype);
        if (ntype != undefined) {
            //console.log(ntype)
            for (p in this.spec.nodes[ntype]['properties']) {
                property[p] = JSON.parse(JSON.stringify(this.spec.nodes[ntype]['properties'][p]));
            }

            for (layer in this.spec['layer_constraints']) {

                if (this.isVisibleVertex(ntype, layer) && this.spec['layer_constraints'][layer]['nodes-properties']) {
                    if (!property['domain-CiscoCucmOne'])
                        property['domain-CiscoCucmOne'] = {}
                    property['domain-CiscoCucmOne']['layer-' + layer] = {};
                    for (p in this.spec['layer_constraints'][layer]['nodes-properties']) {
                        property['domain-CiscoCucmOne']['layer-' + layer][p] = JSON.parse(JSON.stringify(this.spec['layer_constraints'][layer]['nodes-properties'][p]));
                    }
                }

            }
        }

        return property;
    };


    CiscoCucmOne.prototype.getNodeProperties = function(node, nodes) {
        var info_data = this.parent.getNodeProperties.call(this, node, nodes);
        var ntype = node.getType();
        if (ntype != undefined) {
            info_data['type_info'] = {};

            for (p in this.spec.nodes[ntype]['properties']) {
                if (p != "domain-CiscoCucmOne") {
                    info_data['type_info'][p] = node['info']['property'][p];
                }
            }
            info_data['model_info'] = {};
            if (this.spec.nodes[ntype]['properties']["domain-CiscoCucmOne"]) {
                //console.log("#####"+JSON.stringify(this.spec.nodes[ntype]['properties']["domain-CiscoCucmOne"]));
                for (p in this.spec.nodes[ntype]['properties']["domain-CiscoCucmOne"]) {
                    //console.log("dentrooo")
                    info_data['model_info'][p] = node['info']['property']["domain-CiscoCucmOne"][p]
                }
            }

            for (layer in this.spec['layer_constraints']) {
                if (this.isVisibleVertex(ntype, layer) && this.spec['layer_constraints'][layer]['nodes-properties']) {
                    info_data['model_info']['layer-' + layer] = {};
                    for (p in this.spec['layer_constraints'][layer]['nodes-properties']) {
                        if (node['info']['property']["domain-CiscoCucmOne"] && node['info']['property']["domain-CiscoCucmOne"]['layer-' + layer])
                            info_data['model_info']['layer-' + layer][p] = node['info']['property']["domain-CiscoCucmOne"]['layer-' + layer][p];
                    }
                }
            }

        }

        return info_data;
    };

    CiscoCucmOne.prototype.getNodeTypes = function() {
        //console.log("getNodeTypes CiscoCucmOne")
        return this.spec['list_of_all_node_types'];
    };

    CiscoCucmOne.prototype.getEdgeDataView = function(edg, layer){
                //#808080
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
        }


        return {
            color: color
        };

    }

    CiscoCucmOne.prototype.getNodeDataView = function(node, is_closest, layer) {
        var empty_color = "#FFFFFF";
        var img = '/static/assets/img/omini.png';
        var bgcolor;
        var b_color = "#FFFFFF";
        var h_color = "#A8A8A8";

        if (is_closest)
            bgcolor = h_color;
        else
            bgcolor = b_color;

        /*
        if (this.getNodeTypes().indexOf(node.getType()) > -1) {
            var name = node.getType().replace(/ /g, '');
            name = name.toLowerCase();
            img = '/static/assets/img/' + name + '.png'
        }
        */

        var location_type = node.info.property.location_type
        //console.log("location_type", location_type);
        if(location_type != undefined){

            if(location_type == "IPWANProviderBackbone")
                img = '/static/assets/img/location.png';
        }
        var role = node.info.property.role;
        //console.log("role", role);
        if(role != undefined && role == "IPWanTransit"){
            img = '/static/assets/img/location.png';
        }


        var nodeDView = {
            icon: img,
            bgcolor: bgcolor
        };


        return nodeDView;
    };


    CiscoCucmOne.prototype.getDomainData = function() {
        var domaindata = this.parent.getDomainData.call(this);
        return domaindata;

    };

    CiscoCucmOne.prototype.getNodeDomainLabel = function(node) {
        if(node.info.property.border_router_name){
            return node.info.property.border_router_name
        }

        if(node.info.property.location_type != "IPWANProviderBackbone" && node.info.property.border_router_name == undefined){
            return "mapping unwokable";
        }

        return null;
    };

    function getClusterColorBYId(cluster_id) {
        if (clustermap[cluster_id] != undefined)
            return clustermap[cluster_id];

        return undefined;
    };



    return CiscoCucmOne;

}(this));

if (typeof module === 'object') {
    module.exports = dreamer.CiscoCucmOne;
}