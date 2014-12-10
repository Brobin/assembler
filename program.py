from assembler import Assembler

# Runs the assembler. First ir prompts the user for
# input and output file names. The input file should
# be .s or .asm. The output files should be .mif.
# Then it runs the assembler. If an exception is
# raised, it is caught and the error message is
# printed.

program = Assembler()
filename = input("\nEnter the input file name: ")
file_out = input("Enter the output file name: ")
try:
	file = open(filename)
	print("\nAssembling...")
	code = file.readlines()
	output = program.compile(code)
	output_file = open(file_out, 'w')
	for line in output:
		output_file.write("%s\n" % line)
	print("\nAssembly successful!")
except Exception as e:
	print(str(e))
