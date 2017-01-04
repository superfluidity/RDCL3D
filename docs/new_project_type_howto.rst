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

Server side (python django)
-----------
To introduce a new project type, the base classes for project, GUI graph representation and parser
need to be specialized. There is a bash script that assists in the process of creating the
python files for the new project type. The script is ``scripts/new_project_type.sh`` and must be executed 
providing as a parameter the name of the project type (with Capital Case for first letter). Assuming that
the name of the project type is Newtype, the script will be executed as follows: ::
    bash scripts/new_project_type.sh Newtype

After running the script, the following python modules will be created. Please edit them as needed
to implement the specific methods of the new project type: ::
    projecthandler/newtype_model.py
    lib/newtype/newtype_rdcl_graph.py
    lib/newtype/newtype_parser.py
    
In the module ``projecthandler/views.py`` the following lines needs to be added: ::
    from projecthandler.newtype_model import NewtypeProject
    Project.add_project_type('newtype', NewtypeProject)
    
There is also a script to delete a project type (use it with care, it deletes all files and folders
of Newtype): ::
    bash scripts/clean_project_type.sh Newtype

which descriptors will be part of the model ?? The ``data_project`` attribute of the Project class
stores a validated JSON representation of the project, for each descriptor type there is a key and the
value is a list of descriptors

which modules do we need to change ?

get_overview_data in projecthandler/newtype_model.py 

create_descriptor in projecthandler/newtype_model.py (when it is used??)

importprojectfiles in newtype_parser.py

HTML templates
--------------
A set of html templates needs to be added for a new project type. The html templates are located in 
the folder ``projecthandler/template/project/newtype/``. The above described scripts ``scripts/new_project_type.sh``
also takes care of creating a default version of the html templates.

projecthandler/template/project/new_project.html :
add the entry for the new project at line 69

projecthandler/template/project/tosca/tosca_project_details.html :
change the file types


Client side (javascript)
-----------



