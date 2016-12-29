=====
How to create a new project type
=====

The RDCL 3D architecture is based on the concept of *project types*. Each RDCL 3D project belongs to a project type.
The project type specifies which types of files can be handled by the project (e.g. for the "Etsi" project type 
we have Network Service Descriptors files and VNF Descriptors files). The project type specifies which *graph views* are supported.
A graph view is a GUI representation of some aspects of the project (or of a subset of the project). A graph view
can correspond to a file type, but this is not always true, because in general there can be multiple graph views
associated to the same file type or there can be file types that do not have a corresponding graph view.
For example for the "Etsi" project type we have the NSD graph view that describes a given Network Service and the VNFD
graph view that describes the internal of a VNF.

| Base class for project types: ``Project``, module: ``projecthandler/models.py``  
| Derived classes: ``ProjectTypeProject``, module: ``projecthandler/project_type_model.py``  

The RDCL 3D server side logic builds the graph representations starting from the descriptor files.
In general, the approach is to create a comprehensive graph representation (e.g. includind the whole 
project) and then to represent subsets of this graph by proper filtering. A *graph view* can be seen
as a filter on the overall graph representation.

Base class for GUI graph representation: ``RdclGraph``, module: ``lib/rdcl_graph.py``
Derived classes: ``ProjectTypeRdclGraph``, module ``lib/project_type/project_type_rdcl_graph.py`` 

Base class for parsing descriptors: ``Parser``, module: ``lib/parser.py``
Derived classes: ``ProjectTypeParser``, module ``lib/project_type/project_type_parser.py``

Server side (python django)
-----------

HTML templates
--------------

Client side (javascript)
-----------



Syntax examples (to be deleted...)
---------------
Example of code block: ::

    git clone https://github.com/openstack/heat-translator
    cd heat-translator
    sudo python setup.py install

Example of monospaced text: ``--template-file``. Example of italic text *this is italic*. Example of bold text: **this is bold**

