import string
import copy
import networkx as nx
from declaration import *
from createJson import *

def generateTopology(element, connection, nx_topology):
	#nx_topology.add_node(int(node_id_value), city = node_name_value, country = node_country_value, type_node = 'core' )
	#add_edge(src, dst, flow_id, {'size':flow_dict['out']['size'], 'path':[]})

	for e in range(0, len(element)):
		nx_topology.add_node(element[e]['name'], element= element[e]['element'], config= element[e]['config'], flowcode='',processing='',portcount='')

	for c in range(0, len(connection)):
		nx_topology.add_edge(connection[c]['source'], connection[c]['dest'], 'port_config', {'port_input': connection[c]['port-input'],'port_output': connection[c]['port-output']})

def generateJsont3d(element, connection):

	json_data=nx_2_t3d_json(element, connection, 't3d.json')
	return json_data

def parserAllView(file_click, nx_topology):

	for line in file_click:
		words=[]
		element={}
		connection={}
		line2=''
		concatenate_conf=False
		concatenate_compound=False
		list_lines=[]
	
		for line in file_click:
				if line[0]=='/' or len(line)==1 or line[0]=='*':
					continue

				if string.find(line,'//')!=-1:								#elimina i commenti dalla riga
					line=line[0:string.find(line,'//')-1].strip()

				
				try:
					if line[len(line)-1]=='\n':								#elimina il carattere '\n' ed elimina gli spazi 			
						line = line[0:len(line)-1].strip()					#in eccesso		
				except IndexError:
					continue	

				line = line.strip(';')										#elimina ;
					
				if concatenate_conf:										#concatena la dichiarazione di elementi che viene scritta su
					if line[len(line)-1]==',':								#diverse righe
						line=line2+' '+line
					elif line[len(line)-1]==')':
						line=line2+' '+line
						concatenate=False	
				#print line
				if line[len(line)-1]==',':									#avvia la concatenazione degli elementi dichiarati su diverse righe
					line2=line
					concatenate_conf=True
					continue

				if string.find(line, '[') != -1:							#questo blocco modifica l'intera linea per gestire la lettura
					index = string.find(line, '[')							#delle porte di uscita dell'elemento che possono essere scritte
					if line[index-1] == ' ' and line[index-2].islower():	#sia come [num]port che [num] port
						line=line[0:index-1]+''+line[index:]	
					
					
				if string.find(line,'{')!=-1:								#concatena la dichiarazione dei compound element con la riga successiva
					line2=line
					concatenate_compound=True
					continue
				elif concatenate_compound:
					line=line2+' '+line
					concatenate=False
					line2=''
						
					line = compound_element(line)
				#print line	
				explicit_elment_decl(line, element)
				implicit_element_decl(line, element)		
				load_list(line, words)


		rename_element_list(element,words)		
		#print words

		connection_decl(words, connection, element)

		#print '\n'
		#print element
		#print'\n \n \n \n'
		#print words
		#print connection
		words[:] = []


		#generateTopology(element, connection, nx_topology)
		json_data=generateJsont3d(element, connection)
		return json_data
	