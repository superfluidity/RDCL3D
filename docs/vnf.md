# Virtual network function descriptor

## Sub set of VNFD base element 

| Identifier            | Type      | Cardinality | Description                                                                                                                                                                                                                                                                                                                   |
|-----------------------|-----------|:-------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Id                    | Leaf      | 1           | ID of this VNFD.                                                                                                                                                                                                                                                                                                              |
| vendor                | Leaf      | 1           | Vendor of the VNFD.                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                                                                                   
| version               | Leaf      | 1           | Version of the Network Service Descriptor.                                                                                                                                                                                                                                                                                    |
| vdu                   | Element   | 1 ... N     | List of elements related to a particular VDU                                                                                                                                                                                                                                                                                  |
| virtual_link          | Element   | 0 ... N     | List of elements that represent the type of network connectivity between two or more CP                                                                                                                                                                                                                                       |                           
| connection_point      | Element   | 1 ... N     | List of elements that describe an external interface                                                                                                                                                                                                                                                                          |
| monitoring_ parameter | Leaf      | 0 ... N     | List of monitoring parameter which can be tracked for this VNF.                                                                                                                                                                                                                                                               |


### Virtual Deployment Unit

| Identifier            | Type      | Cardinality | Description                                                                                                                                                                                                                                                                                                                   |
|-----------------------|-----------|:-------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Id                    | Leaf      | 1           | ID of this VDU.                                                                                                                                                                                                                                                                                                              |
| vm_image              | Leaf      | 0 ... 1     | Reference to a VM Image.                                                                                                                                                                                                                                                                                                     |                                                                                                                                                                                                                                   
| virtual_network_bandwidth_resource| Leaf  | 1   | This represents the requirements in terms of the virtual network bandwidth needed for the VDU.      |
| lifecycle_event       | Leaf      | 0 ... N     | List of functional scripts/workflows for specific lifecycle events (e.g. initialization, termination, graceful shutdown, scaling out/in) |
| scale_in_out          | Leaf      | 0 ... 1     | Define the minimum and maximum number of istances which can be created to support scale out/in. |
| vnfc                  | Element   | 1 ... N     | List of VNFComponents which will be deployed for this VNFD. |
| monitoring_parameter  | Leaf      | 0 ... N     | Monitoring parameter, which can be tracked for VNFC based on this VDU |


### VNF Component

| Identifier            | Type      | Cardinality | Description                                                      |
|-----------------------|-----------|:-----------:|--------------------------------------------------------------------|
| Id                    | Leaf      | 1           | VNFC identification within the namespace of a specific VNF        |
| connection_point      | Element   | 1 ... N     | Connection point is a reference to an Internal Virtual Link       |


#### Connection Point

| Identifier            | Type      | Cardinality | Description                                                      |
|-----------------------|-----------|:-----------:|--------------------------------------------------------------------|
| Id                    | Leaf      | 1           | VNFC identification within the namespace of a specific VNF        |
| virtual_link_reference | Reference   | 1      | Connection point is a reference to an Internal Virtual Link       |
