import string
import copy
from utility import *

			
def explicit_element_decl(line, element, name_subgraph, group, words,ele_class_dict,ele_class_connections,connection):
	config = False
	words=[]
	index=[]
	ele_class_name=''

	words = load_list(line,words)
	control = False	


	for i in range(0,len(words)):
		control = False	

		if words[i] =='::':
			for c1 in range(0,len(words[i+1])):
				if words[i+1][c1] == '(':
					break
				ele_class_name = ele_class_name + words[i+1][c1]
			for c2 in ele_class_dict.keys(): 
				if ele_class_name == ele_class_dict[c2]['name']:
					control = True
					connection_elem_name,connection_elem_list=element_class_handler(element,words[i-1],ele_class_dict[c2]['name'],ele_class_dict[c2]['elementclasscontenent'],ele_class_dict[c2]['elementclassstr'],connection)	
					ele_class_connections[len(ele_class_connections)]=({'element name':connection_elem_name, 'connection_elem_list':connection_elem_list})

			if control == False:
				index.append(i)



	for i in index:
			
		if string.find(words[i+1], '(') !=-1 and string.find(words[i+1], ')') !=-1:
			explicit_element_decl_with_conf(i, words, element, name_subgraph, group)
		elif string.find(words[i+1], '(') ==-1 and string.find(words[i+1], ')') ==-1:
			explicit_element_decl_without_conf(i,words,element, name_subgraph, group)	




def implicit_element_decl(line, element, name_subgraph, group, words, words2):
	words = []

	words = load_list(line,words)
	
	for w in words:
		words2.append(w)
	for i in range(0,len(words)):
		index=string.find(words[i],'(')
		if words[i][0].isupper():
			if words[i-1]!='::':
				if string.find(words[i], '(') !=-1 and string.find(words[i], ')') !=-1:
					implicit_element_decl_with_conf(i, words, element, name_subgraph, group, words2)
		
				elif string.find(words[i], '(') ==-1 and string.find(words[i], ')') ==-1:
					implicit_element_decl_without_conf(i, words, element, name_subgraph, group, words2)
	
def element_class_handler(element, name_element,name_element_class,ele_class_cont,elementclassstr,connection):			#riceve il nome del element class e il contenuto
	words=[]
	words3=[]
	element_renamed={}
	renamed_element_content=[]

	#print name_element
	#print name_element_class
	#print ele_class_cont
	#print elementclassstr

	#FIXME => il config va letto e inserito
	element[len(element)]=({'element':name_element_class, 'name':name_element, 'config':'','group':'click'})
	
	explicit_compound_decl(elementclassstr, element, name_element+'.', name_element, words, element_renamed)
	implicit_compound_decl(elementclassstr, element, name_element+'.', name_element, words, words3)

	for c1 in ele_class_cont:
		renamed_element_content.append(c1)


	for i in range(0,len(renamed_element_content)):
			try:
				index = renamed_element_content.index('::')
				del renamed_element_content[index+1]
				renamed_element_content[index-1] = name_element+'.'+ renamed_element_content[index-1]
				del renamed_element_content[index]
			except ValueError:
				break
	
	for i in range(0,len(renamed_element_content)):												# rinomina gli elementi precedentementi dichiarati e che hanno ancora
		for e in element_renamed.items():												# ancora il loro nome originale
			if renamed_element_content[i] == e[1]['origin_name']:
				renamed_element_content[i] = e[1]['new_name']
			elif string.find(renamed_element_content[i], '[')!=-1:
				start = string.find(renamed_element_content[i], '[')
				stop = string.find(renamed_element_content[i], ']')
				if start == 0:
					name = renamed_element_content[i][stop+1:]
				elif stop == len(renamed_element_content[i])-1:
					name = renamed_element_content[i][0:start]	
				if name == e[1]['origin_name']:
					renamed_element_content[i] = e[1]['new_name']
	
	return name_element,renamed_element_content
	
def explicit_compound_decl(line, element, name_subgraph, group, words, element_renamed):
	config = False
	words=[]
	index=[]

	words = load_list(line,words)

	for i in range(0,len(words)):
		if words[i] =='::':
			index.append(i)	

	for i in index:
			
		if string.find(words[i+1], '(') !=-1 and string.find(words[i+1], ')') !=-1:
			explicit_element_decl_with_conf(i, words, element, name_subgraph, group)
			element_renamed[len(element_renamed)]={'origin_name':words[i-1], 'new_name':name_subgraph+words[i-1]}
		elif string.find(words[i+1], '(') ==-1 and string.find(words[i+1], ')') ==-1:
			explicit_element_decl_without_conf(i,words,element, name_subgraph, group)
			element_renamed[len(element_renamed)]={'origin_name':words[i-1], 'new_name':name_subgraph+words[i-1]}	



def implicit_compound_decl(line, element, name_subgraph, group, words, words2):
	words = []

	words = load_list(line,words)
	
	for w in words:
		words2.append(w)

	for i in range(0,len(words)):
		index=string.find(words[i],'(')
		if words[i][0].isupper():
			if words[i-1]!='::':
				if string.find(words[i], '(') !=-1 and string.find(words[i], ')') !=-1:
					implicit_element_decl_with_conf(i, words, element, name_subgraph, group, words2)
		
				elif string.find(words[i], '(') ==-1 and string.find(words[i], ')') ==-1:
					implicit_element_decl_without_conf(i, words, element, name_subgraph, group, words2)
	


