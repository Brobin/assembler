from assembler import Assembler

program = Assembler()
filename = "code.s"
file = open(filename)
code = file.readlines()
try:
	output = program.compile(code)
	print(program.labels)
	output_file = open("code.mif", 'w')
	for line in output:
	  output_file.write("%s\n" % line)
except Exception as e:
    print(str(e))