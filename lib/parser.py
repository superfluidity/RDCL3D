import json
import pyaml
import yaml
from lib.util import Util
import logging
import traceback
import glob
import os


class Parser(object):
    """Parser methods base class

    """

    def __init__(self):
        pass
    
    @classmethod        
    def importprojectdir(cls,dir_project, type):
        """Imports all files under a given folder

        Returns an empty project
        """

        project = {}
        return project


