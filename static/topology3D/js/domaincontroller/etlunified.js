if (typeof dreamer === 'undefined') {
    var dreamer = {};
}

dreamer.EtlUnified = (function() {


    EtlUnified.prototype = new dreamer.DomainController();
    EtlUnified.prototype.constructor = EtlUnified;
    EtlUnified.prototype.parent = dreamer.DomainController.prototype;

    function EtlUnified() {
        console.log("EtlUnified-Constructor");
    }


    EtlUnified.prototype.setProperties = function(graph, args, layername) {

        var result = this.parent.setProperties.call(this, graph, args, layername);
        console.log("EtlUnified-setProperties", JSON.stringify(args));

        if (result.error) {
            return result;
        }

        if (args.node) {

        }
        //console.log(JSON.stringify(graph));
        return result;
    }

    EtlUnified.prototype.buildNodeProperties = function(ntype) { //TODO eliminare param inutili
        //console.log("EtlUnified:buildNodeProperties");

        var property = this.parent.buildNodeProperties.call(this, ntype);
        if (ntype != undefined) {
            //console.log(ntype)
            for (p in this.spec.nodes[ntype]['properties']) {
                property[p] = JSON.parse(JSON.stringify(this.spec.nodes[ntype]['properties'][p]));
            }

            for (layer in this.spec['layer_constraints']) {

                if (this.isVisibleVertex(ntype, layer) && this.spec['layer_constraints'][layer]['nodes-properties']) {
                    if (!property['domain-EtlUnified'])
                        property['domain-EtlUnified'] = {}
                    property['domain-EtlUnified']['layer-' + layer] = {};
                    for (p in this.spec['layer_constraints'][layer]['nodes-properties']) {
                        property['domain-EtlUnified']['layer-' + layer][p] = JSON.parse(JSON.stringify(this.spec['layer_constraints'][layer]['nodes-properties'][p]));
                    }
                }

            }
        }

        return property;
    };


    EtlUnified.prototype.getNodeProperties = function(node, nodes) {
        var info_data = this.parent.getNodeProperties.call(this, node, nodes);
        var ntype = node.getType();
        if (ntype != undefined) {
            info_data['type_info'] = {};

            for (p in this.spec.nodes[ntype]['properties']) {
                if (p != "domain-EtlUnified") {
                    info_data['type_info'][p] = node['info']['property'][p];
                }
            }
            info_data['model_info'] = {};
            if (this.spec.nodes[ntype]['properties']["domain-EtlUnified"]) {
                //console.log("#####"+JSON.stringify(this.spec.nodes[ntype]['properties']["domain-EtlUnified"]));
                for (p in this.spec.nodes[ntype]['properties']["domain-EtlUnified"]) {
                    //console.log("dentrooo")
                    info_data['model_info'][p] = node['info']['property']["domain-EtlUnified"][p]
                }
            }

            for (layer in this.spec['layer_constraints']) {
                if (this.isVisibleVertex(ntype, layer) && this.spec['layer_constraints'][layer]['nodes-properties']) {
                    info_data['model_info']['layer-' + layer] = {};
                    for (p in this.spec['layer_constraints'][layer]['nodes-properties']) {
                        if (node['info']['property']["domain-EtlUnified"] && node['info']['property']["domain-EtlUnified"]['layer-' + layer])
                            info_data['model_info']['layer-' + layer][p] = node['info']['property']["domain-EtlUnified"]['layer-' + layer][p];
                    }
                }
            }

        }

        return info_data;
    };

    EtlUnified.prototype.getNodeTypes = function() {
        //console.log("getNodeTypes EtlUnified")
        return this.spec['list_of_all_node_types'];
    };


    EtlUnified.prototype.getNodeDataView = function(node, is_closest, layer) {
        var empty_color = "#FFFFFF";
        var img = '/static/assets/img/location.png';
        var bgcolor;
        var b_color = "#FFFFFF";
        var h_color = "#A8A8A8";
        var label = undefined;
        if (is_closest)
            bgcolor = h_color;
        else
            bgcolor = b_color;

        if (this.getNodeTypes().indexOf(node.getType()) > -1) {
            var name = node.getType().replace(/ /g, '');
            name = name.toLowerCase();
            img = '/static/assets/img/' + name + '.png'
        }
        var location_type = node.info.property.location_type
        if(location_type != undefined){

            if(location_type != "IPWANProviderBackbone"){
                if(node.info.property.border_router_name == undefined){
                    img = '/static/assets/img/omini.png';
                    label = "mapping unwokable"
                }
                else
                    img = '/static/assets/img/location_and_router_red2.png';
            }



        }

        var nodeDView = {
            icon: img,
            bgcolor: bgcolor,
            label: label
        };


        return nodeDView;
    };


    EtlUnified.prototype.getDomainData = function() {
        var domaindata = this.parent.getDomainData.call(this);
        return domaindata;

    };

    EtlUnified.prototype.getNodeDomainLabel = function(node) {
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



    return EtlUnified;

}(this));

if (typeof module === 'object') {
    module.exports = dreamer.EtlUnified;
}