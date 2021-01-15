# Vi Nguyen
# COMP 412
# Lab 3: Instruction Scheduling

# http://webgraphviz.com/

import sys
import utils
import rename
from graph import Node
import cProfile

## GLOBAL VARIABLES ##

block = None
block_str = None
dep_mapping = []
dep_graph = []		# list of nodes with edges
max_cycle = 0
io_ser_edges = []
constants = []		# mapping of registers to constants (from loadI)

### 2. BUILD DEPENDENCY GRAPH ###

def build_dependency_graph(k):
	global dep_mapping
	global dep_graph
	global constants

	dep_mapping = [None] * k
	constants = [None] * k
	dep_graph = []

	loads = []
	stores = []
	outputs = []

	for i in xrange(len(block)):
		# create node
		dep_graph.append(Node(i, block[i].opcode, block[i]))

		if block[i].opcode != 2 and block[i].op3 != None:		# not a `store` op
			vr_def = block[i].op3.vr
			dep_mapping[vr_def] = i

		# arithop
		if block[i].op1 != None and block[i].op2 != None:
			vr_use1 = block[i].op1.vr
			vr_use2 = block[i].op2.vr

			if dep_mapping[vr_use1] != None:
				nbrs(dep_graph[i], dep_graph[dep_mapping[vr_use1]], False)


			if dep_mapping[vr_use2] != None:
				nbrs(dep_graph[i], dep_graph[dep_mapping[vr_use2]], False)

			if constants[vr_use1] != None and constants[vr_use2] != None:
				if block[i].opcode == 3: 	# add
					constants[vr_def] = constants[vr_use1] + constants[vr_use2] 
				elif block[i].opcode == 4:	# sub
					constants[vr_def] = constants[vr_use1] - constants[vr_use2]
				elif block[i].opcode == 5:	# mult
					constants[vr_def] = constants[vr_use1] * constants[vr_use2]
				elif block[i].opcode == 6: 	# rshift
					constants[vr_def] = constants[vr_use1] >> constants[vr_use2]
				elif block[i].opcode == 7: 	# lshift
					constants[vr_def] = constants[vr_use1] << constants[vr_use2]
				else:
					pass

		# load
		if block[i].opcode == 0:
			vr_use1 = block[i].op1.vr

			if dep_mapping[vr_use1] != None:
				nbrs(dep_graph[i], dep_graph[dep_mapping[vr_use1]], False)

		# loadI
		if block[i].opcode == 1:
			constants[block[i].op3.vr] = block[i].op1

		# full latency
		# load and output need an edge to all previous stores (unless independent)
		if block[i].opcode == 0 or block[i].opcode == 8:
			for store in stores:
				if not ind_io(dep_graph[store], dep_graph[i]):
					nbrs(dep_graph[i], dep_graph[store], False)

		# serialization
		# store needs an edge to the previous store and each previous load and output
		# (unless they're independent)
		if block[i].opcode == 2:
			if len(stores) > 0:
				nbrs(dep_graph[i], dep_graph[stores[-1]], True)

			for load in loads:
				if not ind_io(dep_graph[load], dep_graph[i]) and not are_nbrs(dep_graph[i], dep_graph[load]):
					nbrs(dep_graph[i], dep_graph[load], True)

			for output in outputs:
				if not ind_io(dep_graph[output], dep_graph[i]) and not are_nbrs(dep_graph[i], dep_graph[output]):
					nbrs(dep_graph[i], dep_graph[output], True)

		# serialization
		# output needs an edge to the most recent output
		if block[i].opcode == 8:
			if len(outputs) > 0:
				nbrs(dep_graph[i], dep_graph[outputs[-1]], True)

		if block[i].opcode == 0:
			loads.append(i)

		if block[i].opcode == 2:
			stores.append(i)

		if block[i].opcode == 8:
			outputs.append(i)


def nbrs(a, b, is_io_ser):
	global io_edges

	a.out_nbrs.append(b)
	b.in_nbrs.append(a)
	if is_io_ser:
		io_ser_edges.append((a,b))

	# distinct_add(a.out_nbrs, b)
	# distinct_add(b.in_nbrs, a)
	# if is_io_ser:
	# 	distinct_add(io_ser_edges, (a,b))


def are_nbrs(a, b):
	return b in a.out_nbrs


def ind_io(a, b):
	#return False
	# load -> store
	if a.op_type == 0 and b.op_type == 2:
		if constants[a.op.op1.vr] != None and constants[b.op.op2.vr] != None and constants[a.op.op1.vr] != constants[b.op.op2.vr]:
			return True
		else:
			 return False
	# output -> store
	elif a.op_type == 8 and b.op_type == 2:
		if constants[b.op.op2.vr] != None and constants[b.op.op2.vr] != a.op.op1:
			return True
		else:
			return False
	# store -> store
	elif a.op_type == 2 and b.op_type == 2:
		if constants[a.op.op2.vr] != None and constants[b.op.op2.vr] != None and constants[a.op.op2.vr] != constants[b.op.op2.vr]:
			return True
		else:
			return False
	# store -> load
	elif a.op_type == 2 and b.op_type == 0:
		if constants[a.op.op2.vr] != None and constants[b.op.op1.vr] != None and constants[a.op.op2.vr] != constants[b.op.op1.vr]:
			return True
		else:
			return False
	# store -> output
	elif a.op_type == 2 and b.op_type == 8:
		if constants[a.op.op2.vr] != None and constants[a.op.op2.vr] != b.op.op1:
			return True
		else:
			return False
	else:
		return False


