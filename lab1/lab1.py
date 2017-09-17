# Vi Nguyen
# COMP 412
# Lab 1: Local Register Allocation

import sys
from op_list import IROperand
from op_list import Op
from register_class import RegClass
import utils

## GLOBAL VARIABLES ##

scan_i = 0
block_length = 0

vr_name = 0
largest_sr = 0
sr_to_vr = []
lu = []

maxlive = 0


## MAIN METHODS ##


def alloc(filename, k):
	f = open(filename, 'r')
	prog = f.read()
	ops = parser(list(prog))
	rename_registers(ops)
	local_alloc(ops, k)
	return utils.renamed_prog(ops)


def scanner(block):
	global largest_sr
	global scan_i

	c = next_char(block)

	if c == '\n' or c == '\r' or c == ' ' or c == '\t':
		return (None, 10)	# whitespace

	elif c == ',':
		return (10, 7) # ,

	elif c == '=':
		c = next_char(block)
		if c == '>':
			return (11, 8) # =>
		else:
			raise RuntimeError('scanner error: unrecognized token')

	elif c == 's':
		c = next_char(block)
		if c == 't':
			c = next_char(block)
			if c == 'o':
				c = next_char(block)
				if c == 'r':
					c = next_char(block)
					if c == 'e':
						c = next_char(block)
						if c == '\n' or c == '\r' or c == ' ' or c == '\t' or c == None:
							return (2, 0) # store
						else:
							raise RuntimeError('scanner error: unrecognized token')
					else:
						
						raise RuntimeError('scanner error: unrecognized token')
				else:
					
					raise RuntimeError('scanner error: unrecognized token')
			else:
				
				raise RuntimeError('scanner error: unrecognized token')
		elif c == 'u':
			c = next_char(block)
			if c == 'b':
				c = next_char(block)
				if c == '\n' or c == '\r' or c == ' ' or c == '\t' or c == None:
					return (4, 2) # sub
				else:
					raise RuntimeError('scanner error: unrecognized token')
			else:
				
				raise RuntimeError('scanner error: unrecognized token')
		else:
			
			raise RuntimeError('scanner error: unrecognized token')

	elif c == 'r':
		c = next_char(block)
		if c.isdigit():
			num = ''
			while c != None and c.isdigit():
				num += c
				c = next_char(block)
			if c != None:
				scan_i -= 1
			if int(num) > largest_sr:
				largest_sr = int(num)
			return (int(num), 6)
		elif c == 's':
			c = next_char(block)
			if c == 'h':
				c = next_char(block)
				if c == 'i':
					c = next_char(block)
					if c == 'f':
						c = next_char(block)
						if c == 't':
							c = next_char(block)
							if c == '\n' or c == '\r' or c == ' ' or c == '\t' or c == None:
								return (6, 2) #rshift
							else:
								raise RuntimeError('scanner error: unrecognized token')
						else:
							
							raise RuntimeError('scanner error: unrecognized token')
					else:
						
						raise RuntimeError('scanner error: unrecognized token')
				else:
					
					raise RuntimeError('scanner error: unrecognized token')
			else:
				
				raise RuntimeError('scanner error: unrecognized token')
		else:
			
			raise RuntimeError('scanner error: unrecognized token')

	elif c == 'l':
		c = next_char(block)
		if c == 's':
			c = next_char(block)
			if c == 'h':
				c = next_char(block)
				if c == 'i':
					c = next_char(block)
					if c == 'f':
						c = next_char(block)
						if c == 't':
							c = next_char(block)
							if c == '\n' or c == '\r' or c == ' ' or c == '\t' or c == None:
								return (7, 2) #lshift
							else:
								raise RuntimeError('scanner error: unrecognized token')
						else:
							
							raise RuntimeError('scanner error: unrecognized token')
					else:
						
						raise RuntimeError('scanner error: unrecognized token')
				else:
					
					raise RuntimeError('scanner error: unrecognized token')
			else:
				
				raise RuntimeError('scanner error: unrecognized token')
		elif c == 'o':
			c = next_char(block)
			if c == 'a':
				c = next_char(block)
				if c == 'd':
					c = next_char(block)
					if c == 'I':
						c = next_char(block)
						if c == '\n' or c == '\r' or c == ' ' or c == '\t' or c == None:
							return (1, 1)	# loadI
						else:
							raise RuntimeError('scanner error: unrecognized token')
					elif c == '\n' or c == '\r' or c == ' ' or c == '\t' or c == None:
						return (0,0)	# load
					else:
						raise RuntimeError('scanner error: unrecognized token')
				else:
					
					raise RuntimeError('scanner error: unrecognized token')
			else:
				
				raise RuntimeError('scanner error: unrecognized token')
		else:
			
			raise RuntimeError('scanner error: unrecognized token')

	elif c == 'm':
		c = next_char(block)
		if c == 'u':
			c = next_char(block)
			if c == 'l':
				c = next_char(block)
				if c == 't':
					c = next_char(block)
					if c == '\n' or c == '\r' or c == ' ' or c == '\t' or c == None:
						return (5, 2) # mult
					else:
						raise RuntimeError('scanner error: unrecognized token')
				else:
					
					raise RuntimeError('scanner error: unrecognized token')
			else:
				
				raise RuntimeError('scanner error: unrecognized token')
		else:
			
			raise RuntimeError('scanner error: unrecognized token')

	elif c == 'a':
		c = next_char(block)
		if c == 'd':
			c = next_char(block)
			if c == 'd':
				c = next_char(block)
				if c == '\n' or c == '\r' or c == ' ' or c == '\t' or c == None:
					return (3, 2) # add
				else:
					raise RuntimeError('scanner error: unrecognized token')
			else:
				
				raise RuntimeError('scanner error: unrecognized token')
		else:
			
			raise RuntimeError('scanner error: unrecognized token')

	elif c == 'n':
		c = next_char(block)
		if c == 'o':
			c = next_char(block)
			if c == 'p':
				c = next_char(block)
				if c == '\n' or c == '\r' or c == ' ' or c == '\t' or c == None:
					return (9, 4)	# nop
				else:
					raise RuntimeError('scanner error: unrecognized token')
			else:
				
				raise RuntimeError('scanner error: unrecognized token')
		else:
			
			raise RuntimeError('scanner error: unrecognized token')

	elif c == 'o':
		c = next_char(block)
		if c == 'u':
			c = next_char(block)
			if c == 't':
				c = next_char(block)
				if c == 'p':
					c = next_char(block)
					if c == 'u':
						c = next_char(block)
						if c == 't':
							c = next_char(block)
							if c == '\n' or c == '\r' or c == ' ' or c == '\t' or c == None:
								return (8, 3)	# output
							else:
								raise RuntimeError('scanner error: unrecognized token')
						else:
							
							raise RuntimeError('scanner error: unrecognized token')
					else:
						
						raise RuntimeError('scanner error: unrecognized token')
				else:
					
					raise RuntimeError('scanner error: unrecognized token')
			else:
				
				raise RuntimeError('scanner error: unrecognized token')
		else:
			
			raise RuntimeError('scanner error: unrecognized token')

	elif c != None and c.isdigit():
		num = ''
		while c != None and c.isdigit():
			num += c
			c = next_char(block)
		if c != None:
			scan_i -= 1
		return (int(num), 5)	# constant

	elif c == '/':
		c = next_char(block)
		if c == '/':
			while c != None and c != '\r' and c != '\n':
				c = next_char(block)
			if c == '\r':
				c = next_char(block)
				if c == '\n':
					return (12, 9)	# comment
				else:
					
					raise RuntimeError('scanner error: unrecognized token')
			else:
				return (12, 9)	# comment
		else:
			raise RuntimeError('scanner error: unrecognized token')

	else:
		return None


