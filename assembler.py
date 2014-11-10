from helper import *
import re

# Class that contains methods to compile our assembly into
# mcahine readable byte-code for our processor
class Assembler:
	def __init__(self):
		self.op = OpCodes()

	# Run the compilation process
	def compile(self, code):
		cleaned_code = self.clean_code(code)
		return self.get_machine_code(cleaned_code)

	# Strips spaces, tabs, and newlines from the assembly code
	# Also removes comments, delimited by a '#'
	def clean_code(self, code):
		clean_code = []
		for line in code:
			cleaned_line = "";
			if "#" in line:
				cleaned_line = line[0:line.index("#")].strip()
			else:
				cleaned_line = line.strip()
			if cleaned_line != "":
				clean_code.append(cleaned_line)
		return clean_code

	# Converts a register to a binary string of 4 bits
	def reg_to_binary(self, reg):
		number = int(reg[1:])
		output = "{0:b}".format(number)
		while len(output) != 4:
			output = "0" + output
		return output

	# Creates the machine code for a given array of instructions
	def get_machine_code(self, code):
		labels = []
		commands = []
		compiled = []

		# First pass, store labels and commands
		for x in range(0, len(code)):
			line = code[x]
			if ":" in line:
				name = line[0:line.index(":")]
				if name not in labels:
					labels[name] = x
				line = line[line.index(":"):len(line)]
			tokens = re.findall(r"[\w']+", line)
			new_command = Command(tokens, x)
			commands.append(new_command)

		# Second pass, do the things, add the machine code to the list
		for command in commands:
			instruction = self.op.instructions[command.tokens[0]]
			if instruction.type is InstructionType.R:
				compiled.append(self.r_type(command))
			elif instruction.type is InstructionType.D:
				compiled.append(self.d_type(command))
			elif instruction.type is InstructionType.B:
				compiled.append(self.b_type(command))
			elif instruction.type is InstructionType.J:
				compiled.append(self.j_type(command))

		return compiled

	# Creates the R type machine code for a given command
	def r_type(self, command):
		instruction  = self.op.instructions[command.tokens[0]]
		rd = self.reg_to_binary(command.tokens[1])
		rs = self.reg_to_binary(command.tokens[2])
		rt = self.reg_to_binary(command.tokens[3])
		registers = rs + rt + rd
		s = "0"
		cond = "0000"
		op = instruction.opx + s + cond + instruction.op_code
		return "\t{0}\t\t\t:\t{1}{2};".format(str(command.index), registers, op)

	# Creates the D tpe machine code for a given command
	def d_type(self, command):
		return "TO-DO: finish this thing"

	# Creates the B tpe machine code for a given command
	def b_type(self, command):
		return "TO-DO: finish this thing"

	# Creates the J tpe machine code for a given command
	def j_type(self, command):
		return "TO-DO: finish this thing"
