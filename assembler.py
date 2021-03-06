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
        self.extra = 0

    # Run the compilation process
    def compile(self, code):
        cleaned_code = self.clean_code(code)
        return self.get_machine_code(cleaned_code)

    # Strips spaces, tabs, and newlines from the assembly code
    # Also removes comments, delimited by a '#'
    def clean_code(self, code):
        clean_code = []
        for line in code:
            cleaned_line = ""
            if "#" in line:
                cleaned_line = line[0:line.index("#")].strip()
            else:
                cleaned_line = line.strip()
            if cleaned_line != "":
                clean_code.append(cleaned_line)
        return clean_code

    # Creates the machine code for a given array of instructions
    # Calls the first and second pass and then returns the contents
    # of the output file as a list.
    def get_machine_code(self, code):
        commands = self.first_pass(code)
        compiled = self.second_pass(commands)
        return self.get_header() + compiled + self.get_footer()

    # First pass, store labels and commands
    # Also calls update cond to add conditional commands.
    def first_pass(self, code):
        commands = []
        self.data_section = []
        data = False
        for x in range(0, len(code)):
            line = code[x]
            if ";" in line:
                data = True
                index = line[0:line.index(";")]
                value = line[line.index(";"):len(line)]
                tokens = re.findall(r"[\w']+", value)
                self.data_section.append(
                    self.format_data_output(index, tokens[0]))
            if not data:
                if ":" in line:
                    name = line[0:line.index(":")]
                    self.labels[name] = x + 1 + self.extra
                    line = line[line.index(":"):len(line)]
                tokens = re.findall(r"[\w']+", line)
                new_command = Command(tokens, x + 1 + self.extra, "0000")
                commands = commands + self.update_cond(new_command)
        if len(commands) > 40:
            raise Exception("ERROR: Maximum of 40 commands!")
        return commands

    # Second pass, assembles the commands into byte-code. First
    # it checks the type, then calls the corresponding method.
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
            elif instruction.type is InstructionType.H:
                compiled.append(self.h_type(command))
        return compiled + self.data_section

    # Sets the cond variables for a given command and trims the
    # command. also adds the extra cmp instruction needed.
    def update_cond(self, command):
        instruction = command.tokens[0]
        x = len(instruction) - 2
        if len(instruction) >= 3 and instruction is not "bal":
            conds = self.cond.list
            if conds.get(instruction[x:]) is not None:
                command.cond = conds[instruction[x:]]
                self.extra += 1
                command.index += self.extra
                new = instruction[:x]
                command.tokens[0] = new
                instruction = self.op.instructions[new]
                if instruction.type is InstructionType.R:
                    compare = Command(["cmp",
                                       command.tokens[2],
                                       command.tokens[3]],
                                      command.index - 1,
                                      "0000")
                elif instruction.type is InstructionType.D:
                    compare = Command(["cmp",
                                       command.tokens[1],
                                       command.tokens[2]],
                                      command.index - 1,
                                      "0000")
                elif instruction.type is InstructionType.B:
                    compare = Command(["cmp",
                                       command.tokens[1],
                                       command.tokens[2]],
                                      command.index - 1,
                                      "0000")
                    command.tokens = ["b", command.tokens[3]]
                elif instruction.type is InstructionType.J:
                    compare = Command(["cmp",
                                       command.tokens[1],
                                       command.tokens[2]],
                                      command.index - 1,
                                      "0000")
                    command.tokens = ["j", command.tokens[3]]
                return [compare, command]
        return [command]

    # Converts a register address to a binary string of 4 bits
    def reg_to_binary(self, reg, length):
        number = reg[1:]
        return self.int_to_binary(number, length)

    # Converts an integer to a binary string of given length
    def int_to_binary(self, number, length):
        output = "{0:b}".format(int(number))
        if "-" in output:
            output = self.twos_complement(output, length)
        else:
            while len(output) < length:
                output = "0" + output
        return output

    # Remove a negative number from a binary string
    # Converts it into a two's complement form
    def twos_complement(self, data, length):
        data = data.replace("-", "")
        new = ""
        while len(data) < length:
            data = "0" + data
        data = data.replace('0', '%temp%').replace(
            '1', '0').replace('%temp%', '1')
        number = int(data, 2) + 1
        output = "{0:b}".format(int(number))
        return output

    # Makes sure that the command has the expected number of tokens
    def validate_tokens(self, command, length):
        tokens = command.tokens
        if len(tokens) is not length:
            raise Exception("ERROR: instruction {0}: Requires {1} arguments".
                            format(str(command.index), str(length)))

    # header for out mif file
    def get_header(self):
        return ["DEPTH = 128;",
                "WIDTH = 24;",
                "ADDRESS_RADIX = DEC;",
                "DATA_RADIX = HEX;\n",
                "CONTENT",
                "\tBEGIN",
                "\t[0..127]\t:\t000000;"
                ]

    # Formats the output for a line of the file
    def format_output(self, index, data, op):
        hex_string = self.binary_to_hex("{0}{1}".format(data, op))
        return "\t{0}\t\t\t:\t{1};".format(index, hex_string)

    def format_data_output(self, index, data):
        return "\t{0}\t\t\t:\t{1};".format(index, data)

    # Converts a binary string to a hex string
    def binary_to_hex(self, string):
        string = hex(int(string, 2))
        string = string[2:]
        while len(string) < 6:
            string = "{0}{1}".format("0", string)
        return string

    # footer for our mif file
    # hardcoded i/o memory locations
    def get_footer(self):
        return [
            "END;"
        ]

    # Creates the R type machine code for a given command
    def r_type(self, command):
        instruction = self.op.instructions[command.tokens[0]]
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

    # Creates the D type machine code for a given command
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
            self.validate_tokens(command, 2)
            interrupt = self.int_to_binary(command.tokens[1], 15)
            data = interrupt
        op = self.s + command.cond + instruction.op_code
        return self.format_output(str(command.index), data, op)

    # Creates the B type machine code for a given command
    # throws exception if a label is not found
    def b_type(self, command):
        self.validate_tokens(command, 2)
        instruction = self.op.instructions[command.tokens[0]]
        label = command.tokens[1]
        if label not in self.labels:
            raise Exception("ERROR: instruction {0}: Label '{1}' not found".
                            format(str(command.index), label))
        else:
            label_index = self.labels[label] - (command.index + 1)
            data = self.int_to_binary(label_index, 16)
        return self.format_output(str(command.index),
                                  data, command.cond + instruction.op_code)

    # Creates the J type machine code for a given command
    def j_type(self, command):
        instruction = self.op.instructions[command.tokens[0]]
        if instruction.name is "li":
            self.validate_tokens(command, 3)
            register = self.reg_to_binary(command.tokens[1], 4)
            immediate = self.int_to_binary(command.tokens[2], 16)
            output = register + immediate
        else:
            self.validate_tokens(command, 2)
            output = self.int_to_binary(command.tokens[1], 20)
        return self.format_output(str(command.index),
                                  output, instruction.op_code)

    # Creates our custom h-type instruction
    def h_type(self, command):
        instruction = self.op.instructions[command.tokens[0]]
        self.validate_tokens(command, 4)
        rd = self.reg_to_binary(command.tokens[1], 4)
        rs = self.reg_to_binary(command.tokens[2], 4)
        immediate = self.int_to_binary(command.tokens[3], 7)
        output = rd + rs + immediate + "00000"
        return self.format_output(str(command.index),
                                  output, instruction.op_code)
