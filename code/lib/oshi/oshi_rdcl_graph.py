#
#   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni
#
#   Licensed under the Apache License, Version 2.0 (the );
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
import logging
import copy
from lib.rdcl_graph import RdclGraph

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('OshiRdclGraph')

class OshiRdclGraph(RdclGraph):
    """Operates on the graph representation used for the GUI graph views"""

    def __init__(self):
        pass


    def build_graph_from_project(self, json_project, model={}):
        """Creates a single graph for a whole project"""
        # in oshi is not supported
        graph_object = {
            'vertices': [],
            'edges': [],
            'graph_parameters': {},
            'model': model
        }
        # try:
        #
        #
        # except Exception as e:
        #     log.exception('Exception in build_graph_from_project')
        #     raise

        return graph_object

    def build_graph_from_oshi_descriptor(self, json_data, model={}):
        """Creates a single graph for a oshi descriptor"""

        try:
            graph_object = json_data
            graph_object['model'] = model

        except Exception as e:
            log.exception('Exception in build_graph_from_project')
            raise

        return graph_object
