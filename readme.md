# Assembler

####Assembler for CSE230 - Computer Systems final project

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
END;
```


| File | Description |
|------|-------------|
| assembler.py | contains the actual assembler. reads the lines of the assembly file and converts it to machine code |
| code.s | example input file |
| program.py | actually runs the assembler |
| provider.py | contains classes that the assembler uses (Command, InstructionType, OpCodes, OpCode), also, I'm bad at naming things, so yeah |
| readme.md | you're reading it... |

###R-Type

add, sub, and, or, xor, sll, cmp, jr

| [23..20] | [19..16] | [15..12] | [11..9] | [8] | [7..4] | [3..0] |
|----------|----------|----------|---------|-----|--------|--------|
| RegT | RegS |RegD | OpX | S | Cond | OpCode |

`add r2, r3, r4` => r2 = r3 + r4

`sub r2, r3, r4` => r2 = r3 - r4

`and r2, r3, r4` => r2 = r3 AND r4

`or r2, r3, r4` => r2 = r3 OR r4

`xor r2, r3, r4` => r2 = r3 XOR r4

`sll r2, r3, r4` => r2 = r3 << r4

### D-Type

lw, sw, addi, si

| [23..20] | [19..16] | [15..9] | [8] | [7..4] | [3..0] | 
|----|----|----|----|-----|-----|
| RegT | RegS | Immediate | S | Cond | OpCode |

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
