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