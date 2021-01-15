word_mapping = [
				'load',		# 0
				'loadI', 	# 1
				'store', 	# 2
				'add', 		# 3
				'sub', 		# 4
				'mult', 	# 5
				'rshift', 	# 6
				'lshift', 	# 7
				'output', 	# 8
				'nop', 		# 9
				',', 		# 10
				'=>',		# 11
				'comment'	# 12
				]


pos_mapping = [
				'MEMOP',	# 0
				'LOADI', 	# 1
				'ARITHOP', 	# 2
				'OUTPUT', 	# 3
				'NOP', 		# 4
				'CONSTANT', # 5
				'REGISTER', # 6
				'COMMA', 	# 7
				'INTO', 	# 8
				'COMMENT'	# 9
				'WHITESPACE'#10
				]	


def pp_token(token):
	if token == None:
		return None
	if token[1] == 6 or token[1] == 5:
		return (token[0], pos_mapping[token[1]])
	return (word_mapping[token[0]], pos_mapping[token[1]])


def renamed_prog(ops):
	list_of_ops = []

	for op in ops:
		ret=""
		ret += word_mapping[op.opcode]
		# ARITHOP
		if op.op1 != None and op.op2 != None and op.op3 != None:
			ret += (" r" + str(op.op1.vr) + ",r" + str(op.op2.vr) + " => r" + str(op.op3.vr)) 
		# load
		elif op.opcode == 0:
			ret += (" r" + str(op.op1.vr) + " => r" + str(op.op3.vr))
		# store
		elif op.opcode == 2:
			ret += (" r" + str(op.op1.vr) + " => r" + str(op.op2.vr))
		# loadI
		elif op.opcode == 1:
			ret += (" " + str(op.op1) + " => r" + str(op.op3.vr))
		# output
		elif op.opcode == 8:
			ret += (" " + str(op.op1))
		# nop
		else:
			ret += '\n'

		list_of_ops.append(ret)

	return list_of_ops

