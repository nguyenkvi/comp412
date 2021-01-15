import utils

class IROperand:
	def __init__(self):
		self.prev = None
		self.opcode = None
		self.op1 = None
		self.op2 = None
		self.op3 = None
		self.next = None


	def __str__(self):
		return utils.word_mapping[self.opcode] + " " + str(self.op1) + " " + str(self.op2) + " => " + str(self.op3)
		#return '[ OPCODE: ' + utils.word_mapping[self.opcode] + ', OP1: ' + str(self.op1) + ', OP2: ' + str(self.op2) + ', OP3: ' + str(self.op3) + ' ]'

	def set_opcode(self, opcode):
		self.opcode = opcode


	def set_op1(self, op1):
		self.op1 = op1


	def set_op2(self, op2):
		self.op2 = op2


	def set_op3(self, op3):
		self.op3 = op3


class Op:
	def __init__(self, sr):
		self.sr = sr
		self.vr = None
		self.pr = None
		self.nu = float('inf')


	def __str__(self):
		return "r" + str(self.vr)
		#return  '[ SR: ' + str(self.sr) + ', VR: ' + str(self.vr) + ', PR: ' + str(self.pr) + ', NU: ' + str(self.nu) + ' ]'

