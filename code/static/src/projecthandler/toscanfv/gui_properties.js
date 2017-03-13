//***STEFANO
var example_gui_properties = {
  "v1" : { 
    "default": {
      "shape": "cross",
      "color": "#42f44e",
      "label_color": "black",
      "size": 15
    },
    "nodes": {
      "tosca.nodes.nfv.VNF":{
        "image": "vnf-100.png",
        // "shape": "square",
        "color": "#54A698",
        "size": 35,
        "name": "tosca.nodes.nfv.VNF"
      },
      "tosca.nodes.nfv.VDU": {
        "shape": "square",
        //"color": "#50A7CC",
        "color": "#54A698",
        "size": 18,
        "name": "tosca.nodes.nfv.VDU"
      },
      "tosca.nodes.nfv.CP": {
        "image" : "cp-80.png",
        // "shape": "circle",
        "color": "#F27220",
        "size": 20,
        "name": "tosca.nodes.nfv.CP"
      },
      "tosca.nodes.nfv.VL": {
         "image" : "vl-80.png",
        // "shape": "triangle",
        "color": "#196B90",
        "size": 20,
        "name": "tosca.nodes.nfv.VL"
      },
      "tosca.nodes.nfv.VL.ELine": {
         "image" : "vl-80.png",
        // "shape": "triangle",
        "color": "#196B90",
        "size": 20,
        "name": "tosca.nodes.nfv.VL.ELine"
      },
      "tosca.nodes.nfv.VL.ELAN": {
         "image" : "vl-80.png",
        // "shape": "triangle",
        "color": "#196B90",
        "size": 20,
        "name": "tosca.nodes.nfv.VL.ELAN"
      },
      "tosca.nodes.nfv.VL.ETree": {
         "image" : "vl-80.png",
        // "shape": "triangle",
        "color": "#196B90",
        "size": 20,
        "name": "tosca.nodes.nfv.VL.ETree"
      },
      "tosca.nodes.nfv.FP": {
        "shape": "square",
        "color": "#54A698",
        "size": 35,
        "name": "tosca.nodes.nfv.FP"
      }
    },
    "graphs": null
  },

}