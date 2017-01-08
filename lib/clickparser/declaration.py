import string
import copy
from utility import *

			
def explicit_element_decl(line, element, name_subgraph, group, words,ele_class_dict):
	config = False
	words=[]
	index=[]
	ele_class_name=''

	words = load_list(line,words)
	#for ir in ele_class_dict.items():
	#	print ele_class_dict[ir]['name']
	#	ir = ir +1


	for i in range(0,len(words)):
		if words[i] =='::':
			index.append(i)
			for c1 in range(0,len(words[i+1])):
				if words[i+1][c1] == '(':
					break
				ele_class_name = ele_class_name + words[i+1][c1]
			for c2 in ele_class_dict.keys(): 
				if ele_class_name == ele_class_dict[c2]['name']:
					element_class_handler(words[i-1],ele_class_dict[c2]['elementclasscontenent'])	




	for i in index:
			
		if string.find(words[i+1], '(') !=-1 and string.find(words[i+1], ')') !=-1:
			explicit_element_decl_with_conf(i, words, element, name_subgraph, group)
		elif string.find(words[i+1], '(') ==-1 and string.find(words[i+1], ')') ==-1:
			explicit_element_decl_without_conf(i,words,element, name_subgraph, group)	


def element_class_handler(name_element_class,ele_class_cont):			#riceve il nome del element class e il contenuto

	print name_element_class
	print ele_class_cont

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
	
	print line2
	class_element_lines=load_list(line2,class_element_lines)
	print '#####'
	print class_element_lines
	print '######'
	i=0																	#trova il nome della element class
	while i < len(class_element_lines):
		l=class_element_lines[i]
		if l=='elementclass':
			name=class_element_lines[i+1]
		i=i+1	

	for z in class_element_lines:
		if z!='elementclass' and z!='{' and z!='}' and z!=name:
			class_element_cont.append(z)			
		
	 
	ele_class_element[len(ele_class_element)] = ({'name':name, 'elementclasscontenent':class_element_cont})
	
	


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
