import json
import pkgutil

class ofcontroller():

	


	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
	


	"""docstring for ofcontroller"""
	def __init__(self, arg):
		

		self.spec = {
			"node_label" : 'ctr',
			"properties": {
				"tcp_port": "",
				"loopback": "",
				"vm":{
						"mgt_ip": "",
						"interfaces": ""
				}	
			}
		}