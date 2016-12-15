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


def generateJsont3d(element, connection):
    json_data = nx_2_t3d_json(element, connection, 'out.t3d')
    return json_data


def parserDetailView(compound_element_cont, nx_topology):

    words = []
    element = {}
    connection = {}
    line2 = ''
    concatenate = False

    text = "".join([s for s in compound_element_cont.splitlines(True) if s.strip("\r\n")])

    for line in text.splitlines():
        if line[0] != "/":

            if string.find(line, '//') != -1:  # elimina i commenti dalla riga
                line = line[0:string.find(line, '//') - 1]

            if string.find(line, '[') != -1:  # questo blocco modifica l'intera linea per gestire la lettura
                index = string.find(line, '[')  # delle porte di uscita dell'elemento che possono essere scritte
                if line[index - 1] == ' ' and line[index - 2].islower():  # sia come [num]port che [num] port
                    line = line[0:index - 1] + '' + line[index:]

            if string.find(line, '{') != -1:

                line2 = line
                concatenate = True
                continue
            elif concatenate:
                line = line2 + ' ' + line
                start = string.find(line, '{')
                stop = string.find(line, '}')
                concatenate = False
                line2 = ''

                line = compound_element(line)
                
            explicit_elment_decl(line, element)
            implicit_element_decl(line, element)
            load_list(line, words)

    rename_element_list(element, words)

    connection_decl(words, connection, element)


    print '\n'
    print element
    print'\n \n \n \n'
    print words
    # print connection
    words[:] = []

    # generateTopology(element, connection, nx_topology)			#genera la topologia per nx
    json_data = generateJsont3d(element, connection)  # genera elemento Json

    return json_data
