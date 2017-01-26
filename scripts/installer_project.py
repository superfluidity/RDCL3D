import sys
import argparse
import os
import logging
from aetypes import end
from shutil import *
import fileinput

import shutil

DESCRIPTION = '''This script installs a new Project Type on RDCL.
This requires that you have Python 2.7.
'''

def init_logger(logger_name):
    logger = logging.getLogger(logger_name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] '
                                      '[%(name)s] %(message)s',
                                  datefmt='%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


class ProjectInstaller():

    full_path = os.path.realpath(__file__)
    HOME = full_path.split(__file__)[0]
    PHANDLER_PATH = os.path.join(HOME, 'projecthandler')
    LIB_PATH = os.path.join(HOME, 'lib')
    UC_PATH = os.path.join(HOME, 'usecases')
    TEMPLATE_PATH = os.path.join(PHANDLER_PATH, 'template', 'project')

    def __init__(self, uninstall=False, project_name=None, descriptors_type=None):
        lgr.debug(self.HOME)
        lgr.debug(self.PHANDLER_PATH)
        lgr.info(descriptors_type)
        self.uninstall = uninstall
        self.project_name = project_name.lower()
        self.descriptors_type = descriptors_type

    def execute(self):
        MODEL_FILE = os.path.join(self.PHANDLER_PATH, self.project_name + '_model.py')
        if self.uninstall:
            lgr.info('Uninstalling Project from RDCL.')
            sys.exit(self.remove_all())

        if os.path.isdir(MODEL_FILE):
            action = raw_input(
                '{0} already exists. Would you like to continue with the '
                'installation? (This will remove previous folders and files.) '
                '(yes/no):'.format(MODEL_FILE))
            if action in ('y', 'yes'):
                lgr.debug('Cleaning previous %s Project files and folders.',self.project_name)
                self.remove_all()
            else:
                sys.exit(lgr.info('Installation aborted.'))

        self.create_model_file()
        self.create_lib_files()
        self.create_use_case_dir()
        self.create_template_dir()

        lgr.info(
            'You can now run: \n' +
            'python manage.py makemigrations projecthandler \n' +
            'python manage.py migrate\n' +
            'and then run\n' +
            'python manage.py runserver')

    def create_model_file(self):
        MODEL_FILE = os.path.join(self.PHANDLER_PATH, self.project_name+'_model.py')
        #create a new model file from example template
        copyfile(os.path.join(self.PHANDLER_PATH, 'example_model._py'), MODEL_FILE)
        self.replace(MODEL_FILE)
        self.install_model()
        self.setup_model_type_scr(MODEL_FILE)

    def setup_model_type_scr(self, file_path):
        for line in fileinput.input(file_path, inplace=True):
            if line.find("# descriptor list in comment #") >= 0:
                for type in self.descriptors_type:
                    print line.replace("# descriptor list in comment #",type),
            elif line.find('# replace descriptors counter #')>=0:
                for type in self.descriptors_type:
                    print line.replace("# replace descriptors counter #", "'"+type+"': len(current_data['"+type+"'].keys()) if '"+type+"' in current_data else 0,");
            else:
                print line,

    def setup_model_parser(self, file_path):
        for line in fileinput.input(file_path, inplace=True):
            if line.find("# replace descriptor type empty dictionary #")>0:
                for type in self.descriptors_type:
                    print line.replace("# replace descriptor type empty dictionary #", "'"+type +"':{},")
            else:
                print line,

    def create_lib_files(self):
        MODEL_LIB_PATH = os.path.join(self.LIB_PATH, self.project_name)
        if not os.path.isdir(MODEL_LIB_PATH):
            os.makedirs(MODEL_LIB_PATH)

        copyfile(os.path.join(self.LIB_PATH, 'example', 'example_rdcl_graph._py'), os.path.join(MODEL_LIB_PATH, self.project_name + '_rdcl_graph.py'))
        self.replace(os.path.join(MODEL_LIB_PATH, self.project_name + '_rdcl_graph.py'))
        copyfile(os.path.join(self.LIB_PATH, 'example', 'example_parser._py'), os.path.join(MODEL_LIB_PATH, self.project_name + '_parser.py'))
        self.replace(os.path.join(MODEL_LIB_PATH, self.project_name + '_parser.py'))
        copyfile(os.path.join(self.LIB_PATH, 'example', '__init__._py'), os.path.join(MODEL_LIB_PATH, '__init__.py'))
        self.replace(os.path.join(MODEL_LIB_PATH, '__init__.py'))

        self.setup_model_parser(os.path.join(MODEL_LIB_PATH, self.project_name + '_parser.py'))

    def create_use_case_dir(self):
        PJ_UC_PATH = os.path.join(self.UC_PATH, self.project_name.upper())
        if not os.path.isdir(PJ_UC_PATH):
            os.makedirs(PJ_UC_PATH)

    def create_template_dir(self):
        PJ_TEMPLATE_PATH = os.path.join(self.TEMPLATE_PATH, self.project_name)
        if os.path.isdir(PJ_TEMPLATE_PATH):
            shutil.rmtree(PJ_TEMPLATE_PATH)
        self.copydir_and_replace(os.path.join(self.TEMPLATE_PATH, 'example'), PJ_TEMPLATE_PATH)

    def install_model(self):
        MODEL_FILE = os.path.join(self.PHANDLER_PATH, 'views.py')
        for line in fileinput.input(MODEL_FILE, inplace=True):

            print line,
            if line.startswith("# Project Model Type declarations #"):
                new_line = ('Project.add_project_type(\'{0}\', {1}Project)\n'.format(self.project_name, self.project_name.capitalize()))
                print new_line,
            elif line.startswith("# Project Models #"):
                new_line = ('from projecthandler.{0}_model import {1}Project\n'.format(self.project_name, self.project_name.capitalize()))
                print new_line,



    def replace(self, filepath):
        for line in fileinput.input(filepath, inplace=True):
            # inside this loop the STDOUT will be redirected to the file
            # the comma after each print statement is needed to avoid double line breaks
            line = line.replace("Exampletoken", self.project_name.capitalize())
            line = line.replace("exampletoken", self.project_name.lower())
            line = line.replace("EXAMPLETOKEN", self.project_name.upper())
            print line,

    def remove_all(self):
        lgr.info('Uninstalling %s', self.project_name)
        action = raw_input('Would you like to continue with the uninstallation?')
        if action in ('y', 'yes'):

            lgr.info('Uninstall Complete!')
        else:
            lgr.info('Uninstall Aborted.')

    def copydir_and_replace(self, src, dst, symlinks=False, ignore=None):
        names = os.listdir(src)
        if ignore is not None:
            ignored_names = ignore(src, names)
        else:
            ignored_names = set()

        os.makedirs(dst)
        errors = []
        for name in names:
            if name in ignored_names:
                continue
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name.replace('example', self.project_name))
            try:
                if symlinks and os.path.islink(srcname):
                    linkto = os.readlink(srcname)
                    os.symlink(linkto, dstname)
                elif os.path.isdir(srcname):
                    copytree(srcname, dstname, symlinks, ignore)
                else:
                    copy2(srcname, dstname)
                    self.replace(dstname)
            except (IOError, os.error) as why:
                errors.append((srcname, dstname, str(why)))
            # catch the Error from the recursive copytree so that we can
            # continue with other files
            except Error as err:
                errors.extend(err.args[0])
        try:
            copystat(src, dst)
        except shutil.WindowsError:
            # can't copy file access times on Windows
            pass
        except OSError as why:
            errors.extend((src, dst, str(why)))
        if errors:
            raise Error(errors)


def parse_args(args=None):

    parser = argparse.ArgumentParser(
        description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
    default_group = parser.add_mutually_exclusive_group()
    default_group.add_argument('-v', '--verbose', action='store_true',
                               help='Verbose level logging to shell.')
    default_group.add_argument('-q', '--quiet', action='store_true',
                               help='Only print errors.')

    parser.add_argument(
        '--project-name',type=str,  required=True,
        help='Name of the new project')
    parser.add_argument(
        '--descriptors-type', type=str, required=True, nargs='*',
        help='A list of descritors name supported in the project')
    parser.add_argument(
        '--uninstall', action='store_true',
        help='Uninstalls the project from rdcl.')

    return parser.parse_args(args)

lgr = init_logger(__file__)


if __name__ == '__main__':
    args = parse_args()
    if args.quiet:
        lgr.setLevel(logging.ERROR)
    elif args.verbose:
        lgr.setLevel(logging.DEBUG)
    else:
        lgr.setLevel(logging.INFO)

    xargs = ['quiet', 'verbose']
    args = {arg: v for arg, v in vars(args).items() if arg not in xargs}

    installer = ProjectInstaller(**args)
    installer.execute()