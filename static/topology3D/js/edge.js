if (typeof dreamer === 'undefined') {
    var dreamer = {};
}

dreamer.Edge = (function (global) {
    'use strict';
    // Constructor
    function Edge(node1, node2, layer, links) {
        this.node1 = node1;
        this.node2 = node2;
        this.links = [];
        
        if(links && (links instanceof Array)){
            this.links = links;
        }
        else if (links && (typeof links  === "object")) {
           // var val = (links.layer==null || links.layer==="") ? "": links.layer;
           // var edlab = (links.edge_label == null || links.edge_label === "") ? "": links.edge_label;
            this.links.push( new dreamer.Link(links.edge_label, links.layer));
        } 
        else if (layer != undefined){
            //var val = (vll==null || vll===false) ? false: true;
            this.links.push( new dreamer.Link("", layer));
        }
    }



    Edge.prototype.is_touching = function (node) {
        return node === this.node1 || node === this.node2;
    };
    
    Edge.prototype.hasLink = function (layer) {
        for (var l in this.links) {
                console.log("link "+ l);
                if(layer === this.links[l].layer)
                    return true;
        };
        return false;
    };

    Edge.prototype.existBetween= function(n1, n2,layer){
        if((n1 === this.node1 && n2 === this.node2) || (n2 === this.node1 && n1 === this.node2)){
            return true
        }
        return false;
    };

    Edge.prototype.is_loop = function (node) {
        return node === this.node1 && node === this.node2;

    };
    Edge.prototype.connects_to = function (node) {
        var neighbor;
        if (this.node1 === node) {
            neighbor = this.node2;
        }
        if (this.node2 === node) {
            neighbor = this.node1;
        }
        return neighbor;
    };
    Edge.prototype.get_nodes = function () {
        return {
            node1: this.node1,
            node2: this.node2
        };
    };
    
    Edge.prototype.addLink = function (edge_label, layer, properties) {
       this.links.push(new dreamer.Link(edge_label, layer, properties));
    };

    Edge.prototype.setLinkList = function(conlist){
        if(conlist != undefined)
            this.links = conlist.slice(0);
    }



    return Edge;

}(this));

if (typeof module === 'object') {
    module.exports = dreamer.Edge;
}