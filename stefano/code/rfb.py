#!/usr/bin/python

import argparse
import sys
import os
import yaml
import json
 

def run_command(args_in):


	if args_in.read_yaml:

		print "*** Read yaml File"
		path = args_in.file
		if os.path.exists(path):
				conf = open(path,'r')
				data = yaml.load(conf)
				conf.close()
		else:
			print "No Configuration File Find In %s" % path
			sys.exit(-2)	


		my_json = json.dumps(data)
		 
		print(my_json)

# 1) 
# python rfb.py --read_yaml --f ../RFBD/rfb-template-one-rfbc.yaml  


def parse_cmd_line():
	parser = argparse.ArgumentParser(description="rfb description maninpulation")
	parser.add_argument('--in', dest='file_type_in', action='store', default='yaml_rfbd', help='type of input file , default = yaml_rfbd, options = ')
	parser.add_argument('--out', dest='file_type_out', action='store', default='json', help='type of output file, default = json, options = ')
	parser.add_argument('--read_yaml', dest='read_yaml', action='store_true', help='read_yaml')
	parser.add_argument('--f', dest='file', action='store', help='input file to parse')



	args = parser.parse_args()    
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)    
	return args

	
if __name__ == '__main__':
	args = parse_cmd_line()
	run_command(args)