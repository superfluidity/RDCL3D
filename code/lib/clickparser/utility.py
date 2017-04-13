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

import string
import copy


def explicit_element_decl_with_conf(i, words, element, name_subgraph, group, type_element):
	comma=[]
	config=[]
	word=words[i+1]

	index=string.find(word, '(')

	for w in word.split(','):
		if string.find(w,'(')!=-1 and string.find(w,')')==-1:
			config.append(w[string.find(w,'(')+1:len(w)])	
		elif string.find(w,'(')!=-1 and string.find(w,')')!=-1:	
			config.append(w[string.find(w,'(')+1:len(w)-1])	
		elif string.find(w,')')!=-1:
			config.append(w[0:len(w)-1])
		else:
			config.append(w)

	if name_subgraph != '' and name_subgraph[len(name_subgraph)-1] != '.':
		name_subgraph = name_subgraph+'.'
	if group[len(group)-1] == '.':
		group = group[0:len(group)-1]
	element[len(element)]=({'element':word[0:index], 'name':name_subgraph+words[i-1], 'config':config,'group':[group], 'node_type': type_element})
	


def explicit_element_decl_without_conf(i, words, element, name_subgraph, group, type_element):
	if name_subgraph != '' and name_subgraph[len(name_subgraph)-1] != '.':
		name_subgraph = name_subgraph+'.'
	if group[len(group)-1] == '.':
		group = group[0:len(group)-1]
	element[len(element)]=({'element':words[i+1], 'name':name_subgraph+words[i-1], 'config':[],'group':[group], 'node_type': type_element})
	


def implicit_element_decl_with_conf(i, words,element, name_subgraph, group, words2):
	config=[]
	word=words[i]

	index=string.find(word, '(')

	for w in word.split(','):
		if string.find(w,'(')!=-1 and string.find(w,')')==-1:
			config.append(w[string.find(w,'(')+1:len(w)])
		elif string.find(w,'(')!=-1 and string.find(w,')')!=-1:	
			config.append(w[string.find(w,'(')+1:len(w)-1])	
		elif string.find(w,')'):
			config.append(w[0:len(w)-1])
		else:
			config.append(w)

	name=nameGenerator(element, word[0:index])

	if name_subgraph != '' and name_subgraph[len(name_subgraph)-1] != '.':
		name_subgraph = name_subgraph+'.'
	element[len(element)]=({'element':word[0:index], 'name':name_subgraph+name, 'config':config,'group':[group], 'node_type':'element'})
	words2[i] = name_subgraph+name
	


def implicit_element_decl_without_conf(i,words,element, name_subgraph, group, words2):

	name=nameGenerator(element, words[i])

	if name_subgraph != '' and name_subgraph[len(name_subgraph)-1] != '.':
		name_subgraph = name_subgraph+'.'
	element[len(element)]=({'element':words[i], 'name':name_subgraph+name, 'config':[],'group':[group], 'node_type': 'element'})
	words2[i] = name_subgraph+name



def subgraph_element_name(line, compound_element, element, group):

	name=nameGenerator(element, 'subgraph')
	element[len(element)]=({'element':'Compound_Element', 'name':name, 'config':[],'group':[group], 'node_type': 'compound_element'})
	compound_element[len(compound_element)] = ({'name':name, 'compound':line})                      

	return name


def rename_class_element(words, words1,words3, name_ele, name):
	


	for i in range (0,len(words1)):						#Rinomina gli elementi espliciti della riga
		
		if words1[i] != '::' and words1[i] != '->' and string.find(words[i],'@') == -1 and string.find(words1[i], 'input') == -1 and string.find(words1[i], 'output') == -1:
				if string.find(words1[i], '[') != -1:
					start = string.find(words1[i], '[')
					stop = string.find(words1[i], ']')
					if start == 0:
						name_element = words1[i][stop:]
					else:
						name_element = words1[i][0:start]
					words1[i] = name_ele+'.'+name_element
				else:
					words1[i] = name_ele+'.'+words[i]

		try:
			index = words1.index('::')
			del words1[index+1]
			counter = len(name_ele) 
			if name_ele[counter-1] == '.':
				words1[index-1] = name_ele + words1[index-1]
			else:
				words1[index-1] = name_ele + '.' + words1[index-1]

			del words1[index]
		except ValueError:
			break


