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

from toscaparser.functions import GetInput
from translator.hot.syntax.hot_resource import HotResource

# Name used to dynamically load appropriate map class.
TARGET_CLASS_NAME = 'ToscaBlockStorageAttachment'


class ToscaBlockStorageAttachment(HotResource):
    '''Translate TOSCA relationship AttachesTo for Compute and BlockStorage.'''

    toscatype = 'tosca.nodes.BlockStorageAttachment'

    def __init__(self, template, nodetemplates, instance_uuid, volume_id,
                 csar_dir=None):
        super(ToscaBlockStorageAttachment,
              self).__init__(template, type='OS::Cinder::VolumeAttachment',
                             csar_dir=csar_dir)
        self.nodetemplates = nodetemplates
        self.instance_uuid = {'get_resource': instance_uuid}
        self.volume_id = {'get_resource': volume_id}

    def handle_properties(self):
        tosca_props = {}
        for prop in self.nodetemplate.get_properties_objects():
            if isinstance(prop.value, GetInput):
                tosca_props[prop.name] = {'get_param': prop.value.input_name}
            else:
                tosca_props[prop.name] = prop.value
        self.properties = tosca_props
        # instance_uuid and volume_id for Cinder volume attachment
        self.properties['instance_uuid'] = self.instance_uuid
        self.properties['volume_id'] = self.volume_id
        if 'location' in self.properties:
            self.properties['mountpoint'] = self.properties.pop('location')

        # TOSCA type can have a device name specified,
        # this is unsupported by Heat
        if 'device' in self.properties:
            self.properties.pop('device')

    def handle_life_cycle(self):
        return None, None, None
