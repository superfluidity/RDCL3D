import networkx as nx
import json

class RandomBuilder():


	def __init__(self, n, p):
		#super(ModelController, self).__init__()
		
		self.n = int(n)
		self.p = float(p)
		self.vertices = {}
		self.edges = {}
		g = nx.erdos_renyi_graph(self.n, self.p)

		for i in g.nodes():
			self.vertices[i] = { 'info':{'frozen': False}}
		for (n1, n2) in g.edges():
			self.edges[str(n1)+"&&"+str(n2)] = {'links':[{'view':'Data'}]}

		#print(g.nodes())
		#print(g.edges())
		#print(self.vertices)

	def getJson(self):
		grap = {'vertices': self.vertices,
		'edges': self.edges}
		return json.JSONEncoder().encode(grap)

if __name__ == '__main__':
	test = RandomBuilder(8, 0.5)
	print test.getJson()