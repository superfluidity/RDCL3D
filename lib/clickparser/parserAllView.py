import string
import copy
import networkx as nx
from declaration import *
from createJson import *
from utility import *

def remove_tab(line):
    if string.find(line,'\t') != -1:
        line=line[string.find(line,'\t')+1:]
        line = remove_tab(line)
    return line

def generateTopology(element, connection, nx_topology):
    for e in range(0, len(element)):
        nx_topology.add_node(element[e]['name'], element=element[e]['element'], config=element[e]['config'],
                             flowcode='', processing='', portcount='')

    for c in range(0, len(connection)):
        nx_topology.add_edge(connection[c]['source'], connection[c]['target'], 'port_config',
                             {'port_input': connection[c]['port-input'], 'port_output': connection[c]['port-output']})


def generateJsont3d(element, connection):
    json_data = nx_2_t3d_json(element, connection, 't3d.json')
    return json_data



def parserAllView(file_click):
    # with open('/home/user/Progetto_Superfluidity/test-rdcl/lib/clickparser/'+file_click,'r') as f:
    l = 0
    words = []
    
    connection_list = []
    element = {}
    connection = {}
    line2 = ''
    elem_class_control=False
    concatenate_conf = False
    concatenate_compound = False
    concatenate_line = False
    
    list_lines = []
    ele_class_dict = {}
    clean_ele_class_connections=[]
    fluxOutput={}
    ele_class_connections={}
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
            ###########
        if elem_class_control==True and string.find(line, '}') !=-1:
            elem_class_control=False
            subgraph_ele_class(line2,ele_class_dict)       #(contenutodellelementclass, dizionario delle classelement,dizionario element)
            line2=''
            continue    
            ###########
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
            name = subgraph_element_name(compound_line, compound_element, element)
            line = line[0:string.find(line, '{')]+name+line[string.find(line, '}')+1:]

        words2 = []
        
        explicit_element_decl(line, element,'', 'click', words, ele_class_dict,ele_class_connections)
        #print'implicit'
        implicit_element_decl(line, element,'', 'click', words, words2)
        #print'###'
        for i in range(0,len(words2)):                                                          # ad ogni riga sostituisce il da dichiarazione dell'elemento 
            try:                                                                                # con il nome dell'elemento. Per semplificare la dichiarazione 
                index = words2.index('::')                                                      # delle connessioni
                del words2[index+1]
                del words2[index]
            except ValueError:
                break

        for w in words2:                                                                        # inserisce tutte le righe in una lista che verra' passata
            connection_list.append(w)                                                           # alla funzione connection_decl

        load_list(line, words)

    ################################################# PRINTA LA STRINGA DELL'ELEMENT CLASS    
    #print '#############'
    #print connection_list
    #print ele_class_connections
    #print '*************'
    #print ele_class_dict
    ############################################# TEST PER LE DICHIARAZIONI DEGLI ELEMENTI E LE CONNESSIONI DEI COMPOUND ELEMENT###################

    element_renamed={}
    #print 'comp'
    #print compound_element
    for comp in compound_element.items():
        
        words3 = []
        explicit_compound_decl(comp[1]['compound'], element, comp[1]['name']+'.', comp[1]['name'], words, element_renamed)
        implicit_compound_decl(comp[1]['compound'], element, comp[1]['name']+'.', comp[1]['name'], words, words3)
        rename_compound_element(words3, comp, element_renamed)



    for e in compound_element.items():
        for i in range(0,len(connection_list)):
            if e[1]['name'] == connection_list[i]:
                for j in range(0,len(e[1]['compound'])):
                    if e[1]['compound'][j] == 'input':
                        e[1]['compound'][j] = connection_list[i-2]
                    if e[1]['compound'][j] == 'output':
                        e[1]['compound'][j] = connection_list[i+2]

    #print compound_element
    ##############################################################################################################################################
    for c in compound_element.items():
        for e in c[1]['compound']:
            connection_list.append(e)

    ##############################################################################################################################################
    
    connection_element_class_cleaner (connection_list,ele_class_connections,fluxOutput,clean_ele_class_connections)
    connection_element_class_output_closer (connection_list,fluxOutput,clean_ele_class_connections) #gestisce gli output
    for c2 in clean_ele_class_connections:
       connection_list.append(c2)

    
    connection_decl(connection_list, connection, element)
    #print element
    print '\n'
    #print connection
    words[:] = []

    json_data = generateJsont3d(element, connection)
    #print json_data
    return json_data