### 3. COMPUTE PRIORITIES ###

def compute_priority(a,b):
	# latency-weighted distance from root
	roots = [node for node in dep_graph if len(node.in_nbrs) == 0]

	for root in roots:
		root.prio = root.delay
		stack = []
		stack.extend(root.out_nbrs)

		while stack:
			node = stack.pop()
			for nbr in node.out_nbrs:
				if nbr.delay + node.prio > nbr.prio:
					nbr.prio = nbr.delay + node.prio
					stack.append(nbr)


	# boost for number of successors
	for node in dep_graph:
		node.prio = (a * node.prio) + (b * len(node.in_nbrs))
		if node.op_type == 8:
			node.prio += 2


### 4. SCHEDULE ###

func = [[0, 1, 2, 3, 4, 6, 7, 8, 9], 
		[1, 3, 4, 5, 6, 7, 8, 9]]

def schedule():
	global dep_graph
	global max_cycle

	cycle = 1
	ready = [node for node in dep_graph if len(node.out_nbrs) == 0]
	active = []
	free_f = [0,1]

	while len(ready) > 0 or len(active) > 0:
		for f in free_f:
			if len(ready) > 0:
				ready_for_f = [node for node in ready if node.op_type in func[f]]
				if len(ready_for_f) > 0:
					#node = ready_for_f[0]
					node = max(ready_for_f, key=lambda x: x.prio)
					node.S = cycle
					distinct_add(active, node)
					node.f = f
					ready.remove(node)

		for node in active:
			if node.f in free_f:
				free_f.remove(node.f)

		cycle += 1

		to_remove =[]
		for node in active:
			if (node.S + node.delay) <= cycle:
				to_remove.append(node)
				distinct_add(free_f, node.f)
				node.sat = True
				node.complete = True
				for s in node.in_nbrs:
					if is_ready(s) and s.S == None:
						distinct_add(ready, s)
			if (node.op_type == 0 or node.op_type == 2) and (node.S == cycle - 1):
				node.issued = True
				distinct_add(free_f, node.f)
				for s in node.in_nbrs:
					if is_ready(s) and s.S == None:
						distinct_add(ready, s)
			if node.op_type == 5:
				node.issued = True
				distinct_add(free_f, node.f)

		for node in to_remove:
			active.remove(node)

	max_cycle = cycle


def is_ready(node):
	ready = []
	for parent in node.out_nbrs:
		if ((node, parent) in io_ser_edges and parent.issued) or parent.complete:
			ready.append(True)
		else:
			ready.append(False)
	return all(ready)


def print_iloc():
	dep_graph.sort(key=lambda node: node.S)

	i = 0
	j = 1
	while i < len(dep_graph) and j <= max_cycle:
		if i < len(dep_graph) - 1 and dep_graph[i].S == j and dep_graph[i].S == dep_graph[i+1].S:
			print "[ " + str(block_str[dep_graph[i].name]) + " ; " + str(block_str[dep_graph[i+1].name]) + " ]"
			i += 2
		elif dep_graph[i].S == j:
			print "[ " + str(block_str[dep_graph[i].name]) + " ; nop ]" 
			i += 1
		else:
			print "[ nop ; nop ]"

		j += 1

### HELPER METHODS ###

def distinct_add(lst, elt):
	if elt not in lst:
		lst.append(elt)


def pp_print(lst):
	for elt in lst:
		print str(elt)


def get_block(filename,a,b):
	global block
	global block_str

	block, k, block_str = rename.rename(filename)
	# for str in block_str:
	# 	print str

	build_dependency_graph(k)
	compute_priority(a,b)
	#build_graphviz()
	schedule()
	print_iloc()


def build_graphviz():
	print "digraph block {"

	# print labels
	for i in xrange(len(block)):
		label = str(block_str[dep_graph[i].name])
		print "\t" + str(i) + " [label = \"" + str(dep_graph[i]) + " " + label + "\"];"

	print ""

	for node in dep_graph:
		for nbr in node.out_nbrs:
			print "\t" + str(node.name) + " -> " + str(nbr.name) + " [label= \" " + str(nbr.delay) + " " + str((node,nbr) in io_ser_edges) + "\"];"
		
	print "}"

if sys.argv[1] == "-h":
	print "Syntax: schedule <filename> [-h] // filename is the pathname (absolute or relative) to the input file // -h prints this message"
else:
	get_block(sys.argv[1],0.7,0.3)

#get_block("test_code", 0.7, 0.3)
#print max_cycle

#print constants
#build_graphviz()

#cProfile.run('get_block("T2k.i", 0.7, 0.3)')





