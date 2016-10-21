if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.ManoGraphEditor = (function(global) {
    'use strict';

    var DEBUG = true;
    ManoGraphEditor.prototype = new dreamer.GraphEditor();
    ManoGraphEditor.prototype.constructor = ManoGraphEditor;
    ManoGraphEditor.prototype.parent = dreamer.GraphEditor.prototype;

    /**
     * Constructor
     */
    function ManoGraphEditor(args) {

        log("Constructor");

    }


    /**
     * Add a new node to the graph.
     * @param {Object} Required. An object that specifies tha data of the new node.
     * @returns {boolean}
     */
    ManoGraphEditor.prototype.addNode = function(args) {
        this.parent.addNode.call(this, args);
    };

    /**
     * Update the data properties of the node
     * @param {Object} Required. An object that specifies tha data of the node.
     * @returns {boolean}
     */
    ManoGraphEditor.prototype.updateDataNode = function(args) {
        this.parent.updateDataNode.call(this, args);
    };

    /**
     * Remove a node from graph and related links.
     * @param {String} Required. Id of node to remove.
     * @returns {boolean}
     */
    ManoGraphEditor.prototype.removeNode = function(node_id) {
        this.parent.removeNode.call(this, node_id);
    };

    /**
     * Add a new link to graph.
     * @param {Object} Required. An object that specifies tha data of the new Link.
     * @returns {boolean}
     */
    ManoGraphEditor.prototype.addLink = function(link) {
        this.parent.addLink.call(this, link);
    };

    /**
     * Remove a link from graph.
     * @param {String} Required. The identifier of link to remove.
     * @returns {boolean}
     */
    ManoGraphEditor.prototype.removeLink = function(link_id) {
        this.parent.removeLink.call(this, link_id);
    };


    /**
     *  Internal functions
     */

    /**
     *
     *
     */
    ManoGraphEditor.prototype._setupBehaviorsOnEvents = function() {
        log("_setupBehaviorsOnEvents");
        this.behavioursOnEvents = {
            'nodes': {
                'click': function(event) {

                },
                'dblclick': function(event) {

                },
                'contextmenu': function(event){

                }
            },
            'links': {
                'click': function(event) {

                },
                'dblclick': function(event) {

                }
            }
        };
    };

    /**
     *  Deselect previously selected nodes
     *
     */
    ManoGraphEditor.prototype._deselectAllNodes = function() {
        log("_deselectAllNodes");
        this.node.classed("node_selected", false);
        this._selected_node = undefined;
    };

    /**
     *  Select node in exclusive mode
     *  @param {Object} Required. Element selected on click event
     */
    ManoGraphEditor.prototype._selectNodeExclusive = function(node_instance, node_id) {
        log("_selectNodeExclusive ");
        var activeClass = "node_selected";
        var alreadyIsActive = d3.select(node_instance).classed(activeClass);
        this._deselectAllNodes();
        d3.select(node_instance).classed(activeClass, !alreadyIsActive);
        this._selected_node = (alreadyIsActive) ? undefined : node_id;
    };

    /**
     * Log utility
     */
    function log(text) {
        if (DEBUG)
            console.log("::ManoGraphEditor::", text);
    }



    return ManoGraphEditor;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.ManoGraphEditor;
}