def subgraph_ele_class(line2,ele_class_element):    
	class_element_cont=[]
	class_element_lines=[]


	class_element_str=''
	control = False

	class_element_lines=load_list(line2,class_element_lines)
	
	i=0																	#trova il nome della element class
	while i < len(class_element_lines):
		l=class_element_lines[i]
		if l=='elementclass':
			name=class_element_lines[i+1]
		i=i+1	

	for z in class_element_lines:
		if z!='elementclass' and z!='{' and z!='}' and z!=name:
			class_element_cont.append(z)			
		
	for w1 in line2:
		if w1=='{':
			control=True
			continue
		if w1=='}':
			control=False
			break	  
		if control == True:
			class_element_str=class_element_str + w1

	ele_class_element[len(ele_class_element)] = ({'name':name, 'elementclasscontenent':class_element_cont, 'elementclassstr':class_element_str})
	
	


def connection_decl(words, connection, element):
	#print 'words'
	#print words
	#print '\n'
	for i in range(0,len(words)):
		if words[i] == '->':
			port_input=0
			port_output=0

			if words[i-2]=='::': 
				name_element_source=words[i-3]
				
			elif string.find(words[i-1],'[')!=-1:        
				if string.find(words[i-1],'[') == 0:
					index = string.find(words[i-1],']')
					words[i-1] = words[i-1][index+1:]

				if string.find(words[i-1],'[')!=-1:
					index=string.find(words[i-1],'[')
					port_input=words[i-1][index+1:index+2]
					name_element_source=words[i-1][0:index]
				else:
					name_element_source=words[i-1]
					#print name_element_source
			else:
				name_element_source=words[i-1]	
					
			try:		
				if words[i+2]=='::':
					name_element_dest=words[i+1]
				elif string.find(words[i+1],']')!=-1:
					index=string.find(words[i+1],']')
					port_output=words[i+1][1:index]
					name_element_dest=words[i+1][index+1:]
				else:
					name_element_dest=words[i+1]
			except IndexError:
				if string.find(words[i+1],']')!=-1:
					index=string.find(words[i+1],']')
					port_output=words[i+1][1:index]
					name_element_dest=words[i+1][index+1:]
				else:
					name_element_dest=words[i+1]
					
			connection[len(connection)]=({'source':name_element_source, 'target':name_element_dest, 'port-input':port_input, 'port-output':port_output, 'group':'click', 'view':0})

	handle_edgeslevel(connection)


def connection_element_class_cleaner (connection_list,ele_class_connections):
	#  ele_class_connections{'element name':connection_elem_name, 'connection_elem_list':connection_elem_list}
	print connection_list
	print ele_class_connections

	
#Gestione dell'input e output senza porte
	for c1 in ele_class_connections.items():
		for i in range(0,len(connection_list)):
			if connection_list[i]==c1[1]['element name']:
				try:
					if connection_list[i-1]=='->':
						for j in range(0,len(c1[1]['connection_elem_list'])):
							if c1[1]['connection_elem_list'][j]=='input':
								c1[1]['connection_elem_list'][j]=connection_list[i-2]
					if connection_list[i+1]=='->':
						for k in range(0,len(c1[1]['connection_elem_list'])):
							if c1[1]['connection_elem_list'][k]=='output':
								c1[1]['connection_elem_list'][k]=connection_list[i+2]
				except IndexError:
					break
	
	print '********'


#Gestione dell'output con porte
	for c2 in ele_class_connections.items():
		for h in range(0,len(connection_list)):
				if connection_list[h].find(c2[1]['element name']) != -1:				
					if connection_list[h].find('[')!=-1:
						if connection_list[h+1]=='->':
							for j in range(0,len(c2[1]['connection_elem_list'])):
								if c2[1]['connection_elem_list'][j].find('output') != -1:
									port=''
									port_control=False
									for letter in c2[1]['connection_elem_list'][j]:
										if letter == '[':
											port=port+letter
											port_control = True
											continue
										if port_control == True:	
											if letter == ']':
												port=port+letter
												port_control = False
												break
											port=port+letter
										continue
									if connection_list[h].find(port) != -1:
										for s in range(0,len(c2[1]['connection_elem_list'])):
											if c2[1]['connection_elem_list'][s]==port+'output':
												c2[1]['connection_elem_list'][s]=connection_list[h+2]

#Gestione dell'input con porte
	for c3 in ele_class_connections.items():
		for l in range(0,len(connection_list)):
				if connection_list[l].find(c3[1]['element name']) != -1:				
					if connection_list[l].find('[')!=-1:
						if connection_list[l-1]=='->':
							for j in range(0,len(c3[1]['connection_elem_list'])):
								if c3[1]['connection_elem_list'][j].find('input') != -1:
									port=''
									port_control=False
									for letter in c3[1]['connection_elem_list'][j]:
										if letter == '[':
											port=port+letter
											port_control = True
											continue
										if port_control == True:	
											if letter == ']':
												port=port+letter
												port_control = False
												break
											port=port+letter
										continue
									if connection_list[l].find(port) != -1:
										for p in range(0,len(c3[1]['connection_elem_list'])):
											if c3[1]['connection_elem_list'][p]=='input'+port:
												c3[1]['connection_elem_list'][p]=connection_list[h-2]



	print ele_class_connections










		
	#print connection_list

'''
def compound_element(line):
	words=[]
	words_copy=[]
	word2=[]
	control=False

	words = load_list(line, words)

	for w in words:
		if w=='}':
			control=True
			continue
		if control==True:
			word2.append(w)

	for i in range(0,len(words)):
		if words[i]!='output' and words[i]!='{' and words[i]!='}' and words[i]!='input':
			words_copy.append(words[i])
		elif words[i]=='input':
			words_copy.append('Input')
		elif words[i]=='output':
			words_copy.append('Output')
			for w in word2:
				words_copy.append(w) 
		elif words[i]=='}':
			break
	line=''	
	for w in words_copy:
		line=line+' '+w

	return line 
'''