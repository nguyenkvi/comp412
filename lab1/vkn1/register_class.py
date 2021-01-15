class RegClass:
	def __init__(self, size):
		self.size = size
		self.name = [None] * size
		self.next = [float('inf')] * size
		self.free = [True] * size
		self.stack = range(size-1,-1,-1)
		self.stacktop = size-1

	def __str__(self):
		return 'NAME: ' + str(self.name) + '\n' + 'NEXT: ' + str(self.next) + '\n' + 'FREE: ' + str(self.free) + '\n' + 'STACK: ' + str(self.stack) + '\n' + 'STACKTOP: ' + str(self.stacktop) + '\n' 