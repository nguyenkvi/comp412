import utils
import op_list

def delay(op_type):
	if op_type == 0 or op_type == 2:
		return 5
	elif op_type == 5:
		return 3
	else:
		return 1

class Node:
	def __init__(self, name, op_type, op):
		self.name = name
		self.op_type = op_type
		self.op = op
		self.delay = delay(op_type)
		self.prio = 0
		self.S = None
		self.in_nbrs = []	# successors
		self.out_nbrs = []	# parents
		self.complete = False
		self.issued = False
		self.f = None

	def __str__(self):
		return str(self.name) + " " + utils.word_mapping[self.op_type] + " (p: " + str(self.prio) + ", s: " + str(self.S) + ", f: " + str(self.f) + ")"
