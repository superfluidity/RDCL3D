import json
import pkgutil

class ce():

	


	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
	


	"""docstring for ce"""
	def __init__(self, arg):
		

		self.spec = {
			"node_label" : 'cer',
			"properties": {
				"loopback": "",
				"vm":{
						"mgt_ip": "",
						"interfaces": ""
				}	
			}
		}