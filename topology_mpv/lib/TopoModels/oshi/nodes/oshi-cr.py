import json
import pkgutil

class oshicr():

	


	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
	


	"""docstring for Oshi"""
	def __init__(self, arg):
		

		self.spec = {
			"node_label" : 'cro',
			"properties": {
				"loopback": "",
				"vm":{
						"mgt_ip": "",
						"interfaces": ""
				}				
			}
		}
