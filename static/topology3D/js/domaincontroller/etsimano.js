if (typeof dreamer === 'undefined') {
    var dreamer = {};
}

dreamer.Etsimano = (function() {


    Etsimano.prototype = new dreamer.DomainController();
    Etsimano.prototype.constructor = Etsimano;
    Etsimano.prototype.parent = dreamer.DomainController.prototype;

    function Etsimano() {
        console.log("Etsimano-Constructor");
    }


    Etsimano.prototype.setProperties = function(graph, args, layername) {

        var result = this.parent.setProperties.call(this, graph, args, layername);
        console.log("Etsimano-setProperties", JSON.stringify(args));

        if (result.error) {
            return result;
        }

        if (args.node) {

        }
        //console.log(JSON.stringify(graph));
        return result;
    }

    Etsimano.prototype.buildNodeProperties = function(ntype) { //TODO eliminare param inutili
        //console.log("Etsimano:buildNodeProperties");

        var property = this.parent.buildNodeProperties.call(this, ntype);
        if (ntype != undefined) {
            //console.log(ntype)
            for (p in this.spec.nodes[ntype]['properties']) {
                property[p] = JSON.parse(JSON.stringify(this.spec.nodes[ntype]['properties'][p]));
            }

            for (layer in this.spec['layer_constraints']) {

                if (this.isVisibleVertex(ntype, layer) && this.spec['layer_constraints'][layer]['nodes-properties']) {
                    if (!property['domain-Etsimano'])
                        property['domain-Etsimano'] = {}
                    property['domain-Etsimano']['layer-' + layer] = {};
                    for (p in this.spec['layer_constraints'][layer]['nodes-properties']) {
                        property['domain-Etsimano']['layer-' + layer][p] = JSON.parse(JSON.stringify(this.spec['layer_constraints'][layer]['nodes-properties'][p]));
                    }
                }

            }
        }

        return property;
    };


    Etsimano.prototype.getNodeProperties = function(node, nodes) {
        var info_data = this.parent.getNodeProperties.call(this, node, nodes);


        return info_data;
    };

    Etsimano.prototype.getNodeTypes = function() {
        //console.log("getNodeTypes Etsimano")
        return this.spec['list_of_all_node_types'];
    };

    Etsimano.prototype.getEdgeDataView = function(edg, layer){
                //#808080
        //console.log("EDGE", JSON.stringify(edg));
        var selected_color = "#CC0000";
        var closest_color = "#CCC000";
        var from_node_selected_color = "#0000C0";
        var default_color = "#000000";
        var color  = default_color;






        return {
            color: color
        };

    }

    Etsimano.prototype.getNodeDataView = function(node, is_closest, layer) {
        var empty_color = "#FFFFFF";
        var img = '/static/assets/img/punto.png';
        var bgcolor;
        var b_color = "#FFFFFF";
        var h_color = "#A8A8A8";
        var label = undefined;

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
/*
        var location_type = node.info.property.location_type
        //console.log("location_type", location_type);
        if(location_type != undefined){

            if(location_type == "Site")
                img = '/static/assets/img/location.png';

            else if(location_type == "Region")
                img = '/static/assets/img/location.png';
        }

        var role = node.info.property.role;

        if(role != undefined && role == "IPWanTransit"){
            img = '/static/assets/img/location.png';
        }

        */
        var nodeDView = {
            icon: img,
            bgcolor: bgcolor,
            label: label
        };


        return nodeDView;
    };


    Etsimano.prototype.getDomainData = function() {
        var domaindata = this.parent.getDomainData.call(this);
        return domaindata;

    };



    function getClusterColorBYId(cluster_id) {
        if (clustermap[cluster_id] != undefined)
            return clustermap[cluster_id];

        return undefined;
    };



    return Etsimano;

}(this));

if (typeof module === 'object') {
    module.exports = dreamer.Etsimano;
}