def parser(block):
	global sr_to_vr
	global lu
	global block_length

	block_length = len(block)

	parsed_block = []

	while scan_i < block_length:
		next = parser_helper(block)
		if next != None and next.opcode != 9:
			parsed_block.append(next)

	sr_to_vr = [-1] * (largest_sr + 1)
	lu = [float('inf')] * (largest_sr + 1)

	return parsed_block

	# prev_node = None

	# while block:
	# 	node = parser_helper(block)
	# 	node.set_prev(prev_node)
	# 	if prev_node != None:
	# 		prev_node.set_next(node)
	# 	prev_node = node

	# return node


def rename_registers(ops):
	global maxlive
	live_values = []

	for i in xrange(len(ops)-1, -1, -1):
		# ARITHOP
		if ops[i].op1 != None and ops[i].op2 != None and ops[i].op3 != None:
			update(ops[i].op3, i)	# update and kill
			sr_to_vr[ops[i].op3.sr] = -1
			lu[ops[i].op3.sr] = float('inf')

			update(ops[i].op1, i)	# update one use
			update(ops[i].op2, i)	# update other use

			distinct_add(live_values, ops[i].op1.vr)
			distinct_add(live_values, ops[i].op2.vr)
			live_values.remove(ops[i].op3.vr)

		# load
		elif ops[i].opcode == 0:
			update(ops[i].op3, i)	# update and kill
			sr_to_vr[ops[i].op3.sr] = -1
			lu[ops[i].op3.sr] = float('inf')

			update(ops[i].op1, i)	# update one use

			distinct_add(live_values, ops[i].op1.vr)
			live_values.remove(ops[i].op3.vr)

		# store
		elif ops[i].opcode == 2:
			update(ops[i].op1, i)	# update one use
			update(ops[i].op2, i)	# update other use

			distinct_add(live_values, ops[i].op1.vr)
			distinct_add(live_values, ops[i].op2.vr)

		# LOADI
		elif ops[i].opcode == 1:
			update(ops[i].op3, i)	# update and kill
			sr_to_vr[ops[i].op3.sr] = -1
			lu[ops[i].op3.sr] = float('inf')

			live_values.remove(ops[i].op3.vr)

		if len(live_values) > maxlive:
			maxlive = len(live_values)
			maxlive = len(live_values)


