import string
import copy


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
	element[len(element)]=({'element':word[0:index], 'name':name_subgraph+name, 'config':config,'group':group})
	words2[i] = name_subgraph+name
	


def implicit_element_decl_without_conf(i,words,element, name_subgraph, group, words2):

	name=nameGenerator(element, words[i])
	element[len(element)]=({'element':words[i], 'name':name_subgraph+name, 'config':[],'group':group})
	words2[i] = name_subgraph+name



def subgraph_element_name(line, compound_element, element):

	name=nameGenerator(element, 'subgraph')
	element[len(element)]=({'element':'compound', 'name':name, 'config':[],'group':'click'})
	compound_element[len(compound_element)] = ({'name':name, 'compound':line})                      

	return name



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
	print words3




def nameGenerator(element, type_element):      		#nome di default class@num
	num=0
	for i in range(0,len(element)):
		for j in range(0,len(element)):
			pos=string.find(element[i]['name'], str(j))
			if pos != -1:
				num = j
	
	return type_element+'@'+str(num+1)


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
	for i in range(0,len(words)):																#usato per gestire il tipo di dichiarazione di porta d'uscita
		words_new.append(words[i])																#es.:  port[num] o port [num]
		try:
			if string.find(words[i],'[') == 0 and string.find(words[i],']')!=-1 and words[i+1] == '->':
				words_new[i-1]=words_new[i-1]+''+words[i]
				del words_new[len(words_new)-1]
		except IndexError:
			continue

	return words_new


