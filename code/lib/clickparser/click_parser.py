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

import argparse
from parserView import *
from parserAllView import *
import os
import glob
from lib.util import Util

def run_command(type_view, cfg_files, id):
    if type_view == 'View':
        json_click = parserView(cfg_files)

    elif type_view == 'AllView':
        json_click = parserAllView(cfg_files, id)
    elif type_view == 'DetailView':
        json_click = parserDetailView(cfg_files)

    return json_click


# parse_click(args.file, nx_topology)


'''
def parse_cmd_line():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--f', dest='file', action='store', help='file click to parse')
    parser.add_argument('--show', dest='type_view', action='store',
                        help='view type to dispay [View - AllView - DetailView]')
    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if args.type_view != 'View' and args.type_view != 'AllView' and args.type_view != 'DetailView':
        parser.print_help()
        sys.exit(1)

    return args
'''

def importprojectjson(project, model = {}, positions = {}):
    #nx_topology = nx.MultiDiGraph()
    # args = parse_cmd_line()
    all_edges = []
    all_vertices = []
    for click in project['click']:
        type_view = 'AllView'
        json_click = run_command(type_view, project['click'][click], click)
        '''
        if len(nx_topology)!=0:
            xml2py(nx_topology)
            #nx.draw(nx_topology)
            #plt.show()
        '''
        json_click = json.loads(json_click)
        all_vertices = all_vertices + json_click['vertices']
        for edge in json_click['edges']:
            if 'click' in edge['group']:
                edge['group'][edge['group'].index("click")] = click
        all_edges = all_edges + json_click['edges']
    json_click['model'] = model
    json_click['vertices'] = all_vertices
    json_click['edges'] = all_edges
    for vertice in json_click['vertices']:
        key = vertice['id']
        if 'vertices' in positions:
            if key in positions['vertices'].keys():
                vertice['fx'] = positions['vertices'][key]['x']
                vertice['fy'] = positions['vertices'][key]['y']
    for edge in json_click['edges']:
        edge['directed_edge'] = True;
    #print model
    # print json_click
    return json_click


def importprojectfile(cfg_files):
    project = {
        'click': {}
    }

    for file in cfg_files:
        if os.path.basename(str(file.name))== 'vertices.json':
            print 'dentrpp ', str(file)
            project['positions'] = {}
            project['positions']['vertices'] = Util.loadjsonfile(file)
        else:
            project['click'][ os.path.splitext(os.path.basename(str(file)))[0]] = file.read()
    return project

def importprojectdir(dir_project, file_type):
    files = []
    for file_name in glob.glob(os.path.join(dir_project, '*.'+file_type)):
        files.append(Util().openfile(file_name))
    for file_name in glob.glob(os.path.join(dir_project, '*.'+'json')):
        files.append(Util().openfile(file_name))

    return importprojectfile(files)
