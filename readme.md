# Assembler

####Assembler for CSE230 - Computer Systems final project

| File | Description |
|------|-------------|
| assembler.py | contains the actual assembler. reads the lines of the assembly file and converts it to machine code |
| code.s | example input file |
| helper.py | contains classes that the assembler uses (Command, InstructionType, OpCodes, OpCode), also, I'm bad at naming things, so yeah |
| program.py | actually runs the assembler |
| readme.md | you're reading it... |

###R-Type

add, sub, and, or, xor, sll, cmp, jr

| [23..20] | [19..16] | [15..12] | [11..9] | [8] | [7..4] | [3..0] |
|----------|----------|----------|---------|-----|--------|--------|
| RegT | RegS |RegD | OpX | S | Cond | OpCode |

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
