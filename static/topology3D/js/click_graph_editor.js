if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.ClickGraphEditor = (function(global) {
    'use strict';

    var DEBUG = true;
    var SHIFT_BUTTON = 16;

    ClickGraphEditor.prototype = new dreamer.GraphEditor();
    ClickGraphEditor.prototype.constructor = ClickGraphEditor;
    ClickGraphEditor.prototype.parent = dreamer.GraphEditor.prototype;

    /**
     * Constructor
     */
    function ClickGraphEditor(args) {

        log("Constructor");

    } 


    function get_d3_symbol(myString) {
        switch(myString) {
            case "circle":
                return d3.symbolCircle;
            break;
            case "square":
                return d3.symbolSquare;
            break;
            case "diamond":
                return d3.symbolDiamond;
            break;
            case "triangle":
                return d3.symbolTriangle;
            break;
            case "star":
                return d3.symbolStar;
            break;
            case "cross":
                return d3.symbolCross;
            break;
            default:
        // if the string is not recognized
            return d3.symbolCross;
            //return d3.symbolCircleUnknown;
        } 

    }



    ClickGraphEditor.prototype.init = function(args){
         this.parent.init.call(this, args);
         this.current_vnffg = null;


        this.type_property = {};
        this.type_property["unrecognized"] = args.gui_properties["default"];
        this.type_property["unrecognized"]["default_node_label_color"] = args.gui_properties["default"]["label_color"];
        this.type_property["unrecognized"]["shape"] = d3.symbolCross;

        Object.keys(args.gui_properties["nodes"]).forEach(function(key,index) {

            this.type_property[key]=args.gui_properties["nodes"][key];
            this.type_property[key]["shape"] = get_d3_symbol (this.type_property[key]["shape"]);

        },this);
        var self = this;
        d3.json("graph_data/"+args.descriptor_id, function(error, data) {
            console.log(data)
            self.d3_graph.nodes = data.vertices;
            self.d3_graph.links = data.edges;
            self.d3_graph.graph_parameters = data.graph_parameters;
            self.refreshGraphParameters();
            self.refresh();
            self.startForce();
            setTimeout(function(){ self.handleForce(self.forceSimulationActive); }, 500);

        });

    }



    /**
     * Update the data properties of the node
     * @param {Object} Required. An object that specifies tha data of the node.
     * @returns {boolean}
     */
    ClickGraphEditor.prototype.updateDataNode = function(args) {
        this.parent.updateDataNode.call(this, args);
    };




    ClickGraphEditor.prototype.savePositions = function(data) {
        var vertices = {}
        this.node.each(function(d) {
            vertices[d.id] = {}
            vertices[d.id]['x'] = d.x;
            vertices[d.id]['y'] = d.y;
        });
        new dreamer.GraphRequests().savePositions({'vertices': vertices});

    }

    /**
     *  Internal functions
     */

    /**
     *
     *
     */
    ClickGraphEditor.prototype._setupBehaviorsOnEvents = function() {
        log("_setupBehaviorsOnEvents");
        var self = this;
        this.behavioursOnEvents = {
            'nodes': {
                'click': function(d) {

                    d3.event.preventDefault();

                    if (self.lastKeyDown == SHIFT_BUTTON && self._selected_node != undefined) {
                        self.addLink(self._selected_node, d);
                    } else {
                        self._selectNodeExclusive(this, d);
                    }

                },
                'mouseover': function(d) {
                    self.link.style('stroke-width', function(l) {
                        if (d === l.source || d === l.target)
                            return 4;
                        else
                            return 2;
                    });
                },
                'mouseout': function(d) {
                    self.link.style('stroke-width', 2);
                },
                'dblclick': function(c_node) {
                    d3.event.preventDefault();
                    log('dblclick ');
                    if(c_node.info.type!= undefined){



                    }

                },
                'contextmenu':  d3.contextMenu([
                    {
                        title: 'Edit',
                        action: function(elm, d, i) {
                            if(d.info.type!= undefined){
                                if(d.info.type == 'vnf'){
                                    window.location.href='/projects/'+self.project_id+'/descriptors/vnfd/'+d.id;

                                }else{
                                    window.location.href='/projects/'+self.project_id+'/descriptors/'+graph_editor.getCurrentView()+'d/'+graph_editor.getCurrentGroup();

                                }
                             }
                        }

                    },
                ])
            },
            'links': {
                'click': function(d) {
                     self._selectLinkExclusive(this, d);

                },
                'dblclick': function(event) {

                },
                'mouseover': function(d) {
                    d3.select(this).style('stroke-width', 4);
                },
                'mouseout': function(d) {
                    if(d != self._selected_link)
                        d3.select(this).style('stroke-width', 2);
                },
                'contextmenu': d3.contextMenu([
                    {
                        title: 'Delete Link',
                        action: function(elm, link, i) {
                            self.removeLink(link);
                        }

                    }
                ])
            }
        };
    };

    ClickGraphEditor.prototype.exploreLayer = function(args) {

    };

    ClickGraphEditor.prototype.getTypeProperty = function(){
        return this.type_property;
    };

    ClickGraphEditor.prototype.getCurrentGroup = function(){
        return this.filter_parameters.node.group[0];

    }
     ClickGraphEditor.prototype.getCurrentView = function(){
        return this.filter_parameters.link.view[0];

    }
    ClickGraphEditor.prototype.refreshGraphParameters = function(){
      //  setVnffgIds(this.d3_graph.graph_parameters.vnffgIds)
    }
    ClickGraphEditor.prototype.getVnffgParameter = function(){
        return this.d3_graph.graph_parameters.vnffgIds;
    }



    /**
     * Log utility
     */
    function log(text) {
        if (DEBUG)
            console.log("::ClickGraphEditor::", text);
    }



    return ClickGraphEditor;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.ClickGraphEditor;
}