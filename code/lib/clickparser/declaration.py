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
from utility import *


def explicit_element_decl(line, element, name_subgraph, group, words, ele_class_dict, ele_class_connections):
    config = False
    words = []
    index = []
    ele_class_name = ''
    line_class_element = ''
    elementclass_renamed = {}
    words3 = []
    ele_class_lists = []
    name_ele = ''
    words = load_list(line, words)
    control = False

    for i in range(0, len(words)):
        control = False

        if words[i] == '::':
            for c1 in range(0, len(words[i + 1])):
                if words[i + 1][c1] == '(':
                    break
                ele_class_name = ele_class_name + words[i + 1][c1]

            for c2 in ele_class_dict.keys():
                if ele_class_name == ele_class_dict[c2]['name']:
                    control = True
                    if string.find(words[i + 1], '(') != -1 and string.find(words[i + 1], ')') != -1:
                        explicit_element_decl_with_conf(i, words, element, name_subgraph, group, 'class_element')
                    elif string.find(words[i + 1], '(') == -1 and string.find(words[i + 1], ')') == -1:
                        explicit_element_decl_without_conf(i, words, element, name_subgraph, group, 'class_element')
                    for j in ele_class_dict[c2]['elementclassstr']:

                        if j == ';':
                            words1 = []
                            name_ele = name_subgraph
                            if name_ele != '':
                                name_ele = name_ele + words[i - 1]
                            else:
                                name_ele = words[i - 1] + '.'

                            explicit_element_decl(line_class_element, element, name_ele, name_ele, words,
                                                  ele_class_dict, ele_class_connections)

                            implicit_element_decl(line_class_element, element, name_ele, name_ele, words, words1)

                            if name_ele[len(name_ele) - 1] == '.':
                                name_ele = name_ele[0:len(name_ele) - 1]

                            rename_class_element(words, words1, words3, name_ele, words[i - 1])

                            words3.append(words1)

                            line_class_element = ''
                        else:
                            line_class_element = line_class_element + j

                    # '********** Lista di parole pulite*********'

                    ele_class_lists = sum(words3, [])
                    
                    ele_class_connections[len(ele_class_connections)] = (
                    {'element name': name_ele, 'connection_elem_list': ele_class_lists})
                # '*******************************************'

            if control == False:
                index.append(i)

    for i in index:

        if string.find(words[i + 1], '(') != -1 and string.find(words[i + 1], ')') != -1:
            explicit_element_decl_with_conf(i, words, element, name_subgraph, group, 'element')
        elif string.find(words[i + 1], '(') == -1 and string.find(words[i + 1], ')') == -1:
            explicit_element_decl_without_conf(i, words, element, name_subgraph, group, 'element')


def implicit_element_decl(line, element, name_subgraph, group, words, words2):
    words = []
    

    words = load_list(line, words)

    for w in words:
        words2.append(w)

    for i in range(0, len(words)):
        check = False                                                   # se falso significa che e' un elemento implicito e non una variabile con lettera maiuscola
        index = string.find(words[i], '(')
        for el in element:
            check = check_element(check, element[el]['name'], words[i]) 

        if check == False and words[i][0].isupper() and words[i-1]!='::':
                if string.find(words[i], '(') !=-1 and string.find(words[i], ')') !=-1:
                    implicit_element_decl_with_conf(i, words, element, name_subgraph, group, words2)
        
                elif string.find(words[i], '(') ==-1 and string.find(words[i], ')') ==-1:
                        implicit_element_decl_without_conf(i, words, element, name_subgraph, group, words2)



def explicit_compound_decl(line, element, name_subgraph, group, words, element_renamed):
    config = False
    words = []
    index = []

    words = load_list(line, words)

    for i in range(0, len(words)):
        if words[i] == '::':
            index.append(i)

    for i in index:

        if string.find(words[i + 1], '(') != -1 and string.find(words[i + 1], ')') != -1:
            explicit_element_decl_with_conf(i, words, element, name_subgraph, group, 'element')
            element_renamed[len(element_renamed)] = {'origin_name': words[i - 1],
                                                     'new_name': name_subgraph + words[i - 1]}
        elif string.find(words[i + 1], '(') == -1 and string.find(words[i + 1], ')') == -1:
            explicit_element_decl_without_conf(i, words, element, name_subgraph, group, 'element')
            element_renamed[len(element_renamed)] = {'origin_name': words[i - 1],
                                                     'new_name': name_subgraph + words[i - 1]}


def implicit_compound_decl(line, element, name_subgraph, group, words, words2):
    words = []

    words = load_list(line, words)

    for w in words:
        words2.append(w)

    for i in range(0, len(words)):
        check = False
        index = string.find(words[i], '(')
        for el in element:
            check = check_element(check, element[el]['name'], words[i]) 

        if check == False and words[i][0].isupper() and words[i-1]!='::':
                if string.find(words[i], '(') !=-1 and string.find(words[i], ')') !=-1:
                    implicit_element_decl_with_conf(i, words, element, name_subgraph, group, words2)
        
                elif string.find(words[i], '(') ==-1 and string.find(words[i], ')') ==-1:
                        implicit_element_decl_without_conf(i, words, element, name_subgraph, group, words2)



