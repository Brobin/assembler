from assembler import Assembler

program = Assembler()
filename = "code.s"
file = open(filename)
code = file.readlines()
output = program.compile(code)

header = ["DEPTH = 256;",
	"WIDTH = 24;",
	"ADDRESS_RADIX = DEC;",
	"DATA_RADIX = BIN;\n",
	"CONTENT",
    "\tBEGIN",
    "\t[0..255]\t:\t000000000000000000000000;"
]

footer = ["END;"]

output = header + output + footer

output_file = open("code.mif", 'w')
for line in output:
  output_file.write("%s\n" % line)