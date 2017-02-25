# RDCL 3D - RFB Description and Composition Languages Design, Deploy and Direct 
========================================

RDCL 3D is a web framework for the design of NFV services and components. The framework allows editing,
validating, visualizing the descriptors of services and components both textually and graphically.

Later in this README you will find the instructions on how to install and run RDCL 3D.

Documentation is available in the docs folder of this repository.




Mailing list
-------------


Prerequisites
-------------

- Python >= 2.7
- pip
- virtualenv (virtualenvwrapper is recommended)

Installation
------------

Clone the project from repository with ssh:
    
    $ git clone git@github.com:superfluidity/RDCL3D.git
    
or https:

    $ git clone https://github.com/superfluidity/RDCL3D.git
    
Install a recent Django version as shown in in the [install guide](https://docs.djangoproject.com/en/1.9/intro/install/).

Install pip as shown in the [install guide] (https://pip.readthedocs.org/en/stable/installing/)

then move in Django project directory

If you want to use a python virtual environment as shown in in the [guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
call the directory simply "env" otherwise remember to add the new directory in .gitignore file.

To setup a local development environment::

    source env/bin/activate

    pip install -r requirements.txt

#### For the first time:

    $ python manage.py makemigrations

    $ python manage.py makemigrations projecthandler

    $ python manage.py migrate

#### you must create a new super user:

    $ python manage.py createsuperuser


#### To run the server:

    $ python manage.py runserver
or:
    
    $ python manage.py runserver [host]:[port] 



Development
-------

In order to keep your environment consistent, it's a good idea to "freeze" the current state of the environment packages. 
To do this, run

    $ pip freeze > requirements.txt

To add a new site to your existing Django project, use the startapp task of manage.py utility.

    $ django-admin.py startapp [name_django_app]

License
-------

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