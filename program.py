from assembler import Assembler

program = Assembler()
filename = "code.s"
file = open(filename)
code = file.readlines()
output = program.compile(code)

output_file = open("code.mif", 'w')
for line in output:
  output_file.write("%s\n" % line)