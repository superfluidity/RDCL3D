#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from toscaparser.elements.scalarunit import ScalarUnit_Size
from translator.hot.syntax.hot_resource import HotResource

# Name used to dynamically load appropriate map class.
TARGET_CLASS_NAME = 'ToscaObjectStorage'


class ToscaObjectStorage(HotResource):
    '''Translate TOSCA node type tosca.nodes.ObjectStorage.'''

    toscatype = 'tosca.nodes.ObjectStorage'

    def __init__(self, nodetemplate, csar_dir=None):
        super(ToscaObjectStorage, self).__init__(nodetemplate,
                                                 type='OS::Swift::Container',
                                                 csar_dir=csar_dir)
        pass

    def handle_properties(self):
        tosca_props = self.get_tosca_props()
        objectstore_props = {}
        container_quota = {}
        skip_check = False

        for key, value in tosca_props.items():
            if key == "name":
                objectstore_props["name"] = value
            elif key == "size" or key == "maxsize":
                # currently heat is not supporting dynamically increase
                # the container quota-size.
                # if both defined in tosca template, consider store_maxsize.
                if skip_check:
                    continue
                quota_size = None
                if "maxsize" in tosca_props.keys():
                    quota_size = tosca_props["maxsize"]
                else:
                    quota_size = tosca_props["size"]
                container_quota["Quota-Bytes"] = \
                    ScalarUnit_Size(quota_size).get_num_from_scalar_unit()
                objectstore_props["X-Container-Meta"] = container_quota
                skip_check = True

        objectstore_props["X-Container-Read"] = '".r:*"'
        self.properties = objectstore_props
