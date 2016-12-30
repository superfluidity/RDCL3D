if (typeof dreamer === 'undefined') {
    var dreamer = {};
}
var level = {}

dreamer.EtsiController = (function(global) {
    'use strict';

    var DEBUG = true;

    EtsiController.prototype.constructor = EtsiController;

    /**
     * Constructor
     */
    function EtsiController(args) {


    }

   EtsiController.prototype.addVnf= function(self, args, success, error){
        if (args.existing_vnf) {
            new dreamer.GraphRequests().addNode(args, null, function() {
                    self.parent.addNode.call(self, args);
                    if (success)
                        success();
                });

        } else {
            new dreamer.GraphRequests().addNode(args, null, function() {
                self.parent.addNode.call(self, args);
                var vnf_ext_cp = {
                    'id': 'vnf_ext_cp' + "_" + args.id,
                    'info': {
                        'type': 'vnf_ext_cp',
                        'group': [args.id]
                    },
                    'x': args.x,
                    'y': args.y
                }
                new dreamer.GraphRequests().addNode(vnf_ext_cp, null, function() {
                    self.parent.addNode.call(self, vnf_ext_cp);
                    if (success)
                        success();
                });
            });
        }

    };

    EtsiController.prototype.addNode= function(self, args, success, error){
       new dreamer.GraphRequests().addNode(args, null, function() {
                self.parent.addNode.call(self, args);
                if (success)
                    success();
            });
    };


     EtsiController.prototype.addVnfVdu= function(self, args, success, error){
       new dreamer.GraphRequests().addNode(args, null, function() {
                self.parent.addNode.call(self, args);
                var vdu_id = args.id;
                var vnf_vdu_cp = {
                    'id': 'vnf_vdu_cp' + "_" + generateUID(),
                    'info': {
                        'type': 'vnf_vdu_cp',
                        'group': [args.info.group[0]]
                    },
                    'x': args.x - (args.x * 0.1),
                    'y': args.y - (args.y * 0.1)
                }
                new dreamer.GraphRequests().addNode(vnf_vdu_cp, vdu_id, function() {
                    self.parent.addNode.call(self, vnf_vdu_cp);
                    var link = {
                        source: args.id,
                        target: vnf_vdu_cp.id,
                        view: self.filter_parameters.link.view[0],
                        group: [args.info.group[0]],
                    };
                    self.parent.addLink.call(self, link);
                    if (success)
                        success();
                });

            });
    };

     EtsiController.prototype.addVnfVduCp= function(self, args, success, error){
       var vnf_id = args.info.group[0];
            var vnf_vdus = $.grep(self.d3_graph.nodes, function(e) {
                return (e.info.group.indexOf(vnf_id) >= 0 && e.info.type == 'vnf_vdu');
            });
            if (success)
                success();
            if (typeof vnf_vdus == 'undefined' || vnf_vdus.length <= 0) {
                alert('You should add a VDU')
            } else {
                showChooserModal('Select the VDU to link', vnf_vdus, function(choice) {
                    new dreamer.GraphRequests().addNode(args, choice, function() {
                        self.parent.addNode.call(self, args);
                        var link = {
                            source: args.id,
                            target: choice,
                            view: self.filter_parameters.link.view[0],
                            group: [args.info.group[0]],
                        };

                        self.parent.addLink.call(self, link);

                        $('#modal_create_link_chooser').modal('hide');
                    });
                });
            }
    };

    return EtsiController;


}(this));

if (typeof module === 'object') {
    module.exports = dreamer.EtsiController;
}