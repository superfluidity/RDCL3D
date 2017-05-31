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
            "shape":"circle",
            "color":"#1F77B4",
            "size":20,
            "name":"Functional Block"
         },

         "cran/epcbox":{
            "shape":"circle",
            "color":"#17BECF",
            "size":20,
            "name":"EPC_BOX"
         },
         "cran/rrh":{
            "shape":"circle",
            "color":"#BCBD22",
            "size":20,
            "name":"RRH"
         },
         "cran/bbu":{
            "shape":"circle",
            "color":"#E377C2",
            "size":20,
            "name":"BBU"
         },
         "fhaul/fw_switch":{
            "shape":"circle",
            "color":"#7F7F7F",
            "size":20,
            "name":"FW Switch"
         },
         "fhaul/h2h_switch":{
            "shape":"circle",
            "color":"#D62728",
            "size":20,
            "name":"H2H Switch"
         },
         "fhaul/p2p_switch":{
            "shape":"circle",
            "color":"#8C564B",
            "size":20,
            "name":"P2P Switch"
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