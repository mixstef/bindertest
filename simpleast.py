

class ASTNode:

	def __init__(self,subnodes=None,attributes=None,from_json=None):
		
		""" Creates a new AST node. The following optional arguments can be
		supplied:
		- `subnodes` is a list of existing AST nodes that will be linked as
		  children of this node
		- `attributes` is a dict containing (attr-name,attr-value) pairs for
		  this node
		- `from_json` is a JSON string TBD
		""" 
		
		if subnodes is not None:
			self.subnodes = list(subnodes)
		else:
			self.subnodes = []
			
		if attributes is not None:
			self.attributes = dict(attributes)
			
			
	def __str__(self):
		
		""" Returns a pretty-printed textual description of node's content
		(and recursively its children, if any) """
		
		return self._pprint(0,'')
		
		
	def _pprint(self,level,spacer,last=True):
	
		""" Returns formatted node info at a certain `level` of indentation,
		`last` is True if node is last child """
		
		prefix = 'ASTNode'
		if level>0:
			if last: ch = '└── ASTNode'
			else: ch = '├── ASTNode'
			prefix = spacer+ch
			
		infol = [prefix + str(self.attributes)]
		
		# recurse over subnodes
		newspacer = ''
		if level>0:
			if last: newspacer = spacer+'    '
			else: newspacer = spacer+'│   '
		for ix,child in enumerate(self.subnodes):
			infol.append(child._pprint(level+1,newspacer,ix==len(self.subnodes)-1))
		
		return '\n'.join(infol)
			
	
	def subnode(self,i):
	
		""" Returns `i`-th subnode """
		
		return self.subnodes[i]
		 
	
	def attribute(self,name):
	
		""" Returns the value of attribute `name` """
		
		return self.attributes[name]
		
		


