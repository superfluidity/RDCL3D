import argparse
import sys
import networkx as nx
from parserView import *
from parserAllView import *
from parserDetailView import *



def run_command(type_view, cfg_files, nx_topology):
	
	if type_view == 'View':
		json_click=parserView(cfg_files, nx_topology)
	
	elif type_view == 'AllView':
		json_click=parserAllView(cfg_files, nx_topology)
	elif type_view == 'DetailView':
		json_click=parserDetailView(cfg_files, nx_topology)

	return json_click	
	#parse_click(args.file, nx_topology)



def parse_cmd_line():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--f', dest='file', action='store', help='file click to parse')
	parser.add_argument('--show',dest='type_view', action='store', help='view type to dispay [View - AllView - DetailView]')
	args = parser.parse_args()  

	if len(sys.argv)<2:
		parser.print_help()
		sys.exit(1)    
	
	if args.type_view != 'View' and args.type_view != 'AllView' and args.type_view != 'DetailView':
		parser.print_help()
		sys.exit(1)  
	

	return args

def importprojectjson(cfg_files):
	nx_topology = nx.MultiDiGraph()
	#args = parse_cmd_line()
	type_view='AllView'
	json_click=run_command(type_view, cfg_files, nx_topology)
	'''
	if len(nx_topology)!=0:
		xml2py(nx_topology)
		#nx.draw(nx_topology)
		#plt.show()
	'''
	#print json_click
	return json_click 	

def importprojectfile(cfg_files):
    project = {
        'click': {}
    }
    for file in cfg_files:
        click =file.read()
        project['click'] = click
      
    return project

