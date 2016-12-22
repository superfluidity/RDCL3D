import string
import copy
from utility import *

			
def explicit_elment_decl(line, element, name_subgraph, group, words):
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
	


def subgraph_element(line, compound_element, element):

	name=nameGenerator(element, 'subgraph')
	element[len(element)]=({'element':'compound', 'name':name, 'config':[],'group':'click'})
	compound_element[len(compound_element)] = ({'name':name, 'compound':line})                      

	return name



#FIXME = Deve prendere il nome del class element
def subgraph_ele_class(class_element_lines,ele_class_element ,element):    
	name=nameGenerator(element, 'subgraph_element_class')
	element[len(element)]=({'element':'class_element', 'name':name, 'config':[],'group':'click'})
	ele_class_element[len(ele_class_element)] = ({'name':name, 'compound':class_element_lines})



def connection_decl(words, connection, element):
	for i in range(0,len(words)):
		if words[i] == '->':
			port_input=0
			port_output=0

			if words[i-2]=='::': 
				name_element_source=words[i-3]
			elif string.find(words[i-1],'[')!=-1:
				index=string.find(words[i-1],'[')
				port_input=words[i-1][index+1:index+2]
				name_element_source=words[i-1][0:index]
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
					
			connection[len(connection)]=({'source':name_element_source, 'dest':name_element_dest, 'port-input':port_input, 'port-output':port_output, 'group':'click', 'type':0})


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