def subgraph_ele_class(line2, ele_class_element):
    class_element_cont = []
    class_element_lines = []

    class_element_str = ''
    control = False

    class_element_lines = load_list(line2, class_element_lines)

    i = 0  # trova il nome della element class
    while i < len(class_element_lines):
        l = class_element_lines[i]
        if l == 'elementclass':
            name = class_element_lines[i + 1]
        i = i + 1

    for z in class_element_lines:
        if z != 'elementclass' and z != '{' and z != '}' and z != name:
            class_element_cont.append(z)

    for w1 in line2:
        if w1 == '{':
            control = True
            continue
        if w1 == '}':
            control = False
            break
        if control == True:
            class_element_str = class_element_str + w1

    ele_class_element[len(ele_class_element)] = (
    {'name': name, 'elementclasscontenent': class_element_cont, 'elementclassstr': class_element_str})


def connection_decl(words, connection, element):

    for i in range(0, len(words)):
        if words[i] == '->':
            port_input = 0
            port_output = 0

            if words[i - 2] == '::':
                name_element_source = words[i - 3]

            elif string.find(words[i - 1], '[') != -1:
                if string.find(words[i - 1], '[') == 0:
                    index = string.find(words[i - 1], ']')
                    words[i - 1] = words[i - 1][index + 1:]

                if string.find(words[i - 1], '[') != -1:
                    index = string.find(words[i - 1], '[')
                    port_input = words[i - 1][index + 1:index + 2]
                    name_element_source = words[i - 1][0:index]
                else:
                    name_element_source = words[i - 1]

            else:
                name_element_source = words[i - 1]

            try:
                if words[i + 2] == '::':
                    name_element_dest = words[i + 1]
                elif string.find(words[i + 1], ']') != -1:
                    index = string.find(words[i + 1], ']')
                    port_output = words[i + 1][1:index]
                    name_element_dest = words[i + 1][index + 1:]
                else:
                    name_element_dest = words[i + 1]
            except IndexError:
                if string.find(words[i + 1], ']') != -1:
                    index = string.find(words[i + 1], ']')
                    port_output = words[i + 1][1:index]
                    name_element_dest = words[i + 1][index + 1:]
                else:
                    name_element_dest = words[i + 1]

            view = []

            for el1 in element.items():  # gestisce l'attributo view delle connessioni. Puo' essere:
                if el1[1]['name'] == name_element_source:  # 'compact' se i due nodi non sono espandibili
                    for el2 in element.copy().items():  # 'expanded' se i due nodi sono entrambi espandibili
                        if el2[1][
                            'name'] == name_element_dest:  # 'compact''expanded' se uno dei due nodi e' exspandibile e l'altro no
                            if el1[1]['node_type'] == 'element' and el2[1]['node_type'] == 'element':
                                view.append('compact')
                            elif (el1[1]['node_type'] == 'element' and el2[1]['node_type'] == 'compound_element') or (
                                    el2[1]['node_type'] == 'element' and el1[1]['node_type'] == 'compound_element'):
                                view.append('compact')
                                view.append('expandable')
                            elif (el1[1]['node_type'] == 'element' and el2[1]['node_type'] == 'class_element') or (
                                    el2[1]['node_type'] == 'element' and el1[1]['node_type'] == 'class_element'):
                                view.append('compact')
                                view.append('expandable')
                            elif (el1[1]['node_type'] == 'class_element' and el2[1][
                                'node_type'] == 'class_element') or (
                                    el1[1]['node_type'] == 'compound_element' and el2[1][
                                'node_type'] == 'compound_element'):
                                view.append('expandable')

            connection[len(connection)] = (
            {'source': name_element_source, 'target': name_element_dest, 'port-input': port_input,
             'port-output': port_output, 'group': [], 'depth': 0, 'view': view})

    handle_edgeslevel(connection)


