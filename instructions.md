#R-Type

add, sub, and, or, xor, sll, cmp, jr

| [23..20] | [19..16] | [15..12] | [11..9] | [8] | [7..4] | [3..0] |
|----------|----------|----------|---------|-----|--------|--------|
| RegT | RegS |RegD | OpX | S | Cond | OpCode |

# D-Type

lw, sw, addi, si

| [23..20] | [19..16] | [15..9] | [8] | [7..4] | [3..0] | 
|----|----|----|----|-----|-----|
| RegT | RegS | Immediate | S | Cond | OpCode |

# B-Type

b, bal

| [23..8] | [7..4] | [3..0] |
|---------|--------|--------|
| Label | Cond | OpCode |

# J-Type

j, jal, li

| [24..4] | [3..0] |
|---------|--------|
| Constant | OpCode |