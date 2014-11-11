
# R-Type instructions
R:	sub r4,r2,r3 #0010 0011 0100 100 0 0000 1100
	add r3,r4,r5 #0100 0101 0011 011 0 0000 1100
	and r6,r6,r4 #0110 0100 0110 000 0 0000 1100
	or r3,r3,r3 #0011 0011 0011 001 0 0000 1100
	xor r2,r3,r3 #0011 0100 0010 010 0 0000 1100

# D-Type instructions
D:	lw r4,4(r3) #0100 0101 0011001 0 0000 1010
	addi r4,r4,12
	si 2
	b D

# B-Type instructions

# J-Type instructions