def connection_element_class_cleaner(connection_list, ele_class_connections, fluxOutput, clean_ele_class_connections):
    templist = []
    temp_connections = []

    for i in range(0, len(connection_list)):
        if connection_list[i] == '->':
            for j in range(0, len(ele_class_connections.keys())):
                if connection_list[i + 1] == ele_class_connections[j]['element name']:
                    for c1 in range(0, len(ele_class_connections[j]['connection_elem_list'])):
                        if ele_class_connections[j]['connection_elem_list'][c1] == '->':
                            if string.find(ele_class_connections[j]['connection_elem_list'][c1 - 1], 'input') != -1:
                                clean_ele_class_connections.append(connection_list[i - 1])
                                clean_ele_class_connections.append(ele_class_connections[j]['connection_elem_list'][c1])
                                clean_ele_class_connections.append(
                                    ele_class_connections[j]['connection_elem_list'][c1 + 1])
                                temp_connections.append(ele_class_connections[j]['connection_elem_list'][c1 - 1])
                                temp_connections.append(ele_class_connections[j]['connection_elem_list'][c1])
                                temp_connections.append(ele_class_connections[j]['connection_elem_list'][c1 + 1])


                            elif string.find(ele_class_connections[j]['connection_elem_list'][c1 + 1], 'output') != -1:
                                templist.append(ele_class_connections[j]['connection_elem_list'][c1 - 1])
                                templist.append(ele_class_connections[j]['connection_elem_list'][c1])
                                templist.append(ele_class_connections[j]['connection_elem_list'][c1 + 1])
                                fluxOutput[len(fluxOutput)] = (
                                {'Level': ele_class_connections[j]['element name'], 'Output fluttuante': templist})
                                templist = []

                            else:
                                contr = False
                                for k in range(0, len(ele_class_connections.keys())):
                                    if ele_class_connections[j]['connection_elem_list'][c1 + 1] == \
                                            ele_class_connections[k]['element name']:
                                        clean_ele_class_connections.append(
                                            ele_class_connections[j]['connection_elem_list'][c1 - 1])
                                        clean_ele_class_connections.append(
                                            ele_class_connections[j]['connection_elem_list'][c1])
                                        clean_ele_class_connections.append(
                                            ele_class_connections[j]['connection_elem_list'][c1 + 1])
                                        connection_element_class_cleaner(
                                            ele_class_connections[j]['connection_elem_list'], ele_class_connections,
                                            fluxOutput, clean_ele_class_connections)
                                        contr = True

                                if contr == False:
                                    clean_ele_class_connections.append(
                                        ele_class_connections[j]['connection_elem_list'][c1 - 1])
                                    clean_ele_class_connections.append(
                                        ele_class_connections[j]['connection_elem_list'][c1])
                                    clean_ele_class_connections.append(
                                        ele_class_connections[j]['connection_elem_list'][c1 + 1])

                    ele_class_connections[j]['connection_elem_list'] = temp_connections
                    temp_connections = []


def connection_element_class_output_closer(connection_list, fluxOutput, clean_ele_class_connections):
    fluxOutput_new = {}

    for i in range(0, len(fluxOutput)):
        for j in range(0, len(fluxOutput[i]['Output fluttuante'])):
            if string.find(fluxOutput[i]['Output fluttuante'][j], 'output') != -1:
                if fluxOutput[i]['Output fluttuante'][j] == 'output':
                    port_output = '0'
                else:
                    start = string.find(fluxOutput[i]['Output fluttuante'][j], '[')
                    stop = string.find(fluxOutput[i]['Output fluttuante'][j], ']')
                    port_output = fluxOutput[i]['Output fluttuante'][j][start + 1:stop]
                control = False
                for k in range(0, len(clean_ele_class_connections)):
                    if clean_ele_class_connections[k] == '->' and string.find(clean_ele_class_connections[k - 1],
                                                                              fluxOutput[i]['Level']) != -1:
                        length_word = len(fluxOutput[i]['Level'])
                        if len(clean_ele_class_connections[k - 1]) == length_word or clean_ele_class_connections[k - 1][
                            length_word] == '[':
                            if string.find(clean_ele_class_connections[k - 1], '[') == -1:
                                port_input = '0'
                            elif string.find(clean_ele_class_connections[k - 1], '[') != -1:
                                start = string.find(clean_ele_class_connections[k - 1], '[')
                                stop = string.find(clean_ele_class_connections[k - 1], ']')
                                port_output = clean_ele_class_connections[k - 1][start + 1:stop]
                            if port_input == port_output:
                                clean_ele_class_connections.append(fluxOutput[i]['Output fluttuante'][j - 2])
                                clean_ele_class_connections.append(fluxOutput[i]['Output fluttuante'][j - 1])
                                clean_ele_class_connections.append(clean_ele_class_connections[k + 1])
                                control = True

                for z in range(0, len(connection_list)):
                    if connection_list[z] == '->' and string.find(connection_list[z - 1], fluxOutput[i]['Level']) != -1:
                        if connection_list[z - 1] == fluxOutput[i]['Level']:
                            port_input = '0'
                        elif string.find(connection_list[z - 1], '[') != -1:
                            start = string.find(connection_list[z - 1], '[')
                            stop = string.find(connection_list[z - 1], ']')
                            if connection_list[z - 1][:start] == fluxOutput[i]['Level']:
                                port_input = connection_list[z - 1][start + 1:stop]
                                if port_output == port_input:
                                    clean_ele_class_connections.append(fluxOutput[i]['Output fluttuante'][j - 2])
                                    clean_ele_class_connections.append(fluxOutput[i]['Output fluttuante'][j - 1])
                                    clean_ele_class_connections.append(connection_list[z + 1])
                                    control = True

                if control == False:
                    fluxOutput_new[len(fluxOutput_new)] = (
                    {'Level': fluxOutput[i]['Level'], 'Output fluttuante': fluxOutput[i]['Output fluttuante']})

    fluxOutput = fluxOutput_new
    if len(fluxOutput) > 0:
        connection_element_class_output_closer(connection_list, fluxOutput, clean_ele_class_connections)
