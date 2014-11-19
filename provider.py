from enum import Enum

# enum for instruction types
class InstructionType(Enum):
	R = "R"
	D = "D"
	B = "B"
	J = "J"
	NOOP = "NOOP"

# Contains the data for a single line instruction
class Command():
	def __init__(self, tokens, index, cond):
		self.tokens = tokens
		self.index = index
		self.cond = cond

# Has a dictionary of all possible OpCodes
class OpCodes():
	def __init__(self):
		self.instructions = {}
		self.instructions["and"] = OpCode("and", InstructionType.R, "1100", "000")
		self.instructions["or"] = OpCode("or", InstructionType.R, "1100", "001")
		self.instructions["xor"] = OpCode("xor", InstructionType.R, "1100", "010")
		self.instructions["add"] = OpCode("add", InstructionType.R, "1100", "011")
		self.instructions["sub"] = OpCode("sub", InstructionType.R, "1100", "100")

		self.instructions["sll"] = OpCode("sll", InstructionType.R, "1111", "000")
		self.instructions["cmp"] = OpCode("cmp", InstructionType.R, "1110", "000")
		self.instructions["jr"] = OpCode("jr", InstructionType.R, "1101", "000")

		self.instructions["lw"] = OpCode("lw", InstructionType.D, "1000")
		self.instructions["sw"] = OpCode("sw", InstructionType.D, "1001")
		self.instructions["addi"] = OpCode("addi", InstructionType.D, "1010")
		self.instructions["si"] = OpCode("si", InstructionType.D, "1011")

		self.instructions["b"] = OpCode("b", InstructionType.B, "0100")
		self.instructions["bal"] = OpCode("bal", InstructionType.B, "0101")

		self.instructions["j"] = OpCode("j", InstructionType.J, "0000")
		self.instructions["jal"] = OpCode("jal", InstructionType.J, "0001")
		self.instructions["li"] = OpCode("li", InstructionType.J, "0010")

# Contains the data for a single OpCode
class OpCode():
	def __init__(self, name, type, op_code, opx=None):
		self.name = name
		self.type = type
		self.op_code = op_code
		if opx is not None:
			self.opx = opx

class Cond():
	def __init__(self):
		self.list = {
			"al": "0000",
			"nv": "0001",
			"eq": "0010",
			"ne": "0011",
			"vs": "0100",
			"vc": "0101",
			"mi": "0110",
			"pl": "0111",
			"cs": "1000",
			"cc": "1001",
			"hi": "1010",
			"ls": "1011",
			"gt": "1100",
			"lt": "1101",
			"ge": "1110",
			"le": "1111"
		}
