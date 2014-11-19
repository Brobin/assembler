from provider import *
import re

# Class that contains methods to compile our assembly into
# mcahine readable byte-code for our processor
class Assembler:
	def __init__(self):
		self.op = OpCodes()
		self.cond = Cond()
		self.labels = {}
		self.s = "0"

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

	# Sets the cond variables for a given command and trims the command
	def update_cond(self, command):
		instruction = command.tokens[0]
		x = len(instruction) - 2
		if len(instruction) > 3 and instruction is not "bal":
			conds = self.cond.list
			if conds.get(instruction[x:]) is not None:
				command.cond = conds[instruction[x:]]
				command.tokens[0] = instruction[:x]
		return command

	# Converts a register address to a binary string of 4 bits
	def reg_to_binary(self, reg, length):
		number = reg[1:]
		return self.int_to_binary(number, length)

	# Converts an integer to a binarys tring of given length
	def int_to_binary(self, number, length):
		output = "{0:b}".format(int(number))
		if "-" in output:
			length += 1
		while len(output) < length:
			output = "0" + output
		return output

	# Makes sure that the command has the expected number of tokens
	def validate_tokens(self, command, length):
		tokens = command.tokens
		if len(tokens) is not length:
			raise Exception("ERROR: instruction {0}: Requires {1} arguments".
				format(str(command.index), str(length)))

	# Creates the machine code for a given array of instructions
	def get_machine_code(self, code):
		commands = self.first_pass(code)
		compiled = self.second_pass(commands)
		return self.get_header() + compiled + self.get_footer()

	# First pass, store labels and commands
	def first_pass(self, code):
		commands = []
		for x in range(0, len(code)):
			line = code[x]
			if ":" in line:
				name = line[0:line.index(":")]
				self.labels[name] = x+1
				line = line[line.index(":"):len(line)]
			tokens = re.findall(r"[\w']+", line)
			new_command = Command(tokens, x+1, "0000")
			new_command = self.update_cond(new_command)
			commands.append(new_command)
		if len(commands) > 255:
			raise Exception("ERROR: Maximum of 255 commands!")
		return commands

	# Second pass, do the things, add the machine code to the list
	def second_pass(self, commands):
		compiled = []
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

	# header for out mif file
	def get_header(self):
		return ["DEPTH = 256;",
			"WIDTH = 6;",
			"ADDRESS_RADIX = DEC;",
			"DATA_RADIX = HEX;\n",
			"CONTENT",
		    "\tBEGIN",
		    "\t[0..255]\t:\t000000;"
		]

	# Formats the output for a line of the file
	def format_output(self, index, data, op):
		if "-" in data:
			data = self.remove_negative(data)
		hex_string = self.binary_to_hex("{0}{1}".format(data, op))
		return "\t{0}\t\t\t:\t{1};".format(index, hex_string)

	# Remove a negative number from a binary string
	# Converts it into a two's complement form
	def remove_negative(self, data):
		data = data.replace("-", "")
		new = ""
		print(data)
		for x in data:
			if x is "1":
				new = new + "0"
			else:
				new = new + "1"
		print(new)
		new = int(new, 2) + 1
		output = self.int_to_binary(new, len(data))
		print(output)
		return output

	# Converts a binary string to a hex string
	def binary_to_hex(self, string):
		string = hex(int(string, 2))
		string = string[2:]
		while len(string) < 6:
			string = "{0}{1}".format("0", string)
		return string

	# footer for our mif file
	def get_footer(self):
		return ["END;"]

	# Creates the R type machine code for a given command
	def r_type(self, command):
		instruction  = self.op.instructions[command.tokens[0]]
		s = self.s
		if instruction.name is "jr":
			self.validate_tokens(command, 2)
			rs = self.reg_to_binary(command.tokens[1], 4)
			rt = "0000"
			rd = "0000"
		elif instruction.name is "cmp":
			self.validate_tokens(command, 3)
			rs = self.reg_to_binary(command.tokens[1], 4)
			rt = self.reg_to_binary(command.tokens[2], 4)
			rd = "0000"
			s = "1"
		else:
			self.validate_tokens(command, 4)
			rd = self.reg_to_binary(command.tokens[1], 4)
			rt = self.reg_to_binary(command.tokens[2], 4)
			rs = self.reg_to_binary(command.tokens[3], 4)
		registers = rt + rs + rd
		op = instruction.opx + s + command.cond + instruction.op_code
		return self.format_output(str(command.index), registers, op)

	# Creates the D tpe machine code for a given command
	def d_type(self, command):
		instruction = self.op.instructions[command.tokens[0]]
		name = instruction.name
		if name is not "si":
			self.validate_tokens(command, 4)
			rt = self.reg_to_binary(command.tokens[1], 4)
			if name is "sw" or name is "lw":
				immediate = self.int_to_binary(command.tokens[2], 7)
				rs = self.reg_to_binary(command.tokens[3], 4)
			elif name is "addi":
				rs = self.reg_to_binary(command.tokens[2], 4)
				immediate = self.int_to_binary(command.tokens[3], 7)
			data = rt + rs + immediate
		else:
			interrupt = self.int_to_binary(command.tokens[1], 15)
			data = interrupt
		op = self.s + command.cond + instruction.op_code
		return self.format_output(str(command.index), data, op)

	# Creates the B tpe machine code for a given command
	def b_type(self, command):
		self.validate_tokens(command, 2)
		instruction = self.op.instructions[command.tokens[0]]
		label = command.tokens[1]
		if label not in self.labels:
			raise Exception("ERROR: instruction {0}: Label '{1}' not found".
				format(str(command.index), label))
		else:
			label_index = self.labels[label] - (command.index + 1)
			print(label_index)
			data = self.int_to_binary(label_index, 16)
		return self.format_output(str(command.index), data, command.cond + instruction.op_code)

	# Creates the J tpe machine code for a given command
	def j_type(self, command):
		self.validate_tokens(command, 2)
		instruction = self.op.instructions[command.tokens[0]]
		jump = self.int_to_binary(command.tokens[1], 20)
		return self.format_output(str(command.index), jump, instruction.op_code)
