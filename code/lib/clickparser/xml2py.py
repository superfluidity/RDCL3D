#!/usr/bin/env python
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

import xml.etree.ElementTree as ET
import networkx as nx


#Esegue il parsing di elementmap.xml inserendo in root tutte le entry
tree = ET.parse('elementmap.xml')
root = tree.getroot()



def xml2py(nx_topology):
	for node in nx_topology.nodes_iter(data = True):
		foundflag = False
	#Cicla tra le entry fino a quando non trova una corrispondenza 
		for entry in root:
			name = entry.get('name')
			portcount = entry.get('portcount')
			processing = entry.get('processing')
			flowcode = entry.get('flowcode') 	
			if name == node[1]['element']:
				foundflag = True
				node[1]['portcount'] = portcount
				node[1]['processing'] = processing
				node[1]['flowcode'] = flowcode
				break
		if foundflag == False:
		#Se non trova nulla ritorna un errore
			print '\n'
			print "Error! %s not Found" % node[0]
	
	
