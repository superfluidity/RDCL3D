import argparse
from parserView import *
from parserAllView import *
import os
import glob
from lib.util import Util

def run_command(type_view, cfg_files):
    if type_view == 'View':
        json_click = parserView(cfg_files)

    elif type_view == 'AllView':
        json_click = parserAllView(cfg_files)
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

def importprojectjson(cfg_files, model = {}, positions = {}):
    #nx_topology = nx.MultiDiGraph()
    # args = parse_cmd_line()
    type_view = 'AllView'
    json_click = run_command(type_view, cfg_files)
    '''
    if len(nx_topology)!=0:
        xml2py(nx_topology)
        #nx.draw(nx_topology)
        #plt.show()
    '''
    json_click = json.loads(json_click)
    json_click['model'] = model
    for vertice in json_click['vertices']:
        key = vertice['id']
        if 'vertices' in positions:
            if key in positions['vertices'].keys():
                vertice['fx'] = positions['vertices'][key]['x']
                vertice['fy'] = positions['vertices'][key]['y']
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