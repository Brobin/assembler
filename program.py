from assembler import Assembler

# Runs the assembler. Takes an input file (code.s),
# calls the assembler to compile it, and outputes the
# result to code.mif. If an exception is thrown in the
# assembler, it is caught and output here.

program = Assembler()
filename = "code.s"
file = open(filename)
code = file.readlines()
try:
	output = program.compile(code)
	output_file = open("code.mif", 'w')
	for line in output:
		output_file.write("%s\n" % line)
except Exception as e:
	print(str(e))
