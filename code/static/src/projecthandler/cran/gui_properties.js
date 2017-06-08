//***STEFANO
var example_gui_properties = {
   "v1":{
      "default":{
         "shape":"circle",
         "color":"#196B90",
         "label_color":"black",
         "size":30
      },
      "nodes":{
         "functional_block":{
            "property": "rfb-level",

                        "rfb/0":{
                            "shape":"triangle",
                            "color":"#1F77B4",
                            "size":20,
                            "name":"Functional Block"
                        },
                        "rfb/1":{
                            "shape":"square",
                            "color":"#1F77B4",
                            "size":20,
                            "name":"Functional Block"
                        }





         },

         "cran/epcbox":{
            //"shape":"circle",
            "image":"cran-epcbox.png",
            "color":"#17BECF",
            "size":40,
            "name":"EPC_BOX"
         },
         "cran/rrh":{
            //"shape":"circle",
            "image":"cran-rrh.png",
            "color":"#BCBD22",
            "size":40,
            "name":"RRH"
         },
         "cran/bbu":{
            //"shape":"circle",
            "image":"cran-bbu.png",
            "color":"#E377C2",
            "size":40,
            "name":"BBU"
         },
         "fhaul/fw_switch":{
            //"shape":"circle",
            "image":"fhaul-fw-switch.png",
            "color":"#7F7F7F",
            "size":40,
            "name":"FW Switch"
         },
         "fhaul/h2h_switch":{
            //"shape":"circle",
            "image":"fhaul-h2h-switch.png",
            "color":"#D62728",
            "size":40,
            "name":"H2H Switch"
         },
         "fhaul/p2p_switch":{
            //"shape":"circle",
            "image":"fhaul-p2p-switch.png",
            "color":"#8C564B",
            "size":40,
            "name":"P2P Switch"
         },
         "fhaul/sdn_ctrl":{
            "image" : "ofcontroller.png",
            //"shape":"circle",
            "color":"#8C564B",
            "size": 30,
            "name":"Sdn Controller"
         }
      },
      "edges":{
        "hierarchical":{
            "color": "blue"
        },
        "same_level":{
            "color": "red"
        },
        "unrecognized":{
            "color": "red"
        }
      },
      "graphs":null
   }
};