### Manual Installation

See documentation for manual installation in [here](code/manual_install.md)

------------


Clone the project from repository with ssh:
    
    $ git clone git@github.com:superfluidity/RDCL3D.git
    
or https:

    $ git clone https://github.com/superfluidity/RDCL3D.git

### Prerequisites

- Python >= 2.7
- pip
- virtualenv (virtualenvwrapper is recommended)

### Installation

Install a recent Django version as shown in in the [install guide](https://docs.djangoproject.com/en/1.9/intro/install/).

Install pip as shown in the [install guide](https://pip.readthedocs.org/en/stable/installing/)

then move in Django project directory

If you want to use a python virtual environment as shown in in the [guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
call the directory simply "env" otherwise remember to add the new directory in .gitignore file.

To setup a local development environment::

    source env/bin/activate

    pip install -r requirements.txt

#### For the first time:

    $ python manage.py makemigrations sf_user projecthandler

    $ python manage.py migrate

#### you must create a new super user:

    $ python manage.py createsuperuser


#### To run the server:

    $ python manage.py runserver
or:
    
    $ python manage.py runserver [host]:[port] 



Development hints
-------

In order to keep your environment consistent, it's a good idea to "freeze" the current state of the environment packages. 
To do this, run

    $ pip freeze > requirements.txt

To add a new site to your existing Django project, use the startapp task of manage.py utility.

    $ django-admin.py startapp [name_django_app]

