if (typeof dreamer === 'undefined') {
    var dreamer = {};
}

dreamer.EtlUnifiedReduc = (function() {


    EtlUnifiedReduc.prototype = new dreamer.DomainController();
    EtlUnifiedReduc.prototype.constructor = EtlUnifiedReduc;
    EtlUnifiedReduc.prototype.parent = dreamer.DomainController.prototype;

    function EtlUnifiedReduc() {
        console.log("EtlUnifiedReduc-Constructor");
    }


    EtlUnifiedReduc.prototype.setProperties = function(graph, args, layername) {

        var result = this.parent.setProperties.call(this, graph, args, layername);
        console.log("EtlUnifiedReduc-setProperties", JSON.stringify(args));

        if (result.error) {
            return result;
        }

        if (args.node) {

        }
        //console.log(JSON.stringify(graph));
        return result;
    }

    EtlUnifiedReduc.prototype.buildNodeProperties = function(ntype) { //TODO eliminare param inutili
        //console.log("EtlUnifiedReduc:buildNodeProperties");

        var property = this.parent.buildNodeProperties.call(this, ntype);
        if (ntype != undefined) {
            //console.log(ntype)
            for (p in this.spec.nodes[ntype]['properties']) {
                property[p] = JSON.parse(JSON.stringify(this.spec.nodes[ntype]['properties'][p]));
            }

            for (layer in this.spec['layer_constraints']) {

                if (this.isVisibleVertex(ntype, layer) && this.spec['layer_constraints'][layer]['nodes-properties']) {
                    if (!property['domain-EtlUnifiedReduc'])
                        property['domain-EtlUnifiedReduc'] = {}
                    property['domain-EtlUnifiedReduc']['layer-' + layer] = {};
                    for (p in this.spec['layer_constraints'][layer]['nodes-properties']) {
                        property['domain-EtlUnifiedReduc']['layer-' + layer][p] = JSON.parse(JSON.stringify(this.spec['layer_constraints'][layer]['nodes-properties'][p]));
                    }
                }

            }
        }

        return property;
    };


    EtlUnifiedReduc.prototype.getNodeProperties = function(node, nodes) {
        var info_data = this.parent.getNodeProperties.call(this, node, nodes);
        var ntype = node.getType();
        if (ntype != undefined) {
            info_data['type_info'] = {};

            for (p in this.spec.nodes[ntype]['properties']) {
                if (p != "domain-EtlUnifiedReduc") {
                    info_data['type_info'][p] = node['info']['property'][p];
                }
            }
            info_data['model_info'] = {};
            if (this.spec.nodes[ntype]['properties']["domain-EtlUnifiedReduc"]) {
                //console.log("#####"+JSON.stringify(this.spec.nodes[ntype]['properties']["domain-EtlUnifiedReduc"]));
                for (p in this.spec.nodes[ntype]['properties']["domain-EtlUnifiedReduc"]) {
                    //console.log("dentrooo")
                    info_data['model_info'][p] = node['info']['property']["domain-EtlUnifiedReduc"][p]
                }
            }

            for (layer in this.spec['layer_constraints']) {
                if (this.isVisibleVertex(ntype, layer) && this.spec['layer_constraints'][layer]['nodes-properties']) {
                    info_data['model_info']['layer-' + layer] = {};
                    for (p in this.spec['layer_constraints'][layer]['nodes-properties']) {
                        if (node['info']['property']["domain-EtlUnifiedReduc"] && node['info']['property']["domain-EtlUnifiedReduc"]['layer-' + layer])
                            info_data['model_info']['layer-' + layer][p] = node['info']['property']["domain-EtlUnifiedReduc"]['layer-' + layer][p];
                    }
                }
            }

        }

        return info_data;
    };

    EtlUnifiedReduc.prototype.getNodeTypes = function() {
        //console.log("getNodeTypes EtlUnifiedReduc")
        return this.spec['list_of_all_node_types'];
    };

    EtlUnifiedReduc.prototype.getEdgeDataView = function(edg, layer){

        var color = "white";

        return {
            color: color
        };

    }


    EtlUnifiedReduc.prototype.getNodeDataView = function(node, is_closest, layer) {
        var empty_color = "#FFFFFF";
        var img = '/static/assets/img/location.png';
        var bgcolor;
        var b_color = "#FFFFFF";
        var h_color = "#A8A8A8";

        if (is_closest)
            bgcolor = h_color;
        else
            bgcolor = b_color;


        var location_icon = node.info.property.icon
        //console.log("NODO", JSON.stringify(node));
        if(location_icon != undefined){
            if(location_icon != "wan")
                img = '/static/assets/img/location-' + location_icon + '.png';
        }

        var nodeDView = {
            icon: img,
            bgcolor: bgcolor
        };


        return nodeDView;
    };


    EtlUnifiedReduc.prototype.getDomainData = function() {
        var domaindata = this.parent.getDomainData.call(this);
        return domaindata;

    };

    EtlUnifiedReduc.prototype.getNodeDomainLabel = function(node) {
        if(node.info.property.border_router_name){
            return node.info.property.border_router_name
        }

        return null;
    };

    function getClusterColorBYId(cluster_id) {
        if (clustermap[cluster_id] != undefined)
            return clustermap[cluster_id];

        return undefined;
    };



    return EtlUnifiedReduc;

}(this));

if (typeof module === 'object') {
    module.exports = dreamer.EtlUnifiedReduc;
}