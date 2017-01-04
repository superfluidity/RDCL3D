#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from toscaparser.nodetemplate import NodeTemplate
from toscaparser.tests.base import TestCase
from toscaparser.utils.gettextutils import _
import toscaparser.utils.yamlparser
from translator.hot.tosca.tosca_object_storage import ToscaObjectStorage


class ToscaObjectStoreTest(TestCase):

    def _tosca_objectstore_test(self, tpl_snippet, expectedprops):
        nodetemplates = (toscaparser.utils.yamlparser.
                         simple_parse(tpl_snippet)['node_templates'])
        name = list(nodetemplates.keys())[0]
        try:
            nodetemplate = NodeTemplate(name, nodetemplates)
            tosca_object_store = ToscaObjectStorage(nodetemplate)
            tosca_object_store.handle_properties()
            if not self._compare_properties(tosca_object_store.properties,
                                            expectedprops):
                raise Exception(_("Hot Properties are not"
                                  " same as expected properties"))
        except Exception:
            # for time being rethrowing. Will be handled future based
            # on new development
            raise

    def _compare_properties(self, hotprops, expectedprops):
        return all(item in hotprops.items() for item in expectedprops.items())

    def test_node_objectstorage_with_properties(self):
        tpl_snippet = '''
        node_templates:
          server:
            type: tosca.nodes.ObjectStorage
            properties:
              name: test
              size: 1024 KB
              maxsize: 1 MB
        '''
        expectedprops = {'name': 'test',
                         'X-Container-Meta': {'Quota-Bytes': 1000000}}
        self._tosca_objectstore_test(
            tpl_snippet,
            expectedprops)

    def test_node_objectstorage_with_few_properties(self):
        tpl_snippet = '''
        node_templates:
          server:
            type: tosca.nodes.ObjectStorage
            properties:
              name: test
              size: 1024 B
        '''
        expectedprops = {'name': 'test',
                         'X-Container-Meta': {'Quota-Bytes': 1024}}
        self._tosca_objectstore_test(
            tpl_snippet,
            expectedprops)