def rename_compound_element(words3, compound, element_renamed):
	for i in range(0,len(words3)):														# rinomina gli elementi del compound contenuti in word3
            try:
                index = words3.index('::')
                del words3[index+1]
                words3[index-1] = compound[1]['name']+'.'+ words3[index-1]
                del words3[index]
            except ValueError:
                break
	compound[1]['compound']=words3

	for i in range(0,len(words3)):														# rinomina gli elementi precedentementi dichiarati e che hanno ancora
		for e in element_renamed.items():												# ancora il loro nome originale
			if words3[i] == e[1]['origin_name']:
				words3[i] = e[1]['new_name']
			elif string.find(words3[i], '[')!=-1:
				start = string.find(words3[i], '[')
				stop = string.find(words3[i], ']')
				if start == 0:
					name = words3[i][stop+1:]
				elif stop == len(words3[i])-1:
					name = words3[i][0:start]	
				if name == e[1]['origin_name']:
					words3[i] = e[1]['new_name']


def nameGenerator(element, type_element):      		#nome di default class@num
	implicit_name = False

	for e in element.items():
		if string.find(e[1]['name'],'@')!=-1 and string.find(e[1]['name'],'.')==-1:
			index = string.find(e[1]['name'],'@')
			num = int(e[1]['name'][index+1:])
			implicit_name = True

	if implicit_name :
		name = type_element+'@'+str(num+1)
	else:
		name = type_element+'@0'

	return name


def load_list(line, words):
	conf=False
	port=False
	word2=''
	word3=''

	line_old=' ['
	line_new='['

	line=line.replace(line_old,line_new)

	line_old=['::','->',' ;']
	line_new=[' :: ',' -> ',';']
	for i in range(0,len(line_old)):											#gestisce le dichiarazione esplice degli elementi
		line=line.replace(line_old[i],line_new[i])								#es.: name::element o name :: element

	for word in line.split():
		if conf:
			if word[len(word)-1]==')' or word[len(word)-2]==')':
				word=word2+' '+word
				conf=False
			else:
				word2=word2+' '+word
				continue

		if string.find(word,'(')!=-1 and string.find(word,')')==-1:            #concatena le stesse config di un elemento
			conf=True
			word2=word
			continue
		
		elif word[len(word)-1]==']' and word[0]=='[' and words[len(words)-1] == '->':         		#usato per gestire il tipo di dichiarazione di porta d'ingresso
			word3=word 																				#es.: [num]port o [num] port 
			port=True
			continue

		elif port:
			word=word3+''+word
			port=False

		if word[len(word)-1]==';':
			word=word[0:len(word)-1]

		words.append(word)

	words_new=[]	

	return words


def handle_edgeslevel(connection):
	index = 0

	for c in connection.items():	
		target_level = '0'
		source_level = '0'						
		for w in range(0,len(c[1]['target'])):
			if c[1]['target'][w] == '.':
				index = w
				target_level = c[1]['target'][0:index]
		
		for w in range(0,len(c[1]['source'])):
			if c[1]['source'][w] == '.':
				index = w
				source_level = c[1]['source'][0:index]
		
		if source_level == target_level and source_level != '0' and target_level != '0':
			c[1]['group'].append(source_level)
		elif source_level == '0' and target_level == '0':
			c[1]['group'].append('click')
		else:
			c[1]['group'].append('Null')


	connection2 = connection.copy() 

	for c in connection.items():
		if c[1]['group'] != 'click':
			for c1 in connection2.items():
				if c1[1]['target'] == c[1]['group']:
					c[1]['depth'] = c1[1]['depth']+1
	
	
