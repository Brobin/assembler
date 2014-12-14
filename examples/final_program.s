lw r2,40(r0) 		# switches address

lw r3,42(r0) 		# hex0 address
lw r4, 45(r0)		# hex1 address
lw r5, 46(r0)		# hex2 address
lw r14, 47(r0)		# hex3 address

lw r6, 44(r0)		# red led address

lw r8, 41(r0)		# keys address

LOL:lw r7, 0(r2)	# switches value

	addi r9, r0, 15 # counter for keys
	lw r12, 0(r8)	# value of keys

	beq r9, r12, NOT_PRESSED

	sub r7, r7, r0 	# gets two's complement

NOT_PRESSED: sw r7, 0(r6)	# store led values

	hex r10, r7, 0 	# get hex0 value
	lw r11, 48(r10) # load the hex display value
	sw r11, 0(r3) 	# store the hex display value

	hex r10, r7, 1 	# get hex1 value
	lw r11, 48(r10) # load the hex display value
	sw r11, 0(r4) 	# store the hex display value

	hex r10, r7, 2 	# get hex2 value
	lw r11, 48(r10) # load the hex display value
	sw r11, 0(r5) 	# store the hex display value

	hex r10, r7, 3 	# get hex2 value
	lw r11, 48(r10) # load the hex display value
	sw r11, 0(r14) 	# store the hex display value

	b LOL			# loop LOL

# begin data section

# I/O addresses
40; 008000
41; 004000
42; 002000
43; 001000
44; 003000
45; 005000
46; 006000
47; 007000

# hex display values
48; 000040
49; 000079
50; 000024
51; 000030
52; 000019
53; 000012
54; 000002
55; 000078
56; 000000
57; 000010
58; 000008
59; 000003
60; 000046
61; 000021
62; 000006
63; 00000E