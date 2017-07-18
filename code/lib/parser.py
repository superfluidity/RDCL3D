#
#   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an  BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

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

    def get_all_ns_descriptors(self, nsd_id, project_data):
        raise NotImplementedError