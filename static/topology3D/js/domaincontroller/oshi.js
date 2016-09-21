if (typeof dreamer === 'undefined') {
    var dreamer = {};
}

dreamer.Oshi = (function () {

	var clustermap ={
		"1": "red",
		"2": "blue",
		"3": "orage",
		"4": "yellow",
		"5": "green",
		"6": "gray",
		"7": "black",
		"8": "brown",
		"9": "cyan",
		"10": "magenta"
	};

	Oshi.prototype = new dreamer.DomainController();
	Oshi.prototype.constructor = Oshi;
	Oshi.prototype.parent = dreamer.DomainController.prototype;
	function Oshi(){
		console.log("OSHI-Constructor");
	}


	Oshi.prototype.setProperties = function(graph, args, layername) {
		
		var result = this.parent.setProperties.call(this, graph, args, layername);
		//console.log("Oshi-setProperties");

		if(result.error){
			return result;
		}

		if (args.node) {
			 if (args.node.properties['domain-oshi']){
			 	if(graph.vertices[args.node.index]){
	 				 	var n_doshi = graph.vertices[args.node.index].info.property['domain-oshi'];
	 				 	for(key in args.node.properties['domain-oshi']){
	 				 		//console.log(key)
	 				 		n_doshi[key] = args.node.properties['domain-oshi'][key];
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

	Oshi.prototype.buildNodeProperties = function(ntype){ //TODO eliminare param inutili
		//console.log("Oshi:buildNodeProperties");
		
		var property = this.parent.buildNodeProperties.call(this,ntype);
		if(ntype != undefined){
        	//console.log(ntype)
        	for(p in this.spec.nodes[ntype]['properties']){
         			property[p] = JSON.parse(JSON.stringify(this.spec.nodes[ntype]['properties'][p])); 
         	}
         	
         	for(layer in this.spec['layer_constraints'] ){

         		if(this.isVisibleVertex(ntype, layer) && this.spec['layer_constraints'][layer]['nodes-properties']){
         			if(!property['domain-oshi'])
         				property['domain-oshi'] = {}
         			property['domain-oshi']['layer-'+layer] = {};
         			for(p in this.spec['layer_constraints'][layer]['nodes-properties']){
         				property['domain-oshi']['layer-'+layer][p] =  JSON.parse(JSON.stringify(this.spec['layer_constraints'][layer]['nodes-properties'][p]));  
         			}
         		}
         
         	}
		}
		//console.log("property: " + JSON.stringify(property));
        return property;
    };


	Oshi.prototype.getNodeProperties = function(node, nodes){
		//console.log("Oshi:getNodeProperties");
		//console.log(node instanceof dreamer.Vertex);
		//console.log("spec: " + JSON.stringify(this.spec.nodes));
		var info_data = this.parent.getNodeProperties.call(this,node, nodes);
		var ntype = node.getType();
		if(ntype != undefined){
        	info_data['type_info'] = {};

        	for(p in this.spec.nodes[ntype]['properties']){
         		if(p != "domain-oshi"){
         			info_data['type_info'][p] = node['info']['property'][p];
         		}
         	}
         	info_data['model_info'] = {};
         	if(this.spec.nodes[ntype]['properties']["domain-oshi"]){
         		//console.log("#####"+JSON.stringify(this.spec.nodes[ntype]['properties']["domain-oshi"]));
         		for(p in this.spec.nodes[ntype]['properties']["domain-oshi"]){
         			//console.log("dentrooo")
         		 	info_data['model_info'][p] = node['info']['property']["domain-oshi"][p]
         		}
         	}

         	for(layer in this.spec['layer_constraints'] ){
         		if(this.isVisibleVertex(ntype, layer) && this.spec['layer_constraints'][layer]['nodes-properties']){
         			info_data['model_info']['layer-'+layer] = {};
         			for(p in this.spec['layer_constraints'][layer]['nodes-properties']){
         				if(node['info']['property']["domain-oshi"] && node['info']['property']["domain-oshi"]['layer-'+layer])
         					info_data['model_info']['layer-'+layer][p] = node['info']['property']["domain-oshi"]['layer-'+layer][p];
         			}
         		}
         	}

		}

        return info_data;
    };

    Oshi.prototype.getNodeDataView = function(node, is_closest, layer) {
    	
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
    	
    	if(node['info']['property'] != undefined && node['info']['property']['domain-oshi'] != undefined){
    		
    		if(layer == "Control" ){
    			
    			if(node['info']['property']['domain-oshi']['layer-'+layer] != undefined && node['info']['property']['domain-oshi']['layer-'+layer]['cluster_id'] != undefined){
    				var cluster_id = node['info']['property']['domain-oshi']['layer-'+layer]['cluster_id'];
    				var newcolor = getClusterColorBYId(cluster_id);
    				if(newcolor != undefined)
    					nodeDView.bgcolor = newcolor;
    			}
    		}
    	}

    	return nodeDView;
    };

    Oshi.prototype.getNodeTypes = function() {
       
        return this.spec['list_of_all_node_types'];
    
    };

    Oshi.prototype.getDomainData = function() {
        var domaindata = this.parent.getDomainData.call(this);

        domaindata['clustermap'] = clustermap;

        return domaindata;

    };

    function getClusterColorBYId(cluster_id){
    	if(clustermap[cluster_id] != undefined)
    		return clustermap[cluster_id];
    	
    	return undefined;
    };

    return Oshi;

}(this));

if (typeof module === 'object') {
    module.exports = dreamer.Oshi;
}