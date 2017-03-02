# RDCL 3D - RFB Description and Composition Languages Design, Deploy and Direct 

RDCL 3D is a web framework for the design of NFV services and components. The framework allows editing,
validating, visualizing the descriptors of services and components both textually and graphically.

The platform is designed with a modular approach, allowing developers to "plug in" the support for new models (project types).
Currently supported project types are:

* ETSI Release 2 NS and VNF descriptors
* TOSCA Simple Profile for NFV
* Click modular router configurations
* Superfluidity-ETSI (ETSI R2 + Click)

A demo version of RDCL 3D is online [here](http://rdcl-demo.netgroup.uniroma2.it/).

Please find [below](#installation) the instructions on how to install and run your version of RDCL 3D.

## Documentation & publications

Documentation is available in the docs folder of this repository. 

S.Salsano, F. Lombardo, C. Pisa, P. Greto, N. Blefari Melazzi, "RDCL 3D, a Model Agnostic Web Framework for the Design of Superfluid NFV Services and Components", Submitted paper, February 2017 ([pdf on Arxiv](https://arxiv.org/pdf/1702.08242))

## Community

The mailing list [rdcl3d@googlegroups.com](mailto:rdcl3d@googlegroups.com) is available for architecture and design discussions,
requests for help, features request, bug reports...

To join the list, just send an email to [rdcl3d+subscribe@googlegroups.com](mailto:rdcl3d+subscribe@googlegroups.com) or [join with a gmail account](https://groups.google.com/forum/#!forum/rdcl3d)

## Aknowledgements

This work has been performed in the context of the project Superfluidity, which received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 671566

## Installation

Caveat: the code is released as an alpha version. Development is in progress, so you may expect bugs and frequent
code refactorings. Use it at your own risk. 

### Docker installation

#### To build RDCL 3D:
1) Clone the project from repository with ssh:


    $ git clone git@github.com:superfluidity/RDCL3D.git
    
or https:

    $ git clone https://github.com/superfluidity/RDCL3D.git


2) Build the image from the project's root directory:


    $ docker build -t rdcl3d -f code/docker/Dockerfile .

#### To launch RDCL 3D:


    $ docker run -p8000:8000 --name rdcl3d0 rdcl3d


### Manual Installation

See documentation for manual installation [here](code/manual_install.md)


## License

   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.