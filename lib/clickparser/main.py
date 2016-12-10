from parserClick import *
from xml2py import *
import argparse
import sys
import networkx as nx
import matplotlib.pyplot as plt
from parserView import *
from parserAllView import *
from parserDetailView import *



def run_command(data,nx_topology):
	
	if args.type_view == 'View':
		parserView(args.file, nx_topology)
	
	elif args.type_view == 'AllView':
		parserAllView(args.file, nx_topology)
	elif args.type_view == 'DetailView':
		parserDetailView(args.file, nx_topology)

	#parse_click(args.file, nx_topology)


	#add_edge_nodes(nx_topology)
	#flow_allocator(args.controllerRestIp)
	#simulate_flow_allocator(nx_topology, args.file)

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

	
	
if __name__ == '__main__':

	nx_topology = nx.MultiDiGraph()
	args = parse_cmd_line()
	run_command(args,nx_topology)
	if len(nx_topology)!=0:
		xml2py(nx_topology)
		#for node in nx_topology.nodes_iter(data = True):
				#print node[1]['element'] +' '+ node[1]['portcount'] +' '+ node[1]['flowcode'] +' '+node[1]['processing']
		nx.draw(nx_topology)
		plt.show() 
