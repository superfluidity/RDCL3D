#!/usr/bin/env python

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
	
	