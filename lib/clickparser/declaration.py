import string
import copy

def nameGenerator(element, type_element):      		#nome di default class@num
	num=0
	for i in range(0,len(element)):
		for j in range(0,len(element)):
			pos=string.find(element[i]['name'], str(j))
			if pos != -1:
				num = j
	
	return type_element+'@'+str(num+1)


#def rename_element_list_new(element,words):


def rename_element_list(element,words):			#controlla che non ci siano ridondanze tra le dichiarazioni 
	element2=copy.deepcopy(element)				#ed in tal caso rinomina l'elemento in modo incrementale
	names=[]
	start=0
	old_name=''
	new_name=''
	
	for i in range(0,len(words)-1):
		if words[i]=='->': 
			if words[i-2]!='::' and words[i-1][0].isupper():
				index=string.find(words[i-1],'(')
				if index!=-1:
					word=words[i-1][0:index]
				else:
					word=words[i-1]
				for e in element2.items():
					if word==e[1]['element']:
						words[i-1]=e[1]['name']
						e[1]['element']='-1'
						break
			try:			
				if words[i+2]!='::' and words[i+1][0].isupper():
					index=string.find(words[i+1],'(')
					if index!=-1:
						word=words[i+1][0:index]
					else:
						word=words[i+1]
					for e in element2.items():
						if word==e[1]['element']:
							words[i+1]=e[1]['name']
							e[1]['element']='-1'
							break
			except IndexError:
				if words[i+1][0].isupper():
					index=string.find(words[i+1],'(')
					if index!=-1:
						word=words[i+1][0:index]
					else:
						word=words[i+1]
					for e in element2.items():
						if word==e[1]['element']:
							words[i+1]=e[1]['name']
							e[1]['element']='-1'
							break


def explicit_element_decl_with_conf(i, words, element, name_subgraph, group):
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
		
	element[len(element)]=({'element':word[0:index], 'name':name_subgraph+words[i-1], 'config':config,'group':group})
	

def explicit_element_decl_without_conf(i, words, element, name_subgraph, group):
	element[len(element)]=({'element':words[i+1], 'name':name_subgraph+words[i-1], 'config':[],'group':group})


def implicit_element_decl_with_conf(i, words,element, name_subgraph, group):
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
	element[len(element)]=({'element':word[0:index], 'name':name_subgraph+name, 'config':config,'group':group})


def implicit_element_decl_without_conf(i,words,element, name_subgraph, group):
	name=nameGenerator(element, words[i])
	element[len(element)]=({'element':words[i], 'name':name_subgraph+name, 'config':[],'group':group})


def load_list(line, words):
	conf=False
	port=False
	word2=''
	word3=''

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
		
		elif word[len(word)-1]==']' and word[0]=='[':           				#usato per gestire il tipo di dichiarazione di porta d'ingresso
			word3=word 															#es.: [num]port o [num] port 
			port=True
			continue
		elif port:
			word=word3+''+word
			port=False

		if word[len(word)-1]==';':
			word=word[0:len(word)-1]

		words.append(word)
	
			
def explicit_elment_decl(line, element, name_subgraph, group, words):
	config = False
	words=[]
	index=[]

	load_list(line,words)

	for i in range(0,len(words)):
		if words[i] =='::':
			index.append(i)	

	for i in index:
			
		if string.find(words[i+1], '(') !=-1 and string.find(words[i+1], ')') !=-1:
			explicit_element_decl_with_conf(i, words, element, name_subgraph, group)
		elif string.find(words[i+1], '(') ==-1 and string.find(words[i+1], ')') ==-1:
			explicit_element_decl_without_conf(i,words,element, name_subgraph, group)
			

def implicit_element_decl(line, element, name_subgraph, group, words):
	words=[]

	load_list(line,words)

	for i in range(0,len(words)):
		index=string.find(words[i],'(')
		if words[i][0].isupper():
			if words[i-1]!='::':
				if string.find(words[i], '(') !=-1 and string.find(words[i], ')') !=-1:
					implicit_element_decl_with_conf(i, words, element, name_subgraph, group)
				elif string.find(words[i], '(') ==-1 and string.find(words[i], ')') ==-1:
					implicit_element_decl_without_conf(i, words, element, name_subgraph, group)


def subgraph_element(line, compound_element, element):

	name=nameGenerator(element, 'subgraph')
	element[len(element)]=({'element':'compound', 'name':name, 'config':[],'group':'click'})
	compound_element[len(compound_element)] = ({'name':name, 'compound':line})                      

	return name


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
					
			connection[len(connection)]=({'source':name_element_source, 'dest':name_element_dest, 'port-input':port_input, 'port-output':port_output})