def local_alloc(ops, k):
	if maxlive > k:
		k -= 1

	regclass = RegClass(k)

	for op in ops:
		# op r1, r2 => r3
		if op.opcode != 0 and op.opcode != 1 and op.opcode != 2 and op.opcode != 8:
			prx = ensure(op.op1.vr, regclass)
			pry = ensure(op.op2.vr, regclass)

			if op.op1.nu == float('inf'):
				free(prx, regclass)

			if op.op2.nu == float('inf'):
				free(pry, regclass)

			prz = allocate(op.op3.vr, regclass)

			op.op1.pr = prx
			op.op2.pr = pry
			op.op3.pr = prz

			if op.op1.nu != float('inf'):
				regclass.next[prx] = op.op1.nu

			if op.op2.nu != float('inf'):
				regclass.next[pry] = op.op2.nu		

			regclass.next[prz] = op.op3.nu

		# op r1 => r3 (load)
		elif op.opcode == 0:
			prx = ensure(op.op1.vr, regclass)

			if op.op1.nu == float('inf'):
				free(prx, regclass)

			prz = allocate(op.op3.vr, regclass)

			op.op1.pr = prx
			op.op3.pr = prz

			if op.op1.nu != float('inf'):
				regclass.next[prx] = op.op1.nu	

			regclass.next[prz] = op.op3.nu
		
		# op r1, r2 (store)
		elif op.opcode == 2:
			prx = ensure(op.op1.vr, regclass)
			pry = ensure(op.op2.vr, regclass)

			if op.op1.nu == float('inf'):
				free(prx, regclass)

			if op.op2.nu == float('inf'):
				free(pry, regclass)

			op.op1.pr = prx
			op.op2.pr = pry

			if op.op1.nu != float('inf'):
				regclass.next[prx] = op.op1.nu

			if op.op2.nu != float('inf'):
				regclass.next[pry] = op.op2.nu		

		# op c => r3 (loadI)
		elif op.opcode == 1:
			prz = allocate(op.op3.vr, regclass)
			op.op3.pr = prz
			regclass.next[prz] = op.op3.nu


## HELPER METHODS ##


