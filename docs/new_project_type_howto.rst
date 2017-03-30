=================================
How to create a new project type
=================================

The RDCL 3D architecture is based on the concept of *project types*. Each RDCL 3D project belongs to a project type.
The project type specifies which types of files can be handled by the project (e.g. for the "Etsi" project type
we have Network Service Descriptors files and VNF Descriptors files). The project type specifies which *graph views* are supported.
A graph view is a GUI representation of some aspects of the project (or of a subset of the project). A graph view
can correspond to a file type, but this is not always true, because in general there can be multiple graph views
associated to the same file type or there can be file types that do not have a corresponding graph view.
For example for the "Etsi" project type we have the NSD graph view that describes a given Network Service and the VNFD
graph view that describes the internal of a VNF.

The RDCL 3D server side logic builds the graph representations starting from the descriptor files.
In general, the approach is to create a comprehensive graph representation (e.g. includind the whole
project) and then to represent subsets of this graph by proper filtering. A *graph view* can be seen
as a filter on the overall graph representation.

|
| Base class for project types: ``Project``, module: ``projecthandler/models.py``
| Derived classes: ``ProjectTypeProject``, module: ``projecthandler/project_type_model.py``
|
| Base class for GUI graph representation: ``RdclGraph``, module: ``lib/rdcl_graph.py``
| Derived classes: ``ProjectTypeRdclGraph``, module ``lib/project_type/project_type_rdcl_graph.py``
|
| Base class for parsing descriptors: ``Parser``, module: ``lib/parser.py``
| Derived classes: ``ProjectTypeParser``, module ``lib/project_type/project_type_parser.py``
|

To introduce a new project type, the base classes for project, GUI graph representation and parser
need to be specialized. There is a python script that assists in the process of creating the
python, html and js files for the new project type.
The script is ``scripts/installer_project.py`` and must be executed
providing as a parameter the name of the project type and the names list of the files descriptors.
Assuming that the name of the project type is 'Newtype', and have two type of descriptor file 'nsd' and 'vnfd'
the script will be executed as follows: ::

    python scripts/installer_project.py --install  --project-name Newtype --descriptors-type nsd vnfd

if the process is completed without problem you need to execute the following commands: ::

    python manage.py makemigrations
    python manage.py migrate

for more info about the script you can execute: ::

    python scripts/installer_project.py -h

Pyhton server side
------------------
After running the script, the following python modules will be created. Please edit them as needed
to implement the specific methods of the new project type: ::

    projecthandler/newtype_model.py
    lib/newtype/newtype_rdcl_graph.py
    lib/newtype/newtype_parser.py

Description model - YAML file
-----------------------------
A yaml file will be created: ::

    lib/TopologyModels/newtype/newtype.yaml

for more info about Description Model see `here <description-models>`_


HTML templates and JS resources
-------------------------------
A set of html templates will be created for a new project type. The html templates are located in the folder ``projecthandler/template/project/newtype/``. The above described scripts ``scripts/installer_project.py``
also takes care of creating a set of JavaScript files: ::

    static/src/projecthandler/newtype/controller.js
    static/src/projecthandler/newtype/gui_properties.js
    static/src/projecthandler/newtype/project_graph.js



Uninstall
---------
There is also a script to delete a project type (use it with care, it deletes all files and folders
of Newtype): ::

    python scripts/installer_project.py --install  --project-name newtype

if the process is completed without problem you need to execute the following commands: ::

    python manage.py makemigrations
    python manage.py migrate



