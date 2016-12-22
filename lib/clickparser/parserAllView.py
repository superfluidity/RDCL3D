import string
import copy
import networkx as nx
from declaration import *
from createJson import *

def remove_tab(line):
    if string.find(line,'\t') != -1:
        print 'ok'
        line=line[string.find(line,'\t')+1:]
        line = remove_tab(line)
    return line

def generateTopology(element, connection, nx_topology):
    for e in range(0, len(element)):
        nx_topology.add_node(element[e]['name'], element=element[e]['element'], config=element[e]['config'],
                             flowcode='', processing='', portcount='')

    for c in range(0, len(connection)):
        nx_topology.add_edge(connection[c]['source'], connection[c]['dest'], 'port_config',
                             {'port_input': connection[c]['port-input'], 'port_output': connection[c]['port-output']})


def generateJsont3d(element, connection):
    json_data = nx_2_t3d_json(element, connection, 't3d.json')
    return json_data



def parserAllView(file_click, nx_topology):
    # with open('/home/user/Progetto_Superfluidity/test-rdcl/lib/clickparser/'+file_click,'r') as f:
    l = 0
    words = []
    
    file_click_list = []
    element = {}
    connection = {}
    line2 = ''
    elem_class_control=False
    concatenate_conf = False
    concatenate_compound = False
    concatenate_line = False
    element_class_lines=[]
    list_lines = []
    ele_class_element = {}
    compound_element = {}                                                           # lista contenente tutti gli elementi contenuti all'interno nel compound
                                                                                    #con il relativo nome del compound 
    compound_element_prov = {}

    text = "".join([s for s in file_click.splitlines(True) if s.strip("\r\n")])

    for line in text.splitlines():
        if line[0] == '/' or line[0] == '*':
            continue

        if string.find(line, '//') != -1:                                           # elimina i commenti dalla riga
            line = line[0:string.find(line, '//') - 1].strip()

        try:
            if line[len(line) - 1] == '\n':                                         # elimina il carattere '\n' ed elimina gli spazi
                line = line[0:len(line) - 1].strip()                                # in eccesso
        except IndexError:
            continue

###############################ClassElementControl#################################### 
        if string.find(line, 'elementclass') != -1:
            elem_class_control=True
            line2 = line
            continue
        if elem_class_control==True and string.find(line, '}') !=-1:
            elem_class_control=False
            element_class_lines=load_list(line2,element_class_lines)
            subgraph_ele_class(element_class_lines,ele_class_element,element) #(compound_line, compound_element, element)
            continue    
        
        if elem_class_control:
            line2=line2 + ' ' + line                   
            continue
######################################################################################

        if concatenate_line:                                                        # utilizzato per concatenare le righe fino al ;
            if line[len(line)-1]==';' or line[len(line)-2]==';':
                concatenate_line = False
                line = line2+' '+line.strip()
                line2=''
                
            else:
                line2 = line2+' '+line.strip()
                continue

        if line[len(line)-1]!=';' and concatenate_line == False:
            concatenate_line = True
            line2 = line.strip()
            continue
        
        if string.find(line, '{')!=-1 and string.find(line, '}')!=-1:                           # crea il nodo che corrisponde al compound element
            compound_list = []
            element_list = load_list(line,compound_list)

            compound_line=line[string.find(line, '{')+1:string.find(line, '}')]                 # contiene tutta la dichiarazione del compound element
            name = subgraph_element(compound_line, compound_element, element)
            line = line[0:string.find(line, '{')]+name+line[string.find(line, '}')+1:]

        words2 = []
        explicit_elment_decl(line, element,'', 'click', words)
        implicit_element_decl(line, element,'', 'click', words, words2)
    
        for i in range(0,len(words2)):                                                          # ad ogni riga sostituisce il da dichiarazione dell'elemento 
            try:                                                                                # con il nome dell'elemento. Per semplificare la dichiarazione 
                index = words2.index('::')                                                      # delle connessioni
                del words2[index+1]
                del words2[index]
            except ValueError:
                break
       
        for w in words2:                                                                        # inserisce tutte le righe in una lista che verra' passata
            file_click_list.append(w)                                                           # alla funzione connection_decl

        load_list(line, words)
    ################################################# PRINTA LA STRINGA DELL'ELEMENT CLASS    
    print element_class_lines

    #rename_element_list(element, words)
    ############################################# TEST PER LE DICHIARAZIONI DEGLI ELEMENTI E LE CONNESSIONI DEI COMPOUND ELEMENT###################

    file_click_list_compound=[]
    for line in compound_element.items():
        
        words3 = []
        explicit_elment_decl(line[1]['compound'], element, line[1]['name']+'.', line[1]['name'], words)
        implicit_element_decl(line[1]['compound'], element, line[1]['name']+'.', line[1]['name'], words, words3)
        #print words3
        for i in range(0,len(words3)):
            try:
                index = words3.index('::')
                del words3[index+1]
                words3[index-1] = line[1]['name']+'.'+ words3[index-1]
                del words3[index]
            except ValueError:
                break
        line[1]['compound']=words3

    for e in compound_element.items():
        for i in range(0,len(file_click_list)):
            if e[1]['name'] == file_click_list[i]:
                for j in range(0,len(e[1]['compound'])):
                    if e[1]['compound'][j] == 'input':
                        e[1]['compound'][j] = file_click_list[i-2]
                    if e[1]['compound'][j] == 'output':
                        e[1]['compound'][j] = file_click_list[i+2]


    ##############################################################################################################################################

    connection_decl(file_click_list, connection, element)
    #print connection
    words[:] = []

    json_data = generateJsont3d(element, connection)
    #print json_data
    return json_data

    #print element
    #print connection
        #print line

