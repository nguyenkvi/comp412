class RegClass:
	def __init__(self, size):
		self.size = size
		self.name = [None] * size
		self.next = [float('inf')] * size
		self.free = [True] * size
		self.stack = range(size-1,-1,-1)
		self.stacktop = size-1