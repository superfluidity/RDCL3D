# Network Service Descriptor

The Network Service Descriptor contains the values that are defined in ETSI MANO specification

Sub set of NSD base element 

| Identifier            | Type      | Cardinality | Description                                                                                                                                                                                                                                                                                                                   |
|-----------------------|-----------|:-------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Id                    | Leaf      | 1           | ID of this NSD                                                                                                                                                                                                                                                                                                                |
| vendor                | Leaf      | 1           | Provider or vendor of the NSD                                                                                                                                                                                                                                                                                                 |
| vnfd                  | Reference | 1 ... N     | VNF which is part of the Network Service. A Network Service might have multiple graphs, for example, for:  1. Control plane traffic.  2. Management-plane traffic.  3. User plane traffic itself could have multiple NFPs based on the QOS etc.  The traffic is steered amongst 1 of these NFPs based on the policy decisions |
| vld                   | Reference | 0 ... N     | List of Virtual Link which are part of NS                                                                                                                                                                                                                                                                                     |
| vnf_dependency        | Leaf      | 0 ... N     | List of dependencies between VNF                                                                                                                                                                                                                                                                                              |
| monitoring_ parameter | Leaf      | 0 ... N     | List of monitoring parameter which can be tracked for this NS.                                                                                                                                                                                                                                                                |
| version               | Leaf      | 1           | Version of the Network Service Descriptor.                                                                                                                                                                                                                                                                                    |


VNF Dependencies

| Identifier | Type | Cardinality | Description                                                                           |
|------------|------|:-------------:|---------------------------------------------------------------------------------------|
| source     | Leaf | 1           | The name of the VirtualNetworkFunctionDescriptor that provides one or more parameters |
| target     | Leaf | 1           | The name of the VirtualNetworkFunctionDescriptor that provides one or more parameters |
| parameters | Leaf | 0 ... N     | List of name of the parameters that the target requires                               |