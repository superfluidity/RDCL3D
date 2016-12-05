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

def rename_element_list(element,words):			#controlla che non ci siano ridondanze tra le dichiarazioni 
	element2=copy.deepcopy(element)				#ed in tal caso rinomina l'elemento in modo incrementale
	names=[]
	start=0
	old_name=''
	new_name=''

	m=0
	for i in range(0,len(words)):
		if words[i]=='::':
			if len(names)==0:
				names.append(words[i-1])
				continue
			contr=False
			for n in names:
				if n == words[i-1]:
					contr=True
					old_name=words[i-1]
					m=m+1
					words[i-1]=n+str(m)
					new_name=words[i-1]			
					for k in range(i,len(words)):
						if words[k]=='->':
							if string.find(words[k-1],'[')!=-1:
								index=string.find(words[k-1],'[')
								if words[k-1][0:index]==old_name:
									words[k-1]=new_name+words[k-1][index:]
							elif words[k-1]==old_name:
									words[k-1]=new_name
									
					for k in range(i,len(words)):
						if words[k]=='->':
							if string.find(words[k+1],']')!=-1:
								index=string.find(words[k+1],']')								
								if words[k+1][index+1:]==old_name:
									words[k+1]=words[k+1][0:index+1]+new_name
							elif words[k+1]==old_name:
									words[k+1]=new_name


					break
				
			if contr==False:
				names.append(words[i-1])

	
	names=[]
	z=0
	for i in range(0,len(element)):
		if len(names)==0:
			names.append(element[i]['name'])
			continue
		contr=False
		for n in names:
			if n == element[i]['name']:
				contr=True
				z=z+1
				element[i]['name']=n+str(z)
				break
		if contr==False:
			names.append(element[i]['name'])				
	

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


def explicit_element_decl_with_conf(i, words, element):
	comma=[]
	config=[]
	word=words[i+1]

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
		
	element[len(element)]=({'element':word[0:index], 'name':words[i-1], 'config':config})
	

def explicit_element_decl_without_conf(i, words, element):
	element[len(element)]=({'element':words[i+1], 'name':words[i-1], 'config':[]})


def implicit_element_decl_with_conf(i, words,element):
	comma=[]
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
	element[len(element)]=({'element':word[0:index], 'name':name, 'config':config})


def implicit_element_decl_without_conf(i,words,element):
	name=nameGenerator(element, words[i])
	element[len(element)]=({'element':words[i], 'name':name, 'config':[]})


def load_list(line, words):
	conf=False
	port=False
	word2=''
	word3=''

	for word in line.split():
		if conf:
			if word[len(word)-1]==')':
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
	
			
def explicit_elment_decl(line, element):
	config = False
	words=[]
	index=[]

	load_list(line,words)

	for i in range(0,len(words)):
		if words[i] =='::':
			index.append(i)	
	for i in index:
			
		if string.find(words[i+1], '(') !=-1 and string.find(words[i+1], ')') !=-1:
			explicit_element_decl_with_conf(i, words, element)
		elif string.find(words[i+1], '(') ==-1 and string.find(words[i+1], ')') ==-1:
			explicit_element_decl_without_conf(i,words,element)
			

def implicit_element_decl(line, element):
	words=[]

	load_list(line,words)

	for i in range(0,len(words)):
		index=string.find(words[i],'(')
		if words[i][0].isupper():
			if words[i-1]!='::':
				if string.find(words[i], '(') !=-1 and string.find(words[i], ')') !=-1:
					implicit_element_decl_with_conf(i, words, element)
				elif string.find(words[i], '(') ==-1 and string.find(words[i], ')') ==-1:
					implicit_element_decl_without_conf(i, words, element)


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

	
def compound_element(line):
	words=[]
	words_copy=[]
	word2=[]
	control=False

	load_list(line, words)

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
	
	
def compound_element_view(line):
	words=[]
	word2=[]
	word3=[]
	control=False
	control2=False
	

	load_list(line, words)	


	for w in words:												#salva tutto cio che viene prima della graffa in word2 
		if w=='{':												#e tutto cio che viene dopo in word3
			control=True						
			continue							
		if control==True:
			if w == '}':
				control2 = True
				continue
			if control2 == True:
				word3.append(w)	
			continue	
		word2.append(w)

	
	line=''														#cancella contenuto di line
	for w in word2:												#riscrive la linea 									
		line=line+' '+w
	line=line+' Subgraph '
	for w in word3:
		line=line+' '+w

	return line
		


