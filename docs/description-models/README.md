# Description model
The description model includes the types of nodes and links that are supported, their relationships, the constraints in their composition, describes what are the different views of the projects and which nodes and links belongs to which view.

The model is composed of four sections: 

```
nodes:            #List of nodes, with id and label used in the gui (We can add more fields)
layer:            #List of Layers
action:           #Actions to show on rightclick on a node/link
callback:         #List of callbacks used
```


## Details
### List of nodes
In the description model you can define the list of nodes and for each of them you can define the label which will be displayed on the gui, for example in the ETSI model:
```
nodes:                                  #List of nodes, with id and label used in the gui (We can add more fields)
    vnf:
        label: VNF
    ns_vl:
        label: VL
    ns_cp:
        label: SAP
    vnf_vl:
        label: intVL
    vnf_vdu:
        label: VduCP
    vnf_ext_cp:
        label: ExtCP
    vnf_vdu_cp:
        label: VDU
```
### List of layer
Inside the ```layer``` object you can define the list of layers and for each of them which types of nodes you want to be displayed in that layer, and if they can be added/removed:

*   For each node the value of the attribute ```addable``` is the callback that will be called when the that node will be added.
*   For each node the value of the attribute ```removable``` is the callback that will be called when the that node will be removed.
*   For each node the value of the attribute ```expands``` is the layer in which the node will expands the a double click on it.

```
layer:            #List of Layers
    ns:
        nodes:                  #List of node to be visualized in the current layer
            vnf:
                addable:
                    callback: addVnf
                removable:
                    callback: removeNode
                expands : vnf           # With the double click the node will expands in the specified layer
            ns_vl:
                addable:
                    callback: addNode
                removable:
                    callback: removeNode
            ns_cp:
                addable:
                    callback: addNode
                removable:
                    callback: removeNode
```
In each layer you can specify what edges are allowed, and for each of them you can specify:

* The callback that will call when that link will be made.
* The callback that will call when that link will be removed.
* If the link is directed or else.

```
layer:            #List of Layers
    ns:
        allowed_edges:                  #List of allowed edges between the layer's nodes
                    vnf:                        #Edge's source
                        destination:            #List of edge's destination with the list of controls callback id to call when there is a connections
                            ns_vl:
                                callback: linkVnftoNsVl
                                direct_edge: false
                                removable:
                                    callback: removeLink
                            ns_cp:
                                callback: linkVnftoNsCp
                                direct_edge: false
                                removable:
                                    callback: removeLink
```
For each layer, in the ```action``` object, you can specify customized action and the related callback to be executed when the user triggers a right click on the link/node in that layer.


```
layer:            #List of Layers
    ns:
        action:           #Action to show on rightclick all types of node/link
            node:
                addToCurrentVNFFG:
                    title: Add to current VNFFG
                    callback: addToCurrentVNFFG
            link:
```
### List of callbacks
In this object you have to specify each callback used in all the previous attributes and the related JavaScript class and the file which contains that class.

```
callback:                             #List of callbacks used
  chooseVnfExp:
      file: etsi_controller.js
      class: EtsiController
```