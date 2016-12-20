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



def parserAllView_new(file_click, nx_topology):
    # with open('/home/user/Progetto_Superfluidity/test-rdcl/lib/clickparser/'+file_click,'r') as f:

    words = []
    element = {}
    connection = {}
    line2 = ''
    concatenate_conf = False
    concatenate_compound = False
    concatenate_line = False
    list_lines = []
    compound_element = {}                                                           # lista contenente tutti gli elementi contenuti all'interno nel compound
                                                                                    #con il relativo nome del compound 

    text = "".join([s for s in file_click.splitlines(True) if s.strip("\r\n")])
    #print text
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

        #if string.find(line, 'elementclass'):
        #    print ''   

        if concatenate_line:
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
            compound_line=line[string.find(line, '{')+1:string.find(line, '}')]                 # contiene tutta la dichiarazione del compound elment
            name = subgraph_element(compound_line, compound_element, element)
            line = line[0:string.find(line, '{')]+name+line[string.find(line, '}')+1:]


        explicit_elment_decl(line, element,'', 'click', words)
        implicit_element_decl(line, element,'', 'click', words)
        load_list(line, words)
    
        
    print words
    #print '\n'
    #print element
    print '########################'

    rename_element_list(element, words)
    print words
    #rename_element_list_new(element, words)
    '''
    for line in compound_element.items():
        explicit_elment_decl(line[1]['compound'], element, line[1]['name']+'.', line[1]['name'], words)
        implicit_element_decl(line[1]['compound'], element, line[1]['name']+'.', line[1]['name'], words)
    ''' 
    #print words
    connection_decl(words, connection, element)
    words[:] = []

    json_data = generateJsont3d(element, connection)
    #print json_data
    return json_data

    #print element
    #print connection
        #print line