def parser_helper(block):
	node = IROperand()
	token = next_token(block)

	if token == None:
		return None

	if token[1] == 4:		# NOP
		node.set_opcode(token[0])
		return node

	elif token[1] == 3:		# OUTPUT
		node.set_opcode(token[0])
		token = next_token(block)
		if token[1] == 5:
			node.set_op1(token[0])
			return node
		else:
			raise RuntimeError('parser error: malformed input')

	elif token[1] == 2: 	# ARITHOP
		node.set_opcode(token[0])
		token = next_token(block)
		if token[1] == 6:
			node.set_op1(Op(token[0]))
			# sr_to_vr[token[0]] = -1
			# lu[token[0]] = float('inf')
			token = next_token(block)
			if token[1] == 7:
				token = next_token(block)
				if token[1] == 6:
					node.set_op2(Op(token[0]))
					# sr_to_vr[token[0]] = -1
					# lu[token[0]] = float('inf')
					token = next_token(block)
					if token[1] == 8:
						token = next_token(block)
						if token[1] == 6:
							node.set_op3(Op(token[0]))
							# sr_to_vr[token[0]] = -1
							# lu[token[0]] = float('inf')
							return node
						else:
							raise RuntimeError('parser error: malformed input')
					else:
						raise RuntimeError('parser error: malformed input')
				else:
					raise RuntimeError('parser error: malformed input')
			else:
				raise RuntimeError('parser error: malformed input')
		else:
			raise RuntimeError('parser error: malformed input')

	elif token[1] == 1:		# LOADI
		node.set_opcode(token[0])
		token = next_token(block)
		if token[1] == 5:
			node.set_op1(token[0])
			token = next_token(block)
			if token[1] == 8:
				token = next_token(block)
				if token[1] == 6:
					node.set_op3(Op(token[0]))
					# sr_to_vr[token[0]] = -1
					# lu[token[0]] = float('inf')
					return node
				else:
					raise RuntimeError('parser error: malformed input')
			else:
				raise RuntimeError('parser error: malformed input')
		else:
			raise RuntimeError('parser error: malformed input')

	elif token[1] == 0:		# MEMOP
		node.set_opcode(token[0])
		token = next_token(block)
		if token[1] == 6:
			node.set_op1(Op(token[0]))
			token = next_token(block)
			if token[1] == 8:
				token = next_token(block)
				if token[1] == 6:
					if node.opcode == 0:	# load
						node.set_op3(Op(token[0]))
					if node.opcode == 2:	# store
						node.set_op2(Op(token[0]))
					return node
				else:
					raise RuntimeError('parser error: malformed input')
			else:
				raise RuntimeError('parser error: malformed input')
		else:
			raise RuntimeError('parser error: malformed input')

	else:
		raise RuntimeError('parser error: malformed input')


def next_char(block):
	global scan_i

	if scan_i >= block_length:
		return None

	next = block[scan_i]
	scan_i += 1
	return next


def next_token(block):
	token = scanner(block)

	if token == None:
		return None

	while token[1] == 10 or token[1] == 9:
		token = scanner(block)
		if token == None:
			return None

	return token


def update(op, index):
	global vr_name
	if sr_to_vr[op.sr] == -1:	# sr has no vr
		sr_to_vr[op.sr] = vr_name
		vr_name += 1
	op.vr = sr_to_vr[op.sr]
	op.nu = lu[op.sr]
	lu[op.sr] = index


def distinct_add(arr, x):
	if x not in arr:
		arr.append(x)


def ensure(vr, regclass):
	if vr in regclass.name:
		return regclass.name.index(vr)
	else:
		ret = allocate(vr, regclass)
		# emit code to move vr into result
		return ret


def allocate(vr, regclass):
	if regclass.stacktop >= 0:
		i = pop(regclass)
	else:
		i = regclass.next.index(max(regclass.next))
		# store contents of j
	regclass.name[i] = vr
	regclass.next[i] = -1
	regclass.free[i] = False
	return i


def pop(regclass):
	ret = regclass.stack[regclass.stacktop]
	regclass.stacktop -= 1
	return ret


def free(pr, regclass):
	regclass.stacktop += 1
	regclass.stack[regclass.stacktop] = pr
	regclass.name[pr] = None
	regclass.next[pr] = float('inf')
	regclass.free[pr] = True


## RUN SCRIPT ##
# print alloc(sys.argv[2])
print alloc('test_code', 3)

