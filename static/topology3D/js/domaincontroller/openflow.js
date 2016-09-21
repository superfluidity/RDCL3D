if (typeof dreamer === 'undefined') {
    var dreamer = {};
}

dreamer.OpenFlow = (function () {

	

	OpenFlow.prototype = new dreamer.DomainController();
	OpenFlow.prototype.constructor = OpenFlow;
	OpenFlow.prototype.parent = dreamer.DomainController.prototype;
	function OpenFlow(){
		console.log("OpenFlow-Constructor");
	}


	OpenFlow.prototype.setProperties = function(graph, args, layername) {
		
		var result = this.parent.setProperties.call(this, graph, args, layername);
		//console.log("OpenFlow-setProperties");

		if(result.error){
			return result;
		}

		if (args.node) {
			 if (args.node.properties['domain-OpenFlow']){
			 	if(graph.vertices[args.node.index]){
	 				 	var n_dOpenFlow = graph.vertices[args.node.index].info.property['domain-OpenFlow'];
	 				 	for(key in args.node.properties['domain-OpenFlow']){
	 				 		//console.log(key)
	 				 		n_dOpenFlow[key] = args.node.properties['domain-OpenFlow'][key];
	 				 	}
	 				 }
	 			else{
	 				result["error"] = "error !!";
	 			}
			 }

			 if (args.node.properties.type){
	
			 		var newp = this.buildNodeProperties(args.node.properties.type);
                    for( p in newp){
                        graph.vertices[args.node.index].info['property'][p] = newp[p];
                    }
			 }
		}
		//console.log(JSON.stringify(graph));
		return result;
	}

	OpenFlow.prototype.buildNodeProperties = function(ntype){ //TODO eliminare param inutili
		//console.log("OpenFlow:buildNodeProperties");
		
		var property = this.parent.buildNodeProperties.call(this,ntype);
		if(ntype != undefined){
        	//console.log(ntype)
        	for(p in this.spec.nodes[ntype]['properties']){
         			property[p] = JSON.parse(JSON.stringify(this.spec.nodes[ntype]['properties'][p])); 

         	}
         	
         	for(layer in this.spec['layer_constraints'] ){

         		if(this.isVisibleVertex(ntype, layer) && this.spec['layer_constraints'][layer]['nodes-properties']){
         			if(!property['domain-OpenFlow'])
         				property['domain-OpenFlow'] = {}
         			property['domain-OpenFlow']['layer-'+layer] = {};
         			for(p in this.spec['layer_constraints'][layer]['nodes-properties']){
         				property['domain-OpenFlow']['layer-'+layer][p] = JSON.parse(JSON.stringify(this.spec['layer_constraints'][layer]['nodes-properties'][p]));
         			}
         		}
         
         	}
		}
		//console.log("property: " + JSON.stringify(property));
        return property;
    };


	OpenFlow.prototype.getNodeProperties = function(node, nodes){
		var info_data = this.parent.getNodeProperties.call(this,node, nodes);
		var ntype = node.getType();
		if(ntype != undefined){
        	info_data['type_info'] = {};

        	for(p in this.spec.nodes[ntype]['properties']){
         		if(p != "domain-OpenFlow"){
         			info_data['type_info'][p] = node['info']['property'][p];
         		}
         	}
         	info_data['model_info'] = {};
         	if(this.spec.nodes[ntype]['properties']["domain-OpenFlow"]){
         		//console.log("#####"+JSON.stringify(this.spec.nodes[ntype]['properties']["domain-OpenFlow"]));
         		for(p in this.spec.nodes[ntype]['properties']["domain-OpenFlow"]){
         			//console.log("dentrooo")
         		 	info_data['model_info'][p] = node['info']['property']["domain-OpenFlow"][p]
         		}
         	}

         	for(layer in this.spec['layer_constraints'] ){
         		if(this.isVisibleVertex(ntype, layer) && this.spec['layer_constraints'][layer]['nodes-properties']){
         			info_data['model_info']['layer-'+layer] = {};
         			for(p in this.spec['layer_constraints'][layer]['nodes-properties']){
         				if(node['info']['property']["domain-OpenFlow"] && node['info']['property']["domain-OpenFlow"]['layer-'+layer])
         					info_data['model_info']['layer-'+layer][p] = node['info']['property']["domain-OpenFlow"]['layer-'+layer][p];
         			}
         		}
         	}

		}

        return info_data;
    };

    OpenFlow.prototype.getNodeTypes = function() {
        //console.log("getNodeTypes OpenFlow")
        return this.spec['list_of_all_node_types'];
    };


    OpenFlow.prototype.getNodeDataView = function(node, is_closest, layer) {
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
    	var nodeDView = {icon: img, bgcolor: bgcolor};

    	if(node['info']['property'] != undefined && node['info']['property']['domain-OpenFlow'] != undefined){
    		
    		if(layer == "Control" ){
    			
    			if(node['info']['property']['domain-OpenFlow']['layer-'+layer] != undefined && node['info']['property']['domain-OpenFlow']['layer-'+layer]['cluster_id'] != undefined){
    				var cluster_id = node['info']['property']['domain-OpenFlow']['layer-'+layer]['cluster_id'];
    				var newcolor = getClusterColorBYId(cluster_id);
    				if(newcolor != undefined)
    					nodeDView.bgcolor = newcolor;
    			}
    		}
    	}

    	return nodeDView;
    };


    OpenFlow.prototype.getDomainData = function() {
        var domaindata = this.parent.getDomainData.call(this);

        //domaindata['clustermap'] = clustermap;

        return domaindata;

    };

    function getClusterColorBYId(cluster_id){
    	if(clustermap[cluster_id] != undefined)
    		return clustermap[cluster_id];
    	
    	return undefined;
    };

    return OpenFlow;

}(this));

if (typeof module === 'object') {
    module.exports = dreamer.OpenFlow;
}