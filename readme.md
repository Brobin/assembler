# Assembler

###Assembler for CSE230 - Computer Systems final project

Reads in a .s assembly file and outputs a .mif (Memory initialization File)

Example input:
```
		addi r2, r2, 8	# r2 = 8
		addi r4, r2, 3	# r4 = 11
URMOM:	sw r2, 4(r2)	# mem(12) = 8
		lw r3, 4(r2)	# r3 = 8
		add r3,r3,r3	# r3 = 16
		cmp r2, r3		# N = 1, C = 0, V = 0, Z = 0
		jr r4			# jump to line 11
		addi r5, r5, 0	# r5 = 0 SKIPPED
		addi r6, r6, 1 	# r6 = 1 SKIPPED
		addi r7, r7, 2 	# r7 = 2 SKIPPED
		b 69			# branch to 69
		addi r8, r8, 0	# SKIPPPED
69:		addi r9, r9, 6 	# r9 = 6
		sw r9 4(r2)		# mem(12) = 6
		bal URMOM		# branch to URMOM

40; 008000
64; FFF5D3
```

Example output:
```
DEPTH = 256;
WIDTH = 6;
ADDRESS_RADIX = DEC;
DATA_RADIX = HEX;

CONTENT
	BEGIN
	[0..255]	:	000000;
	1			:	22100a;
	2			:	42060a;
	3			:	220809;
	4			:	320808;
	5			:	33360c;
	6			:	32010e;
	7			:	04000d;
	8			:	55000a;
	9			:	66020a;
	10			:	77040a;
	11			:	000104;
	12			:	88000a;
	13			:	990c0a;
	14			:	920809;
	15			:	fff305;
	42 			:	008000;
	64 			:	FFF5D3;
END;
```

### Data section

Additionaly, a simple data section can be implemented. The data section should be after all of the code. I didn't have much time to make it too complicated, so for now, you create a data section like the following

```
40; 008000
64; FFF5D3
```

The first number is the location you want it stored in memory, and the second is a 24-bit hex value that represents the data you want stored.

###File List

| File | Description |
|------|-------------|
| assembler.py | contains the actual assembler. reads the lines of the assembly file and converts it to machine code |
| examples/final_program.s | example input file, our final program |
| examples/final_program.mif | example output file, our final program |
| program.py | actually runs the assembler |
| provider.py | contains classes that the assembler uses (Command, InstructionType, OpCodes, OpCode), also, I'm bad at naming things, so yeah |
| readme.md | you're reading it... |

###R-Type

add, sub, and, or, xor, sll, cmp, jr

| [23..20] | [19..16] | [15..12] | [11..9] | [8] | [7..4] | [3..0] |
|----------|----------|----------|---------|-----|--------|--------|
| RegT | RegS |RegD | OpX | S | Cond | OpCode |


### D-Type

lw, sw, addi, si, hex

| [23..20] | [19..16] | [15..9] | [8] | [7..4] | [3..0] | 
|----|----|----|----|-----|-----|
| RegT | RegS | Immediate | S | Cond | OpCode |

The hex instruction is a custom instruction that we implemented to help with our final test program. It takes in the value of the switches on our board and outputs the four bits that we are looking at in order to retrieve the correct hex display value from memory.

### B-Type

b, bal

| [23..8] | [7..4] | [3..0] |
|---------|--------|--------|
| Label | Cond | OpCode |

### J-Type

j, jal, li

| [24..4] | [3..0] |
|---------|--------|
| Constant | OpCode |
